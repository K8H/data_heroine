import csv
import datetime
import sys
import requests

from configparser import ConfigParser


FILE_NAME_T = 'time_series.csv'
FILE_NAME_AVG = 'avg_weekly_price.csv'


def get_conf_api_key():
    """
    Config parser reads 'config.ini' file and returns api key value.

    :return: api key string value
    """
    print_datetime_output('Reads api key value from \'config.ini\' file.')
    config_parser = ConfigParser()
    config_parser.read('config.ini')
    return config_parser.get('download_crypto', 'api_key')


def print_datetime_output(output=''):
    """
    Prints the cmd output with formatted date and time.
    """
    print('{:%Y-%m-%d %H:%M}'.format(datetime.datetime.now()), output)


def download_crypto_curr_to_csv(url=('https://www.alphavantage.co/query?'
                                     'function=DIGITAL_CURRENCY_DAILY&'
                                     'symbol=BTC&'
                                     'market=USD&'
                                     'apikey=%s'
                                     'datatype=csv' % get_conf_api_key())):
    """
    Downloads the historical time series from the API anf store them into csv file.

    Makes GET request to API's endpoint for the "Daily Digital & Crypto Currencies", specifying as symbol ‘BTC’ and as 
    market ‘USD’.

    :return: a response of API
    """
    try:
        print_datetime_output('Make request to url \'%s\'' % url)
        response = requests.get(url)
        store_to_csv(response)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)


def store_to_csv(time_series):
    """
    Takes API's response in bytes and store row after row into csv file, named 'time_series.csv'

    :param time_series: API's response in bytes
    """
    if time_series:
        print_datetime_output('Store response to file \'%s\'' % FILE_NAME_T)
        with open(FILE_NAME_T, 'w') as f:
            writer = csv.writer(f)
            reader = csv.reader(time_series.text.splitlines())

            for row in reader:
                writer.writerow(row)
    return Exception('Time series should not be None.')