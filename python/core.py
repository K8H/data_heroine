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


def store_pd2csv(df, file_name):
    """
    Stores pandas data frame into csv file.

    :param df: data frame to be stored into csv file
    :param file_name: name of the csv file
    """
    df.to_csv(file_name)


def avg_weekly_price():
    """
    Groups timestamps by week and computes mean price on each group. 
    
    :return: GroupBy object of average weekly values
    """
    df = get_t_series_df()
    return df.groupby(pd.TimeGrouper(freq='W')).mean()


def max_relative_span():
    """
    Compute what is the week that had the greatest relative span on closing prices (difference between the maximum and 
    minimum closing price, divided by the minimum closing price), and print this on screen.
    
    Mathematically: relative_span = (max(price) min(price)) / min(price)
    
    :return: date of a week with the maximum relative span on closing prices
    """
    open_df = get_t_series_df()['open (USD)']
    min_max_df = pd.DataFrame()
    min_max_df['min'] = open_df.groupby(pd.TimeGrouper(freq='W')).min()
    min_max_df['max'] = open_df.groupby(pd.TimeGrouper(freq='W')).max()
    min_max_df['rel_span'] = ((min_max_df['max'] - min_max_df['min']) / min_max_df['min'])
    max_rel_span = min_max_df['rel_span'].max()
    return min_max_df[min_max_df['rel_span'] == max_rel_span].index.date[0]

if __name__ == '__main__':
    if len(sys.argv) == 3:
        t_series = download_crypto_curr(url=sys.argv[2])
        store2cvs_file(time_series=t_series)
    else:
        t_series = download_crypto_curr()
        store2cvs_file(time_series=t_series)

    if sys.argv[1] == 'avg':
        avg_weekly_df = avg_weekly_price()
        store_pd2csv(avg_weekly_df, FILE_NAME_AVG)
    elif sys.argv[1] == 'span':
        rel_span = max_relative_span()
        print(rel_span)
