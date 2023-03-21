import argparse
from recbole.config import Config
from recbole.data import create_dataset, data_preparation
from recbole.quick_start import run_recbole

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        usage="%(prog)s --algorithm [ALGORITHM] --config [CONFIG_FILE] --save (OPTIONAL)", formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-a', '--algorithm', action='store',
                        help='Recommendation Algorithm', required=True)
    parser.add_argument('-c', '--config', action='store',
                        help='Configuration File', required=True)
    parser.add_argument('-s', '--save', action='store_true',
                        help='Whether to save the model')

    args = parser.parse_args()

    run_recbole(model=args.algorithm, config_file_list=[
                args.config], saved=args.save)
