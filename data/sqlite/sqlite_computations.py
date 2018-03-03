import csv
import sqlite3

from computation_provider import ComputationProvider


class Sqlite(ComputationProvider):

    def __init__(self):
        """

        """
        super().__init__()
        self.db_name = self.config_parser.get('database', 'file_name')
        self.db_table = self.config_parser.get('database', 'table_name')
        self.download_crypto_curr_to_csv()
        self.create_sqlite_table()

    def create_sqlite_table(self, test=False):
        """
        Method establish sqlite database connection, creates data table and import data from csv file.
    
        :param test: if True (running in test mode), name of the csv file gets 'sqlite/test/' prefix
        :return: opened connection with sqlite db
        """
        file_name = '%s/%s' % (self.dir_path, self.time_series_file_name)
        if test:
            file_name = '%s/sqlite/test/%s' % (self.dir_path, self.time_series_file_name)

        self.print_datetime_output('Connect to data base %s' % self.db_name)
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()

        # check if table exists
        cur.execute("select count(*) from sqlite_master where type='table' and name='%s'" % self.db_table)
        if cur.fetchall()[0][0] == 1:
            self.print_datetime_output('Previous table %s was dropped' % self.db_table)
            cur.execute("DROP TABLE %s;" % self.db_table)

        self.print_datetime_output('Create table %s and import data from csv file %s' % (self.db_table, self.time_series_file_name))
        cur.execute(
            "CREATE TABLE %s (timestamp, close_USD);" % self.db_table)

        with open(file_name, 'r') as fin:
            dr = csv.DictReader(fin)
            to_db = [(i['timestamp'], i['close (USD)']) for i in dr]

        cur.executemany(
            "INSERT INTO %s (timestamp, close_USD) "
            "VALUES (?, ?);" % self.db_table,
            to_db)
        con.commit()
        return con

    def compute_avg_weekly_price_to_csv(self):
        raise NotImplementedError

    def get_week_of_max_relative_span(self):
        raise NotImplementedError
