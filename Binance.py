from binance.client import Client
from binance.exceptions import *

import time
import random
import numpy as np
import pandas as pd 

class BinanceCB:

    def __init__(self, api_key=None, secret_key=None):
        self.a_k = api_key
        self.s_k = secret_key
        self.instance = Client(api_key, secret_key)

    def getBalance(self,currency):
        data = self.instance.get_asset_balance(asset='BTC')
        self.instance.get_all_balances()
        return data

    def getCandles(self, market, interval):

        ''' [
            1499040000000,      # Open time
            "0.01634790",       # Open
            "0.80000000",       # High
            "0.01575800",       # Low
            "0.01577100",       # Close
            "148976.11427815",  # Volume
            1499644799999,      # Close time
            "2434.19055334",    # Quote asset volume
            308,                # Number of trades
            "1756.87402397",    # Taker buy base asset volume
            "28.46694368",      # Taker buy quote asset volume
            "17928899.62484339" # Can be ignored
        ] '''
        
        excep = True
        cand = []
        while excep:
            try:            
                data = self.instance.get_klines(symbol=market, interval=Client.KLINE_INTERVAL_30MINUTE)
                if data:
                    excep = False                    
            except (BinanceAPIException, BinanceRequestException, BinanceOrderException) as e:
                print('Reconectando con Binance... 2(s) Candles')
                print(e.message)
                time.sleep(2)  
                excep = True
            finally:
                if not excep:
                    for i in data:
                        data2 = {}
                        data2['T'] = float(i[0])
                        data2['O'] = float(i[1])
                        data2['H'] = float(i[2])
                        data2['L'] = float(i[3])
                        data2['C'] = float(i[4])
                        data2['V'] = float(i[5])
                        cand.append(data2)
                    return cand
                else:
                    excep = True
    # dataframe
    def test_run ():
        df=pd.read['T','O','H','L','C','V']
        print(df)

    # Use: getCandlesBy(<var>) <var> -> 'O', 'H', 'L', 'C', 'V', 'BV', 'T'

    def getCandlesBy(self, candles, var):
        #Market: example('NEO-BTC')
        # T, O, H, L, C, V (Time, Open, High, Low, Close, Volume)
        by = []        
        for j in candles:
            by.append(j[var])
        return by       
    
    #Scanner de Monedas
    def market_ex(self):
        excep = True
        arr = []
        while excep:
            try:                
                coins = self.instance.get_all_tickers()
                if coins:
                    excep = False
            except:                
                print('Reconectando con Binance... 2(s)')
                time.sleep(2)  
                excep = True
            finally:
                if not excep:
                    for i in coins:
                        if 'BTC' in i['symbol']:
                            arr.append(i['symbol'])
                    return arr
                else:
                    excep = True
                    
    def bid_ask(self, market):
        excep = True
        Ask = []
        Bid = []

        while excep:
            try:
                print('currency')
                currency = self.instance.get_order_book(symbol=market)
                if currency:
                    excep = False
            except:                
                print('Reconectando con Binance... 2(s) Bid-Ask')                
                time.sleep(2)  
                excep = True
            finally:
                if not excep:
                    Bid.append(currency['bids'][0][0])
                    Ask.append(currency['asks'][0][0])
                    buy = float(Bid[0])
                    sell = float(Ask[0])
                    return buy, sell
                else:
                    excep = True

x = BinanceCB(None, None)
candles = x.getCandles("LTCBTC",None)
print(candles)
