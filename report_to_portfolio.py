# -*- coding: utf-8 -*-
# !/usr/local/bin/python3

# Project name: Saxo Bank To Portfolio Manager
# Version: 0.1
# Written by Simonepsp

import argparse
import os
import sys
import json
import pandas as pd
import csv


class Main(object):

    # Settings
    CONFIG_FILE_PATH = 'config.json'
    UTILITY_NAME = 'Saxo Bank (SB) XLSX Report ---> Portfolio Manager CSV'
    KNOWN_CURRENCIES = ['USD', 'EUR', 'GBP'] # EDIT ME IF YOUR CURRENCY IS MISSING

    CSV_HEADER = ['Date', 'Cash Account', 'Security Name', 'Type', 'Shares', 'Value', 'Transaction Currency', 'Note']
    TRANSACTION_TYPES_MAPPING = {'Cash Amount': 'Deposit',
                                'Cash dividend': 'Dividend',
                                'Custody Fee': 'Fees',
                                'VAT': 'Taxes'}

    # Saxo Bank report xlsx columns mappings
    XLS_COL_TRADE_DATE = 0
    XLS_COL_ACCOUNT_ID = 1
    XLS_COL_ASSET_TYPE = 2
    XLS_COL_INSTRUMENT_NAME = 3
    XLS_COL_INSTRUMENT_ID = 4
    XLS_COL_TRANSACTION_TYPE = 5
    XLS_COL_EVENT = 6
    XLS_COL_CORPORATE_ACTION_ID = 7
    XLS_COL_TRADE_ID = 8
    XLS_COL_AMOUNT = 9
    XLS_COL_PRICE = 10
    XLS_COL_BOOKED_AMOUNT_CLIENT_CUR = 11
    XLS_COL_BOOKED_AMOUNT_INSTRUMENT_CUR = 12
    XLS_COL_BOOKED_AMOUNT_ACCOUNT_CUR = 13

    def run(self):
        # === Args ===
        parser = argparse.ArgumentParser(
            description="\033[95m** %s ** \033[0m" % self.UTILITY_NAME)
        parser.add_argument(
            '-i', '--filePath', help='XLSX Report file path (.xlsx allowed)', type=str, required=True)
        # parser.add_argument(
        #     '-f', '--folder', help='(Batch mode) .xlsx files path', type=str, required=False)
        parser.add_argument(
            '-o', '--output', help='Write output to a .csv file', type=str, required=True)
        parser.add_argument(
            '-v', '--verbose', help='Verbose', default=False, action='store_true')

        args = parser.parse_args()

        self.osClear()
        print(self.UTILITY_NAME)

        # Check if config file exists
        if not os.path.isfile(self.CONFIG_FILE_PATH):
            print('Creating config file')
            with open(self.CONFIG_FILE_PATH, 'w') as fp:
                pass

        def getConfig(path):
            with open(path, mode='r') as configFile:
                try:
                    return json.load(configFile)
                except Exception as ex:
                    print(ex)
                    sys.exit('Not a valid JSON config file')

        def saveConfig(path, config):
            with open(path, 'w') as configFile:
                json.dump(config, configFile)
                return True

        config = getConfig(self.CONFIG_FILE_PATH)

        if not 'accounts' in config:
            config['accounts'] = {}

        # Check if file has an allowed extension
        if not '.xlsx' in args.filePath:
            sys.exit('File must have an .xlsx extension')

        # Check if report path exists
        if not os.path.isfile(args.filePath):
            sys.exit('Report file not found. Double check provided path [-i]')

        # Parse pdf file
        print('Reading %s' % args.filePath)
        # Load xls file
        xls = pd.read_excel(args.filePath,
                            'Transactions', 
                            keep_default_na=False)

        # Add csv extension if missing
        if not '.csv' in args.output[-4:]:
            outputPath = args.output + '.csv'
        else:
            outputPath = args.output

        print('Will write to ---> %s\n' % outputPath)

        # Open csv file for write
        csvFile = open(outputPath, 'w')
        csvWriter = csv.writer(csvFile)

        # Write header
        csvWriter.writerow(self.CSV_HEADER)

        rows = []
        # Loop through Transactions
        for transaction in xls.values:

            accountID = transaction[self.XLS_COL_ACCOUNT_ID]

            # Add new account ID to config if undiscovered
            if not accountID in config['accounts']:

                # Ask user what currency account has
                currency = self.askCurrency(accountID)

                config['accounts'][accountID] = {'currency': currency}
                saveConfig(self.CONFIG_FILE_PATH, config)

            # Extract transaction data
            date = transaction[self.XLS_COL_TRADE_DATE]
            securityName = transaction[self.XLS_COL_INSTRUMENT_NAME]
            transactionType = transaction[self.XLS_COL_EVENT]

            # Translate transaction type to a compatible one
            if transactionType in self.TRANSACTION_TYPES_MAPPING:
                transactionType = self.TRANSACTION_TYPES_MAPPING[transactionType]

            qty = transaction[self.XLS_COL_AMOUNT]
            if qty == '-':
                qty = ''
                
            price = transaction[self.XLS_COL_BOOKED_AMOUNT_INSTRUMENT_CUR]

            if price == '-':
                price = ''

            currency = config['accounts'][accountID]['currency']
            note = transaction[self.XLS_COL_TRANSACTION_TYPE]

            # Add to row
            rows.append([date, accountID, securityName, transactionType, qty, price, currency, note])
        
        csvWriter.writerows(rows)

        csvFile.close()

        print('- Done -')
    # Ask user what currency an account ID is set on
    def askCurrency(self, accountID):

        while True:
            currency = input("** NEW ACCOUNT discovered ** [ID %s].\nPlease provide currency code (eg. %s):  " % (
                accountID, self.KNOWN_CURRENCIES[:5]))
            
            if not currency in self.KNOWN_CURRENCIES:
                print("\nSorry, I don't recognise that currency!\nAllowed currency codes are: %s\n" %
                      self.KNOWN_CURRENCIES)
                continue

            return currency.upper()

    def osClear(self):
        # CLEAR SCREEN
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')


if __name__ == '__main__':
    try:
        Main().run()
    except KeyboardInterrupt:
        print('\n\nScript terminated. Bye! ^^')
