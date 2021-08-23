# About

A simple yet functional Saxo Bank Transactions report to Portfolio Performance (.csv file) tool.

See https://www.portfolio-performance.info/

## Prerequisites

* [Python 3.X]
* [Pandas for python] pip install pandas, pip install openpyxl

## Transactions report
If you are familiar with Saxo Bank Trader interface you probably know what I'm talking 'bout.
If not, log in into your Saxo Trader account and head to Account --> Historic Reports --> Transaction Report --> Export --> Excel.

Once you have an .xlsx file downloaded, you are all set.

## Why didn't you just write a csv configuration for Portfolio Performance / 're u dumb?
First of all since Saxo Bank doesn't provide a .csv file I would have had to convert their xlsx file either through the impressive xlsx2csv or by exporting manually on Numbers / OnlyOffice / younameit.

Also, even after converting it, the transaction report contains dashes which produce import errors on Portfolio Performance. That sucks.

My script also automatically translates the transaction type to a compatible one so that you don't have to. 
And yeah, it stores transaction currencies too! No more currency mismatch errors on PM

This script wasn't meant to be public but I feel like it could be useful to whoever uses Saxo Bank services.
Feel free to send me PR requests or open issues if something doesn't work for you.

## How to run
python report_to_portfolio.py -i YOUR_TRANSACTIONS_FILE.xlsx -o output.csv

## How to import into Portfolio Performance

File --> Import --> CSV Files

## License

GNU General Public License v3.0 (gpl-3.0)