import sys
import unittest

# sys.path.append("..")
from sqlite import sqlite_computations  # noqa


class SqliteComputationsTestCase(unittest.TestCase):
    def setUp(self):
        self.sqlite = sqlite_computations.Sqlite()

    def test_create_sqlite_table_created(self):
        connection = self.sqlite.create_sqlite_table(True)
        cur = connection.cursor()
        cur.execute("select count(*) from sqlite_master where type='table' and name='%s'" % self.sqlite.db_table)
        self.assertEqual(cur.fetchall()[0][0], 1)
