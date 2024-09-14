#!/usr/bin/env/python3.12

import csv
import gspread
import os


'''
This script will pull the data from a Google Sheet and save to a local .csv file to prevent multiple api hits.

Run with `python3 data-extractor.py`
'''

try:
    SHEET_NAME = os.environ["SHEET_NAME"]
    CRED_FILE = os.environ["CRED_FILE"]
    DATA_FILE = os.environ["DATA_FILE"]
except KeyError as e:
    print(f"ERROR: Missing necessary environment variable: {e}")
    raise SystemExit(1)


gc = gspread.service_account(filename=CRED_FILE)
data = gc.open(SHEET_NAME).sheet1.get()

with open(DATA_FILE, 'w') as outfile:
    writer = csv.writer(outfile)
    for row in data:
        writer.writerow(row)