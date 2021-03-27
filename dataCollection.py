from dydx3 import Client
from web3 import Web3
import json
from dydx3.constants import MARKET_BTC_USD, MARKET_ETH_USD, MARKET_LINK_USD
import os


client = Client(
      host='https://api.dydx.exchange',
  )

def generate_filepath(json):
  filepath = os.path.join('data', json)
  if not os.path.exists('./data/'):
      os.makedirs('./data/')
  return filepath

'''
Get available markets.
  market	(Optional): Specific market to be fetched.
'''
def markets():
  markets = client.public.get_markets()
  filepath = generate_filepath('markets.json')
  with open(filepath, 'w') as outfile:
    json.dump(markets, outfile, indent = 4)
  with open(filepath) as json_file:
    all_markets = json.load(json_file)
  return all_markets

'''
Get Market Stats.
  market	Market whose statistics are being fetched.
  days	(Optional): Specified day range  to have been compiled over
                    Can be one of 1, 7, 30.
'''
def market_stats(market, day):
  market_stats = client.public.get_stats(
    market=market,
    days=day
  )

  filepath = generate_filepath('marketStats.json')
  with open(filepath, 'w') as outfile:
    json.dump(market_stats, outfile, indent = 4)
  with open(filepath) as json_file:
    marketStats = json.load(json_file)
  return marketStats

'''
Get orderbook
  market	Market whose statistics are being fetched.
'''
def orderbook(market):
  orderbook = client.public.get_orderbook(
    market=market,
  )
  filepath = generate_filepath('orderbook.json')
  with open(filepath, 'w') as outfile:
    json.dump(orderbook, outfile, indent = 4)
  with open(filepath) as json_file:
    orderbookStats = json.load(json_file)
  return orderbookStats
'''
Get trades
  market	Market whose statistics are being fetched.
'''
def trades(market):
  all_trades = client.public.get_trades(
    market=market,
  )
  filepath = generate_filepath('trades.json')
  with open(filepath, 'w') as outfile:
    json.dump(all_trades, outfile, indent = 4)
  with open(filepath) as json_file:
    all_trades = json.load(json_file)
  return all_trades


'''
Get historical funding
  market	Market whose statistics are being fetched.
'''
def historical_funding(market):
  historical_funding = client.public.get_historical_funding(
    market=market,
  )
  filepath = generate_filepath('historicalFundings.json')
  with open(filepath, 'w') as outfile:
    json.dump(historical_funding, outfile, indent = 4)
  with open(filepath) as json_file:
    historicalFunding = json.load(json_file)
  return historicalFunding