# -*- coding: utf-8 -*-
import sys
import pandas as pd


FILE_NAME_AVG = 'avg_weekly_price.csv'
FILE_NAME_T = 'time_series.csv'


def store_pd2csv(df, file_name):
    """
    Stores pandas data frame into csv file.

    :param df: data frame to be stored into csv file
    :param file_name: name of the csv file
    """
    df.to_csv(file_name)


class DataImport(object):
    def __init__(self, url='https://www.alphavantage.co/query?'
                           'function=DIGITAL_CURRENCY_DAILY&'
                           'symbol=BTC&'
                           'market=USD&'
                           'apikey=1LUM05IW26CBPVKM&'
                           'datatype=csv'):
        self.url = url

    def download_crypto_curr(self):
        """
        Downloads the historical time series from the API. 

        Makes GET request to API's endpoint for the "Daily Digital & Crypto Currencies", specifying as symbol ‘BTC’ and as 
        market ‘USD’.

        :return: a response of API
        """
        import requests

        try:
            response = requests.get(self.url)
            return response
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

    @staticmethod
    def store2cvs_file(time_series, file_name):
        """
        Takes API's response in bytes and store row after row into csv file, named 'time_series.csv'

        :param time_series: API's response in bytes
        """
        import csv

        if time_series:
            with open(file_name, 'w') as f:
                writer = csv.writer(f)
                reader = csv.reader(time_series.text.splitlines())

                for row in reader:
                    writer.writerow(row)
        return Exception('Time series should not be None.')


class DataComputations(object):

    def __init__(self, file_name):
        self.file_name = file_name

    def avg_weekly_price(self):
        """
        Groups timestamps by week and computes mean price on each group. 

        :return: GroupBy object of average weekly values
        """
        df = self.get_t_series_df()
        return df.groupby(pd.TimeGrouper(freq='W')).mean()

    def max_relative_span(self):
        """
        Compute what is the week that had the greatest relative span on closing prices (difference between the maximum and 
        minimum closing price, divided by the minimum closing price), and print this on screen.

        Mathematically: relative_span = (max(price) min(price)) / min(price)

        :return: date of a week with the maximum relative span on closing prices
        """
        open_df = self.get_t_series_df()['open (USD)']
        min_max_df = pd.DataFrame()
        min_max_df['min'] = open_df.groupby(pd.TimeGrouper(freq='W')).min()
        min_max_df['max'] = open_df.groupby(pd.TimeGrouper(freq='W')).max()
        min_max_df['rel_span'] = ((min_max_df['max'] - min_max_df['min']) / min_max_df['min'])
        max_rel_span = min_max_df['rel_span'].max()
        return min_max_df[min_max_df['rel_span'] == max_rel_span].index.date[0]

    def get_t_series_df(self):
        """
        Returns pandas data frame of csv file

        :return: time series pandas.DataFrame
        """
        df = pd.read_csv(self.file_name).set_index('timestamp')
        df.index = pd.to_datetime(df.index)
        return df


if __name__ == '__main__':
    if len(sys.argv) == 3:
        data_import = DataImport(url=sys.argv[2])
        t_series = data_import.download_crypto_curr()
        data_import.store2cvs_file(time_series=t_series, file_name=FILE_NAME_T)
    else:
        data_import = DataImport()
        t_series = data_import.download_crypto_curr()
        data_import.store2cvs_file(time_series=t_series, file_name=FILE_NAME_T)

    data_computations = DataComputations(FILE_NAME_AVG)

    if sys.argv[1] == 'avg':
        avg_weekly_df = data_computations.avg_weekly_price()
        store_pd2csv(avg_weekly_df, FILE_NAME_AVG)
    elif sys.argv[1] == 'span':
        rel_span = data_computations.max_relative_span()
        print(rel_span)
