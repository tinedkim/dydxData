# dydxData

Fetches market, trade, orderbook, fundings data from dydx's API

# Credentials

Go on this [link](https://developers.google.com/sheets/api/quickstart/python#step_1_turn_on_the) to turn on Google Sheets API. Follow through the dialog that pops up and install your credentials.

# Installation

Install the Google Client library

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

# Usage

Once you run `python quickStart.py`, it should update values in this [spreadsheet](https://docs.google.com/spreadsheets/d/1fOpQr0Sh7zIdXwH0J-BiWk9egr_VPOnYgZ5HPjgqe3k/edit?usp=sharing). To change values for number of days that market stats are fetched and which market you want to look at (from BTC-USD, ETH-USD, or LINK-USD), edit the MARKET and DAYS constants in quickStart file.

# Roadmap

I'm still working on:

- automating updates (easier done in Javascript)
- showing multiple markets at once
