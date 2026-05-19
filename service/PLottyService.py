import configparser

# Data viz
import plotly.graph_objs as go
# import talib
import pandas as pd
import numpy as np
import plotly.offline as pyo
from plotly.subplots import make_subplots

class PlottyService:

    # def __init__(self):
    #     self.name = None
    #     self.url = None
    #     self.eth_min_val
    #     self.results = list()


    def __init__(self, showMa1= True, showMa2=True, showMa3=True, showMa4=True, showBoolinger=False):
        print("iniciando")
        config = configparser.ConfigParser()
        config.read('config.ini')
        try:
            self.env = config['DEFAULT']['DEF_CONF']
        except Exception as e:
            import platform
            sistema = platform.system()
            if sistema == "Windows":
                self.env = "WINDOWS"
            else:
                print("Error defaut LINUX Plotty")
                self.env = "LINUX"

        # print(f"Active env : {self.env}")

        if "WINDOWS" in self.env:
            self.path = './img'
        else:
            self.path = '/home/MarketManager/img'
        self.showBoolinger = showBoolinger
        self.showMa1 = showMa1
        self.showMa2 = showMa2
        self.showMa3 = showMa3
        self.showMa4 = showMa4


    def generateGraphBytpe(self, type):
        hasGraphic = False
        tickers = ""
        if "ETH" in type or "BTC" in type:
            hasGraphic = True
            tickers = type+"-USD"
        elif "EURUSD" in type:
            hasGraphic = True
            tickers = type + "=X"


        if hasGraphic:

            data = " "


            # Adding Moving average calculated field
            data['MA5'] = data['Close'].rolling(5).mean()
            data['MA20'] = data['Close'].rolling(20).mean()

            # declare figure
            fig = go.Figure()

            # Candlestick
            fig.add_trace(go.Candlestick(x=data.index,
                                         open=data['Open'],
                                         high=data['High'],
                                         low=data['Low'],
                                         close=data['Close'], name='market data'))

            # Add Moving average on the graph
            fig.add_trace(go.Scatter(x=data.index, y=data['MA20'], line=dict(color='blue', width=1.5), name='Long Term MA'))
            fig.add_trace(
                go.Scatter(x=data.index, y=data['MA5'], line=dict(color='orange', width=1.5), name='Short Term MA'))

            # img_bytes = fig.to_image(format="png")
            # fig.write_image("{self.path}fig1.jpeg")
            fig.write_image(f"{self.path}/{type}.png")

    def drawData(self, data):


         # Adding Moving average calculated field
        data['MA5'] = data['value'].rolling(5).mean()
        data['MA20'] = data['value'].rolling(20).mean()

        # declare figure
        fig = go.Figure()



        # Add Moving average on the graph
        fig.add_trace(go.Scatter(x=data['date'], y=data['value'], line=dict(color='green', width=3), name='value'))
        fig.add_trace(go.Scatter(x=data['date'], y=data['MA20'], line=dict(color='blue', width=1.5), name='Long Term MA'))
        fig.add_trace(
            go.Scatter(x=data['date'], y=data['MA5'], line=dict(color='orange', width=1.5), name='Short Term MA'))

        #fig.show()
        fig.show(block=False,renderer="browser")
        # img_bytes = fig.to_image(format="png")
        # fig.write_image("{self.path}/fig1.jpeg")
        # fig.write_image(f"{self.path}/{type}.png")

    def drawDataYahooDays(self, data,ima1,ima3,drawWeekend=False, type=None, send=False, rangehours=None):


         # Adding Moving average calculated field
        data5 = data['Close'].rolling(ima1).mean()
        data20 = data['Close'].rolling(ima3).mean()

        # declare figure
        fig = go.Figure()



        # Add Moving average on the graph
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], line=dict(color='green', width=3), name=type))
        fig.add_trace(go.Scatter(x=data.index, y=data20, line=dict(color='blue', width=1.5), name='Long Term MA'))
        fig.add_trace(
            go.Scatter(x=data.index, y=data5, line=dict(color='orange', width=1.5), name='Short Term MA'))

        # if drawWeekend == False:
        #      fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])
        #      if rangehours is not None:
        #          fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"]), dict(bounds=rangehours, pattern="hour")])
        # else:
        #      if rangehours is not None:
        #          fig.update_xaxes(rangebreaks=[dict(bounds=rangehours, pattern="hour")])
        # fig.update_xaxes(minor=dict(ticks="inside", showgrid=True))  # hide weekends

        if send:
            fig.write_image(f"{self.path}/{type}.png")
        else:
            #fig.show()
            fig.show(block=False)


        # img_bytes = fig.to_image(format="png")
        # fig.write_image("{self.path}/fig1.jpeg")
        # fig.write_image(f"{self.path}/{type}.png")

    def drawDataBaseXDays(self, data,ima1,ima3,drawWeekend=False, type=None, send=False, rangehours=None):


         # Adding Moving average calculated field
        data5 = data['value'].rolling(ima1).mean()
        data20 = data['value'].rolling(50).mean()

        # declare figure
        fig = go.Figure()

         # Add Moving average on the graph
        fig.add_trace(go.Scatter(x=data['date'], y=data['value'], line=dict(color='green', width=3), name=type))
        fig.add_trace(go.Scatter(x=data['date'], y=data20, line=dict(color='blue', width=1.5), name='Long Term MA'))
        fig.add_trace(
             go.Scatter(x=data['date'], y=data5, line=dict(color='orange', width=1.5), name='Short Term MA'))

        if drawWeekend == False:
             fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])
             if rangehours is not None:
                 fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"]), dict(bounds=rangehours, pattern="hour")])
        else:
             if rangehours is not None:
                 fig.update_xaxes(rangebreaks=[dict(bounds=rangehours, pattern="hour")])
        # fig.update_xaxes(minor=dict(ticks="inside", showgrid=True))  # hide weekends

        if send:
            fig.write_image(f"{self.path}/{type}.png")
        else:
            #fig.show()
            fig.show(block=False)


        # img_bytes = fig.to_image(format="png")
        # fig.write_image("{self.path}/fig1.jpeg")
        # fig.write_image(f"{self.path}/{type}.png")

    def drawDataYahoo(self, data,ima1,ima3,drawWeekend=False, type=None, send=False, rangehours=None):


         # Adding Moving average calculated field
        data5 = data['Close'].rolling(ima1).mean()
        data20 = data['Close'].rolling(ima3).mean()

        # declare figure
        fig = go.Figure()



        # Add Moving average on the graph
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], line=dict(color='green', width=3), name=type))
        fig.add_trace(go.Scatter(x=data.index, y=data20, line=dict(color='blue', width=1.5), name='Long Term MA'))
        fig.add_trace(
            go.Scatter(x=data.index, y=data5, line=dict(color='orange', width=1.5), name='Short Term MA'))

        if drawWeekend == False:
             fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])
             if rangehours is not None:
                 fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"]), dict(bounds=rangehours, pattern="hour")])
        else:
             if rangehours is not None:
                 fig.update_xaxes(rangebreaks=[dict(bounds=rangehours, pattern="hour")])
        fig.update_xaxes(minor=dict(ticks="inside", showgrid=True))  # hide weekends

        if send:
            fig.write_image(f"{self.path}/{type}.png")
        else:
            #fig.show()
            fig.show(block=False)


        # img_bytes = fig.to_image(format="png")
        # fig.write_image("{self.path}/fig1.jpeg")
        # fig.write_image(f"{self.path}/{type}.png")

    def drawDataDB(self, data, ima1, ima3, type=None, send=False, drawWeekEnd=False):


         # Adding Moving average calculated field
        data5 = data['value'].rolling(ima1).mean()
        data20 = data['value'].rolling(ima3).mean()

        # declare figure
        fig = go.Figure()



        # Add Moving average on the graph
        fig.add_trace(go.Scatter(x=data['date'], y=data['value'], line=dict(color='green', width=3), name='value'))
        fig.add_trace(go.Scatter(x=data['date'], y=data20, line=dict(color='blue', width=1.5), name='Long Term MA'))
        fig.add_trace(
            go.Scatter(x=data['date'], y=data5, line=dict(color='orange', width=1.5), name='Short Term MA'))

        if drawWeekEnd == False:
            fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])
        fig.update_xaxes(minor=dict(ticks="inside", showgrid=True))  # hide weekends
        if send:
            fig.write_image(f"{self.path}/{type}.png")
        else:
            #fig.show()
            fig.show(block=False)


        # img_bytes = fig.to_image(format="png")
        # fig.write_image("{self.path}/fig1.jpeg")
        # fig.write_image(f"{self.path}/{type}.png")

    def drawDataDBActions(self, data, buyData, sellData, closeData, ima1, ima2, ima3, ima4, bollinger=10, type=None, send=False,
                          drawWeekend=False, rangehours=None, simulation= False):

        # Adding Moving average calculated field
        data['MA5'] = data['value'].rolling(ima1).mean()
        data['MA15'] = data['value'].rolling(ima2).mean()
        data['MA20'] = data['value'].rolling(ima3).mean()
        data['ima4'] = data['value'].rolling(ima4).mean()
        # data['EMA10'] = talib.EMA(data['value'], timeperiod=10)
        # data['EMA20'] = talib.EMA(data['value'], timeperiod=20)

        data['EMA10'] = data['value'].ewm(span=10, adjust=False).mean()
        data['EMA20'] = data['value'].ewm(span=20, adjust=False).mean()

        eval_name = ""
        if 'eval_name' in data:
            eval_name = data.iloc[[-1]]['eval_name'].values[0]
        if self.showBoolinger:

            data['20_MA'] = data['value'].rolling(window=bollinger).mean()
            # Calcular la desviaci?n est?ndar de 20 d?as
            data['20_std'] = data['value'].rolling(window=bollinger).std()
            # Calcular las Bandas de Bollinger
            data['Upper_band'] = data['20_MA'] + 2 * data['20_std']
            data['Lower_band'] = data['20_MA'] - 2 * data['20_std']

        # declare figure
        fig = go.Figure()
        print(f"start drawDataDBActions")
        fig.update_layout(title=type+" "+eval_name)
        # Add Moving average on the graph
        fig.add_trace(go.Scatter(x=data['date'], y=data['value'], line=dict(color='green', width=2), name=type))
        if self.showMa3:
            fig.add_trace(go.Scatter(x=data['date'], y=data['MA20'], line=dict(color='blue', width=1.5),
                                     name='ima3: ' + str(ima3)))
        if self.showMa2:
            fig.add_trace(go.Scatter(x=data['date'], y=data['MA15'], line=dict(color='purple', width=2),
                                     name='ima2: ' + str(ima2)))
        if self.showMa4:
            fig.add_trace(go.Scatter(x=data['date'], y=data['ima4'], line=dict(color='#bcbd22', width=3),
                                     name='ima4 :' + str(ima4)))
        if self.showMa1:
            fig.add_trace(
                go.Scatter(x=data['date'], y=data['MA5'], line=dict(color='orange', width=1.5),
                           name='ima1: ' + str(ima1)))

        fig.add_trace(
            go.Scatter(x=data['date'], y=data['EMA10'], line=dict(color='red', width=1.5), name='EMA10: '))

        fig.add_trace(
            go.Scatter(x=data['date'], y=data['EMA20'], line=dict(color='black', width=1.5),
                       name='EMA20: '))

        fig.add_trace(
            go.Scatter(x=data['date'], y=data['value'], marker=dict(color="blue", size=7), mode="markers",
                       name="puntos", ))
        if self.showBoolinger:
            # boollinger
            fig.add_trace(
                go.Scatter(x=data['date'], y=data['Upper_band'], mode='lines', name='Banda superior',
                           line=dict(color='red')))

            fig.add_trace(
                go.Scatter(x=data['date'], y=data['Lower_band'], mode='lines', name='Banda inferior',
                           line=dict(color='green')))

            fig.add_trace(
                go.Scatter(x=data['date'], y=data['20_MA'], mode='lines', name='Media movil de '+str(bollinger)+' dias',
                           line=dict(color='orange', dash='dash')))

        sizeBuy = 15
        sizeSell = 13
        sizeClose = 10
        if simulation == True:
            sizeBuy = 30
            sizeSell = 25
            sizeClose = 20
        if buyData is not None and len(buyData) > 0:


            fig.add_trace(
                go.Scatter(x=buyData['date'], y=buyData['value'], marker=dict(color="green", size=sizeBuy),
                           mode="markers",
                           name="BUY", ))
        if sellData is not None and len(sellData) > 0:
            fig.add_trace(
                go.Scatter(x=sellData['date'], y=sellData['value'], marker=dict(color="red", size=sizeSell),
                           mode="markers",
                           name="SELL", ))
        if closeData is not None and len(closeData) > 0:
            fig.add_trace(
                go.Scatter(x=closeData['date'], y=closeData['value'], marker=dict(color="black", size=sizeClose),
                           mode="markers",
                           name="CLOSE", ))

        if drawWeekend == False:
            fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])
            if rangehours is not None:
                fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"]), dict(bounds=rangehours, pattern="hour")])
        else:
            if rangehours is not None:
                fig.update_xaxes(rangebreaks=[dict(bounds=rangehours, pattern="hour")])
        fig.update_xaxes(minor=dict(ticks="inside", showgrid=True))  # hide weekends

        if send:
            fig.write_image(f"{self.path}/{type}.png")
        else:
            print(f"start drawDataDBActions pre show")
            # fig.show()
            fig.show(block=False)
        print(f"start drawDataDBActions end")

        # img_bytes = fig.to_image(format="png")
        # fig.write_image("{self.path}/fig1.jpeg")
        # fig.write_image(f"{self.path}/{type}.png")

    def drawDataYahooSimulation(self, data, tendence=None, accumulated=None, sellData = None, buyData=None, closeData = None, tendenceUP=None,tendenceDOWN=None,tendenceWAIT=None,type=None, send=False, rangehours=None, drawWeekend = False, ima1=5, ima2=15, ima3=20, ima4=30, rsiData =None):


         # Adding Moving average calculated field
        data['MA5'] = data['Close'].rolling(ima1).mean()
        data['MA15'] = data['Close'].rolling(ima2).mean()
        data['MA20'] = data['Close'].rolling(ima3).mean()
        data['ima4'] = data['Close'].rolling(ima4).mean()

        # declare figure
        fig = go.Figure()



        # Add Moving average on the graph
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], line=dict(color='green', width=3), name=type))
        fig.add_trace(go.Scatter(x=data.index, y=data['MA20'], line=dict(color='blue', width=1.5), name='ima3: '+str(ima3)))
        fig.add_trace(go.Scatter(x=data.index, y=data['MA15'], line=dict(color='purple', width=3), name='ima2: '+str(ima2)))
        fig.add_trace(go.Scatter(x=data.index, y=data['ima4'], line=dict(color='yellow', width=3), name='ima4 :'+str(ima4)))
        fig.add_trace(
            go.Scatter(x=data.index, y=data['MA5'], line=dict(color='orange', width=1.5), name='ima1: '+str(ima1)))

        fig.add_trace(
             go.Scatter(x=data.index, y=data['Close'], marker=dict(color="green", size=7), mode="markers",
                        name="puntos", ))

        if tendence is not None:
            fig.add_trace(
                 go.Scatter(x=tendence['date'], y=tendence['value'], marker=dict(color="crimson", size=12), mode="markers",
                            name="Tendencia", ))
        if accumulated is not None:
            fig.add_trace(
                 go.Scatter(x=accumulated['date'], y=accumulated['value'], marker=dict(color="green", size=12), mode="markers",
                            name="Accumulado", ))

        if buyData is not None:
            fig.add_trace(
                 go.Scatter(x=buyData['date'], y=buyData['value'], marker=dict(color="green", size=24),
                            mode="markers",
                            name="BUY", ))
        if sellData is not None:
             fig.add_trace(
                 go.Scatter(x=sellData['date'], y=sellData['value'], marker=dict(color="red", size=24),
                            mode="markers",
                            name="SELL", ))
        if closeData is not None:
             fig.add_trace(
                 go.Scatter(x=closeData['date'], y=closeData['value'], marker=dict(color="black", size=20),
                            mode="markers",
                            name="CLOSE", ))

        if tendenceUP is not None:
             fig.add_trace(
                 go.Scatter(x=tendenceUP['date'], y=tendenceUP['value'], marker=dict(color="yellow", size=12),
                            mode="markers",
                            name="tendenceUP", ))
        if tendenceDOWN is not None:
             fig.add_trace(
                 go.Scatter(x=tendenceDOWN['date'], y=tendenceDOWN['value'], marker=dict(color="blue", size=12),
                            mode="markers",
                            name="tendenceDOWN", ))
        if tendenceWAIT is not None:
             fig.add_trace(
                 go.Scatter(x=tendenceWAIT['date'], y=tendenceWAIT['value'], marker=dict(color="purple", size=12),
                            mode="markers",
                            name="tendenceWAIT", ))
        # fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])], minor=dict(ticks="inside", showgrid=True)) #hide weekends
        if drawWeekend == False:
            fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])
            if rangehours is not None:
                fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"]), dict(bounds=rangehours, pattern="hour")])
        else:
            if rangehours is not None:
                fig.update_xaxes(rangebreaks=[dict(bounds=rangehours, pattern="hour")])
        fig.update_xaxes(minor=dict(ticks="inside", showgrid=True)) #hide weekends
        if send:

            #fig.show()
            fig.show(block=False)
            fig.write_image(f"{self.path}/{type}.png")

        else:
            #fig.show()
            fig.show(block=False)

    def drawDatabaseSimulation(self, data, tendence=None, accumulated=None, sellData = None, buyData=None, closeData = None, tendenceUP=None,tendenceDOWN=None,tendenceWAIT=None,type=None, send=False, rangehours=None, drawWeekend = False, ima1=5, ima2=15, ima3=20):


         # Adding Moving average calculated field
        data['MA5'] = data['value'].rolling(ima1).mean()
        data['MA15'] = data['value'].rolling(ima2).mean()
        data['MA20'] = data['value'].rolling(ima3).mean()
        # data['MA50'] = data['Close'].rolling(50).mean()

        # declare figure
        fig = go.Figure()



        # Add Moving average on the graph
        fig.add_trace(go.Scatter(x=data['date'], y=data['value'], line=dict(color='green', width=3), name='value'))
        fig.add_trace(go.Scatter(x=data['date'], y=data['MA20'], line=dict(color='blue', width=1.5), name='Long Term 20'))
        fig.add_trace(go.Scatter(x=data['date'], y=data['MA15'], line=dict(color='purple', width=3), name='Long Term 15'))
        # fig.add_trace(go.Scatter(x=data.index, y=data['MA50'], line=dict(color='orange', width=4), name='Long Term 50'))
        fig.add_trace(
            go.Scatter(x=data['date'], y=data['MA5'], line=dict(color='orange', width=1.5), name='Short Term MA'))
        if tendence is not None:
            fig.add_trace(
                 go.Scatter(x=tendence['date'], y=tendence['value'], marker=dict(color="crimson", size=12), mode="markers",
                            name="Tendencia", ))
        if accumulated is not None:
            fig.add_trace(
                 go.Scatter(x=accumulated['date'], y=accumulated['value'], marker=dict(color="green", size=12), mode="markers",
                            name="Accumulado", ))

        if buyData is not None:
            fig.add_trace(
                 go.Scatter(x=buyData['date'], y=buyData['value'], marker=dict(color="green", size=12),
                            mode="markers",
                            name="BUY", ))
        if sellData is not None:
             fig.add_trace(
                 go.Scatter(x=sellData['date'], y=sellData['value'], marker=dict(color="red", size=12),
                            mode="markers",
                            name="SELL", ))
        if closeData is not None:
             fig.add_trace(
                 go.Scatter(x=closeData['date'], y=closeData['value'], marker=dict(color="black", size=12),
                            mode="markers",
                            name="CLOSE", ))

        if tendenceUP is not None:
             fig.add_trace(
                 go.Scatter(x=tendenceUP['date'], y=tendenceUP['value'], marker=dict(color="yellow", size=12),
                            mode="markers",
                            name="tendenceUP", ))
        if tendenceDOWN is not None:
             fig.add_trace(
                 go.Scatter(x=tendenceDOWN['date'], y=tendenceDOWN['value'], marker=dict(color="blue", size=12),
                            mode="markers",
                            name="tendenceDOWN", ))
        if tendenceWAIT is not None:
             fig.add_trace(
                 go.Scatter(x=tendenceWAIT['date'], y=tendenceWAIT['value'], marker=dict(color="purple", size=12),
                            mode="markers",
                            name="tendenceWAIT", ))
        # fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])], minor=dict(ticks="inside", showgrid=True)) #hide weekends
        if drawWeekend == False:
            fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])
        if rangehours is not None:
            fig.update_xaxes(rangebreaks=[dict(bounds=rangehours, pattern="hour")])
        fig.update_xaxes(minor=dict(ticks="inside", showgrid=True)) #hide weekends
        if send:

            #fig.show()
            fig.show(block=False)
            fig.write_image(f"{self.path}/{type}.png")

        else:
            #fig.show()
            fig.show(block=False)

    def calculate_rsi(self,data, period=14):
        delta = data.diff()

        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)

        gain = pd.Series(gain).rolling(window=period).mean()
        loss = pd.Series(loss).rolling(window=period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    def drawDatabaseSimulationClose(self, data, tendence=None, accumulated=None, sellData = None, buyData=None, closeData = None, tendenceUP=None,tendenceDOWN=None,tendenceWAIT=None,type=None, send=False, rangehours=None, drawWeekend = False, ima1=5, ima2=15, ima3=20, ima4=50, bollinger = 10, rsiData =None, active=None, eval_name = None):

        data["RSI"] = self.calculate_rsi(data["value"], 14)
         # Adding Moving average calculated field
        data['MA5'] = data['value'].rolling(ima1).mean()
        data['MA15'] = data['value'].rolling(ima2).mean()
        data['MA20'] = data['value'].rolling(ima3).mean()
        data['ima4'] = data['value'].rolling(ima4).mean()
        # eval_name = ""
        # if 'eval_name' in data:
        #     eval_name = data.iloc[[-1]]['eval_name'].values[0]
        ema_10 = 10
        ema_20 = 20
        if active:
         ema_10 = active.parameters.ema10
         ema_20 = active.parameters.ema20
        # data['EMA10'] = talib.EMA(data['value'], timeperiod=ema_10)
        # data['EMA20'] = talib.EMA(data['value'], timeperiod=ema_20)
        data['EMA10'] = data['value'].ewm(span=10, adjust=False).mean()
        data['EMA20'] = data['value'].ewm(span=20, adjust=False).mean()
        # data['MA50'] = data['Close'].rolling(50).mean()
        #boollinger
        if self.showBoolinger:
            bollinger = bollinger
            data['20_MA'] = data['value'].rolling(window=bollinger).mean()
            # Calcular la desviaci?n est?ndar de 20 d?as
            data['20_std'] = data['value'].rolling(window=bollinger).std()
            # Calcular las Bandas de Bollinger
            data['Upper_band'] = data['20_MA'] + 2 * data['20_std']
            data['Lower_band'] = data['20_MA'] - 2 * data['20_std']

        # declare figure
        # fig = go.Figure()
        fig = make_subplots(
            rows=2,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            row_heights=[0.75, 0.25]
        )

        fig.update_layout(title=type + " " + eval_name)




        # Add Moving average on the graph
        fig.add_trace(go.Scatter(x=data['date'], y=data['value'], line=dict(color='green', width=2), name=type),row=1, col=1)
        if self.showMa3:
            fig.add_trace(go.Scatter(x=data['date'], y=data['MA20'], line=dict(color='blue', width=1.5), name='ima3: '+str(ima3)),row=1, col=1)
        if self.showMa2:
            fig.add_trace(go.Scatter(x=data['date'], y=data['MA15'], line=dict(color='purple', width=2), name='ima2: '+str(ima2)),row=1, col=1)
        if self.showMa4:
            fig.add_trace(go.Scatter(x=data['date'], y=data['ima4'], line=dict(color='#bcbd22', width=3), name='ima4 :'+str(ima4)),row=1, col=1)
        if self.showMa1:
            fig.add_trace(
                go.Scatter(x=data['date'], y=data['MA5'], line=dict(color='orange', width=1.5), name='ima1: '+str(ima1)),row=1, col=1)

        fig.add_trace(
         go.Scatter(x=data['date'], y=data['EMA10'], line=dict(color='red', width=1.5), name='EMA10: '+str(ema_10)),row=1, col=1 )

        fig.add_trace(
         go.Scatter(x=data['date'], y=data['EMA20'], line=dict(color='black', width=1.5),
                    name='EMA20 : '+str(ema_20)),row=1, col=1 )

        fig.add_trace(
             go.Scatter(x=data['date'], y=data['value'], marker=dict(color="blue", size=7),mode="markers",
                            name="puntos", ),row=1, col=1)
        if self.showBoolinger:
            #boollinger
            fig.add_trace(
                 go.Scatter(x=data['date'], y=data['Upper_band'], mode='lines', name='Banda superior', line=dict(color='red')),row=1, col=1)

            fig.add_trace(
                 go.Scatter(x=data['date'], y=data['Lower_band'], mode='lines', name='Banda inferior', line=dict(color='green')),row=1, col=1)

            fig.add_trace(
                 go.Scatter(x=data['date'], y=data['20_MA'], mode='lines', name='Media movil de '+str(bollinger)+' dias', line=dict(color='orange', dash='dash')),row=1, col=1)

        if tendence is not None:
            fig.add_trace(
                 go.Scatter(x=tendence['date'], y=tendence['value'], marker=dict(color="crimson", size=12), mode="markers",
                            name="Tendencia", ))
        if accumulated is not None:
            fig.add_trace(
                 go.Scatter(x=accumulated['date'], y=accumulated['value'], marker=dict(color="green", size=12), mode="markers",
                            name="Accumulado", ),row=1, col=1)

        if buyData is not None:
            fig.add_trace(
                 go.Scatter(x=buyData['date'], y=buyData['value'], marker=dict(color="green", size=30),
                            mode="markers",
                            name="BUY", ),row=1, col=1)
        # fig.add_trace(
        #      go.Scatter(x=data['date'], y=data['RSI'], line=dict(color='orange', width=1.5),
        #                 name='rsi: '))
        if rsiData is not None:
             fig.add_trace(
                 go.Scatter(x=rsiData['date'], y=rsiData['value'], line=dict(color='orange', width=1.5),
                            name='rsi: '))

        if sellData is not None:
             fig.add_trace(
                 go.Scatter(x=sellData['date'], y=sellData['value'], marker=dict(color="red", size=22),
                            mode="markers",
                            name="SELL", ),row=1, col=1)
        if closeData is not None:
             fig.add_trace(
                 go.Scatter(x=closeData['date'], y=closeData['value'], marker=dict(color="black", size=20),
                            mode="markers",
                            name="CLOSE", ),row=1, col=1)

        if tendenceUP is not None:
             fig.add_trace(
                 go.Scatter(x=tendenceUP['date'], y=tendenceUP['value'], marker=dict(color="yellow", size=12),
                            mode="markers",
                            name="tendenceUP", ),row=1, col=1)
        if tendenceDOWN is not None:
             fig.add_trace(
                 go.Scatter(x=tendenceDOWN['date'], y=tendenceDOWN['value'], marker=dict(color="blue", size=12),
                            mode="markers",
                            name="tendenceDOWN", ),row=1, col=1)
        if tendenceWAIT is not None:
             fig.add_trace(
                 go.Scatter(x=tendenceWAIT['date'], y=tendenceWAIT['value'], marker=dict(color="purple", size=12),
                            mode="markers",
                            name="tendenceWAIT", ),row=1, col=1)
        #rSI
        fig.add_trace(
            go.Scatter(
                x=data["date"],
                y=data["RSI"],
                mode="lines",
                name="RSI"
            ),
            row=2,
            col=1
        )

        # Líneas 30 y 70
        fig.add_hline(y=70, line_dash="dash", row=2, col=1)
        fig.add_hline(y=50, line_color="red", line_width=1, row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", row=2, col=1)

        # fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])], minor=dict(ticks="inside", showgrid=True)) #hide weekends
        if drawWeekend == False:
            fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])
            if rangehours is not None:
                fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"]), dict(bounds=rangehours, pattern="hour")])
        else:
            if rangehours is not None:
                fig.update_xaxes(rangebreaks=[dict(bounds=rangehours, pattern="hour")])
        fig.update_xaxes(minor=dict(ticks="inside", showgrid=True))  # hide weekends

        fig.update_layout(
            xaxis_rangeslider_visible=False,
            height=900
        )

        if send:

            # fig.show()
            fig.show(block=False)
            fig.write_image(f"{self.path}/{type}.png")

        else:
            # fig.show()
            fig.show(block=False)