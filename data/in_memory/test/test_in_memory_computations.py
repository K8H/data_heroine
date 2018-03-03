import datetime
import sys
import unittest

import pandas as pd


# sys.path.append("..")
from in_memory import in_memory_computations  # noqa


class InMemoryComputationsTestCase(unittest.TestCase):
    def setUp(self):
        self.in_memory = in_memory_computations.InMemory()

    def test_compute_avg_weekly_price_df_returns_df(self):
        self.in_memory.download_crypto_curr_to_csv()
        self.in_memory.compute_avg_weekly_price_to_csv()
        self.assertIsInstance(pd.read_csv(self.in_memory.avg_price_file_name), pd.DataFrame)

    def test_get_week_of_max_relative_span_in_memory_file(self):
        week_max_rel_span = self.in_memory.get_week_of_max_relative_span(test=True)
        self.assertEqual(week_max_rel_span, datetime.date(2015, 1, 18))
