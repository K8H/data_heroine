# -*- coding: utf-8 -*-
import sys
import argparse

import pandas as pd

sys.path.append("..")
from data import core   # noqa


def get_t_series_df(file_name):
    """
    Returns pandas data frame of csv file and set the index to 'timestamp'. 
        
    :param file_name: name of the csv file ('data/test/' prefix if running in test mode)
    :return: time series pandas.DataFrame
    """
    core.print_datetime_output('Converting csv file \'%s\' into data frame.' % file_name)
    df = pd.read_csv(file_name).set_index('timestamp')
    df.index = pd.to_datetime(df.index)
    return df


def compute_avg_weekly_price_to_csv():
    """
    Groups timestamps by week and computes mean price on each group and store the data frame into csv file.
    
    """
    df = get_t_series_df(file_name=core.FILE_NAME_T)
    core.print_datetime_output('Group time series by week and compute mean price')
    df = df.groupby(pd.Grouper(freq='W-MON')).mean()
    core.print_datetime_output('Store data frame to file \'%s\'' % core.FILE_NAME_AVG)
    df.to_csv(core.FILE_NAME_AVG)


def get_week_of_max_relative_span(test=False):
    """
    Compute what is the week that had the greatest relative span on closing prices (difference between the maximum and 
    minimum closing price, divided by the minimum closing price), and prints it on a screen.

    Mathematically: relative_span = (max(price) min(price)) / min(price)
    
    :param test: if True (running in test mode), name of the csv file gets 'data/test/' prefix
    :return: date of a week with the maximum relative span on closing prices
    """
    file_name = core.FILE_NAME_T
    if test:
        file_name = 'in_memory/test/%s' % core.FILE_NAME_T

    close_df = get_t_series_df(file_name=file_name)['close (USD)']

    core.print_datetime_output(
        'Group time series by week on close price, computes min & max and calculates max relative span')
    min_max_close_price_df = pd.DataFrame()
    min_max_close_price_df['min'] = close_df.groupby(pd.Grouper(freq='W-MON')).min()
    min_max_close_price_df['max'] = close_df.groupby(pd.Grouper(freq='W-MON')).max()
    min_max_close_price_df['rel_span'] = ((min_max_close_price_df['max'] - min_max_close_price_df['min'])
                                          / min_max_close_price_df['min'])
    max_rel_span = min_max_close_price_df['rel_span'].max()
    week_max_rel_span = min_max_close_price_df[min_max_close_price_df['rel_span'] == max_rel_span].index.date[0]
    core.print_datetime_output('The week with max relative span is: %s' % week_max_rel_span)
    return week_max_rel_span


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--feature', action='store', help="choose a feature", default="avg")
    parser.add_argument('--url', action='store', help="optional url from which to download values", default=None)
    args = parser.parse_args()

    if args.url is not None:
        core.download_crypto_curr_to_csv(url=args.url)
    else:
        core.download_crypto_curr_to_csv()

    if args.feature == 'avg':
        compute_avg_weekly_price_to_csv()
    elif args.feature == 'span':
        get_week_of_max_relative_span()
    else:
        core.print_datetime_output('You must run the software with parameter \'--feature span\' or \'--feature avg\'')
