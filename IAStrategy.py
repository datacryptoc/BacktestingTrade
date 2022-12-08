# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 14:30:19 2022

@author: Juanjo
"""

import pandas as pd
import numpy as np
import talib
import matplotlib.pyplot as plt
import seaborn as sns
import mplfinance as mpf
from backtesting import Backtesting, getData
import requests


def getIndicadores(df):
   
    #--- Nombres Globales
    high = df["High"]
    low = df["Low"]
    close = df["Close"]
    
    #--- Amplitud
    df["amplitud"] = 0
    df["amplitud_"] = 0 
    
    #--- Media Movil Exponencial
    ema_rapida = talib.EMA(close, timeperiod=20)
    ema_media = talib.EMA(close, timeperiod=40)
    ema_lenta = talib.EMA(close, timeperiod=100)
    df["ema_rapida"] = 0
    df["ema_media"] = 0
    df["ema_lenta"] = 0
    df["ema_rapida_"] = 0
    df["ema_media_"] = 0
    df["ema_lenta_"] = 0
    
    #--- Kaufman Adaptative Moving Average
    kama = talib.KAMA(close, timeperiod=14)
    df["kama"] = 0
    
    #--- Estocástico
    stoch = talib.STOCH(high, low, close, fastk_period=7, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    stoch1 = stoch[0]
    stoch2 = stoch[1]
    df["stoch1"] = 0
    df["stoch2"] = 0
    df["stoch_"] = 0
    
    #--- Momentum
    momentum = talib.MOM(close, timeperiod=10)
    df["momentum"] = 0
    df["momentum_"] = 0
    
    #--- RSI
    rsi = talib.RSI(close, timeperiod=14)
    df["rsi"] = 0
    
    #--- ADX
    adx = talib.ADX(high, low, close, timeperiod=14)
    df["adx"] = 0
    
    #--- Target
    df["target"] = 0
    df["target_"] = 0
    

    #--- Cálculos iterativos
    for i in range(1, len(df)):
        
        #AMPLITUD
        df["amplitud"][i] = df["Close"][i] - df["Open"].iloc[i]
        if df["amplitud"][i] >= 0:
            df["amplitud_"][i] = 1
        else: df["amplitud_"][i] = -1
        #EMA
        df["ema_rapida"][i] = ema_rapida[i]
        if ema_rapida[i] >= 0: df["ema_rapida_"][i] = 1
        else: df["ema_rapida_"][i] = -1
        df["ema_media"][i] = ema_media[i]
        if ema_media[i] >= 0: df["ema_media_"][i] = 1
        else: df["ema_media_"][i] = -1
        df["ema_lenta"][i] = ema_lenta[i]
        if ema_lenta[i] >= 0: df["ema_lenta_"][i] = 1
        else: df["ema_lenta_"][i] = -1
        #KAMA
        df["kama"][i] = kama[i]
        #STOCKASTICO
        df["stoch1"][i] = stoch1[i]
        df["stoch2"][i] = stoch2[i]
        if stoch1[i] >= stoch2[i]: df["stoch_"] = 1
        else: df["stoch_"] = -1
        #MOMENTUM
        df["momentum"].iloc[i] = momentum[i] * 100
        if momentum[i] >= momentum[i-1]: df["momentum_"] = 1
        else: df["momentum_"] = -1
        #RSI
        df["rsi"] = rsi[i]
        #ADX
        df["adx"] = adx[i]
        df["target"][i-1] = df["amplitud"][i]
        df["target_"][i-1] = df["amplitud_"][i]
    df = np.round(df, 2)[100:]    
    return df
 
#############################################################################################################
#                                   RANDOM FOREST  
#############################################################################################################   
 
datos = getData(2000,"BTCUSDT","1d")  
df = getIndicadores(datos)   

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    