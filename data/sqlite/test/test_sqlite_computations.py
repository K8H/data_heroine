import sys
import unittest

sys.path.append("..")
from data.sqlite import sqlite_computations  # noqa


class CoreTestCase(unittest.TestCase):
    def setUp(self):
        self.sqlite = sqlite_computations

    def test_create_sqlite_table_created(self):
        connection = self.sqlite.create_sqlite_table(True)
        cur = connection.cursor()
        cur.execute("select count(*) from sqlite_master where type='table' and name='%s'" % self.sqlite.TABLE_NAME)
        self.assertEqual(cur.fetchall()[0][0], 1)
