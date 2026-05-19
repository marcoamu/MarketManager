"""Simulation functions for MarketManager - standalone entry points."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import datetime
import configparser
import pandas as pd
from openpyxl import Workbook
from openpyxl import load_workbook

# Import from parent package (MarketManager.py)
from MarketManager import (
    MarketManager, MarketSQLManager, PlottyService,
    ActiveHelper, TelegramService
)

from core.simulation.analysis import (
    generateAnalisysData,
    generateAnalisysDataColoredOK,
    generateAnalisysDataColored,
    evaluateMarketMovements,
)


def simulateFlowConfig():
    useConfig = True
    isDBData = True
    simulation = True
    startSimGroup = 0
    send = True

    marketService = MarketManager(simulation=simulation, isDBData=isDBData, useConfig=useConfig, showLog=True,
                                  useSimulateDB=False)
    plotty = PlottyService()
    activeHelper = ActiveHelper(simulation=simulation, isDBData=isDBData)
    # actives = marketService.prepareUrlsTradingView()
    telegram = TelegramService()
    dataBDMan = MarketSQLManager(False)
    group = -613511116
    # rangehours = None #filtro horas no laborables ex [17,9]
    # telegram = None
    weekend = False

    # active = activeHelper.prepareAAPL2()
    # active = activeHelper.prepareDIS()
    # active = activeHelper.prepareDIS01()
    # active = activeHelper.prepareKO()
    # active = activeHelper.prepareNFLX2()
    # active = activeHelper.prepareTSLA01()
    # active = activeHelper.prepareMSFT()
    active = activeHelper.prepareINTC()
    # active = activeHelper.prepareMCD()
    # active = activeHelper.prepareGOOG()
    # active = activeHelper.prepareNVDA()
    # active = activeHelper.prepareBTC02()
    # active = activeHelper.prepareETH()
    # active = activeHelper.prepareAMZN1()
    # active = activeHelper.prepareAMZN2()

    period = 2
    if isDBData:
        period = 3
        weekno = datetime.datetime.today().weekday()

        if weekno == 0:
            period = 4
        data = dataBDMan.getAllWithNameForXdays(active.parameters.name, period)
    else:
        # DATA YAHOO
        nada = ""
        # data = yf.download(tickers=active.parameters.name, period=str(period) + 'd', interval='15m')
        # data = yf.download(tickers=active.parameters.name, interval='15m', start=start,end=end)

    # DATA FROM DB
    if useConfig:
        marketService.initConfig(active)

    size = len(data)
    print(f"TOTAL {size}")
    actives = list()
    actives.append(active)
    for x in range(startSimGroup, size + 1):
        print(f"\n\nSIMULACION {x} \n")
        subData = data.head(x)
        marketService.search_prices_list_data_simulation(actives, subData)

    # VER RESULTADOS FINALES
    tendence = None
    accumulated = None
    sellData = None
    buyData = None
    closeData = None
    tendenceUP = None
    tendenceDOWN = None
    tendenceWAIT = None

    # if len(marketService.operations.tendenceData)>0:
    #     tendence = pd.DataFrame(marketService.tendenceData)
    #     tendence['date'] = pd.to_datetime(tendence['date'] + pd.DateOffset(hours=active.parameters.hourOffset), format='%Y-%m-%d')
    # if len(marketService.accumulattedData) > 0:
    #     accumulated = pd.DataFrame(marketService.accumulattedData)
    #     accumulated['date'] = pd.to_datetime(accumulated['date'] + pd.DateOffset(hours=active.parameters.hourOffset), format='%Y-%m-%d')

    if len(marketService.operations.sellData) > 0:
        sellData = pd.DataFrame(marketService.operations.sellData)
        sellData['date'] = pd.to_datetime(sellData['date'] + pd.DateOffset(hours=active.parameters.hourOffset),
                                          format='%Y-%m-%d')
    if len(marketService.operations.buyData) > 0:
        buyData = pd.DataFrame(marketService.operations.buyData)
        buyData['date'] = pd.to_datetime(buyData['date'] + pd.DateOffset(hours=active.parameters.hourOffset),
                                         format='%Y-%m-%d')
    if len(marketService.operations.closeData) > 0:
        closeData = pd.DataFrame(marketService.operations.closeData)
        closeData['date'] = pd.to_datetime(closeData['date'] + pd.DateOffset(hours=active.parameters.hourOffset),
                                           format='%Y-%m-%d')
    # if len(marketService.operations.tendenceUPData)>0:
    #     tendenceUP = pd.DataFrame(marketService.operations.tendenceUPData)
    #     tendenceUP['date'] = pd.to_datetime(tendenceUP['date'] + pd.DateOffset(hours=active.parameters.hourOffset), format='%Y-%m-%d')
    # if len(marketService.operations.tendenceDOWNData)>0:
    #     tendenceDOWN = pd.DataFrame(marketService.operations.tendenceDOWNData)
    #     tendenceDOWN['date'] = pd.to_datetime(tendenceDOWN['date'] + pd.DateOffset(hours=active.parameters.hourOffset), format='%Y-%m-%d')
    # if len(marketService.operations.tendenceWAITData)>0:
    #     tendenceWAIT = pd.DataFrame(marketService.operations.tendenceWAITData)
    #     tendenceWAIT['date'] = pd.to_datetime(tendenceWAIT['date'] + pd.DateOffset(hours=active.parameters.hourOffset), format='%Y-%m-%d')

    # print(f"buyData {len(buyData)}")
    # print(f"sellData {len(sellData)}")

    if send == True:
        if telegram is not None:
            telegram.send_message(f"{active.parameters.name} simulateFlowConfig -> size {size}", group)
        else:
            print("NO TELEGRAM")

    # pl.plotActive(buyData, sellData, closeData, None, None, None,  active, name, period, None, None)
    # plotty.plotActive(buyData, sellData, closeData, None, None, None, active, name=f"{active.parameters.name}_simulateFlowConfig", period=period)

    sellvalues = marketService.operations.sellData
    buyValues = marketService.operations.buyData
    normalValues = marketService.operations.closeData
    generateAnalisysData(buyValues, sellvalues, normalValues, active)


def simulateFlow():
    useConfig = False
    isDBData = True
    simulation = True
    startSimGroup = 1
    send = True

    marketService = MarketManager(simulation=simulation, isDBData=isDBData, useConfig=useConfig, useSimulateDB=True)
    plotty = PlottyService()
    activeHelper = ActiveHelper(simulation=simulation, isDBData=isDBData)
    # actives = marketService.prepareUrlsTradingView()
    telegram = TelegramService()
    dataBDMan = MarketSQLManager(False)

    active = activeHelper.prepareAAPL1()
    # active = activeHelper.prepareDIS()
    # active = activeHelper.prepareKO()
    # active = activeHelper.prepareNFLX()
    # active = activeHelper.prepareTSLA()
    # active = activeHelper.prepareBTC()
    # active = activeHelper.prepareETH()
    # active = activeHelper.prepareAMZN()

    if isDBData:
        period = 2
        data = dataBDMan.getAllWithNameForXdays(active.parameters.name, period)
    else:
        # DATA YAHOO
        nada = ""
        # data = yf.download(tickers=active.parameters.name, period='3d', interval='15m')

    # DATA FROM DB
    if isDBData == False:
        marketService.initConfig(active)

    size = len(data)
    print(f"TOTAL {size}")
    actives = list()
    actives.append(active)
    for x in range(startSimGroup, size + 1):
        print(f"\n\nSIMULACION {x} \n")
        subData = data.head(x)
        marketService.search_prices_list_data_simulation(actives, subData)

    # VER RESULTADOS FINALES
    tendence = None
    accumulated = None
    sellData = None
    buyData = None
    closeData = None
    tendenceUP = None
    tendenceDOWN = None
    tendenceWAIT = None

    # if len(marketService.operations.tendenceData)>0:
    #     tendence = pd.DataFrame(marketService.tendenceData)
    #     tendence['date'] = pd.to_datetime(tendence['date'] + pd.DateOffset(hours=active.parameters.hourOffset), format='%Y-%m-%d')
    # if len(marketService.accumulattedData) > 0:
    #     accumulated = pd.DataFrame(marketService.accumulattedData)
    #     accumulated['date'] = pd.to_datetime(accumulated['date'] + pd.DateOffset(hours=active.parameters.hourOffset), format='%Y-%m-%d')

    if len(marketService.operations.sellData) > 0:
        sellData = pd.DataFrame(marketService.operations.sellData)
        sellData['date'] = pd.to_datetime(sellData['date'] + pd.DateOffset(hours=active.parameters.hourOffset),
                                          format='%Y-%m-%d')
    if len(marketService.operations.buyData) > 0:
        buyData = pd.DataFrame(marketService.operations.buyData)
        buyData['date'] = pd.to_datetime(buyData['date'] + pd.DateOffset(hours=active.parameters.hourOffset),
                                         format='%Y-%m-%d')
    if len(marketService.operations.closeData) > 0:
        closeData = pd.DataFrame(marketService.operations.closeData)
        closeData['date'] = pd.to_datetime(closeData['date'] + pd.DateOffset(hours=active.parameters.hourOffset),
                                           format='%Y-%m-%d')

    # print(f"buyData {len(buyData)}")
    # print(f"sellData {len(sellData)}")

    if send == True:
        if telegram is not None:
            telegram.send_message(f"{active.parameters.name} simulateFlow -> size {size}", group)
        else:
            print("NO TELEGRAM")

    sellvalues = marketService.operations.sellData
    buyValues = marketService.operations.buyData
    normalValues = marketService.operations.closeData
    generateAnalisysDataColored(buyValues, sellvalues, normalValues, active)


def RealModeConfig():
    isDBData = True
    useConfig = True
    simulation = False
    disableCloseEndRevenue = True
    disableInitPROB = False
    marketService = MarketManager(simulation=simulation, isDBData=isDBData, useConfig=useConfig, showLog=True,
                                  disableInitPROB=disableInitPROB, disableCloseEndRevenue=disableCloseEndRevenue)
    activeHelper = ActiveHelper(isDBData=isDBData)
    actives = activeHelper.prepareActives()
    marketService.updateIntervalForAll(actives)
    marketService.search_prices_list(actives)
    marketService.updateCounterForAll()
    marketService.sendResultsEndDay()


def RealMode():
    isDBData = True
    useConfig = False
    simulation = False
    disableCloseEndRevenue = True
    disableInitPROB = False
    marketService = MarketManager(simulation=simulation, isDBData=isDBData, useConfig=useConfig, showLog=False,
                                  disableInitPROB=disableInitPROB, disableCloseEndRevenue=disableCloseEndRevenue)
    activeHelper = ActiveHelper(isDBData=isDBData)
    actives = activeHelper.prepareActives()
    allactives = activeHelper.prepareActives()
    # marketService.updateTimeZoneValues()
    # todos los activos
    marketService.updateIntervalForAll(allactives)
    marketService.search_prices_list(actives)
    marketService.updateCounterForAll()
    marketService.sendResultsEndDay()


def RealModeLocal(skipDayControl):
    isDBData = True
    useConfig = False
    simulation = False
    disableCloseEndRevenue = True
    disableInitPROB = False
    marketService = MarketManager(simulation=simulation, isDBData=isDBData, useConfig=useConfig, showLog=False,
                                  disableInitPROB=disableInitPROB, disableCloseEndRevenue=disableCloseEndRevenue)
    activeHelper = ActiveHelper(isDBData=isDBData)
    actives = activeHelper.prepareActives()
    allactives = activeHelper.prepareActives()
    # marketService.updateTimeZoneValues()
    # todos los activos
    marketService.updateIntervalForAll(allactives)
    marketService.search_prices_list(actives)
    marketService.updateCounterForAll()
    marketService.sendResultsEndDay()


def drawActive():
    isDBData = True
    simulation = True
    marketService = MarketManager(simulation=simulation, isDBData=isDBData)
    activeHelper = ActiveHelper(simulation=simulation, isDBData=isDBData)

    active = activeHelper.prepareAAPL1()

    marketService.updateIntervalForAll([active])
    marketService.search_prices_list([active])


def drawActiveDates(skipDayControl = False):
    isDBData = True
    simulation = True
    marketService = MarketManager(simulation=simulation, isDBData=isDBData)
    activeHelper = ActiveHelper(simulation=simulation, isDBData=isDBData)
    telegram = TelegramService()

    active = activeHelper.prepareAAPL1()

    marketService.updateIntervalForAll([active])
    marketService.search_prices_list([active])

    sellvalues = marketService.operations.sellData
    buyValues = marketService.operations.buyData
    normalValues = marketService.operations.closeData
    evaluateMarketMovements(buyValues, sellvalues)


def drawActiveDatesSelected(skipDayControl = False):
    print("NOT IMPLEMENTED YET")


def simulateFlowActive():
    print("FLOW ACTIVE NOT IMPLEMENTED YET")


def drawRelativeTendence():
    print("NOT IMPLEMENTED YET")


def simulateWeekDirection():
    print("NOT IMPLEMENTED YET")


def simulateIndicatorDates():
    print("NOT IMPLEMENTED YET")


def simulateEvaluatorsForActiveDates():
    print("NOT IMPLEMENTED YET")


def simulate_Star_Close_ForActiveDates():
    print("NOT IMPLEMENTED YET")


def simulate_EMA_parameters_ForActiveDates():
    print("NOT IMPLEMENTED YET")


def simulate_Control_ForActiveDates():
    print("NOT IMPLEMENTED YET")
