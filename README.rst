python
======

The aim of the software is to provide quick look on the Bitcoin stock market and derive some insights from it. It
collects some crypto currencies data, accessing the API provided by www.alphavantage.co.

Two main features have been developed:
- Computation of the average price of each week (stored into csv file, named 'avg_weekly_price.csv'
- Computation of a week, that had the greatest relative span on closing prices (date of the week printed on screen)

Requirements
------------
The software requires python version 3 and libraries ``pandas``, ``requests`` and ``configparser``.

Running the Software
--------------------

First feature can be run in cmd with ``$ python3 in_memory/in_memory_computations.py --feature avg`` and the second with
command ``$ python3 in_memory/in_memory_computations.py --feature span``

By default it calculates data for "Daily Digital & Crypto Currencies", for currency ‘BTC’ and USD market, although it
may be altered by passing URL, which specifies different parameters (for additional info check see
[documentation](https://www.alphavantage.co/documentation/) ). In such case run the software with:
``$ python3 core.py --feature avg --url url_with_custom_parameters``

Running the Tests
-----------------
The tests can be run in cmd with ``$ python3 -m unittest discover -b`` where -b denotes nicer cmd output.


