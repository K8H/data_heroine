import datetime
import unittest

import pandas as pd
import requests
import python.core as core


def get_df(file_name):
    """
    Returns pandas data frame of csv file

    :param file_name: name of the csv file
    :return: time series pandas.DataFrame
    """
    return pd.read_csv(file_name)


class CoreTestCase(unittest.TestCase):

    def setUp(self):
        self.core = core

    def test_download_crypto_curr_status(self):
        response = self.core.download_crypto_curr()
        self.assertEquals(200, response.status_code)

    def test_download_crypto_curr_invalid_url(self):
        with self.assertRaises(SystemExit) as cm:
            requests.exceptions.MissingSchema, self.core.download_crypto_curr(url='www.alphaantage.co/query?'
                                                                                  'function=DIGITAL_CURRENCY_DAILY&'
                                                                                  'symbol=BTC&'
                                                                                  'market=USD&'
                                                                                  'apikey=1LUM05IW26CBPVKM&'
                                                                                  'datatype=csv')
        self.assertEqual(cm.exception.code, 1)

    def test_download_crypto_curr_content(self):
        response = self.core.download_crypto_curr()
        self.assertEquals(b'timestamp', response.content[:9])

    def test_store2cvs_file_df(self):
        time_series = self.core.download_crypto_curr()
        self.core.store2cvs_file(time_series)
        self.assertIsInstance(get_df(self.core.FILE_NAME_T), pd.DataFrame)

    def test_store2cvs_file_no_t_series(self):
        self.assertRaises(Exception, self.core.store2cvs_file(''), 'Time series should not be None.')

    def test_avg_weekly_price_df(self):
        time_series = self.core.download_crypto_curr()
        self.core.store2cvs_file(time_series)
        self.core.avg_weekly_price()
        self.assertIsInstance(get_df(self.core.FILE_NAME_AVG), pd.DataFrame)

    def test_max_relative_span(self):
        week_max_rel_span = self.core.max_relative_span()
        self.assertEquals(week_max_rel_span, datetime.date(2017, 12, 10))
