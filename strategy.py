import pandas as pd
import numpy as np
from backtesting import Backtesting
import datetime
import seaborn as sns

df = pd.read_csv("eurusd.csv")
df = df[["Fecha","Último","Apertura","Máximo","Mínimo"]]
df.columns = ["Date","Close","Open","High","Low"]

df.Date = pd.to_datetime(df.Date)
df.Close = df.Close.str.replace(",",".")
df.Close = df.Close.astype("double")
df.Open = df.Open.str.replace(",",".")
df.Open = df.Open.astype("double")
df.High = df.High.str.replace(",",".")
df.High = df.High.astype("double")
df.Low = df.Low.str.replace(",",".")
df.Low = df.Low.astype("double")

df["Inc"] = 0

for i in range(len(df)):
    df["Inc"][i] = df["Close"][i] - df["Open"][i]
    
    
bt = Backtesting() 

for i in range(len(df)-2):
    precio = df.Open[i+1]
    hist = bt.dict_ordenes
    cantidad = 0.2 * bt.fondo_inicial
    
    if bt.compra == 0 and bt.venta == 0:
        if df.Inc[i] > 0:
            bt.buy(precio, cantidad)
            bt.buy_close(df.Close[i+1])
        elif df.Inc[i] < 0:
            bt.sell(precio, cantidad)
            bt.sell_close(df.Close[i+1])
    

history = bt.plot_hist(df)
            
            
            
            
            
            
            
            
        
        
        