from dydx3 import Client
from web3 import Web3
import json
from dydx3.constants import MARKET_BTC_USD

client = Client(
      host='https://api.dydx.exchange',
  )

'''
Get available markets
'''
def markets():
  markets = client.public.get_markets()

  with open('markets.json', 'w') as outfile:
      json.dump(markets, outfile, indent = 4)

'''
Get Market Stats
Available days: 1, 7, 30
'''
def market_stats(market, day):
  market_stats = client.public.get_stats(
    market=market,
    days=day
  )

  with open('marketStats.json', 'w') as outfile:
      json.dump(market_stats, outfile, indent = 4)
