import os
import unittest

import collections
import requests
import python.core as core


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

    def test_store2cvs_file(self):
        time_series = self.core.download_crypto_curr()
        csv_file = self.core.store2cvs_file(time_series)
        self.assertIsInstance(csv_file, collections.Iterator)
