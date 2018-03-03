python
======

The aim of the software is to provide quick look on the Bitcoin stock market and derive some insights from it. It
collects some crypto currencies data, accessing the API provided by www.alphavantage.co. It calculates data for
"Daily Digital & Crypto Currencies", for currency ‘BTC’ and USD market

Requirements
------------
The software requires python version 3 and libraries ``pandas``, ``requests`` and ``configparser``.

Running the Software
--------------------

Software support two computation mode:
- In memory: using python libraries, run with ``$ python3 core.py --mode in_memory``
- Sqlite: using sqlite queries, run with ``$ python3 core.py --mode sqlite``

Both modes support two features:
- Computation of the average price of each week (stored into csv file, named 'avg_weekly_price.csv':
    ``$ python3 core.py --mode sqlite --feature avg``
- Computation of a week, that had the greatest relative span on close prices (date of the week printed on screen):
    ``$ python3 core.py --mode sqlite --feature span``

Running the Tests
-----------------
The tests can be run in cmd with ``$ python3 -m unittest discover -b`` where -b denotes nicer cmd output.

Configuration
-------------
Configuration file ``config.ini`` provides some default names for database and file names as well as api key
(grants access to API's data). Localy change name of file ``config.ini.template`` to ``config.ini`` and replace
``your_api_key`` with you own api key.


