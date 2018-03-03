import unittest
import sys
import datetime

import pandas as pd

sys.path.append("..")
from data import computation_provider   # noqa


class ComputationProviderTestCase(unittest.TestCase):
    def setUp(self):
        self.computation_provider = computation_provider.ComputationProvider()

    def test_compute_avg_weekly_price_to_csv_not_implemented(self):
        self.assertRaises(NotImplementedError)

    def test_get_week_of_max_relative_span_not_implemented(self):
        self.assertRaises(NotImplementedError)

    def test_print_datetime_output(self):
        with self.computation_provider.captured_output() as (out, err):
            self.computation_provider.print_datetime_output('hello world')
        output = out.getvalue().strip()
        self.assertEqual(output, '%s hello world' % '{:%Y-%m-%d %H:%M}'.format(datetime.datetime.now()))

    def test_print_datetime_no_msg(self):
        with self.computation_provider.captured_output() as (out, err):
            self.computation_provider.print_datetime_output()
        output = out.getvalue().strip()
        self.assertEqual(output, '%s' % '{:%Y-%m-%d %H:%M}'.format(datetime.datetime.now()))

    def test_store_to_csv_creates_csv(self):
        self.computation_provider.download_crypto_curr_to_csv()
        self.assertIsInstance(pd.read_csv(self.computation_provider.time_series_file_name), pd.DataFrame)

    def test_store_to_csv_file_without_t_series(self):
        self.assertRaises(Exception, self.computation_provider.store_to_csv(''), 'Time series should not be None.')
