import torch
import torch.nn as nn

from recbole.utils import InputType
from recbole.model.abstract_recommender import ContextRecommender
from recbole.model.context_aware_recommender import fm
from recbole.model.loss import BPRLoss
from recbole.model.init import xavier_normal_initialization

from logging import getLogger
from recbole.utils import init_logger, init_seed
from recbole.trainer import Trainer
from recbole.config import Config
from recbole.data import create_dataset, data_preparation
from sys import argv

import numpy as np
import pandas as pd

class LastRS(fm.FM):

    input_type = InputType.PAIRWISE

    def __init__(self, config, dataset):
        super().__init__(config, dataset)

    def calculate_loss(self, interaction):
        super().calculate_loss(interaction)

    def predict(self, interaction):
        user = interaction[self.USER_ID]
        item = interaction[self.ITEM_ID]

        user_e = self.user_embedding(user)            # [batch_size, embedding_size]
        item_e = self.item_embedding(item)            # [batch_size, embedding_size]

        scores = torch.mul(user_e, item_e).sum(dim=1) # [batch_size]

        return scores

    def full_sort_predict(self, interaction):
        user = interaction[self.USER_ID]

        user_e = self.user_embedding(user)                        # [batch_size, embedding_size]
        all_item_e = self.item_embedding.weight                   # [n_items, batch_size]

        scores = torch.matmul(user_e, all_item_e.transpose(0, 1)) # [batch_size, n_items]

        return scores


if __name__ == '__main__':

    config = Config(model=LastRS, config_file_list=[argv[1]])
    init_seed(config['seed'], config['reproducibility'])

    # logger initialization
    init_logger(config)
    logger = getLogger()

    logger.info(config)

    # dataset filtering
    dataset = create_dataset(config)
    logger.info(dataset)

    # dataset splitting
    train_data, valid_data, test_data = data_preparation(config, dataset)

    # model loading and initialization
    model = LastRS(config, train_data.dataset).to(config['device'])
    logger.info(model)

    # trainer loading and initialization
    trainer = Trainer(config, model)

    # model training
    best_valid_score, best_valid_result = trainer.fit(train_data, valid_data)

    # model evaluation
    test_result = trainer.evaluate(test_data)

    logger.info('Best valid result: {}'.format(best_valid_result))
    logger.info('Test result: {}'.format(test_result))