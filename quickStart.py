from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import json
from pprint import pprint
from googleapiclient import discovery
import string
from dataCollection import *

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a spreadsheet.
SPREADSHEET_ID = '1fOpQr0Sh7zIdXwH0J-BiWk9egr_VPOnYgZ5HPjgqe3k'

'''
Parameters for market stats data:
    market	Market whose statistics are being fetched.
            Can be one of MARKET_BTC_USD, MARKET_ETH_USD, MARKET_LINK_USD
    days	Specified day range for the statistics to have been compiled over. 
            Can be one of 1, 7, 30.
'''
MARKET = MARKET_BTC_USD
DAYS = 7
    
def get_markets(sheet, values = []):
    all_markets = markets()
    for market in all_markets['markets']:
        each_market = []
        keys = []
        for key in all_markets['markets'][market]:
            keys.append(key)
            each_market.append(all_markets['markets'][market][key])
        values.append(each_market)
        
    data = [
        {
        "range": "Markets!A1:S5",
        "majorDimension": "ROWS",
        "values": [keys, values[0], values[1], values[2]]
        },
    ]
    body = {
        'valueInputOption': 'USER_ENTERED',
        'data': data
    }
    marketsResults = sheet.values().batchUpdate(
        spreadsheetId=SPREADSHEET_ID, body=body).execute()
    print('{0} cells updated.'.format(marketsResults.get('totalUpdatedCells')))

def get_market_stats(sheet, values = []):
    marketStats = market_stats(MARKET, DAYS)
    values = [["days", str(DAYS)]]
    for markets in marketStats['markets']:
        count_key = 0
        for key in marketStats['markets'][markets]:
            count_key += 1
            values.append([key, marketStats['markets'][markets][key]])
    range = "MarketStats!A1:{}2".format(string.ascii_uppercase[count_key])
    body = {
            'values': values,
            'majorDimension':'COLUMNS',
        }
    marketStatResults = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID, range=range, 
        valueInputOption='USER_ENTERED', body=body).execute()
    print('{0} cells updated.'.format(marketStatResults.get('updatedCells')))

def get_orderbook(sheet):
    orderbookStats = orderbook(MARKET)
    bids, asks = [], []
    bid_count, ask_count = 0, 0
    for entry in orderbookStats['bids']:
        bids.append([entry['price'], entry['size']])
        bid_count += 1
    for entry in orderbookStats['asks']:
        asks.append([entry['price'], entry['size']])
        ask_count += 1

    data = [
        {
        "range": "Orderbook!A1:B2",
        "majorDimension": "ROWS",
        "values": [
                ["Bids", MARKET],
                ["Price","Size"]
            ]
        },
        {
        "range": "Orderbook!A3:B{0}".format(bid_count + 3),
        "majorDimension": "ROWS",
        "values": bids
        },
        {
        "range": "Orderbook!D1:E2",
        "majorDimension": "ROWS",
        "values": [
                ["Asks", MARKET],
                ["Price","Size"]
            ]
        },
        {
        "range": "Orderbook!D3:E{0}".format(ask_count + 3),
        "majorDimension": "ROWS",
        "values": asks
        },
    ]
    body = {
        'valueInputOption': 'USER_ENTERED',
        'data': data
    }
    marketsResults = sheet.values().batchUpdate(
        spreadsheetId=SPREADSHEET_ID, body=body).execute()
    print('{0} cells updated.'.format(marketsResults.get('totalUpdatedCells')))

def get_trades(sheet, values = []):
    all_trades = trades(MARKET)
    trade_count = 0
    for trade in all_trades['trades']:
        values.append([trade['side'], trade['size'], trade['price'], trade['createdAt']])
        trade_count += 1
        
    data = [
        {
        "range": "Trades!A1:B1",
        "majorDimension": "ROWS",
        "values": [
                ["Trades", MARKET],
            ]
        },
        {
        "range": "Trades!A2:D2",
        "majorDimension": "ROWS",
        "values": [
                ["Side", "Size", "Price", "CreatedAt"]
            ]
        },
        {
        "range": "Trades!A3:E{0}".format(trade_count + 3),
        "majorDimension": "ROWS",
        "values": values
        },
    ]
    body = {
        'valueInputOption': 'USER_ENTERED',
        'data': data
    }
    marketsResults = sheet.values().batchUpdate(
        spreadsheetId=SPREADSHEET_ID, body=body).execute()
    print('{0} cells updated.'.format(marketsResults.get('totalUpdatedCells')))


def get_historicalFunding(sheet, values = []):
    historicalFunding = historical_funding(MARKET)
    funding_count = 0
    for funding in historicalFunding['historicalFunding']:
        values.append([funding['market'], funding['rate'], funding['price'], funding['effectiveAt'] ])
        funding_count += 1
    data = [
        {
        "range": "HistoricalFunding!A1:B1",
        "majorDimension": "ROWS",
        "values": [
                ["Historical Fundings", MARKET],
            ]
        },
        {
        "range": "HistoricalFunding!A2:D2",
        "majorDimension": "ROWS",
        "values": [
                ["Market", "Rate", "Price", "EffectiveAt"]
            ]
        },
        {
        "range": "HistoricalFunding!A3:E{0}".format(funding_count + 3),
        "majorDimension": "ROWS",
        "values": values
        },
    ]
    body = {
        'valueInputOption': 'USER_ENTERED',
        'data': data
    }
    marketsResults = sheet.values().batchUpdate(
        spreadsheetId=SPREADSHEET_ID, body=body).execute()
    print('{0} cells updated.'.format(marketsResults.get('totalUpdatedCells')))


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = discovery.build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    get_market_stats(sheet)
    get_markets(sheet)
    get_orderbook(sheet)
    get_trades(sheet)
    get_historicalFunding(sheet)


if __name__ == '__main__':
    main()