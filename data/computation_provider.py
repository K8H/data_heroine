import csv
import datetime
import os
import sys
from contextlib import contextmanager

import requests

from configparser import ConfigParser
from io import StringIO

FILE_NAME_AVG = 'avg_weekly_price.csv'
FILE_NAME_T = 'time_series.csv'


class ComputationProvider(object):
    def __init__(self):
        self.dir_path = os.path.dirname(os.path.abspath(__file__))

        ComputationProvider.print_datetime_output('Reads values from \'config.ini\' file.')
        self.config_parser = ConfigParser()
        self.config_parser.read(self.dir_path + '/config.ini')

        self.api_key = self.config_parser.get('download_crypto', 'api_key')
        self.time_series_file_name = self.config_parser.get('file_name', 'time_series')
        self.avg_price_file_name = self.config_parser.get('file_name', 'average')

    def compute_avg_weekly_price_to_csv(self):
        raise NotImplementedError

    def get_week_of_max_relative_span(self):
        raise NotImplementedError

    def download_crypto_curr_to_csv(self):
        """
        Downloads the historical time series from the API anf store them into csv file.

        Makes GET request to API's endpoint for the "Daily Digital & Crypto Currencies", specifying as symbol ‘BTC’ and 
        as market ‘USD’.

        :return: a response of API
        """
        url = ('https://www.alphavantage.co/query?'
               'function=DIGITAL_CURRENCY_DAILY&'
               'symbol=BTC&'
               'market=USD&'
               'apikey=%s&'
               'datatype=csv' % self.api_key)
        try:
            self.print_datetime_output('Make request to url \'%s\'' % url)
            response = requests.get(url)
            self.store_to_csv(response)
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

    @staticmethod
    def print_datetime_output(output=''):
        """
        Prints the cmd output with formatted date and time.
        """
        print('{:%Y-%m-%d %H:%M}'.format(datetime.datetime.now()), output)

    def store_to_csv(self, time_series):
        """
        Takes API's response in bytes and store row after row into csv file, named 'time_series.csv'

        :param time_series: API's response in bytes
        """
        if time_series:
            self.print_datetime_output('Store response to file \'%s\'' % self.time_series_file_name)
            with open(self.time_series_file_name, 'w') as f:
                writer = csv.writer(f)
                reader = csv.reader(time_series.text.splitlines())

                for row in reader:
                    writer.writerow(row)
        return Exception('Time series should not be None.')

    @contextmanager
    def captured_output(self):
        new_out, new_err = StringIO(), StringIO()
        old_out, old_err = sys.stdout, sys.stderr
        try:
            sys.stdout, sys.stderr = new_out, new_err
            yield sys.stdout, sys.stderr
        finally:
            sys.stdout, sys.stderr = old_out, old_err
