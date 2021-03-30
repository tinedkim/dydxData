#!/usr/bin/env python3

from dydx3 import Client
from dydx3.constants import MARKET_BTC_USD, MARKET_ETH_USD, MARKET_LINK_USD
from web3 import Web3
import pymongo
import time
from datetime import date
# Connecting to Public Endpoint
ENDPOINT = 'https://api.dydx.exchange'

# Reading DB address from file
# DO NOT MAKE THE ADDERSS PUBLIC
def readDBFile():
    addressFile = open("db.txt", "r")
    return str(addressFile.read())

# Daemon Driver Code
def daemon(seconds):
    iterator = 0
    while(True):
        try:
            # Connecting to the DB
            if (iterator%10 == 0):
                client = pymongo.MongoClient(readDBFile())
                db = client.admin
                dydx_marketStats = db.dydx_marketStats
                print("[DB] Mongo cursor obtained")
                client = Client(
                    host=ENDPOINT,
                )
            
            MARKET = MARKET_ETH_USD
            MARKET_NAME = 'ETH-USD'
            
            market_stats = client.public.get_stats(market=MARKET, days=1)
            market_info = client.public.get_markets()['markets'][MARKET_NAME]

            entries = []
        
            market = market_stats['markets'][MARKET_NAME]
            market['volume24H'] = market_info["volume24H"]
            market['trades24H'] = market_info["trades24H"]
            market['openInterest'] = market_info["openInterest"]
            market['timeStamp'] = time.ctime(time.time())
            entries.append(market)
        
                # Insert into DB
            dydx_marketStats.insert_many(entries)
            local_time = time.ctime(time.time())
            print(local_time, "Loop -", iterator)
            iterator = iterator + 1
         
            # Sleep for 60 seconds
            time.sleep(seconds)
        
        except Exception as e:
            print("[ERROR]", e)
            time.sleep(30)
           

daemon(3600)
