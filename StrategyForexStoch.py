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
from backtesting import Backtesting, getData
import requests


df = getData(25000,"EURUSDT","15m")

#############################################################################################################
#                                   PREPARACIÓN DE DATAFRAME   
#############################################################################################################

#--- Nombres Globales
high = df["High"]
low = df["Low"]
close = df["Close"]

#--- Amplitud
df["amplitud"] = 0
df["amplitud_"] = 0 


#--- Estocástico
stoch = talib.STOCH(high, low, close, fastk_period=7, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
stoch1 = stoch[0]
stoch2 = stoch[1]
df["stoch1"] = 0
df["stoch2"] = 0

#--- Media Movil Exponencial
ema = talib.EMA(close, timeperiod=50)
df["media50"] = 0

#--- Cálculos iterativos
for i in range(0, len(df)):
    
    df["stoch1"].iloc[i] = stoch1.iloc[i]
    df["stoch2"].iloc[i] = stoch2.iloc[i]
    df["media50"].iloc[i] = ema[i]
    df["amplitud"].iloc[i] = df["Close"].iloc[i] - df["Open"].iloc[i]
    if df["amplitud"].iloc[i] >= 0:
        df["amplitud_"].iloc[i] = 1
    else: df["amplitud_"].iloc[i] = -1
  

#############################################################################################################
#                                   BACKTESTING ESTRATEGIA
#############################################################################################################

#--- Inicialización 
bt = Backtesting()
bt.fondo_inicial = 1000
cantidad = 0.2*(bt.fondos)

i = 50
while i<len(df):
    #Inicializo variables de compra/venta
    compra = bt.compra 
    venta = bt.venta
    date = i
    
    stoch = df["stoch1"].iloc[i]
    media = df["media50"].iloc[i]
    close = df["Close"].iloc[i]
    high = df["High"].iloc[i]
    low = df["Low"].iloc[i]
    
    #---COMPRAS
    if compra == 0 and venta == 0 and stoch <= 20: #ESTOCÁSTICO < 20
        if close > media:            
            for e in range(i,i+10):
                if df["Close"].iloc[e] > df["media50"].iloc[e]:
                    
                    if df["amplitud_"].iloc[e] == -1 and compra == 0:          #Esperando para comprar
                        pass
                    elif df["amplitud_"].iloc[e] == 1 and compra == 0:           #Momento de comprar
                        bt.buy(date ,close,cantidad)
                        precio_compra = close
                        i = e
                        break
                    elif compra == 1:                                            #Ya se ha comprado
                        break
                    else: pass
    #---VENTAS
    if compra == 0 and venta == 0 and stoch >= 80:  #ESTOCÁSTICO > 80  
        if close < media:
            for e in range(i,i+10):
                print(e)
                if df["Close"].iloc[e] < df["media50"].iloc[e]:
                    
                    if df["amplitud_"].iloc[e] == -1 and venta == 0:           #Esperando para vender
                        pass
                    elif df["amplitud_"].iloc[e] == 1 and venta == 0:            #Momento de vender
                        bt.sell(date, close,cantidad)
                        precio_venta = close
                        i = e
                        break
                    elif venta == 1:                                             #Ya se ha vendido
                        break
                    else: pass
                
    #---CIERRE COMPRA 
    if compra == 1 and high >= (precio_compra + 0.01):
        bt.buy_close(i, precio_compra + 0.01, 0.5)
    elif compra == 2 and high >= (precio_compra + 0.02):
        bt.buy_close(i, precio_compra + 0.02, 0.5)  
    elif compra == 3 and high >= (precio_compra + 0.03):
        bt.buy_close(i, precio_compra + 0.03)  
    elif compra != 0 and low <= (precio_compra - 0.0025):
        bt.buy_close(i, precio_compra - 0.01)
    
    #---CIERRE VENTA
    if venta == 1 and low <= (precio_venta - 0.01):
        bt.sell_close(i, precio_venta - 0.01, 0.5)
    elif venta == 2 and low <= (precio_venta - 0.02):
        bt.sell_close(i, precio_venta - 0.02, 0.5)
    elif venta == 3 and low <= (precio_venta - 0.03):
        bt.sell_close(i, precio_venta - 0.03)
    elif venta != 0 and high >= (precio_venta + 0.0025):
        bt.sell_close(i, precio_venta + 0.01)
    
    i = i+1

bt.plot_hist()    