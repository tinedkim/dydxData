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
                dydx_fundingRates = db.dydx_fundingRates
                print("[DB] Mongo cursor obtained")
                client = Client(
                    host=ENDPOINT,
                )
            
            MARKET = MARKET_ETH_USD
            MARKET_NAME = 'ETH-USD'
            
            historical_funding = client.public.get_historical_funding(
                market=MARKET,
            )

            entries = []
        
            funding_rate = historical_funding['historicalFunding'][0]
            funding_rate['timeStamp'] = time.ctime(time.time())
            entries.append(funding_rate)
        
                # Insert into DB
            dydx_fundingRates.insert_many(entries)
            local_time = time.ctime(time.time())
            print(local_time, "Loop -", iterator)
            iterator = iterator + 1
         
            time.sleep(seconds)
        
        except Exception as e:
            print("[ERROR]", e)
            time.sleep(30)
           

daemon(3600)
