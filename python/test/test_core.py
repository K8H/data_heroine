import datetime
import sys
import unittest
from contextlib import contextmanager
from io import StringIO

import pandas as pd
import requests

sys.path.append("..")
from python import core  # noqa


def get_df(file_name):
    """
    Returns pandas data frame of csv file

    :param file_name: name of the csv file
    :return: time series pandas.DataFrame
    """
    return pd.read_csv(file_name)


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


class CoreTestCase(unittest.TestCase):
    def setUp(self):
        self.core = core

    def test_print_datetime_output(self):
        with captured_output() as (out, err):
            self.core.print_datetime_output('hello world')
        output = out.getvalue().strip()
        self.assertEqual(output, '%s hello world' % '{:%Y-%m-%d %H:%M}'.format(datetime.datetime.now()))

    def test_print_datetime_no_msg(self):
        with captured_output() as (out, err):
            self.core.print_datetime_output()
        output = out.getvalue().strip()
        self.assertEqual(output, '%s' % '{:%Y-%m-%d %H:%M}'.format(datetime.datetime.now()))

    def test_download_crypto_curr_invalid_url(self):
        with self.assertRaises(SystemExit) as cm:
            requests.exceptions.MissingSchema, self.core.download_crypto_curr_to_csv(
                url='www.alphaantage.co/query?'
                    'function=DIGITAL_CURRENCY_DAILY&'
                    'symbol=BTC&'
                    'market=USD&'
                    'apikey=1LUM05IW26CBPVKM&'
                    'datatype=csv')
        self.assertEqual(cm.exception.code, 1)

    def test_store_to_csv_creates_csv(self):
        time_series = self.core.download_crypto_curr_to_csv()
        self.core.store_to_csv(time_series)
        self.assertIsInstance(get_df(self.core.FILE_NAME_T), pd.DataFrame)

    def test_store_to_csv_file_without_t_series(self):
        self.assertRaises(Exception, self.core.store_to_csv(''), 'Time series should not be None.')

    def test_compute_avg_weekly_price_df_returns_df(self):
        time_series = self.core.download_crypto_curr_to_csv()
        self.core.store_to_csv(time_series)
        self.core.compute_avg_weekly_price_to_csv()
        self.assertIsInstance(get_df(self.core.FILE_NAME_AVG), pd.DataFrame)

    def test_get_week_of_max_relative_span_in_memory_file(self):
        week_max_rel_span = self.core.get_week_of_max_relative_span(test=True)
        self.assertEqual(week_max_rel_span, datetime.date(2018, 2, 5))
