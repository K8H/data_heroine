import unittest

import datetime
import pandas as pd

from sqlite import sqlite_computations


class SqliteComputationsTestCase(unittest.TestCase):
    def setUp(self):
        self.sqlite = sqlite_computations.Sqlite(True)

    def test_create_sqlite_table_created(self):
        connection = self.sqlite.create_sqlite_table()
        cur = connection.cursor()
        cur.execute("select count(*) from sqlite_master where type='table' and name='%s'" % self.sqlite.db_table)
        self.assertEqual(cur.fetchall()[0][0], 1)

    def test_compute_avg_weekly_price_df_returns_df(self):
        self.sqlite.compute_avg_weekly_price_to_csv()
        self.assertIsInstance(pd.read_csv('%s/%s' % (self.sqlite.dir_path, self.sqlite.avg_price_file_name)),
                              pd.DataFrame)

    def test_compute_avg_weekly_price_df_correct_calculations(self):
        self.sqlite.compute_avg_weekly_price_to_csv()
        avg_df = pd.read_csv('%s/%s' % (self.sqlite.dir_path, self.sqlite.avg_price_file_name))
        self.assertEqual(avg_df.get('20140405')[1], '430.9361690214286')

    def test_get_week_of_max_relative_span_in_memory_file(self):
        week_max_rel_span = self.sqlite.get_week_of_max_relative_span()
        self.assertEqual(datetime.datetime.strptime(week_max_rel_span, '%Y-%M-%d').date(), datetime.date(2015, 1, 9))
