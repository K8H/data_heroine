import sys
import pandas as pd

FILE_NAME_T = 'time_series.csv'
FILE_NAME_AVG = 'avg_weekly_price.csv'


def download_crypto_curr(url='https://www.alphavantage.co/query?' 
                             'function=DIGITAL_CURRENCY_DAILY&' 
                             'symbol=BTC&' 
                             'market=USD&' 
                             'apikey=1LUM05IW26CBPVKM&' 
                             'datatype=csv'):
    """
    Downloads the historical time series from the API. 
    
    Makes GET request to API's endpoint for the "Daily Digital & Crypto Currencies", specifying as symbol ‘BTC’ and as 
    market ‘USD’.
        
    :return: a response of API
    """
    import requests

    try:
        response = requests.get(url)
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)


def store2cvs_file(time_series):
    """
    Takes API's response in bytes and store row after row into csv file, named 'time_series.csv'
    
    :param time_series: API's response in bytes
    """
    import csv

    if time_series:
        with open(FILE_NAME_T, 'w') as f:
            writer = csv.writer(f)
            reader = csv.reader(time_series.text.splitlines())

            for row in reader:
                writer.writerow(row)
    return Exception('Time series should not be None.')


def get_t_series_df():
    """
    Returns pandas data frame of csv file
    
    :return: time series pandas.DataFrame
    """
    df = pd.read_csv(FILE_NAME_T).set_index('timestamp')
    df.index = pd.to_datetime(df.index)
    return df


def avg_weekly_price():
    """
    Groups timestamps by week and computes mean price on each group. The data frame is stored to a csv file. 
    """
    df = get_t_series_df()
    mean_weekly_df = df.groupby(pd.TimeGrouper(freq='W')).mean()
    mean_weekly_df.to_csv(FILE_NAME_AVG)

if __name__ == '__main__':
    t_series = download_crypto_curr()
    store2cvs_file(time_series=t_series)
    avg_weekly_price()
