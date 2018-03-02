# -*- coding: utf-8 -*-
import csv
import sys
from datetime import datetime

import pandas as pd
import requests

FILE_NAME_T = 'time_series.csv'
FILE_NAME_AVG = 'avg_weekly_price.csv'


def print_datetime_output(output=''):
    """
    Prints the cmd output with formatted date and time.
    """
    print('{:%Y-%m-%d %H:%M}'.format(datetime.now()), output)


def download_crypto_curr_to_csv(url=('https://www.alphavantage.co/query?'
                              'function=DIGITAL_CURRENCY_DAILY&'
                              'symbol=BTC&'
                              'market=USD&'
                              'apikey=1LUM05IW26CBPVKM&'
                              'datatype=csv')):
    """
    Downloads the historical time series from the API anf store them into csv file.

    Makes GET request to API's endpoint for the "Daily Digital & Crypto Currencies", specifying as symbol ‘BTC’ and as 
    market ‘USD’.

    :return: a response of API
    """
    try:
        response = requests.get(url)
        store_to_csv(response)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)


def store_to_csv(time_series):
    """
    Takes API's response in bytes and store row after row into csv file, named 'time_series.csv'

    :param time_series: API's response in bytes
    """
    if time_series:
        with open(FILE_NAME_T, 'w') as f:
            writer = csv.writer(f)
            reader = csv.reader(time_series.text.splitlines())

            for row in reader:
                writer.writerow(row)
    return Exception('Time series should not be None.')


def get_t_series_df(file_name):
    """
    Returns pandas data frame of csv file and set the index to 'timestamp'. 
        
    :param file_name: name of the csv file ('python/test/' prefix if running in test mode)
    :return: time series pandas.DataFrame
    """
    print_datetime_output('Converting csv file \'%s\' into data frame.' % file_name)
    df = pd.read_csv(file_name).set_index('timestamp')
    df.index = pd.to_datetime(df.index)
    return df


def compute_avg_weekly_price_to_csv():
    """
    Groups timestamps by week and computes mean price on each group and store the data frame into csv file.
    
    """
    df = get_t_series_df(file_name=FILE_NAME_T)
    print_datetime_output('Group time series by week and compute mean price')
    df = df.groupby(pd.Grouper(freq='W-MON')).mean()
    print_datetime_output('Store data frame to file \'%s\'' % FILE_NAME_AVG)
    df.to_csv(FILE_NAME_AVG)


def get_week_of_max_relative_span(test=False):
    """
    Compute what is the week that had the greatest relative span on closing prices (difference between the maximum and 
    minimum closing price, divided by the minimum closing price), and prints it on a screen.

    Mathematically: relative_span = (max(price) min(price)) / min(price)
    
    :param test: if True (running in test mode), name of the csv file gets 'python/test/' prefix
    :return: date of a week with the maximum relative span on closing prices
    """
    file_name = FILE_NAME_T
    if test:
        file_name = 'test/%s' % FILE_NAME_T

    close_df = get_t_series_df(file_name=file_name)['close (USD)']

    print_datetime_output(
        'Group time series by week on close price, computes min & max and calculates max relative span')
    min_max_close_price_df = pd.DataFrame()
    min_max_close_price_df['min'] = close_df.groupby(pd.Grouper(freq='W-MON')).min()
    min_max_close_price_df['max'] = close_df.groupby(pd.Grouper(freq='W-MON')).max()
    min_max_close_price_df['rel_span'] = ((min_max_close_price_df['max'] - min_max_close_price_df['min'])
                                          / min_max_close_price_df['min'])
    max_rel_span = min_max_close_price_df['rel_span'].max()
    week_max_rel_span = min_max_close_price_df[min_max_close_price_df['rel_span'] == max_rel_span].index.date[0]
    print_datetime_output('The week with max relative span is: %s' % week_max_rel_span)
    return week_max_rel_span


if __name__ == '__main__':

    if len(sys.argv) == 3:
        download_crypto_curr_to_csv(url=sys.argv[2])
    else:
        download_crypto_curr_to_csv()

    if sys.argv[1] == 'avg':
        compute_avg_weekly_price_to_csv()
    elif sys.argv[1] == 'span':
        get_week_of_max_relative_span()
