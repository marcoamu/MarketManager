import configparser
import datetime
import time

from service.Constants import Constants
from service.PLottyService import PlottyService
from service.TelegramService import TelegramService


class Active:



    def __init__(self, parameters, evaluator):
        self.telegram = TelegramService()
        self.parameters = parameters
        self.evaluator = evaluator
        showBoolinger = True
        showima1 = True
        showima2 = False
        showima3 = False
        showima4 = False

        data = None

        # plotty = PlottyService()
        # plotty = PlottyService(showMa1=showima1, showMa2=showima2, showMa3=showima3,
        #                        showMa4=showima4, showBoolinger=showBoolinger)
        self.plotty = PlottyService(showMa1=showima1, showMa2=showima2, showMa3=showima3,
                               showMa4=showima4, showBoolinger=showBoolinger)

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

                print("Error defaut LINUX Active")
                self.env = "LINUX"
        print(f"Active env : {self.env}")
        if "WINDOWS" in self.env:
            self.path = './img'
        else:
            self.path = '/home/MarketManager/img'


        self.name = "M3_15min"


    def evaluate(self,results):
        self.evaluator.evaluate(results,self.parameters)



    def drawInfo(self, data, send=True):
        if data is not None:
            ima1 = self.parameters.ima1
            ima3 = self.parameters.ima3
            weekend = self.parameters.weekend
            rangehours = self.parameters.rangehours
            self.plotty.drawDataYahoo(data,ima1,ima3,weekend, self.parameters.name, send, rangehours)
            self.telegram.enviarDocumento(f"{self.path}/{self.parameters.name}.png", self.parameters.tele_group, self.parameters.name)

    def drawInfoDB(self, data, send=True, drawWeekEnd=False):
        if data is not None:
            ima1 = self.parameters.ima1
            ima3 = self.parameters.ima3
            drawWeekEnd = self.parameters.weekend
            self.plotty.drawDataDB(data, ima1, ima3, self.parameters.name, send, drawWeekEnd)
            if send:
                self.telegram.enviarDocumento(f"{self.path}/{self.parameters.name}.png", self.parameters.tele_group, self.parameters.name)

    def drawDataDBActions(self, data, buyData, sellData, closeData, send=True, rangehours=None, simulation=False):
        if data is not None:
            ima1 = self.parameters.ima1
            ima2 = self.parameters.ima2
            ima3 = self.parameters.ima3
            ima4 = self.parameters.ima4
            bollinger = self.parameters.bollinger
            drawWeekEnd = self.parameters.weekend
            self.plotty.drawDataDBActions(data,buyData,sellData,closeData, ima1,ima2, ima3,ima4,bollinger, self.parameters.name, send, drawWeekEnd, rangehours, simulation)
            if send:
                self.telegram.enviarDocumento(f"{self.path}/{self.parameters.name}.png", self.parameters.tele_group, self.parameters.name+" "+self.name)


    def drawMidNIght(self, data):
        # grafico
        t = time.localtime()
        current_time_h = time.strftime("%H", t)
        current_time_min = time.strftime("%M", t)
        print(f" hora : {current_time_h} minutos: {current_time_min}")

        if int(current_time_h) <= 0 and int(current_time_min) <= 15:
            self.drawInfo(data)

    def drawMidNIghtDB(self, data):
        # grafico
        t = time.localtime()
        current_time_h = time.strftime("%H", t)
        current_time_min = time.strftime("%M", t)
        print(f" gettime hora sistema: {current_time_h} minutos: {current_time_min}")
        currentTime = int(current_time_h + current_time_min)

        if currentTime>=2330 and currentTime<=2400:
            self.drawInfoDB(data, True, True)


    def drawInfoSimulation(self, data, data2):
        if data is not None:
            self.plotty.drawDataYahooSimulation(data, data2, self.name,ima1=self.ima1,ima2=self.ima2,ima3=self.ima3, drawWeekend =False)



