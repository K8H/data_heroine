import csv
import sqlite3

import pandas as pd
from computation_provider import ComputationProvider


class Sqlite(ComputationProvider):

    def __init__(self, test=False):
        """
        The class provides calculations on data, that are stored in sqlite database, executing queries.
        """
        super().__init__()
        self.db_name = self.config_parser.get('database', 'file_name')
        self.db_table = self.config_parser.get('database', 'table_name')

        self.file_name = '%s/%s' % (self.dir_path, self.time_series_file_name)
        if test:
            self.file_name = '%s/sqlite/test/%s' % (self.dir_path, self.time_series_file_name)

        self.download_crypto_curr_to_csv()
        self.connection = self.create_sqlite_table()

    def create_sqlite_table(self):
        """
        Method establish sqlite database connection, creates data table and import data from csv file.
    
        :return: opened connection with sqlite db
        """
        self.print_datetime_output('Connect to data base %s' % self.db_name)
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()

        # check if table exists
        cur.execute("select count(*) from sqlite_master where type='table' and name='%s'" % self.db_table)
        if cur.fetchall()[0][0] == 1:
            self.print_datetime_output('Previous table %s was dropped' % self.db_table)
            cur.execute("DROP TABLE %s;" % self.db_table)

        self.print_datetime_output('Create table %s and import data from csv file %s' % (self.db_table,
                                                                                         self.time_series_file_name))
        cur.execute("CREATE TABLE %s (timestamp, close_USD);" % self.db_table)

        with open(self.file_name, 'r') as fin:
            dr = csv.DictReader(fin)
            to_db = [(i['timestamp'], i['close (USD)']) for i in dr]

        cur.executemany("INSERT INTO %s (timestamp, close_USD) VALUES (?, ?);" % self.db_table, to_db)
        con.commit()
        return con

    def compute_avg_weekly_price_to_csv(self):
        """
        Groups timestamps by week, computes mean close price on each group and store the data frame into csv file.
        """
        c = self.connection.cursor()
        self.print_datetime_output('Group time series by week and compute mean price')
        query = "SELECT min((strftime('%Y%m%d', timestamp)/7*7 - 19000101) + 19000106) AS start_day, timestamp, " \
                "avg(close_USD) FROM " + self.db_table + " GROUP BY (strftime('%Y%m%d', timestamp) - 19000106)/7"
        c.execute(query)
        avg_close_by_week_df = pd.DataFrame({x[0]: x[1:] for x in c.fetchall()})
        self.print_datetime_output('Store data frame to file \'%s\'' % self.avg_price_file_name)
        avg_close_by_week_df.to_csv('%s/%s' % (self.dir_path, self.avg_price_file_name))

    def get_week_of_max_relative_span(self):
        """
        Compute what is the week that had the greatest relative span on closing prices (difference between the maximum 
        and minimum closing price, divided by the minimum closing price), and prints it on a screen.
    
        Mathematically: relative_span = (max(price) min(price)) / min(price)
    
        :return: date of a week with the maximum relative span on closing prices
        """
        c = self.connection.cursor()
        self.print_datetime_output('Group time series by week and compute mean price')
        query = "SELECT min((strftime('%Y%m%d', timestamp)/7*7 - 19000101) + 19000106) AS start_day, timestamp, " \
                "min(close_USD), max(close_USD) FROM " + self.db_table + " GROUP BY (strftime('%Y%m%d', timestamp) - " \
                                                                         "19000106)/7"
        c.execute(query)
        min_max_close_week_df = pd.DataFrame(c.fetchall())
        min_max_close_week_df.columns = ['date', 'date_2', 'min', 'max']
        min_max_close_week_df['min'] = min_max_close_week_df['min'].astype(float)
        min_max_close_week_df['max'] = min_max_close_week_df['max'].astype(float)

        min_max_close_week_df['rel_span'] = ((min_max_close_week_df['max'] - min_max_close_week_df['min']) /
                                             min_max_close_week_df['min'])
        max_rel_span = min_max_close_week_df['rel_span'].max()
        week_max_rel_span = min_max_close_week_df[min_max_close_week_df['rel_span'] == max_rel_span]['date_2'].values[0]
        self.print_datetime_output('The week with max relative span is: %s' % week_max_rel_span)
        return week_max_rel_span
