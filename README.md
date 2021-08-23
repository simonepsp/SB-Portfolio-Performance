# About

A simple yet functional Saxo Bank Transactions report to Portfolio Manager (.csv file).

## Prerequisites

* [Python 3.X]
* [Pandas for python] pip install pandas, pip install openpyxl

## What is this transactions report
If you are familiar with Saxo Bank Trader interface you probably know what I'm talking 'bout.
If not, log in into your Saxo Trader account and head to Account --> Historic Reports --> Transaction Report --> Export --> Excel.

Once you have an .xlsx file downloaded, you are ready to go.

## How to run
python report_to_portfolio.py -i YOUR_TRANSACTIONS_FILE.xlsx -o output.csv

## How to import into Portfolio manager

File --> Import --> CSV Files

## License

GNU General Public License v3.0 (gpl-3.0)