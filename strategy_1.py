# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 22:49:46 2022

@author: Juanjo
"""

import pandas as pd
import talib
import matplotlib.pyplot as plt
import seaborn as sns
import mplfinance as mpf
import backtesting as bt
import requests


data = bt.getData(2000,"BTCUSDT","1d")
'''
df = pd.read_csv("eurusd_corregido.csv", sep=";")
columns = ["date", "hour", "open", "high", "low", "close", "volume"]
df.columns = columns
df = df[490000:]
df["newdate"] = df["date"] + " "+ df["hour"]
df["newdate"] = pd.to_datetime(df["newdate"])
df = df.set_index("newdate")



#Insertar stochastico
high = df["high"]
low = df["low"]
close = df["close"]

#AMPLITUD VELAS
df["amplitud"] = 0
df["amplitud_"] = 0 


#ESTOCÁSTICO
stoch = talib.STOCH(high, low, close, fastk_period=7, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
stoch1 = stoch[0]
stoch2 = stoch[1]
df["stoch1"] = 0
df["stoch2"] = 0

#MEDIA
ema = talib.EMA(close, timeperiod=50)
df["media50"] = 0

for i in range(0, len(df)):
    
    df["stoch1"].iloc[i] = stoch1.iloc[i]
    df["stoch2"].iloc[i] = stoch2.iloc[i]
    df["media50"].iloc[i] = ema[i]
    df["amplitud"].iloc[i] = df["close"].iloc[i] - df["open"].iloc[i]
    if df["amplitud"].iloc[i] >= 0:
        df["amplitud_"].iloc[i] = 1
    else: pass
  

a = bt.Backtesting  
compra = 0
venta = 0
for i in range(0, len(df)):
    stoch = df["stoch1"].iloc[i]
    media = df["media50"].iloc[i]
    close = df["close"].iloc[i]
    
    #---COMPRAS
    if stoch <= 20 and compra == 0:
        if close > media:            
            for e in range(i,i+10):
                if df["close"].iloc[e] > df["media50"].iloc[e]:
                    
                    if df["amplitud_"].iloc[e] == 0 and compra == 0:
                        print("espero")
                        print(compra)
                    if df["amplitud_"].iloc[e] == 1 and compra == 0:
                        print("compro")
                        print(df.index[e])
                        compra = 1
                    if compra == 1:
                        break
                    else: pass
    #---VENTAS
    if stoch >= 80 and compra == 0:      
        if close < media:
            for e in range(i,i+10):
                if df["close"].iloc[e] < df["media50"].iloc[e]:
                    
                    if df["amplitud_"].iloc[e] == 0 and venta == 0:
                        print("espero")
                        print(venta)
                    if df["amplitud_"].iloc[e] == 1 and venta == 0:
                        print("vendo")
                        print(df.index[e])
                        venta = 1
                    if venta == 1:
                        break
                    else: pass

    #---CIERRE COMPRA
    if compra == 1:
        pass
    
    #---CIERRE VENTA
    if venta == 1:
        pass
'''        