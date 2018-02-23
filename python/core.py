import sys


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

    with open('time_series.csv', 'w') as f:
        writer = csv.writer(f)
        reader = csv.reader(time_series.text.splitlines())

        for row in reader:
            writer.writerow(row)
        return f


if __name__ == '__main__':
    t_series = download_crypto_curr()
    store2cvs_file(time_series=t_series)
    print('blablablabl')
