# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 16:59:05 2022

@author: Juanjo
"""
import talib
import numpy as np
from backtesting import Backtesting, getData


def getIndicators(df):
     
    df = np.round(df,4)
    
    Open = df["Open"]
    High = df["High"]
    Low = df["Low"]
    Close = df["Close"]
    
    
    ema_rapida = talib.EMA(Close, timeperiod=20)
    ema_media = talib.EMA(Close, timeperiod=40)
    ema_lenta = talib.EMA(Close, timeperiod=100)
    df["ema_rapida"] = ""
    df["ema_rapida_"] = ""
    df["ema_media"] = ""
    df["ema_media_"] = ""
    df["ema_lenta"] = ""
    df["ema_lenta_"] = ""
    df["volatilidad"] = ""
    df["mecha_sup"] = ""
    df["mecha_inf"] = ""
    df["amplitud"] = ""
    df["amplitud_"] = ""
    df["amplitud1"] = ""
    df["amplitud1_"] = ""
    df["amplitud2"] = ""
    df["amplitud2_"] = ""
    df["amplitud3"] = ""
    df["amplitud3_"] = ""
    df["amplitud12"] = ""
    df["amplitud12_"] = ""
    df["amplitud123"] = ""
    df["amplitud123_"] = ""
    
    for i in range(len(df)-3):
     
        df["ema_rapida"][i] = ema_rapida[i]
        if ema_rapida[i] >= 0: 
           df["ema_rapida_"][i] = 1
        else: df["ema_rapida_"][i] = -1
       
        df["ema_media"][i] = ema_media[i]
        if ema_media[i] >= 0: 
           df["ema_media_"][i] = 1
        else: df["ema_media_"][i] = -1
       
        df["ema_lenta"][i] = ema_lenta[i]
        if ema_lenta[i] >= 0: 
           df["ema_lenta_"][i] = 1
        else: df["ema_lenta_"][i] = -1 
       
        df["amplitud"][i] = Close[i] - Open[i]
        if df["amplitud"][i] >= 0: 
            df["amplitud_"][i] = 1
            df["volatilidad"][i] = High[i] - Low[i]
            df["mecha_sup"][i] = High[i] - Close[i]
            df["mecha_inf"][i] = Open[i] - Low[i]
        else: 
            df["amplitud_"] = -1
            df["volatilidad"] = Low[i] - High[i]
            df["mecha_sup"][i] = High[i] - Open[i]
            df["mecha_inf"][i] = Close[i] - Low[i]
        
        df["amplitud1"][i] = Close[i+1] - Open[i+1]
        if df["amplitud1"][i] >= 0: 
            df["amplitud1_"][i] = 1
        else: df["amplitud1_"][i] = -1
        
        df["amplitud2"][i] = Close[i+2] - Open[i+2]
        if df["amplitud2"][i] >= 0: 
            df["amplitud2_"][i] = 1
        else: df["amplitud2_"][i] = -1
        
        df["amplitud3"][i] = Close[i+3] - Open[i+3]
        if df["amplitud3"][i] >= 0: 
            df["amplitud3_"][i] = 1
        else: df["amplitud3_"][i] = -1
        
        df["amplitud12"][i] = df["amplitud1"][i] + df["amplitud2"][i]
        if df["amplitud12"][i] >= 0: 
            df["amplitud12_"][i] = 1
        else: df["amplitud12_"][i] = -1
        
        df["amplitud123"][i] = df["amplitud12"][i] + df["amplitud3"][i]
        if df["amplitud123"][i] >= 0: 
            df["amplitud123_"][i] = 1
        else: df["amplitud123_"][i] = -1
    
    return df[100:]
    
    
data = getData(1000,"EURUSDT","1d")     
df = getIndicators(data)
    
    
    
    
    
    
    
    
    
    
    
    
    
    