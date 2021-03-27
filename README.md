# dydxData

Fetches market, trade, orderbook, fundings data from dydx's API

## Credentials

Go on this [link](https://developers.google.com/sheets/api/quickstart/python#step_1_turn_on_the) to turn on Google Sheets API. Follow through the dialog that pops up and install your credentials.

## Installation

Install the Google Client library

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
and the ```dydx-v3-python``` package
 ```bash
 pip install dydx-v3-python
 ```

## Usage

Once you run `python quickStart.py`, it should update values in this [spreadsheet](https://docs.google.com/spreadsheets/d/1fOpQr0Sh7zIdXwH0J-BiWk9egr_VPOnYgZ5HPjgqe3k/edit?usp=sharing). To change values for number of days that market stats are fetched and which market you want to look at (from BTC-USD, ETH-USD, or LINK-USD), edit the MARKET and DAYS constants in quickStart file.

### Orderbook Daemon
* We fetch the current ETH-USD perpertual orderbook
* Compute the value of trade via ```price * size```
* Save records where ```value > THRESHOLD```
* Then, push these records into ```admin > dydx_orderbook``` DB
* Daemon then sleeps for 60 seconds
* Rinse and Repeat
## Roadmap

I'm still working on:

- automating updates (easier done in Javascript)
- showing multiple markets at once
