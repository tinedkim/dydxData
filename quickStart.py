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

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1fOpQr0Sh7zIdXwH0J-BiWk9egr_VPOnYgZ5HPjgqe3k'


def get_market_stats(sheet, values = []):
    days = 7
    market = MARKET_BTC_USD
    market_stats(market, days)
    values = [["days", str(days)]]
    with open('marketStats.json') as json_file:
        marketStats = json.load(json_file)
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
    

def get_markets(sheet, values = []):
    markets()
    with open('markets.json') as json_file:
        all_markets = json.load(json_file)
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
    

    

    

if __name__ == '__main__':
    main()