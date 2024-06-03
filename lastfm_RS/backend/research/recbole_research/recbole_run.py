# Recbole utilities adapted from recbole.quick_start to this project
# @Time   : 2024/05/27
# @Author : Javier Wang Zhou

import argparse
import importlib
import pathlib
import json
import sys

from recbole.quick_start import run_recboles
from recbole.utils.utils import get_model
from logging import getLogger
from torch import load, cuda, device

from recbole.config import Config
from recbole.data import (
    create_dataset,
    data_preparation,
)

from recbole.data.transform import construct_transform
from recbole.utils import (
    init_logger,
    get_model,
    get_trainer,
    init_seed,
    set_color,
    get_flops,
)

# use CPU if CUDA unavailable
load_device = device("cpu") if not cuda.is_available() else None

def parse_model(model):
    try:
        model_class = get_model(model)
    except ValueError as v:
        # Import from current directory
        if importlib.util.find_spec(model):
            module = importlib.import_module(model)
            model_class = getattr(module, model)
        if not model_class:
            raise v

    return model_class


def load_data_and_model(load_model, preload_dataset=None, update_config=None, use_training=False, verbose=False):
    r"""Load filtered dataset, split dataloaders and saved model.

    Args:
        load_model (dict | str): Preloaded checkpoint or path to saved model.
        preload_dataset (Dataset): Preloaded dataset.
        update_config (dict): Config entries to update.
        use_training (bool): Whether to use training set or full dataset.
        verbose (bool): Whether to log data preparation.

    Returns:
        tuple:
            - config (Config): An instance object of Config, which record parameter information in :attr:`model_file`.
            - model (AbstractRecommender): The model load from :attr:`model_file`.
            - dataset (Dataset): The filtered dataset.
            - train_data (AbstractDataLoader): The dataloader for training.
            - valid_data (AbstractDataLoader): The dataloader for validation.
            - test_data (AbstractDataLoader): The dataloader for testing.
    """
    sys.path.insert(1, str(pathlib.Path(__file__).parent.resolve()))

    checkpoint = load_model
    if isinstance(load_model, str):
        checkpoint = load(load_model, map_location=load_device)

    config: Config = checkpoint["config"]
    if update_config:
        for key, value in update_config.items():
            config[key] = value
    config.compatibility_settings()

    if config['data_path']:
        config['data_path'] = config['data_path'].replace('\\', '/')

    if not cuda.is_available():
        config['device'] = 'cpu'

    init_seed(config["seed"], config["reproducibility"])
    init_logger(config)
    if verbose:
        logger = getLogger()
        logger.info(config)

    config_seed = config['seed']
    config['seed'] = 2020

    dataset = preload_dataset or create_dataset(config)

    config['seed'] = config_seed

    if verbose:
        logger.info(dataset)

    init_seed(config["seed"], config["reproducibility"])

    model = parse_model(config["model"])

    train_data = valid_data = test_data = None
    if use_training:
        train_data, valid_data, test_data = data_preparation(config, dataset)
        model = model(config, train_data._dataset).to(config["device"])
    else:
        model = model(config, dataset).to(config["device"])

    model.load_state_dict(checkpoint["state_dict"])
    model.load_other_parameter(checkpoint.get("other_parameter"))

    return config, model, dataset, train_data, valid_data, test_data


def evaluate_saved_model(saved_model, update_config=None, evaluation_mode='full'):
    load_model = load(saved_model, map_location=load_device)
    eval_args = load_model["config"]["eval_args"]
    eval_mode_dict = {'valid': evaluation_mode, 'test': evaluation_mode}

    if eval_args:
        eval_args["mode"] = eval_mode_dict
    else:
        config["eval_args"] = {"mode": eval_mode_dict}

    config, model, _, _, _, test_data = load_data_and_model(load_model,
                                                            update_config=update_config,
                                                            use_training=True,
                                                            verbose=True)

    # trainer loading and initialization
    trainer = get_trainer(config["MODEL_TYPE"], config["model"])(config, model)

    # model evaluation
    test_result = trainer.evaluate(test_data,
                                   load_best_model=False,
                                   show_progress=config["show_progress"],
                                   model_file=saved_model)

    getLogger().info(set_color("test result", "yellow") + f": {test_result}")


def run_recbole(
    model=None, dataset=None, config_file_list=None, config_dict=None, saved=True
):
    r"""A fast running api, which includes the complete process of
    training and testing a model on a specified dataset

    Args:
        model (str | AbstractRecommender, optional): Model name or class. Defaults to ``None``.
        dataset (str, optional): Dataset name. Defaults to ``None``.
        config_file_list (list, optional): Config files used to modify experiment parameters. Defaults to ``None``.
        config_dict (dict, optional): Parameters dictionary used to modify experiment parameters. Defaults to ``None``.
        saved (bool, optional): Whether to save the model. Defaults to ``True``.
    """
    # configurations initialization
    config = Config(
        model=model,
        dataset=dataset,
        config_file_list=config_file_list,
        config_dict=config_dict,
    )
    init_seed(config["seed"], config["reproducibility"])
    # logger initialization
    init_logger(config)
    logger = getLogger()
    logger.info(sys.argv)
    logger.info(config)

    # dataset filtering
    dataset = create_dataset(config)
    logger.info(dataset)

    # dataset splitting
    train_data, valid_data, test_data = data_preparation(config, dataset)

    # model loading and initialization (modified to accept custom models)
    init_seed(config["seed"] + config["local_rank"], config["reproducibility"])
    model = (get_model(config["model"]) if isinstance(model, str) else model)(
        config, train_data._dataset).to(config["device"])
    logger.info(model)

    transform = construct_transform(config)
    flops = get_flops(model, dataset, config["device"], logger, transform)
    logger.info(set_color("FLOPs", "blue") + f": {flops}")

    # trainer loading and initialization
    trainer = get_trainer(config["MODEL_TYPE"], config["model"])(config, model)

    # model training
    best_valid_score, best_valid_result = trainer.fit(
        train_data, valid_data, saved=saved, show_progress=config["show_progress"]
    )

    # model evaluation
    test_result = trainer.evaluate(
        test_data, load_best_model=saved, show_progress=config["show_progress"]
    )

    logger.info(set_color("best valid ", "yellow") + f": {best_valid_result}")
    logger.info(set_color("test result", "yellow") + f": {test_result}")

    return {
        "best_valid_score": best_valid_score,
        "valid_score_bigger": config["valid_metric_bigger"],
        "best_valid_result": best_valid_result,
        "test_result": test_result,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", "-m", type=str,
                        default="BPR", help="name of models")
    parser.add_argument(
        "--evaluate_model", "-e", type=str, default=None, help="path to saved model to evaluate"
    )
    parser.add_argument(
        "--evaluation_mode", "-em", type=str, default='full', help="evaluation mode (e.g: full, uni100, pop100)"
    )
    parser.add_argument(
        "--config_dict", "-c", type=str, default=None, help="JSON dict to update config"
    )
    parser.add_argument(
        "--dataset", "-d", type=str, default="ml-100k", help="name of datasets"
    )
    parser.add_argument(
        "--save", "-s", action='store_true', default=False, help="save the trained model"
    )
    parser.add_argument("--config_files", type=str,
                        default=None, help="config files")
    parser.add_argument(
        "--nproc", type=int, default=1, help="the number of process in this group"
    )
    parser.add_argument(
        "--ip", type=str, default="localhost", help="the ip of master node"
    )
    parser.add_argument(
        "--port", type=str, default="5678", help="the port of master node"
    )
    parser.add_argument(
        "--world_size", type=int, default=-1, help="total number of jobs"
    )
    parser.add_argument(
        "--group_offset",
        type=int,
        default=0,
        help="the global rank offset of this group",
    )

    args, _ = parser.parse_known_args()

    model = parse_model(args.model)

    config_file_list = (
        args.config_files.strip().split(" ") if args.config_files else None
    )

    if args.config_dict:
        args.config_dict = json.loads(args.config_dict)

    if args.nproc == 1 and args.world_size <= 0:
        if args.evaluate_model:
            evaluate_saved_model(
                args.evaluate_model, update_config=args.config_dict, evaluation_mode=args.evaluation_mode)
        else:
            run_recbole(
                model=model, dataset=args.dataset, config_file_list=config_file_list, saved=args.save, config_dict=args.config_dict
            )
    else:
        if args.world_size == -1:
            args.world_size = args.nproc
        import torch.multiprocessing as mp

        # does not work with custom models
        mp.spawn(
            run_recboles,
            args=(
                args.model,
                args.dataset,
                config_file_list,
                args.ip,
                args.port,
                args.world_size,
                args.nproc,
                args.group_offset,
            ),
            nprocs=args.nproc,
        )
