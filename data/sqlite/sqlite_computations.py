import sys
import csv
import sqlite3

sys.path.append("..")
import data.core as core    # noqa

SQLITE_FILE = 'crypto_curr.sqlite'  # name of the sqlite database file
TABLE_NAME = 'daily_usd_btc'  # name of the table to be created


def create_sqlite_table(test=False):

    file_name = core.FILE_NAME_T
    if test:
        file_name = 'sqlite/test/%s' % core.FILE_NAME_T          # TODO delete data/sqlite

    core.print_datetime_output('Connect to data base %s' % SQLITE_FILE)
    con = sqlite3.connect(SQLITE_FILE)
    cur = con.cursor()

    # check if table exists
    cur.execute("select count(*) from sqlite_master where type='table' and name='%s'" % TABLE_NAME)
    if cur.fetchall()[0][0] == 1:
        core.print_datetime_output('Previous table %s was dropped' % TABLE_NAME)
        cur.execute("DROP TABLE %s;" % TABLE_NAME)

    core.print_datetime_output('Create table %s and import data from csv file %s' % (TABLE_NAME, core.FILE_NAME_T))
    cur.execute(
        "CREATE TABLE %s (timestamp, open_USD, high_USD, low_USD, close_USD, volume, market_cap_USD);" % TABLE_NAME)

    with open(file_name, 'r') as fin:
        dr = csv.DictReader(fin)
        to_db = [(i['timestamp'], i['open (USD)'], i['high (USD)'], i['low (USD)'], i['close (USD)'], i['volume'],
                  i['market cap (USD)']) for i in dr]

    cur.executemany(
        "INSERT INTO %s (timestamp, open_USD, high_USD, low_USD, close_USD, volume, market_cap_USD) "
        "VALUES (?, ?, ?, ?, ?, ?, ?);" % TABLE_NAME,
        to_db)
    con.commit()
    return con


if __name__ == '__main__':
    core.download_crypto_curr_to_csv()
    connection = create_sqlite_table()
    connection.close()
