#!/usr/bin/env python3

from dydx3 import Client
from dydx3.constants import MARKET_BTC_USD, MARKET_ETH_USD
from web3 import Web3
import pymongo
import time
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
                dydx_orderbook = db.dydx_orderbook
                print("[DB] Mongo cursor obtained")
                client = Client(
                    host=ENDPOINT,
                )
            
            ORDER_1M = []
            THRESHOLD = 100000
            orderbook = client.public.get_orderbook(market=MARKET_ETH_USD)

            for index, bid in enumerate(orderbook['bids']):
                usdValue = float(bid['price']) * float(bid['size'])
                if(usdValue > THRESHOLD):
                    ORDER_1M.append(bid)

            for index, ask in enumerate(orderbook['asks']):
                usdValue = float(ask['price']) * float(ask['size'])
                if(usdValue > THRESHOLD):
                    ORDER_1M.append(ask)

                # Insert into DB
            dydx_orderbook.insert_many(ORDER_1M)
            local_time = time.ctime(time.time())
            print(local_time, "Loop -", iterator)
            iterator = iterator + 1
            # Sleep for 60 seconds
            time.sleep(seconds)

        except Exception as e:
            print("[ERROR]", e)
            time.sleep(30)

daemon(60)
