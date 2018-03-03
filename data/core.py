import argparse

from sqlite import sqlite_computations
from in_memory import in_memory_computations


def get_computation_mode_object(mode):
    """

    :param mode: computation mode (sqlite or in_memory)
    :return:
    """
    if mode == 'sqlite':
        return sqlite_computations.Sqlite()
    elif mode == 'in_memory':
        return in_memory_computations.InMemory()
    else:
        print('You must run the software with parameter \'--feature span\' or \'--feature avg\'')


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', action='store', help="choose a computation mode", default="sqlite")
    parser.add_argument('--feature', action='store', help="choose a feature", default="avg")
    parser.add_argument('--url', action='store', help="optional url from which to download values", default=None)
    args = parser.parse_args()

    if args.feature == 'avg':
        get_computation_mode_object(args.mode).compute_avg_weekly_price_to_csv()
    elif args.feature == 'span':
        get_computation_mode_object(args.mode).get_week_of_max_relative_span()
    else:
        print('You must run the software with parameter \'--feature span\' or \'--feature avg\'')
