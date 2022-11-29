#############################################################################################################
#                                   CLASE BACKTESTING   
#############################################################################################################

class Backtesting:

    def __init__(self):
        #Inicializacion con contadores de compra/venta a 0
        self.compra = 0
        self.venta = 0
        self.dict_ordenes = {}
        self.id_compra = 0
        self.id_venta = 0
        self.id = 1
        self.id_ultima_venta = 0
        self.id_ultima_compra = 0
        self.fondo_inicial = 1000

    def buy(self, precio, cantidad):
        if self.compra == 1: #Si ya existe op de compra
            pass
        elif self.venta == 1: #Ya existe una venta
            pass
        elif self.compra == 0: #OPERACION DE COMPRA
            self.compra = 1
            self.dict_ordenes[str(self.id)] = {}
            self.dict_ordenes[str(self.id)]["id"] = self.id
            self.dict_ordenes[str(self.id)]["tipo"] = "compra"
            self.dict_ordenes[str(self.id)]["precio_apertura"] = precio
            self.dict_ordenes[str(self.id)]["cantidad"] = cantidad
            self.dict_ordenes[str(self.id)]["precio_cierre"] = ""
            self.dict_ordenes[str(self.id)]["profit"] = ""
            self.dict_ordenes[str(self.id)]["porcentaje"] = ""
            self.dict_ordenes[str(self.id)]["fondos"] = self.fondo_inicial

            self.id_ultima_compra = self.id
            
            print(">>>> OP COMPRA ID: ", self.id, "; PRECIO: ", precio, "; CANT: ", cantidad)
            self.id = self.id + 1
        else: print("WARNING: Hay mas de 1 op activa")
        

    def sell(self, precio, cantidad):
        if self.venta == 1: #Si ya existe op de venta
            pass
        elif self.compra == 1: #Ya existe op de compra
            pass
        elif self.venta == 0: #OPERACION DE VENTA
            self.venta = 1
            self.dict_ordenes[str(self.id)] = {}
            self.dict_ordenes[str(self.id)]["id"] = self.id
            self.dict_ordenes[str(self.id)]["tipo"] = "venta"
            self.dict_ordenes[str(self.id)]["precio_apertura"] = precio
            self.dict_ordenes[str(self.id)]["cantidad"] = cantidad
            self.dict_ordenes[str(self.id)]["precio_cierre"] = ""
            self.dict_ordenes[str(self.id)]["porcentaje"] = ""
            self.dict_ordenes[str(self.id)]["profit"] = ""
            self.dict_ordenes[str(self.id)]["fondos"] = self.fondo_inicial
            self.id_ultima_venta = self.id

            print("<<<< OP VENTA ID: ", self.id, "; PRECIO: ", precio, "; CANT: ", cantidad)
            self.id = self.id + 1
        else: print("WARNING: Hay mas de 1 op activa")

    def sell_close(self, precio_cierre):
        self.venta = 0
        
        self.dict_ordenes[str(self.id_ultima_venta)]["precio_cierre"] = precio_cierre
        precio_apertura = self.dict_ordenes[str(self.id_ultima_venta)]["precio_apertura"]
        
        self.dict_ordenes[str(self.id_ultima_venta)]["porcentaje"] = ((precio_apertura/precio_cierre)-1)*100

        porcentaje = self.dict_ordenes[str(self.id_ultima_venta)]["porcentaje"]
        cantidad_apertura = self.dict_ordenes[str(self.id_ultima_venta)]["cantidad"]
        self.dict_ordenes[str(self.id_ultima_venta)]["profit"] = cantidad_apertura*(porcentaje/100)
        profit = self.dict_ordenes[str(self.id_ultima_venta)]["profit"]

        self.fondo_inicial = self.fondo_inicial + profit
        self.dict_ordenes[str(self.id_ultima_venta)]["fondos"] = self.fondo_inicial

        print("---- Cierre venta ID: ", self.id_ultima_venta, "; PRECIO: ", precio_cierre, "; PROFIT: ", porcentaje, "%")

    def buy_close(self, precio_cierre):
        self.compra = 0
        
        self.dict_ordenes[str(self.id_ultima_compra)]["precio_cierre"] = precio_cierre
        precio_apertura = self.dict_ordenes[str(self.id_ultima_compra)]["precio_apertura"]
        
        self.dict_ordenes[str(self.id_ultima_compra)]["porcentaje"] = ((precio_cierre/precio_apertura)-1)*100

        porcentaje = self.dict_ordenes[str(self.id_ultima_compra)]["porcentaje"]
        cantidad_apertura = self.dict_ordenes[str(self.id_ultima_compra)]["cantidad"]
        self.dict_ordenes[str(self.id_ultima_compra)]["profit"] = cantidad_apertura*(porcentaje/100)
        profit = self.dict_ordenes[str(self.id_ultima_compra)]["profit"]

        self.fondo_inicial = self.fondo_inicial + profit
        self.dict_ordenes[str(self.id_ultima_compra)]["fondos"] = self.fondo_inicial
        
        print("---- Cierre compra ID: ", self.id_ultima_compra, "; PRECIO: ", precio_cierre, "; PROFIT: ", porcentaje, "%")
        
        
    def plot_hist(self,df):        
        import pandas as pd
        import seaborn as sns
        trade = []
        fondos = []
        for i in range(1,len(self.dict_ordenes)):
            
            i=str(i)
            fondo = self.dict_ordenes[i]["fondos"]
            fondos.append(fondo)
            trade.append(i)
                      
        history = pd.DataFrame(list(zip(trade,fondos)), columns=["trade","fondo"])
        sns.lineplot(history.trade, history.fondo)
        
        historico_trades = pd.DataFrame(self.dict_ordenes).transpose()
        print(historico_trades)
        
        return historico_trades
        
#############################################################################################################
#                                        FUNCIONES INDEPENDIENTES   
#############################################################################################################
    
def getData(N,moneda,periodo):
    #(100, "EURUSD", "4h")
    import requests
    import json
    import time
    import numpy as np
    import pandas as pd
    valor = 864 #DEPENDE DEL PERIODO
    contador = 0
    respuesta = requests.get("https://api2.binance.com/api/v3/klines?symbol="+moneda+"&interval="+periodo+"&limit=1").text
    respuesta = json.loads(respuesta)
    try: 
        fecha = respuesta[0][0]
    except:
        print(respuesta)
    data = []
    while contador < N:
        time.sleep(1)
        if contador == 0:
            response = requests.get("https://api2.binance.com/api/v3/klines?symbol="+moneda+"&interval="+periodo+"&limit=1&endTime="+str(int(fecha-valor))).text
            response = np.array(json.loads(response)).astype(float)
            try: 
                fecha = response[0][0]
            except:
                print(contador)
                print(N)
                print(response)
            contador += 1
            data = response
        if contador + 1000 < N:
            response = requests.get("https://api2.binance.com/api/v3/klines?symbol="+moneda+"&interval="+periodo+"&limit=1000&endTime="+str(int(fecha-valor))).text
            response = np.array(json.loads(response)).astype(float)
            try: 
                fecha = response[0][0]
            except:
                print("https://api2.binance.com/api/v3/klines?symbol="+moneda+"&interval="+periodo+"&limit=1000&endTime="+str(int(fecha-valor)))
                print(contador)
                print(N)
                print(response)
            contador += 1000
            data = np.concatenate((response,data))
        else:
            response = requests.get("https://api2.binance.com/api/v3/klines?symbol="+moneda+"&interval="+periodo+"&limit="+str(int(N-contador))+"&endTime="+str(int(fecha-valor))).text
            response = np.array(json.loads(response)).astype(float)
            try: 
                fecha = response[0][0]
            except:
                print(contador)
                print(N)
                print(response)
            contador += 1000
            data = np.concatenate((response,data))
    #OPEN/HIGH/LOW/CLOSE/VOLUME/RSITipo/RSIPendiente/Media1Pendiente/Media2Pendiente/Media3Pendiente/Target
            data = pd.DataFrame(data[:,1:6])
            data.columns = ["Open", "High", "Low", "Close", "Volume"]
            data = data.round(2)
    return data   
        
       
        
       
        
       
        
       
        
       
        
       
        