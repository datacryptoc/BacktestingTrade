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
        self.id = 0
        self.id_ultima_venta = 0
        self.id_ultima_compra = 0
        self.fondo_inicial = 1000
        self.fondos = self.fondo_inicial

    #--- COMPRA     
    def buy(self, date, precio, cantidad):
        
        if self.compra == 1: #Si ya existe op de compra
            pass
        elif self.venta == 1: #Ya existe una venta
            pass
        elif self.compra == 0: #OPERACION DE COMPRA
            self.id = self.id + 1    
            self.compra = 1
            
            self.dict_ordenes[str(self.id)] = {}
            self.dict_ordenes[str(self.id)]["fecha_apertura"] = date
            self.dict_ordenes[str(self.id)]["tipo"] = "compra"
            self.dict_ordenes[str(self.id)]["precio_apertura"] = precio
            self.dict_ordenes[str(self.id)]["cantidad"] = cantidad
            self.dict_ordenes[str(self.id)]["fecha_cierre"] = ""
            self.dict_ordenes[str(self.id)]["precio_cierre"] = ""
            self.dict_ordenes[str(self.id)]["cantidad_cierre"] = 0
            self.dict_ordenes[str(self.id)]["profit"] = 0
            self.dict_ordenes[str(self.id)]["porcentaje"] = ""
            self.dict_ordenes[str(self.id)]["fondos"] = self.fondos
            self.id_ultima_compra = self.id
            #print(">>>> OP COMPRA FECHA: ", date, "; PRECIO: ", precio, "; CANT: ", cantidad)
            
        else: pass

        
    #--- VENTA
    def sell(self, date, precio, cantidad):
        if self.venta == 1: #Si ya existe op de venta
            pass
        elif self.compra == 1: #Ya existe op de compra
            pass
        elif self.venta == 0: #OPERACION DE VENTA
            self.id = self.id + 1
            self.venta = 1
            
            self.dict_ordenes[str(self.id)] = {}
            self.dict_ordenes[str(self.id)]["fecha_apertura"] = date
            self.dict_ordenes[str(self.id)]["tipo"] = "venta"
            self.dict_ordenes[str(self.id)]["precio_apertura"] = precio
            self.dict_ordenes[str(self.id)]["cantidad"] = cantidad
            self.dict_ordenes[str(self.id)]["fecha_cierre"] = ""
            self.dict_ordenes[str(self.id)]["precio_cierre"] = ""
            self.dict_ordenes[str(self.id)]["cantidad_cierre"] = 0
            self.dict_ordenes[str(self.id)]["porcentaje"] = ""
            self.dict_ordenes[str(self.id)]["profit"] = 0
            self.dict_ordenes[str(self.id)]["fondos"] = self.fondos
            self.id_ultima_venta = self.id
            #print("<<<< OP VENTA FECHA: ", date, "; PRECIO: ", precio, "; CANT: ", cantidad)
            
        else: pass
    
   
    #--- CIERRE COMPRA PARCIAL
    def buy_close(self, date, precio_cierre, pc_cierre=1):
        
        if self.compra == 0:
            pass
        
        elif self.compra == 1 and pc_cierre == 1: #Se debe usar para terminar cierres parciales o cierre total único

            self.compra = 0            
            self.dict_ordenes[str(self.id_ultima_compra)]["fecha_cierre"] = date
            self.dict_ordenes[str(self.id_ultima_compra)]["precio_cierre"] = precio_cierre
            
            precio_apertura = self.dict_ordenes[str(self.id_ultima_compra)]["precio_apertura"]
            porcentaje = ((precio_cierre/precio_apertura)-1)*100
            cantidad_apertura = self.dict_ordenes[str(self.id_ultima_compra)]["cantidad"] - self.dict_ordenes[str(self.id_ultima_compra)]["cantidad_cierre"]
            profit = cantidad_apertura*(porcentaje/100)
            
            self.dict_ordenes[str(self.id)]["tipo"] = self.dict_ordenes[str(self.id)]["tipo"] + "/cierreTotal"
            self.dict_ordenes[str(self.id_ultima_compra)]["cantidad_cierre"] = self.dict_ordenes[str(self.id_ultima_compra)]["cantidad_cierre"] + cantidad_apertura
            self.dict_ordenes[str(self.id_ultima_compra)]["porcentaje"] = porcentaje
            self.dict_ordenes[str(self.id_ultima_compra)]["profit"] = self.dict_ordenes[str(self.id_ultima_compra)]["profit"] + profit
            self.fondos = self.fondos + profit
            self.dict_ordenes[str(self.id_ultima_compra)]["fondos"] = self.fondos
        
        elif self.compra == 1 and pc_cierre != 1:
            
            self.dict_ordenes[str(self.id)]["fecha_cierre"] = date
            self.dict_ordenes[str(self.id_ultima_compra)]["precio_cierre"] = precio_cierre
            
            precio_apertura = self.dict_ordenes[str(self.id_ultima_compra)]["precio_apertura"]
            porcentaje = ((precio_cierre/precio_apertura)-1)*100
            cantidad_apertura = self.dict_ordenes[str(self.id_ultima_compra)]["cantidad"]
            profit = cantidad_apertura*(porcentaje/100) * pc_cierre
            
            self.dict_ordenes[str(self.id)]["tipo"] = self.dict_ordenes[str(self.id)]["tipo"] + "/cierreParcial"
            self.dict_ordenes[str(self.id_ultima_compra)]["cantidad_cierre"] = self.dict_ordenes[str(self.id_ultima_compra)]["cantidad_cierre"] + cantidad_apertura*pc_cierre
            self.dict_ordenes[str(self.id_ultima_compra)]["porcentaje"] = porcentaje
            self.dict_ordenes[str(self.id_ultima_compra)]["profit"] = self.dict_ordenes[str(self.id_ultima_compra)]["profit"] + profit
            self.fondos = self.fondos + profit
            self.dict_ordenes[str(self.id_ultima_compra)]["fondos"] = self.fondos
            
            self.compra = self.compra + 1
        
        else: pass


    #--- CIERRE VENTA PARCIAL
    def sell_close(self, date, precio_cierre, pc_cierre=1):
        
        if self.venta == 0:
            pass
        
        elif self.venta == 1 and pc_cierre == 1: #Se debe usar para terminar cierres parciales o cierre total único
          
            self.venta = 0            
            self.dict_ordenes[str(self.id_ultima_venta)]["fecha_cierre"] = date
            self.dict_ordenes[str(self.id_ultima_venta)]["precio_cierre"] = precio_cierre
            
            precio_apertura = self.dict_ordenes[str(self.id_ultima_venta)]["precio_apertura"]    
            porcentaje = ((precio_apertura/precio_cierre)-1)*100
            cantidad_apertura = self.dict_ordenes[str(self.id_ultima_venta)]["cantidad"] - self.dict_ordenes[str(self.id_ultima_venta)]["cantidad_cierre"]
            profit = cantidad_apertura*(porcentaje/100)
            
            self.dict_ordenes[str(self.id)]["tipo"] = self.dict_ordenes[str(self.id)]["tipo"] + "/cierreTotal"
            self.dict_ordenes[str(self.id_ultima_venta)]["cantidad_cierre"] = self.dict_ordenes[str(self.id_ultima_venta)]["cantidad_cierre"] + cantidad_apertura
            self.dict_ordenes[str(self.id_ultima_venta)]["porcentaje"] = porcentaje
            self.dict_ordenes[str(self.id_ultima_venta)]["profit"] = self.dict_ordenes[str(self.id_ultima_venta)]["profit"] + profit
            self.fondos = self.fondos + profit
            self.dict_ordenes[str(self.id_ultima_venta)]["fondos"] = self.fondos
            
            
        elif self.venta == 1 and pc_cierre != 1:
          
            self.dict_ordenes[str(self.id)]["fecha_cierre"] = date
            self.dict_ordenes[str(self.id_ultima_venta)]["precio_cierre"] = precio_cierre
  
            precio_apertura = self.dict_ordenes[str(self.id_ultima_venta)]["precio_apertura"]    
            porcentaje = ((precio_apertura/precio_cierre)-1)*100
            cantidad_apertura = self.dict_ordenes[str(self.id_ultima_venta)]["cantidad"]
            profit = cantidad_apertura*(porcentaje/100) * pc_cierre
            
            self.dict_ordenes[str(self.id)]["tipo"] = self.dict_ordenes[str(self.id)]["tipo"] + "/cierreParcial"
            self.dict_ordenes[str(self.id_ultima_venta)]["cantidad_cierre"] = self.dict_ordenes[str(self.id_ultima_venta)]["cantidad_cierre"] + cantidad_apertura*pc_cierre
            self.dict_ordenes[str(self.id_ultima_venta)]["porcentaje"] = porcentaje
            self.dict_ordenes[str(self.id_ultima_venta)]["profit"] = self.dict_ordenes[str(self.id_ultima_venta)]["profit"] + profit
            self.fondos = self.fondos + profit
            self.dict_ordenes[str(self.id_ultima_venta)]["fondos"] = self.fondos
            
            self.venta = self.venta + 1
        
        else:pass
          
 
    #--- PLOT OPERACIONES
    def plot_hist(self):    #df:dict_ordenes    
        import pandas as pd
        import seaborn as sns
        trade = []
        fondos = []
        dict_ordenes = self.dict_ordenes
        for i in range(1,len(dict_ordenes)):
            
            i=str(i)
            fondo = dict_ordenes[i]["fondos"]
            fondos.append(fondo)
            trade.append(dict_ordenes[i]["fecha_cierre"])
                      
        history = pd.DataFrame(list(zip(trade,fondos)), columns=["trade","fondo"])
        sns.lineplot(history.trade, history.fondo) 
        historico_trades = pd.DataFrame(dict_ordenes).transpose()
        #print(historico_trades)
        
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
            data = data.round(5)
    return data   
        
       
        

        
'''
    #--- CIERRE COMPRA TOTAL
    def buy_close(self, date, precio_cierre):
        
        if self.compra == 0:
            pass
        
        else:
            self.compra = 0            
            self.dict_ordenes[str(self.id)]["fecha_cierre"] = date
            self.dict_ordenes[str(self.id_ultima_compra)]["precio_cierre"] = precio_cierre
            
            precio_apertura = self.dict_ordenes[str(self.id_ultima_compra)]["precio_apertura"]
            porcentaje = ((precio_cierre/precio_apertura)-1)*100
            cantidad_apertura = self.dict_ordenes[str(self.id_ultima_compra)]["cantidad"]
            profit = cantidad_apertura*(porcentaje/100)
            
            self.dict_ordenes[str(self.id_ultima_compra)]["porcentaje"] = porcentaje
            self.dict_ordenes[str(self.id_ultima_compra)]["profit"] = profit
            self.fondos = self.fondos + profit
            self.dict_ordenes[str(self.id_ultima_compra)]["fondos"] = self.fondos
            
            
            print("---- Cierre compra FECHA: ", date, "; PRECIO: ", precio_cierre, "; PROFIT: ", porcentaje, "%")
    

    #--- CIERRE VENTA TOTAL
    def sell_close(self, date, precio_cierre):
        
        if self.venta == 0:
            pass
        
        else:
            self.venta = 0            
            self.dict_ordenes[str(self.id)]["fecha_cierre"] = date
            self.dict_ordenes[str(self.id_ultima_venta)]["precio_cierre"] = precio_cierre
            
            precio_apertura = self.dict_ordenes[str(self.id_ultima_venta)]["precio_apertura"]    
            porcentaje = ((precio_apertura/precio_cierre)-1)*100
            cantidad_apertura = self.dict_ordenes[str(self.id_ultima_venta)]["cantidad"]
            profit = cantidad_apertura*(porcentaje/100)
            
            self.dict_ordenes[str(self.id_ultima_venta)]["profit"] = profit
            self.dict_ordenes[str(self.id_ultima_venta)]["porcentaje"] = porcentaje
            self.fondos = self.fondos + profit
            self.dict_ordenes[str(self.id_ultima_compra)]["fondos"] = self.fondos
    
            print("---- Cierre venta FECHA: ", date, "; PRECIO: ", precio_cierre, "; PROFIT: ", porcentaje, "%")
'''
 
        
       
        
       
        