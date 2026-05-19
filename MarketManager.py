
import datetime
import time

import pandas as pd
import configparser
import logging
# import talib
import math

from helpers.Operations import Operations
from service.Active import Active
from service.ActiveHelper import ActiveHelper
from service.AlpacaServiceBot import AlpacaServiceBot
from service.AnalisisHelper import AnalisisHelper
from service.Constants import Constants
from service.MarketSQLManager import MarketSQLManager
from service.PLottyService import PlottyService
from service.Parameters import Parameters
from service.ProbEvaluator import ProbEvaluator
from service.TelegramService import TelegramService
from backtesting.lib import crossover


# === PURE FUNCTIONS EXTRACTED TO core/pure/ ===
from core.pure.math_utils import (
    calcular_angulo, calcular_minutos_entre_fechas, determineFlow,
    determineMedMomentFlow, determine_Direction_percent_Flow, calculatePercentFcst,
    getProMEDSTD_MID, determinePercentDistance, determinarRelativePercent,
    calculate_rsi, mide_tiempo,
)
from core.pure.evaluation_utils import (
    isHour, postcalculation, _eval_init_parameters, _eval_bollinger_distances,
    _eval_set_final_defaults, determinarIndicatorTendenceMomentBest, determinar_flujo_WEEK,
)
from core.pure.data_utils import (
    addmessages, updateMinMaxValues, printValues, reviewControls,
    search_pricesYahoo, findActiveInDB,
)

import numpy as np



def mide_tiempo(funcion):
    def funcion_medida(*args, **kwargs):
        inicio = time.time()
        c = funcion(*args, **kwargs)
        print(f"Tiempo para {str(funcion)} es : {time.time() - inicio}")
        return c
    return funcion_medida

class MarketManager:

    def __init__(self, simulation=False, isDBData=False, useConfig=False, showLog=True, useSimulateDB=False, start=None,
                 end=None, disableInitPROB=True, disableCloseEndRevenue=True, needAnalsis=False,allAnalysLogs = False, operate=True, onlyStartEnd = False, showAnallisisFlow = False, updateDBSimulation = False):

        self.telegram = TelegramService()
        self.probEvaluator = ProbEvaluator()
        self.simulation = simulation
        self.onlyStartEnd = onlyStartEnd
        self.operate = operate
        self.allAnalysLogs = allAnalysLogs
        self.needAnalsis = needAnalsis
        self.disableCloseEndRevenue = disableCloseEndRevenue
        self.useConfig = useConfig
        self.isDBData = isDBData
        self.showLog = showLog
        self.closeValue = 'Close'
        self.start = start
        self.end = end
        self.analisisHelper = AnalisisHelper()
        self.updateDBSimulation = updateDBSimulation
        self.showAnallisisFlow = showAnallisisFlow

        #LOGS PARA EXCEL
        self.showRSILogs = False
        self.showMinMaxLogs = False
        self.showHourlyLogs = False
        self.showExtraLogs = False
        self.showMarketTrendLogs = True
        self.showBLGLogs = False
        self.showAngleLogs = True
        self.showDirBotLog = True
        self.showWeekLogs = True

        #para dibujar los puntos frios y calientes en base a:
        self.drawnMedia_UPDOWN = False
        self.drawnEMA_UPDOWN = True
        if isDBData:
            self.closeValue = 'value'
        self.config_obj = configparser.ConfigParser()
        self.dataBDMan = MarketSQLManager(useSimulateDB)
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
            self.configPath = "F:\\WORK\\2026\\MarketManager\\config\\config.ini"
        else:
            self.configPath = "/home/MarketManager/config/config.ini"
        self.alpaca = AlpacaServiceBot()
        self.activeHelper = ActiveHelper(self.simulation, self.isDBData)
        self.operations = Operations()
        self.init()
        self.disableInitProb = disableInitPROB

    def init(self):
        self.MAX = 5
        self.config_obj.read(self.configPath)
        self.log = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        # self.newTelegroup = -4197698684
        self.newTelegroup = -5007791008
        self.resultsTelegroup = -956772885
        # self.errorTelegroup = -911722660
        self.errorTelegroup = -5272431097
        self.importanteslTelegroup = -4023047810
        self.sendres = False
        self.diffValues = list()
        self.enableControlWIN = False
        self.name = "M3_15min"
        self.intervalTime = 15
        # calculos finales
        self.closeStart = 2050
        self.closeEnd = 2055

        # caluclos iniciales
        self.iniStart = 1430
        self.iniEnd = 1435

        # retornar intervalo
        self.normalIntervalStart = 1500
        self.normalIntervalEnd = 1505

        # prepare relative values
        self.prepRelStart = 1420
        self.prepRelEnd = 1430

        self.minimunActionAcum = 0.5
        self.prepareVerano()

    def createConfig(self, active):
        self.config_obj.add_section(active.parameters.name)
        self.config_obj.set(active.parameters.name, 'value', '0')
        self.config_obj.set(active.parameters.name, 'action', 'WAIT')
        self.config_obj.set(active.parameters.name, 'action_acum', '0')
        self.config_obj.set(active.parameters.name, 'action_count', '0')
        self.config_obj.set(active.parameters.name, 'min', '99999')
        self.config_obj.set(active.parameters.name, 'max', '0')
        self.config_obj.set(active.parameters.name, 'direction', 'DIR_WAIT')
        self.config_obj.set(active.parameters.name, 'min_dir', '99999')
        self.config_obj.set(active.parameters.name, 'max_dir', '0')
        self.config_obj.set(active.parameters.name, 'flujo', 'NONE')
        self.config_obj.set(active.parameters.name, 'RELATIVE_min', '999999')
        self.config_obj.set(active.parameters.name, 'RELATIVE_prev_min', '999999')
        self.config_obj.set(active.parameters.name, 'RELATIVE_max', '0')
        self.config_obj.set(active.parameters.name, 'RELATIVE_prev_max', '0')
        self.config_obj.set(active.parameters.name, 'week_flow', 'WEEK_FLOW_NOTINIT')
        self.config_obj.set(active.parameters.name, 'week_min_dir', '999999')
        self.config_obj.set(active.parameters.name, 'week_max_dir', '0')
        self.config_obj.set(active.parameters.name, 'angle_ima', '0')
        self.config_obj.set(active.parameters.name, 'angle_ima_counter', '0')
        self.config_obj.set(active.parameters.name, 'angle_counter', '0')
        self.config_obj.set(active.parameters.name, 'angle', '0')
        self.config_obj.set(active.parameters.name, 'week_dir', 'WEEK_FLOW_UNDEF')
        self.config_obj.set(active.parameters.name, 'week_dir_flow', '0')
        self.config_obj.set(active.parameters.name, 'week_flow_std', '0')
        self.config_obj.set(active.parameters.name, 'week_flow_med', '0')
        self.config_obj.set(active.parameters.name, 'rel_fcst', 'IND_REL_FCST_NOTINIT')
        self.config_obj.set(active.parameters.name, 'rel_fcst_std', '0')
        self.config_obj.set(active.parameters.name, 'rel_fcst_med', '0')
        self.config_obj.set(active.parameters.name, 'rel_fcst_min', '0')
        self.config_obj.set(active.parameters.name, 'rel_fcst_max', '0')
        self.config_obj.set(active.parameters.name, 'rel_fcst_percent', '0')
        self.config_obj.set(active.parameters.name, 'close_nxt_up', '0')
        self.config_obj.set(active.parameters.name, 'close_nxt_down', '0')
        self.config_obj.set(active.parameters.name, 'close_nxt_middle', '0')

        self.config_obj.set(active.parameters.name, 'minweek', '0')
        self.config_obj.set(active.parameters.name, 'maxweek', '0')
        self.config_obj.set(active.parameters.name, 'minmonth', '0')
        self.config_obj.set(active.parameters.name, 'maxmonth', '0')

        with open(self.configPath, 'w') as configfile:
            self.config_obj.write(configfile)

    def initConfig(self, active, data):
        # update config
        try:
            RELATIVE_prev_min = '999999'
            RELATIVE_min = '999999'
            RELATIVE_prev_max = '0'
            RELATIVE_max = '0'
            week_flow_std = '0'
            week_flow_med = '0'
            rel_fcst_std = '0'
            rel_fcst_med = '0'
            rel_fcst_min = '0'
            rel_fcst_max = '0'
            rel_fcst_percent = '0'
            close_nxt_up = '0'
            close_nxt_down = '0'
            close_nxt_middle = '0'
            angle_ima = '0'
            angle_ima_counter = '0'
            angle = '0'
            angle_counter = '0'

            minweek = '0'
            maxweek = '0'
            minmonth = '0'
            maxmonth = '0'

            week_flow = Constants.WEEK_FLOW_NOTINIT
            week_dir = Constants.WEEK_FLOW_NOTINIT
            week_min_dir = '99999'
            week_max_dir = '0'
            week_dir_flow = ""
            rel_fcst = Constants.IND_REL_FCST_NOTINIT
            if data.empty == False:
                if 'global_min' in data:
                    RELATIVE_prev_min = data['global_min'][0]
                    if RELATIVE_prev_min:
                        RELATIVE_prev_min = float(RELATIVE_prev_min)
                    else:
                        RELATIVE_prev_min = '999999'

                    RELATIVE_min = data['relative_min'][0]
                    if RELATIVE_min:
                        RELATIVE_min = float(RELATIVE_min)
                    else:
                        RELATIVE_min = '999999'

                    RELATIVE_prev_max = data['global_max'][0]
                    if RELATIVE_prev_max:
                        RELATIVE_prev_max = float(RELATIVE_prev_max)
                    else:
                        RELATIVE_prev_max = '0'

                    RELATIVE_max = data['relative_max'][0]
                    if RELATIVE_max:
                        RELATIVE_max = float(RELATIVE_max)
                    else:
                        RELATIVE_max = '0'

                    week_flow = data['week_flow'][0]
                    if week_flow is None:
                        week_flow = Constants.WEEK_FLOW_NOTINIT

                    week_dir = data['week_dir'][0]
                    if week_dir is None:
                        week_dir = Constants.WEEK_FLOW_NOTINIT

                    week_min_dir = data['week_min_dir'][0]
                    if week_min_dir is None:
                        week_min_dir = '99999'

                    week_max_dir = data['week_max_dir'][0]
                    if week_max_dir is None:
                        week_min_dir = '0'

                    week_dir_flow = data['week_dir_flow'][0]
                    if week_dir_flow is None:
                        week_dir_flow = '0'

                    week_flow_std = data['week_flow_std'][0]
                    if week_flow_std:
                        week_flow_std = float(week_flow_std)
                    else:
                        week_flow_std = '0'

                    week_flow_med = data['week_flow_med'][0]
                    if week_flow_med:
                        week_flow_med = float(week_flow_med)
                    else:
                        week_flow_med = '0'

                    rel_fcst = data['rel_fcst'][0]
                    if rel_fcst is None:
                        rel_fcst = Constants.IND_REL_FCST_NOTINIT

                    rel_fcst_std = data['rel_fcst_std'][0]
                    if rel_fcst_std:
                        rel_fcst_std = float(rel_fcst_std)
                    else:
                        rel_fcst_std = '0'

                    rel_fcst_med = data['rel_fcst_med'][0]
                    if rel_fcst_med:
                        rel_fcst_med = float(rel_fcst_med)
                    else:
                        rel_fcst_med = '0'

                    rel_fcst_min = data['rel_fcst_min'][0]
                    if rel_fcst_min:
                        rel_fcst_min = float(rel_fcst_min)
                    else:
                        rel_fcst_min = '0'

                    rel_fcst_max = data['rel_fcst_max'][0]
                    if rel_fcst_max:
                        rel_fcst_max = float(rel_fcst_max)
                    else:
                        rel_fcst_max = '0'

                    rel_fcst_percent = data['rel_fcst_percent'][0]
                    if rel_fcst_percent:
                        rel_fcst_percent = float(rel_fcst_percent)
                    else:
                        rel_fcst_percent = '0'

                    close_nxt_up = data['close_nxt_up'][0]
                    if close_nxt_up:
                        close_nxt_up = float(close_nxt_up)
                    else:
                        close_nxt_up = '0'

                    angle_ima = data['angle_ima'][0]
                    if angle_ima:
                        angle_ima = float(angle_ima)
                    else:
                        angle_ima = '0'

                    angle_ima_counter = data['angle_ima_counter'][0]
                    if angle_ima_counter:
                        angle_ima_counter = float(angle_ima_counter)
                    else:
                        angle_ima_counter = '0'

                    angle = data['angle'][0]
                    if angle:
                        angle = float(angle)
                    else:
                        angle = '0'

                    angle_counter = data['angle_counter'][0]
                    if angle_counter:
                        angle_counter = float(angle_counter)
                    else:
                        angle_counter = '0'
    
                    close_nxt_down = data['close_nxt_down'][0]
                    if close_nxt_down:
                        close_nxt_down = float(close_nxt_down)
                    else:
                        close_nxt_down = '0'

                    close_nxt_middle = data['close_nxt_middle'][0]
                    if close_nxt_middle:
                        close_nxt_middle = float(close_nxt_middle)
                    else:
                        close_nxt_middle = '0'

                    # maxweek = data['maxweek'][0]
                    # if maxweek:
                    #     maxweek = float(maxweek)
                    # else:
                    #     maxweek = '0'
                    #     maxweek = data['maxweek'][0]
                    #
                    # minweek = data['minweek'][0]
                    # if minweek:
                    #     minweek = float(minweek)
                    # else:
                    #     minweek = '0'
                    #     minweek = data['minweek'][0]
                    #
                    # if minmonth:
                    #     minmonth = float(minmonth)
                    # else:
                    #     minmonth = '0'
                    #
                    # maxmonth = data['maxmonth'][0]
                    # if maxmonth:
                    #     maxmonth = float(maxmonth)
                    # else:
                    #     maxmonth = '0'


            edit = self.config_obj[active.parameters.name]
            edit['action'] = 'WAIT'
            edit['value'] = '0'
            edit['action_count'] = '0'
            edit['action_acum'] = '0'
            edit['min'] = '99999'
            edit['max'] = '0'
            edit['direction'] = 'DIR_WAIT'
            edit['min_dir'] = '99999'
            edit['max_dir'] = '0'
            edit['flujo'] = 'None'
            edit['RELATIVE_min'] = str(RELATIVE_min)
            edit['RELATIVE_prev_min'] = str(RELATIVE_prev_min)
            edit['RELATIVE_max'] = str(RELATIVE_max)
            edit['RELATIVE_prev_max'] = str(RELATIVE_prev_max)
            edit['week_flow'] = str(week_flow)
            edit['week_dir'] = str(week_dir)
            edit['week_dir_flow'] = str(week_dir_flow)
            edit['week_min_dir'] = str(week_min_dir)
            edit['week_max_dir'] = str(week_max_dir)
            edit['week_flow_std'] = str(week_flow_std)
            edit['week_flow_med'] = str(week_flow_med)
            edit['angle_ima'] = str(angle_ima)
            edit['angle_ima_counter'] = str(angle_ima_counter)
            edit['angle'] = str(angle)
            edit['angle_counter'] = str(angle_counter)
            edit['week_flow_med'] = str(week_flow_med)
            edit['rel_fcst'] = str(rel_fcst)
            edit['rel_fcst_std'] = str(rel_fcst_std)
            edit['rel_fcst_med'] = str(rel_fcst_med)
            edit['rel_fcst_min'] = str(rel_fcst_min)
            edit['rel_fcst_max'] = str(rel_fcst_max)
            edit['rel_fcst_percent'] = str(rel_fcst_percent)
            edit['close_nxt_up'] = str(close_nxt_up)
            edit['close_nxt_down'] = str(close_nxt_down)
            edit['close_nxt_middle'] = str(close_nxt_middle)

            edit['minweek'] = str(minweek)
            edit['maxweek'] = str(maxweek)
            edit['minmonth'] = str(minmonth)
            edit['maxmonth'] = str(maxmonth)

            with open(self.configPath, 'w') as configfile:
                self.config_obj.write(configfile)
        except Exception as e:
            print(f"ERROR initonfig {str(e)}")
            param = self.createConfig(active)

    def reviewControls(self, data, active):
        ids = list()
        try:
            algo = ""
        except Exception as e:
            print(f"ERROR reviewControls {str(e)}")

    #@mide_tiempo
    def review_results(self, data, results, active):
        if data is not None:
            # print(f"review Results")
            results[Constants.NAME] = active.parameters.name
            alert = "FALSE"
            # encontrar tendencia
            cambio = False
            contador = len(data) - 1
            current = data.iloc[[-1]]
            act = 'WAIT'
            act_val = 0
            last_val = 0
            action_acum = 0
            min = 99999
            max = 0
            id = 0
            action_min_dist = 0
            action_max_dist = 0
            direction = Constants.DIR_WAIT
            min_dir = 9999
            max_dir = 0
            indi_dir = ""
            tendence = None
            changePoint = None
            flujo_count = 0
            acumulado = 0.0
            action_distance = 0
            RELATIVE_min = 99999
            RELATIVE_prev_min = 99999
            RELATIVE_max = 0
            RELATIVE_prev_max = 0
            RELATIVE_max_dist = 0
            RELATIVE_min_dist = 0
            action_count = 0
            week_flow = ""
            week_dir = ""
            week_min_dir = 99999
            week_max_dir = 0
            week_flow_std = 0
            week_flow_med = 0
            rel_fcst = ""
            rel_fcst_std = 0
            rel_fcst_med = 0
            rel_fcst_min = 0
            rel_fcst_max = 0
            rel_fcst_percent = 0
            close_nxt_up = 0
            close_nxt_down = 0
            close_nxt_middle = 0

            currentValue = float(current[self.closeValue].iloc[0])

            # print(f" CURRENT VALUE : {currentValue}")
            results[Constants.VALUE] = currentValue
            results[Constants.PROFIT] = float(current['profit'].iloc[0])
            results[Constants.PROTECT] = float(current['protect'].iloc[0])
            if self.isDBData:
                results[Constants.DATE] = current['date']
            else:
                results[Constants.DATE] = current.index
            if Constants.FLUJO not in results:
                flujo = self.determinar_flujo(data)
            else:
                flujo = results[Constants.FLUJO]

            results[Constants.ACTION_MIN] = 0

            results[Constants.ACTION_MAX] = 0

            # DETERMINAR EL ACUMULADO
            count = 0
            while cambio != True:
                if contador <= 0:
                    cambio = True
                    break
                valor = data.iloc[[contador]]
                valorPre = data.iloc[[contador - 1]]
                if valor is not None:
                    dif = float(valor[self.closeValue].iloc[0]) - float(valorPre[self.closeValue].iloc[0])
                    # difabs = abs(float(valor[self.closeValue]) - float(valorPre[self.closeValue]))

                    if flujo == "SUBE":
                        if dif < 0:
                            cambio = True
                            if count == 0:
                                changePoint = float(valorPre[self.closeValue].iloc[0])
                            else:
                                changePoint = float(valor[self.closeValue].iloc[0])
                            if acumulado == 0:
                                acumulado = acumulado + dif
                        elif dif > 0:
                            flujo_count = flujo_count + 1
                            acumulado = acumulado + dif
                        else:
                            flujo_count = flujo_count + 1
                            acumulado = acumulado + dif
                    else:
                        if dif > 0:
                            cambio = True
                            if count == 0:
                                changePoint = float(valorPre[self.closeValue].iloc[0])
                            else:
                                changePoint = float(valor[self.closeValue].iloc[0])
                            if acumulado == 0:
                                acumulado = acumulado + dif
                        elif dif < 0:
                            flujo_count = flujo_count + 1
                            acumulado = acumulado + dif
                        else:
                            flujo_count = flujo_count + 1
                            acumulado = acumulado + dif
                else:
                    cambio = True
                    # flujo_count = 0
                    # acumulado = 0.0
                    break
                contador = contador - 1
                count = count + 1

            if Constants.CURRENT_ACTION not in results:
                if self.useConfig:
                    try:
                        param = self.config_obj[active.parameters.name]
                        results[Constants.DBID] = data.iloc[-1]['id']
                        act = param['action']
                        act_val = param['value']
                        action_count = param['action_count']
                        min = param['min']
                        max = param['max']
                        direction = param['direction']
                        min_dir = param['min_dir']
                        max_dir = param['max_dir']
                        week_flow = param['week_flow']
                        week_dir = param['week_dir']
                        week_dir_flow_prev = param['week_dir_flow']
                        week_min_dir = param['week_min_dir']
                        week_max_dir = param['week_max_dir']
                        week_flow_std = param['week_flow_std']
                        week_flow_med = param['week_flow_med']
                        rel_fcst = param['rel_fcst']
                        rel_fcst_std = param['rel_fcst_std']
                        rel_fcst_med = param['rel_fcst_med']
                        rel_fcst_min = param['rel_fcst_min']
                        rel_fcst_max = param['rel_fcst_max']
                        rel_fcst_percent = param['rel_fcst_percent']
                        close_nxt_up = param['close_nxt_up']
                        close_nxt_down = param['close_nxt_down']
                        close_nxt_middle = param['close_nxt_middle']
                        angle_ima = param['angle_ima']
                        angle_ima_counter = param['angle_ima_counter']
                        angle = param['angle']
                        angle_counter = param['angle_counter']
                        tendence = param['flujo']

                        last_val = act_val

                        action_acum = param["action_acum"]
                        if action_acum is None:
                            action_acum = 0
                        else:
                            if act != 'WAIT' and act != 'CLOSE':
                                action_acum = float(action_acum) + (float(currentValue) - float(last_val))
                            else:
                                action_acum = 0

                        RELATIVE_min = param['RELATIVE_min']
                        if RELATIVE_min:
                            RELATIVE_min = float(RELATIVE_min)

                        RELATIVE_prev_min = param['RELATIVE_prev_min']
                        if RELATIVE_prev_min:
                            RELATIVE_prev_min = float(RELATIVE_prev_min)

                        RELATIVE_max = param['RELATIVE_max']
                        if RELATIVE_max:
                            RELATIVE_max = float(RELATIVE_max)

                        RELATIVE_prev_max = param['RELATIVE_prev_max']
                        if RELATIVE_prev_max:
                            RELATIVE_prev_max = float(RELATIVE_prev_max)

                        close_nxt_up = param['close_nxt_up']
                        if close_nxt_up:
                            close_nxt_up = float(close_nxt_up)
                        else:
                            close_nxt_up = 0

                        close_nxt_down = param['close_nxt_down']
                        if close_nxt_down:
                            close_nxt_down = float(close_nxt_down)
                        else:
                            close_nxt_down = 0

                        close_nxt_middle = param['close_nxt_middle']
                        if close_nxt_middle:
                            close_nxt_middle = float(close_nxt_middle)
                        else:
                            close_nxt_middle = 0
                    except Exception as e:
                        print(f"ERROR review_results useConfig {str(e)}")
                        param = self.createConfig(active)
                        act = 'WAIT'
                        act_val = 0
                else:
                    try:
                        oldDBvalue = self.dataBDMan.getLastValueWithName(active.parameters.name)
                        if oldDBvalue is not None:
                            act = oldDBvalue[0]["action"]
                            if act is None:
                                act = 'WAIT'
                            act_val = oldDBvalue[0]["value"]

                            last_val = oldDBvalue[0]["lastValue"]
                            if last_val is None:
                                last_val = act_val

                            action_acum = oldDBvalue[0]["action_acum"]
                            if action_acum is None:
                                action_acum = 0
                            else:
                                if act != 'WAIT' and act != 'CLOSE':
                                    action_acum = action_acum + (float(act_val) - float(last_val))
                                else:
                                    action_acum = 0

                            action_count = oldDBvalue[0]["action_count"]
                            if action_count is None:
                                action_count = 0

                            angle_ima = oldDBvalue[0]["angle_ima"]
                            if angle_ima is None:
                                angle_ima = 0

                            angle_ima_counter = oldDBvalue[0]["angle_ima_counter"]
                            if angle_ima_counter is None:
                                angle_ima_counter = 0

                            angle = oldDBvalue[0]["angle"]
                            if angle is None:
                                angle = 0

                            angle_counter = oldDBvalue[0]["angle_counter"]
                            if angle_counter is None:
                                angle_counter = 0

                            min = oldDBvalue[0]["min_value"]
                            max = oldDBvalue[0]["max_value"]
                            id = oldDBvalue[0]["id"]
                            results[Constants.DBID] = id
                            direction = oldDBvalue[0]["direction"]
                            min_dir = oldDBvalue[0]["min_dir"]
                            tendence = oldDBvalue[0]["tendence"]
                            if min_dir is None:
                                min_dir = 99999
                            max_dir = oldDBvalue[0]["max_dir"]
                            if max_dir is None:
                                max_dir = 0
                            indi_dir = oldDBvalue[0]["indi_dir"]

                            RELATIVE_min = oldDBvalue[0]['motion_min']
                            if RELATIVE_min:
                                RELATIVE_min = float(RELATIVE_min)
                            else:
                                RELATIVE_min = 99999
                            RELATIVE_max = oldDBvalue[0]['motion_max']
                            if RELATIVE_max:
                                RELATIVE_max = float(RELATIVE_max)
                            else:
                                RELATIVE_max = 0

                            RELATIVE_prev_min = oldDBvalue[0]['global_min']
                            if RELATIVE_prev_min:
                                RELATIVE_prev_min = float(RELATIVE_prev_min)
                            else:
                                RELATIVE_prev_min = 99999
                            RELATIVE_prev_max = oldDBvalue[0]['global_max']
                            if RELATIVE_prev_max:
                                RELATIVE_prev_max = float(RELATIVE_prev_max)
                            else:
                                RELATIVE_prev_max = 0

                            week_flow = oldDBvalue[0]['week_flow']
                            if week_flow is None:
                                week_flow = Constants.WEEK_FLOW_NOTINIT

                            week_flow_std = oldDBvalue[0]['week_flow_std']
                            if week_flow_std:
                                week_flow_std = float(week_flow_std)
                            else:
                                week_flow_std = 0

                            week_flow_med = oldDBvalue[0]['week_flow_med']
                            if week_flow_med:
                                week_flow_med = float(week_flow_med)
                            else:
                                week_flow_med = 0

                            rel_fcst = oldDBvalue[0]['rel_fcst']
                            if rel_fcst is None:
                                rel_fcst = Constants.IND_REL_FCST_NOTINIT

                            rel_fcst_std = oldDBvalue[0]['rel_fcst_std']
                            if rel_fcst_std:
                                rel_fcst_std = float(rel_fcst_std)
                            else:
                                rel_fcst_std = 0

                            rel_fcst_med = oldDBvalue[0]['rel_fcst_med']
                            if rel_fcst_med:
                                rel_fcst_med = float(rel_fcst_med)
                            else:
                                rel_fcst_med = 0

                            rel_fcst_min = oldDBvalue[0]['rel_fcst_min']
                            if rel_fcst_min:
                                rel_fcst_min = float(rel_fcst_min)
                            else:
                                rel_fcst_min = 0

                            rel_fcst_max = oldDBvalue[0]['rel_fcst_max']
                            if rel_fcst_max:
                                rel_fcst_max = float(rel_fcst_max)
                            else:
                                rel_fcst_max = 0

                            rel_fcst_percent = oldDBvalue[0]['rel_fcst_percent']
                            if rel_fcst_percent:
                                rel_fcst_percent = float(rel_fcst_percent)
                            else:
                                rel_fcst_percent = 0

                            close_nxt_up = oldDBvalue[0]['close_nxt_up']
                            if close_nxt_up:
                                close_nxt_up = float(close_nxt_up)
                            else:
                                close_nxt_up = 0

                            close_nxt_down = oldDBvalue[0]['close_nxt_down']
                            if close_nxt_down:
                                close_nxt_down = float(close_nxt_down)
                            else:
                                close_nxt_down = 0

                            close_nxt_middle = oldDBvalue[0]['close_nxt_middle']
                            if close_nxt_middle:
                                close_nxt_middle = float(close_nxt_middle)
                            else:
                                close_nxt_middle = 0

                            week_dir_flow_prev = oldDBvalue[0]['week_dir_flow']
                            if week_dir_flow_prev is None:
                                week_dir_flow_prev = 0

                            week_dir = oldDBvalue[0]['week_dir']
                            if week_dir is None:
                                week_dir = Constants.WEEK_FLOW_NOTINIT

                            week_min_dir = oldDBvalue[0]['week_min_dir']
                            if week_min_dir is None:
                                week_min_dir = 99999

                            week_max_dir = oldDBvalue[0]['week_max_dir']
                            if week_max_dir is None:
                                week_max_dir = 0


                    except Exception as e:
                        print(f"ERROR review_results oldDBvalue {str(e)}")
                        self.log.error(f"Error {str(e)}")

                # print(f"action for {active.parameters.name} : {act} start value :{act_val}")
                results[Constants.CURRENT_ACTION] = act
                results[Constants.ACTION_COUNT] = int(action_count)
                results[Constants.ACTION_ACUM] = float(action_acum)

                # valores recuperados
                results[Constants.WEEK_FLOW] = week_flow
                results[Constants.WEEK_FLOW_MED] = float(week_flow_med)
                results[Constants.WEEK_FLOW_STD] = float(week_flow_std)
                results[Constants.IND_REL_FCST] = rel_fcst
                results[Constants.IND_REL_FCST_STD] = rel_fcst_std
                results[Constants.IND_REL_FCST_MED] = rel_fcst_med
                results[Constants.IND_REL_FCST_MIN] = rel_fcst_min
                results[Constants.IND_REL_FCST_MAX] = rel_fcst_max
                results[Constants.IND_REL_FCST_PREV_PERCENT] = rel_fcst_percent
                results[Constants.WEEK_DIR] = week_dir
                results[Constants.WEEK_MIN_DIR] = week_min_dir
                results[Constants.WEEK_MAX_DIR] = week_max_dir
                results[Constants.WEEK_DIR_FLOW_PREV] = week_dir_flow_prev
                results[Constants.ANGLE_IMA1_PREV] = angle_ima
                results[Constants.ANGLE_IMA1_COUNTER] = angle_ima_counter
                # results[Constants.ANGLE] = angle
                results[Constants.ANGLE_PREV] = angle
                results[Constants.ANGLE_COUNTER] = angle_counter

                # CLOSE NXT VALUES
                results[Constants.CLOSE_NXT_UP] = close_nxt_up
                results[Constants.CLOSE_NXT_DOWN] = close_nxt_down
                results[Constants.CLOSE_NXT_MIDDLE] = close_nxt_middle

                results[Constants.START_ACTION_VAL] = float(act_val)
                if act == Constants.ACTION_BUY or act == Constants.ACTION_SELL or act == Constants.ACTION_WAIT or Constants.ACTION_CLOSE in act:

                    # print(f" MIN DIR antiguo ES {min_dir} MAX_DIR es {max_dir} direction {direction} tendence {tendence}")

                    if float(min_dir) >= 99999:
                        min_dir = currentValue
                        max_dir = currentValue
                    if direction is None or direction == Constants.DIR_WAIT:

                        if flujo == Constants.FLUJO_SUBE:
                            direction = Constants.DIR_UP
                        elif flujo == Constants.FLUJO_BAJA:
                            direction = Constants.DIR_DOWN

                    # CAMBIO DE DIRECCION
                    if tendence != flujo:
                        if flujo == Constants.FLUJO_SUBE:
                            if changePoint:
                                min_dir = changePoint
                            else:
                                min_dir = min_dir
                        elif flujo == Constants.FLUJO_BAJA:
                            if changePoint:
                                max_dir = changePoint
                            else:
                                max_dir = max_dir

                    # print(f"NUEVOS MIN {min_dir} MAX  {max_dir}")
                    if currentValue < float(min_dir):
                        min_dir = currentValue
                        if direction == Constants.DIR_UP:
                            direction = Constants.DIR_CHANGE
                        elif direction == Constants.DIR_DOWN:
                            direction = Constants.DIR_DOWN
                        elif direction == Constants.DIR_CHANGE:
                            direction = Constants.DIR_PRE_DOWN
                        elif direction == Constants.DIR_PRE_DOWN:
                            direction = Constants.DIR_DOWN
                        elif direction == Constants.DIR_PRE_UP:
                            direction = Constants.DIR_CHANGE

                    if currentValue > float(max_dir):
                        max_dir = currentValue
                        if direction == Constants.DIR_UP:
                            direction = Constants.DIR_UP
                        elif direction == Constants.DIR_DOWN:
                            direction = Constants.DIR_CHANGE
                        elif direction == Constants.DIR_CHANGE:
                            direction = Constants.DIR_PRE_UP
                        elif direction == Constants.DIR_PRE_DOWN:
                            direction = Constants.DIR_CHANGE
                        elif direction == Constants.DIR_PRE_UP:
                            direction = Constants.DIR_UP

                    # determinar minimos y maximos
                    if currentValue < float(min):
                        if currentValue == 0:
                            nada = ""
                            # print(f"CURRENT VALUE 0")
                        else:
                            min = currentValue
                    if currentValue > float(max):
                        max = currentValue

                    action_min_dist = abs(float(currentValue) - float(min))
                    action_max_dist = abs(float(currentValue) - float(max))

                    # print(f"INDICATOR DIRECTION : {results[Constants.DATE].values[0]} {direction} value {results[Constants.VALUE]} min_dir {min_dir} max_dir {max_dir}")

                    results[Constants.ACTION_MIN] = min
                    results[Constants.ACTION_MIN_DIST] = action_min_dist
                    results[Constants.ACTION_MAX] = max
                    results[Constants.ACTION_MAX_DIST] = action_max_dist
                    results[Constants.DIRECTION] = direction
                    results[Constants.MIN_DIR] = min_dir
                    results[Constants.MAX_DIR] = max_dir
                    results[Constants.INDI_DIR] = indi_dir

            if results[Constants.START_ACTION_VAL] != 0:
                action_distance = float(results[Constants.VALUE]) - float(results[Constants.START_ACTION_VAL])
            results[Constants.ACTION_DISTANCE] = action_distance

            previousValue = results[Constants.START_ACTION_VAL]
            if previousValue is None:
                previousValue = 0
            previusDistance = currentValue - float(previousValue)

            results[Constants.PREVIOUS_DIST] = previusDistance

            results[Constants.FLUJO] = flujo
            results[Constants.FLUJO_COUNT] = flujo_count
            results[Constants.ACUMULADO] = acumulado
            results[Constants.ACUMULADO_ABS] = abs(acumulado)
            results[Constants.RELATIVE_MIN] = RELATIVE_min
            results[Constants.RELATIVE_PREV_MIN] = RELATIVE_prev_min
            results[Constants.RELATIVE_MAX] = RELATIVE_max
            results[Constants.RELATIVE_PREV_MAX] = RELATIVE_prev_max

            # CALCULATE BOLLINGER
            closenxtdown = results[Constants.CLOSE_NXT_DOWN]
            if closenxtdown == 0:
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] != 0 and results[
                    Constants.IND_BLG_UPPER_DST_PERCENT] <= active.parameters.bollingerDst:
                    results[Constants.CLOSE_NXT_DOWN] = 1

            if results[Constants.IND_BLG_LOWER_DST_PERCENT] != 0 and results[
                Constants.IND_BLG_LOWER_DST_PERCENT] <= active.parameters.bollingerDst:
                results[Constants.CLOSE_NXT_UP] = 1

            self.calculateRelativeValuesFIXED2(results, active)
            #calcular flowdiff
            flowDiff = self.getflowDiff(data,active)
            results[Constants.FLOW_DIFF] = flowDiff


    def calculateRelativeValuesFIXED2(self, results, active):

        # preparacion relative
        self.prepareRelative(results)

        relativeDistance = active.parameters.relativeDistance
        relativeDistanceMid = relativeDistance / 2

        relativeMinAction = relativeDistance * active.parameters.relativeDistanceMultiplicator
        relativeMinActionMid = relativeMinAction / 2

        currentValue = results[Constants.VALUE]
        currentDate = results[Constants.DATE].values[0]

        relative_min = results[Constants.RELATIVE_MIN]
        relative_prev_min = results[Constants.RELATIVE_PREV_MIN]
        relative_prev_min_dist = results[Constants.RELATIVE_PREV_MIN_DIST]
        relative_min_dist = results[Constants.RELATIVE_MIN_DIST]
        relative_max = results[Constants.RELATIVE_MAX]
        relative_prev_max = results[Constants.RELATIVE_PREV_MAX]
        relative_prev_max_dist = results[Constants.RELATIVE_PREV_MAX_DIST]
        relative_max_dist = results[Constants.RELATIVE_MAX_DIST]
        max_relative_dist = active.parameters.relativeDistance

        relativeMinABSValue = abs(relative_min_dist)
        relativeMaxABSValue = abs(relative_max_dist)
        relativePREVMinABSValue = abs(relative_prev_min_dist)
        relativePREVMaxABSValue = abs(relative_prev_max_dist)

        # solo si tiene valores previos
        if relativePREVMinABSValue < 9999:
            absDifference = abs(relative_prev_max - relative_prev_min)
            if absDifference > relativeDistance:
                relativeDistance = relativeDistance + relativeDistanceMid
                if absDifference > relativeDistance:
                    # aun hay mucha diferencia
                    relativeDistance = absDifference + (absDifference / 3)

                relativeMinAction = relativeDistance * active.parameters.relativeDistanceMultiplicator
                # relativeDistance = absDifference
                # relativeMinAction = relativeDistance * active.parameters.relativeDistanceMultiplicator

        directionMEDST = None
        if results[Constants.INDICATOR_MED_MOMENT] == Constants.INDICATOR_TM_UP:
            directionMEDST = Constants.FLUJO_SUBE
        elif results[Constants.INDICATOR_MED_MOMENT] == Constants.INDICATOR_TM_DOWN:
            directionMEDST = Constants.FLUJO_BAJA
        elif results[Constants.INDICATOR_MED_MOMENT] == Constants.INDICATOR_TM_UNDEF:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                directionMEDST = Constants.FLUJO_SUBE
            elif results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                directionMEDST = Constants.FLUJO_BAJA
        if relativePREVMinABSValue < 9999:
            if relative_prev_min_dist > relative_prev_max_dist:
                # SUBE
                # verificar si hay un valor bueno para apertura
                if relativePREVMinABSValue >= relativeMinAction:
                    if relativePREVMinABSValue <= relativeDistance:  # comprobar el valor llega al maximo para cambio
                        if relativePREVMinABSValue + relativeMinAction < relativeDistance:
                            # aun dentro del rango
                            if directionMEDST:
                                if directionMEDST == Constants.FLUJO_SUBE:
                                    results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP
                                else:
                                    results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN
                            else:
                                results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP
                        else:
                            results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP_CHANGE

                    else:
                        # # fix para verificar si sobrepaso y aun es DOWN
                        # if (relativePREVMinABSValue > relativeDistance + relativeMinActionMid):
                        #     results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP
                        # else:
                        if relativePREVMaxABSValue == 0:  # aun esta subiendo
                            if directionMEDST:
                                if directionMEDST == Constants.FLUJO_SUBE:
                                    results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP
                                else:
                                    results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN
                            else:
                                results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP

                        else:
                            results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP_CHANGE

                else:
                    results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP
            elif relative_prev_min_dist < relative_prev_max_dist:
                # BAJA
                # verificar si hay un valor bueno para apertura
                if relativePREVMaxABSValue >= relativeMinAction:
                    if relativePREVMaxABSValue <= relativeDistance:  # comprobar el valor llega al maximo para cambio
                        if relativePREVMaxABSValue + relativeMinAction < relativeDistance:
                            # aun dentro del rango

                            if directionMEDST:
                                if directionMEDST == Constants.FLUJO_SUBE:
                                    results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP
                                else:
                                    results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN
                            else:
                                results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN
                        else:
                            results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN_CHANGE
                    else:
                        # #fix para verificar si sobrepaso y aun es DOWN
                        # if relativePREVMaxABSValue >=(relativeDistance+relativeMinActionMid):
                        #     results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN
                        # else:
                        if relativePREVMinABSValue == 0:  # aun esta subiendo
                            if directionMEDST:
                                if directionMEDST == Constants.FLUJO_SUBE:
                                    results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP
                                else:
                                    results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN
                            else:
                                results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN
                        else:
                            results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN_CHANGE
                else:

                    results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN
            else:
                results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_WAIT
        # valores relativos para el dia
        else:
            if relative_min_dist > relative_max_dist:
                # SUBE
                # verificar si hay un valor bueno para apertura
                if relativeMinABSValue >= relativeMinAction:
                    if relativeMinABSValue <= relativeDistance:  # verifica si paso el rango maximo de cambio
                        if relativeMinABSValue + relativeMinAction < relativeDistance:
                            # aun dentro del rango
                            if directionMEDST:
                                if directionMEDST == Constants.FLUJO_SUBE:
                                    results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP
                                else:
                                    results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN
                            else:
                                results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP
                        else:
                            results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP_CHANGE
                    else:
                        if relativePREVMaxABSValue == 0:  # aun esta subiendo
                            if directionMEDST:
                                if directionMEDST == Constants.FLUJO_SUBE:
                                    results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP
                                else:
                                    results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN
                            else:
                                results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP

                        else:
                            results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP_CHANGE

                else:
                    # fix para evitar valores incorrectos si min y max estan cerca
                    # cntrol por si no hay mucha diferencia entre min y max puede dar informacion incorrecta
                    relativeABSDiff = abs(relativeMaxABSValue - relativeMinABSValue)
                    if relativeABSDiff < (relativeDistance / 2):
                        # el cambio es muy pequeno es informacion incorrecta
                        if relativeMinABSValue == 0:
                            # esta en subida
                            if directionMEDST:
                                if directionMEDST == Constants.FLUJO_SUBE:
                                    results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP
                                else:
                                    results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN
                            else:
                                results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP
                        else:
                            results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP_CHANGE
                    else:
                        if directionMEDST:
                            if directionMEDST == Constants.FLUJO_SUBE:
                                results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP
                            else:
                                results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN
                        else:
                            results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP
            elif relative_min_dist < relative_max_dist:
                # BAJA
                # verificar si hay un valor bueno para apertura
                if relativeMaxABSValue >= relativeMinAction:
                    if relativeMaxABSValue <= relativeDistance:  # verifica si paso el rango maximo de cambio
                        if relativeMaxABSValue + relativeMinAction < relativeDistance:
                            # aun dentro del rango
                            if directionMEDST:
                                if directionMEDST == Constants.FLUJO_SUBE:
                                    results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP
                                else:
                                    results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN
                            else:
                                results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN
                        else:
                            results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN_CHANGE
                    else:
                        if relativePREVMinABSValue == 0:  # aun esta subiendo
                            if directionMEDST:
                                if directionMEDST == Constants.FLUJO_SUBE:
                                    results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP
                                else:
                                    results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN
                            else:
                                results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN

                        else:
                            results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN_CHANGE

                else:
                    nada = ""
                    # fix para evitar valores incorrectos si min y max estan cerca
                    # cntrol por si no hay mucha diferencia entre min y max puede dar informacion incorrecta
                    relativeABSDiff = abs(relativeMaxABSValue - relativeMinABSValue)
                    if relativeABSDiff < (relativeDistance / 3):
                        # el cambio es muy pequeno es informacion incorrecta
                        if relativeMinABSValue == 0:
                            # esta en bajada
                            if directionMEDST:
                                if directionMEDST == Constants.FLUJO_SUBE:
                                    results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP
                                else:
                                    results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN
                            else:
                                results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN
                        else:
                            results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN_CHANGE
                    else:
                        if directionMEDST:
                            if directionMEDST == Constants.FLUJO_SUBE:
                                results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP
                            else:
                                results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN
                        else:
                            results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN
            else:
                results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_WAIT
        # if active.parameters.relativeDistance >
        if self.simulation:
            if self.needAnalsis:
                nada =""
                # print(
                #     f"RELATIVE VALUES RELATIVE {results[Constants.DATE].values[0]} {results[Constants.RELATIVE]} relMinDist {relative_min_dist} relMaxDist {relative_max_dist} relmin {relative_min} relMax {relative_max} relPrevMInDist {relative_prev_min_dist} relPrevMaxDist {relative_prev_max_dist} relPrevMin {relative_prev_min} relPrevMax {relative_prev_max} MINACTION {relativeMinAction} DISTANCE {(relativeDistance)} ")
                # print(
                #     f"INDICATOR MEDSTDF VALUES {results[Constants.DATE].values[0]} {results[Constants.INDICATOR_MED_STD]} MEDIA {results[Constants.MEDIA]} STD {results[Constants.STDDESV]} : {results[Constants.INDICATOR_MED]} : {results[Constants.INDICATOR_STD]} minSTD {active.parameters.minSTDNormal} minMED {active.parameters.minMEDNormal}")
                # print(
                #     f"RELATIVE VALUES CSV {results[Constants.RELATIVE]}, {relative_min_dist}, {relative_max_dist} , {relative_prev_min_dist} , {relative_prev_max_dist}, {relativeMinAction}, {(relativeDistance - relativeMinAction)}, {results[Constants.DATE]}")

    def get3daysValue(self, results, active):
        min3Days = None
        max3Days = None
        # recuperar el valor min max hace 3 dias

        currentValue = results[Constants.VALUE]
        currentDate = results[Constants.DATE].values[0]

        try:
            minmaxValues = self.dataBDMan.getMinMaxFor3days(active.parameters.name, currentDate)
            if minmaxValues is not None:

                min3Days = minmaxValues['global_min'][0]
                if min3Days:
                    min3Days = float(min3Days)
                else:
                    min3Days = None

                max3Days = minmaxValues['global_max'][0]
                if max3Days:
                    max3Days = float(max3Days)
                else:
                    max3Days = None

        except Exception as e:
            print(f"ERROR ereview_results oldDBvalue {str(e)}")
            self.log.error(f"Error {str(e)}")
        return min3Days, max3Days

    def prepareRelative(self, results):
        # #calcular el valor min y max para RELATIVE
        currentTime = self.gettime(results)
        currentValue = float(results[Constants.VALUE])
        RELATIVE_max = results[Constants.RELATIVE_MAX]
        RELATIVE_min = results[Constants.RELATIVE_MIN]
        RELATIVE_prev_min = results[Constants.RELATIVE_PREV_MIN]
        RELATIVE_prev_max = results[Constants.RELATIVE_PREV_MAX]

        if currentTime and currentTime >= int(self.prepRelStart) and currentTime <= int(self.prepRelEnd):
            if RELATIVE_min != RELATIVE_max:
                RELATIVE_prev_max = RELATIVE_max
                RELATIVE_prev_min = RELATIVE_min

                RELATIVE_min = float(99999)
                RELATIVE_max = float(0)

        # print(f"evaluara relative_min {RELATIVE_min}")
        if currentValue < RELATIVE_min:
            RELATIVE_min = currentValue

        if currentValue > RELATIVE_max:
            RELATIVE_max = currentValue

        RELATIVE_min_dist = currentValue - RELATIVE_min
        RELATIVE_max_dist = RELATIVE_max - currentValue

        # update relative PREV with relative values

        if abs(RELATIVE_prev_min) < 9999:
            if RELATIVE_min < RELATIVE_prev_min:
                RELATIVE_prev_min = RELATIVE_min

            if RELATIVE_max > RELATIVE_prev_max:
                RELATIVE_prev_max = RELATIVE_max

        RELATIVE_prev_min_dist = currentValue - RELATIVE_prev_min
        RELATIVE_prev_max_dist = RELATIVE_prev_max - currentValue

        results[Constants.RELATIVE_MAX] = RELATIVE_max
        results[Constants.RELATIVE_MIN] = RELATIVE_min
        results[Constants.RELATIVE_MIN_DIST] = RELATIVE_min_dist
        results[Constants.RELATIVE_MAX_DIST] = RELATIVE_max_dist
        results[Constants.RELATIVE_PREV_MIN_DIST] = RELATIVE_prev_min_dist
        results[Constants.RELATIVE_PREV_MIN] = RELATIVE_prev_min
        results[Constants.RELATIVE_PREV_MAX_DIST] = RELATIVE_prev_max_dist
        results[Constants.RELATIVE_PREV_MAX] = RELATIVE_prev_max

    def calculateRelativeValuesWith3days(self, results, active):

        # preparacion relative
        self.prepareRelative(results)

        # calculos relative
        relativeDistance = active.parameters.relativeDistance
        relativeDistanceMid = relativeDistance / 2
        relativeMinAction = relativeDistance * active.parameters.relativeDistanceMultiplicator

        currentValue = results[Constants.VALUE]
        currentDate = results[Constants.DATE].values[0]

        min3Days = None
        max3Days = None
        # recuperar el valor min max hace 3 dias
        try:
            minmaxValues = self.dataBDMan.getMinMaxFor3days(active.parameters.name, currentDate)
            if minmaxValues is not None:

                min3Days = minmaxValues['global_min'][0]
                if min3Days:
                    min3Days = float(min3Days)
                else:
                    min3Days = None

                max3Days = minmaxValues['global_max'][0]
                if max3Days:
                    max3Days = float(max3Days)
                else:
                    max3Days = None

        except Exception as e:
            print(f"ERROR ereview_results oldDBvalue {str(e)}")
            self.log.error(f"Error {str(e)}")

        relative_min = results[Constants.RELATIVE_MIN]
        relative_prev_min = results[Constants.RELATIVE_PREV_MIN]
        relative_prev_min_dist = results[Constants.RELATIVE_PREV_MIN_DIST]
        relative_min_dist = results[Constants.RELATIVE_MIN_DIST]
        relative_max = results[Constants.RELATIVE_MAX]
        relative_prev_max = results[Constants.RELATIVE_PREV_MAX]
        relative_prev_max_dist = results[Constants.RELATIVE_PREV_MAX_DIST]
        relative_max_dist = results[Constants.RELATIVE_MAX_DIST]
        max_relative_dist = active.parameters.relativeDistance

        relativeMinABSValue = abs(relative_min_dist)
        relativeMaxABSValue = abs(relative_max_dist)
        relativePREVMinABSValue = abs(relative_prev_min_dist)
        relativePREVMaxABSValue = abs(relative_prev_max_dist)

        if min3Days and max3Days:
            relative_prev_min_dist = currentValue - min3Days
            relative_prev_max_dist = max3Days - currentValue

            if relative_prev_min_dist > relative_prev_max_dist:
                # SUBE
                # verificar si hay un valor bueno para apertura
                if relativePREVMinABSValue >= relativeMinAction:
                    if relativePREVMinABSValue <= relativeDistance:  # comprobar el valor llega al maximo para cambio
                        # verificar si estamos iniciando o mas de la mitad
                        if relativePREVMaxABSValue >= relativeMinAction:
                            if relative_prev_max_dist < 0:  # comprobar si es negativo
                                results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP_CHANGE
                            else:
                                results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP
                        else:
                            # control por si esta subiendo
                            if relativePREVMaxABSValue >= (relativeMinAction / 2):
                                results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP_CHANGE
                            else:
                                estasbuiento = True  # es un comentario
                                results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP

                    else:
                        results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP_CHANGE
                else:
                    results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP
            elif relative_prev_min_dist < relative_prev_max_dist:
                # BAJA
                # verificar si hay un valor bueno para apertura
                if relativePREVMaxABSValue >= relativeMinAction:
                    if relativePREVMaxABSValue <= relativeDistance:  # comprobar el valor llega al maximo para cambio
                        if relativePREVMinABSValue >= relativeMinAction:
                            # if relative_prev_min_dist <0:#comprobar si es negativo
                            #     results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN_CHANGE
                            # else:
                            results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN
                        else:

                            # control por si esta subiendo
                            if relativePREVMinABSValue >= (relativeMinAction / 2):
                                results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN_CHANGE
                            else:
                                estasbuiento = True  # es un comentario
                                results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN
                    else:
                        results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN_CHANGE
                else:

                    results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN
            else:
                results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_WAIT
        # valores relativos para el dia
        else:
            if relative_min_dist > relative_max_dist:
                # SUBE
                # verificar si hay un valor bueno para apertura
                if relativeMinABSValue >= relativeMinAction:
                    if relativeMinABSValue <= relativeDistance:  # verifica si paso el rango maximo de cambio
                        # verificar si estamos iniciando o mas de la mitad
                        if relativeMaxABSValue >= relativeMinAction:
                            if relative_max_dist < 0:  # comprobar si es negativo
                                results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP_CHANGE
                            else:
                                results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP
                        else:
                            # cntrol por si no hay mucha diferencia entre min y max puede dar informacion incorrecta
                            relativeABSDiff = abs(relativeMaxABSValue - relativeMinABSValue)
                            if relativeABSDiff < (
                                    relativeDistance / 2):  # el cambio es muy pequeno es informacion incorrecta
                                # results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP_CHANGE
                                if relativeMinABSValue == 0:
                                    # esta en subida
                                    results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP
                                else:
                                    results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP_CHANGE
                            else:
                                # control por si esta subiendo
                                if relativeMaxABSValue >= (relativeMinAction / 2):
                                    results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP_CHANGE
                                else:
                                    estasbuiento = True  # es un comentario
                                    results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP
                    else:
                        results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP_CHANGE
                else:
                    # fix para evitar valores incorrectos si min y max estan cerca
                    # cntrol por si no hay mucha diferencia entre min y max puede dar informacion incorrecta
                    relativeABSDiff = abs(relativeMaxABSValue - relativeMinABSValue)
                    if relativeABSDiff < (relativeDistance / 2):
                        # el cambio es muy pequeno es informacion incorrecta
                        if relativeMinABSValue == 0:
                            # esta en subida
                            results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP
                        else:
                            results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP_CHANGE
                    else:
                        results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_UP
            elif relative_min_dist < relative_max_dist:
                # BAJA
                # verificar si hay un valor bueno para apertura
                if relativeMaxABSValue >= relativeMinAction:
                    if relativeMaxABSValue <= relativeDistance:  # verifica si paso el rango maximo de cambio
                        if relativeMinABSValue >= relativeMinAction:
                            if relative_min_dist < 0:
                                results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN_CHANGE
                            else:
                                results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN
                        else:
                            relativeABSDiff = abs(relativeMaxABSValue - relativeMinABSValue)
                            if relativeABSDiff < (
                                    relativeDistance / 2):  # el cambio es muy pequeno es informacion incorrecta
                                # results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN_CHANGE
                                if relativeMinABSValue == 0:
                                    # esta en bajada
                                    results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN
                                else:
                                    results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN_CHANGE
                            else:
                                # control por si esta bajando
                                if relativeMaxABSValue >= (relativeMinAction / 2):
                                    results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN_CHANGE
                                else:
                                    estasbuiento = True  # es un comentario
                                    results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN
                    else:
                        results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN_CHANGE

                else:
                    # fix para evitar valores incorrectos si min y max estan cerca
                    # cntrol por si no hay mucha diferencia entre min y max puede dar informacion incorrecta
                    relativeABSDiff = abs(relativeMaxABSValue - relativeMinABSValue)
                    if relativeABSDiff < (relativeDistance / 2):
                        # el cambio es muy pequeno es informacion incorrecta
                        if relativeMinABSValue == 0:
                            # esta en bajada
                            results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN
                        else:
                            results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN_CHANGE
                    else:
                        results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_DOWN
            else:
                results[Constants.RELATIVE] = Constants.INDICATOR_RELATIVE_WAIT

        # if active.parameters.relativeDistance >
        if self.simulation:
            print(
                f"RELATIVE VALUES RELATIVE {results[Constants.DATE].values[0]} {results[Constants.RELATIVE]} relMinDist {relative_min_dist} relMaxDist {relative_max_dist} relmin {relative_min} relMax {relative_max} relPrevMInDist {relative_prev_min_dist} relPrevMaxDist {relative_prev_max_dist} min3days {min3Days} max3days {max3Days} MINACTION {relativeMinAction} DISTANCE {(relativeDistance - relativeMinAction)} ")
            print(
                f"INDICATOR MEDSTDF VALUES {results[Constants.DATE].values[0]} {results[Constants.INDICATOR_MED_STD]} MEDIA {results[Constants.MEDIA]} STD {results[Constants.STDDESV]} : {results[Constants.INDICATOR_MED]} : {results[Constants.INDICATOR_STD]} minSTD {active.parameters.minSTDNormal} minMED {active.parameters.minMEDNormal}")
            print(
                f"RELATIVE VALUES CSV {results[Constants.RELATIVE]}, {relative_min_dist}, {relative_max_dist} , {relative_prev_min_dist} , {relative_prev_max_dist}, {relativeMinAction}, {(relativeDistance - relativeMinAction)}, {results[Constants.DATE]}")

    def gettime(self, results):
        currentTime = None
        try:
            import time
            from datetime import datetime

            if self.simulation:
                temp = results[Constants.DATE].values[0]
                t = datetime.strptime(temp, '%Y-%m-%d %H:%M:%S.%f')
                current_time_h = t.hour * 100
                current_time_min = t.minute
                # print(f" gettime hora : {current_time_h} minutos: {current_time_min}")
                currentTime = int(current_time_h + current_time_min)
            else:
                t = time.localtime()
                current_time_h = time.strftime("%H", t)
                current_time_min = time.strftime("%M", t)
                # print(f" gettime hora sistema: {current_time_h} minutos: {current_time_min}")
                currentTime = int(current_time_h + current_time_min)
        except Exception as e:
            nada = ""
            # print(f"ERROR determinar_flujo {str(e)}")

        # print(f"current time es : {currentTime}")
        return currentTime

    def getInterval(self, results):
        interval = []
        currentTime = None
        try:
            import time
            from datetime import datetime
            interval5Min = 5
            interval10Min = 10
            interval15Min = 15
            interval20Min = 20
            interval30Min = 30
            interval60Min = 60
            isHour = False
            if self.simulation:
                temp = results[Constants.DATE].values[0]
                t = datetime.strptime(temp, '%Y-%m-%d %H:%M:%S.%f')
                current_time_h = t.hour * 100
                current_time_min = t.minute
                # print(f" gettime hora : {current_time_h} minutos: {current_time_min}")
                currentTime = int(current_time_h + current_time_min)
            else:
                t = time.localtime()
                current_time_h = time.strftime("%H", t)
                current_time_min = time.strftime("%M", t)
                if current_time_min ==0:
                    isHour = True
                currentTime = int(current_time_min)
                print(f"getInterval current time hour: {current_time_h} minutes :{current_time_min}")

                if currentTime % interval5Min == 0:
                    interval.append(interval5Min)
                    print(f"getInterval match 5 min")
                if currentTime % interval10Min == 0:
                    interval.append(interval10Min)
                    print(f"getInterval match 10 min")
                if currentTime % interval15Min == 0:
                    interval.append(interval15Min)
                    print(f"getInterval match 15 min")
                if currentTime % interval15Min == 0:
                    interval.append(interval15Min)
                    print(f"getInterval match 15 min")

                if currentTime % interval20Min == 0:
                    interval.append(interval20Min)
                    print(f"getInterval match {interval20Min} min")

                if currentTime % interval30Min == 0:
                    interval.append(interval30Min)
                    print(f"getInterval match {interval30Min} min")

                if isHour:
                    interval.append(interval60Min)
                    print(f"getInterval match {interval60Min} min")

                print(f"getInterval interval is: {interval}")

        except Exception as e:
            nada = ""
            # print(f"ERROR determinar_flujo {str(e)}")

        return interval

    def updateMinMaxValues(self, results):
        currentValue = results[Constants.VALUE]
        results[Constants.ACTION_MIN] = currentValue
        results[Constants.ACTION_MIN_DIST] = 0
        results[Constants.ACTION_MAX] = currentValue
        results[Constants.ACTION_MAX_DIST] = 0
        results[Constants.ACTION_COUNT] = 0
        if results[Constants.CHANGE_ACTION] == 1:
            results[Constants.ACTION_ACUM] = 0

    def processAlerts(self, alert, results, active):
        if alert:
            message = f'\n\nMARKETMANAGER {self.name}  \n' \
                      f'ACTIVO {results[Constants.NAME]} \n VALOR: <b>{round(float(results[Constants.VALUE]), active.parameters.round)}</b> \n' \
                      f'ACTION : <b>{results[Constants.CURRENT_ACTION]} </b>  \n' \
                      f'EVAl_NAME : <b>{results[Constants.EVAl_NAME]} </b>  \n' \
                      f'ACUMULADO: {results[Constants.ACUMULADO]} \n' \
                      f'FLUJO: {results[Constants.FLUJO]} \n' \
                      f'FLUJO_COUNT: {results[Constants.FLUJO_COUNT]} \n' \
                      f'MARKET_TENDENCE: {results[Constants.MARKET_TENDENCE]} \n' \
                      f'INDICATOR_EMA: {results[Constants.INDICATOR_EMA]} \n' \
                      f'ANGLE_FLOW: {results[Constants.ANGLE_FLOW]} \n' \
                      f'IMA1EMADIFF: {results[Constants.IMA1EMADIFF]} \n' \
                      f'WEEK_DIR_BOT_DST_NEW: {results[Constants.WEEK_DIR_BOT_DST_NEW]} \n' \
                      f'WEEK_DIR_BOT_DST_MED_NEW: {results[Constants.WEEK_DIR_BOT_DST_MED_NEW]} \n' \
                      f'MONTH_DIR_BOT_DST: {results[Constants.MONTH_DIR_BOT_DST]} \n' \
                      f'MONTH_DIR_BOT_DST_MED: {results[Constants.MONTH_DIR_BOT_DST_MED]} \n' \
                      f'IND_BLG: {results[Constants.IND_BLG]} \n' \
                      f'BLG_MA_X: {results[Constants.BLG_MA_X]} \n' \
                      f'MIN_DIR: {results[Constants.MIN_DIR]} \n' \
                      f'MAX_DIR: {results[Constants.MAX_DIR]} \n' \
                      f'ANGLE: {results[Constants.ANGLE]} \n' \
                      f'ANGLEm1: {results[Constants.ANGLEm1]} \n' \
                      f'ANGLE_EMA: {results[Constants.ANGLE_EMA]} \n' \
                      f'ANGLE_EMA20: {results[Constants.ANGLE_EMA20]} \n' \
                      f'IND_PROB_FLOW: {results[Constants.IND_PROB_FLOW]} \n'
            if Constants.ACTION_CLOSE in results[Constants.CURRENT_ACTION]:
                    message = message +f'ACTION_ACUM: {results[Constants.ACTION_ACUM]} \n ' \
                                       f'ACTION_COUNT: {results[Constants.ACTION_COUNT]}'


            print(f' SEND MESSAGE Valor '
                  f'ACTIVO : {active.parameters.name} Valor: {results[Constants.VALUE]} '
                  f'Acumulado: {results[Constants.ACUMULADO]} '
                  f'INDICADOR: {results[Constants.IMA5MA20]} '
                  f'Tendencia: {results[Constants.FLUJO]} '
                  f'tendencia count: {results[Constants.FLUJO_COUNT]}'
                  f'DATE: {results[Constants.DATE].values[0]}'

                  )

            if self.simulation is False:
                self.telegram.enviarMensaje(message, self.telegram.tokenBot, active.parameters.tele_group)
                if results[Constants.MESSAGES] and len(results[Constants.MESSAGES]) > 0:
                    messages = results[Constants.MESSAGES]
                    self.telegram.enviarMensaje(messages, self.telegram.tokenBot, active.parameters.tele_group)
                    results[Constants.MESSAGES] = ""

        else:
            print("No envio mensaje")
            # update config

    def updateConfig(self, active, results):
        # print("guardando config")
        edit = self.config_obj[active.parameters.name]
        edit['action'] = str(results[Constants.CURRENT_ACTION])
        edit['action_count'] = str(results[Constants.ACTION_COUNT] + 1)
        edit['action_acum'] = str(float(results[Constants.ACTION_ACUM]))
        edit['value'] = str(results[Constants.VALUE])
        # if Constants.ACTION_MIN in results:
        #     edit['min'] = str(results[Constants.ACTION_MIN])
        # if Constants.ACTION_MAX in results:
        #     edit['max'] = str(results[Constants.ACTION_MAX])
        edit['min'] = str(results.get(Constants.ACTION_MIN, "0"))
        edit['max'] = str(results.get(Constants.ACTION_MAX, "0"))
        edit['direction'] = str(results.get(Constants.DIRECTION, ""))
        edit['min_dir'] = str(results.get(Constants.MIN_DIR, ""))
        edit['max_dir'] = str(results.get(Constants.MAX_DIR, ""))
        edit['flujo'] = str(results.get(Constants.FLUJO, ""))
        edit['RELATIVE_min'] = str(results.get(Constants.RELATIVE_MIN, ""))
        edit['RELATIVE_prev_min'] = str(results.get(Constants.RELATIVE_PREV_MIN, ""))
        edit['RELATIVE_max'] = str(results.get(Constants.RELATIVE_MAX, ""))
        edit['RELATIVE_prev_max'] = str(results.get(Constants.RELATIVE_PREV_MAX, ""))
        edit['week_flow'] = str(results.get(Constants.WEEK_FLOW, ""))
        edit['week_dir'] = str(results.get(Constants.WEEK_DIR, ""))
        edit['week_dir_flow'] = str(results.get(Constants.WEEK_DIR_FLOW_PREV, ""))
        edit['week_min_dir'] = str(results.get(Constants.WEEK_MIN_DIR, ""))
        edit['week_max_dir'] = str(results.get(Constants.WEEK_MAX_DIR, ""))
        edit['week_flow_std'] = str(results.get(Constants.WEEK_FLOW_STD, ""))
        edit['week_flow_med'] = str(results.get(Constants.WEEK_FLOW_MED, ""))
        edit['rel_fcst'] = str(results.get(Constants.IND_REL_FCST, ""))
        edit['rel_fcst_std'] = str(results.get(Constants.IND_REL_FCST_STD, ""))
        edit['rel_fcst_med'] = str(results.get(Constants.IND_REL_FCST_MED, ""))
        edit['rel_fcst_min'] = str(results.get(Constants.IND_REL_FCST_MIN, ""))
        edit['rel_fcst_max'] = str(results.get(Constants.IND_REL_FCST_MAX, ""))
        edit['rel_fcst_percent'] = str(results.get(Constants.IND_REL_FCST_PERCENT, ""))
        edit['close_nxt_up'] = str(results.get(Constants.CLOSE_NXT_UP, ""))
        edit['close_nxt_down'] = str(results.get(Constants.CLOSE_NXT_DOWN, ""))
        edit['angle_ima'] = str(results.get(Constants.ANGLE_IMA1, ""))
        edit['angle_ima_counter'] = str(results.get(Constants.ANGLE_IMA1_COUNTER, ""))
        edit['angle'] = str(results.get(Constants.ANGLE, ""))
        edit['angle_counter'] = str(results.get(Constants.ANGLE_COUNTER, ""))
        edit['close_nxt_middle'] = str(results.get(Constants.CLOSE_NXT_MIDDLE, ""))

        edit['minweek'] = str(results[Constants.MIN_WEEK])
        edit['maxweek'] = str(results[Constants.MAX_WEEK])
        edit['minmonth'] = str(results[Constants.MIN_MONTH])
        edit['maxmonth'] = str(results[Constants.MAX_MONTH])
        with open(self.configPath, 'w') as configfile:
            self.config_obj.write(configfile)

    def printValues(self, results):
        print(f' IMPRIMIR Valor '
              f'ACTIVO : {results[Constants.NAME]} Valor: {results[Constants.VALUE]} '
              f'Acumulado: {results[Constants.ACUMULADO]} '
              f'Tendencia: {results[Constants.FLUJO]} '
              f'INDICADOR: {results[Constants.INDICATOR]} '
              f'ACTION_DISTANCE: {results[Constants.ACTION_DISTANCE]} '
              f'tendencia count: {results[Constants.FLUJO_COUNT]}'
              f'DATE: {results[Constants.DATE].values[0]}')

    def determinar_flujo(self, data):
        res = 'MANTIENE'
        try:
            algo = ""
            if data is not None:
                current = data.iloc[[-1]]
                size = len(data)

                old = data.iloc[[- 2]]
                dif = float(current[self.closeValue].iloc[0]) - float(old[self.closeValue].iloc[0])
                if dif > 0:
                    res = "SUBE"
                elif dif < 0:
                    res = "BAJA"
                else:

                    res = old[Constants.FLUJO]
        except Exception as e:
            nada = ""
            # print(f"ERROR determinar_flujo {str(e)}")
        return res

    def getflowDiff(self, data, active):
        res = 0
        try:
            if data is not None:
                current = data.iloc[[-1]]
                size = len(data)
                interval = active.parameters.flowDiffInterval

                if(size)>interval:
                    old = data.iloc[[- interval]]


                res = float(current[self.closeValue].iloc[0]) - float(old[self.closeValue].iloc[0])

        except Exception as e:
            nada = ""
            # print(f"ERROR determinar_flujo {str(e)}")
        return res

    def determinar_flujo_WEEK(self, data):
        res = 'MANTIENE'
        value = 0
        try:
            algo = ""
            if data is not None and len(data) > 0:
                current = data.iloc[[-1]]
                size = len(data)

                old = data.iloc[[- 2]]
                dif = float(current.values[0]) - float(old.values[0])
                value = dif
                if dif > 0:
                    res = "SUBE"
                elif dif < 0:
                    res = "BAJA"
                else:
                    res = 'MANTIENE'
        except Exception as e:
            nada = ""
            # print(f"ERROR determinar_flujo {str(e)}")
        return res, value

    def determinarFlujoSTDMEDIA(self, maNEW, results, active):
        # DETERMINAMOS ANGULO DE TENDENCIA
        ma15Size = len(maNEW)
        elements_past = 120

        if ma15Size >= elements_past:

            # recorremos X elementos atras
            count = 0
            fin = False
            contador = len(maNEW) - 1
            posicion = elements_past
            valores = list()
            weekLevel = Constants.WEEK_FLOW_MED_LEVEL_UNDEF
            # currentDataValue = data.iloc[[contador]]
            valor = maNEW.iloc[[contador]].values[0]
            if pd.isna(valor) is True:
                valor = 0
            while fin != True:

                valorPre = maNEW.iloc[[contador - posicion]].values[0]

                if pd.isna(valorPre) is not True and valorPre is not None:
                    valores.append(valorPre)
                # else:
                #     valores.append(0)

                if posicion <= 0:
                    break
                else:
                    posicion = posicion - 1

            # calculamos el angulo
            cambios = [valores[-1] - valor for valor in valores]
            if self.simulation:
                nada = ""
                # print(f"valores determinarFlujoSTDMEDIA {valores}")
                # print(f"cambios determinarFlujoSTDMEDIA {cambios}")

            # ma_past = maNEW[-elements_past]
            ma_past = maNEW[ma15Size - elements_past]
            if len(valores) > 0:
                # Calcula la desviacion estandar
                desviacion_estandar = np.std(cambios)
                media = np.mean(cambios)
                marketAngle = media

                # marketAngle = maNEWValue - ma_past
                marketAngleAbs = abs(marketAngle)
                # print(f" fecha : {results[Constants.DATE]}")
                # print(f"ma15Value {maNEWValue}  ma_past {ma_past} cantidad {elements_past}")

                indicador_STD = Constants.INDICATOR_TSTD_MID

                if abs(marketAngle) <= active.parameters.weekDistanceMedDistance:
                    if media > 0:
                        if abs(media) > desviacion_estandar:
                            results[Constants.WEEK_FLOW] = Constants.WEEK_FLOW_UP
                        else:
                            results[Constants.WEEK_FLOW] = Constants.WEEK_FLOW_UP_LOW
                    elif media <= 0:
                        if abs(media) > desviacion_estandar:
                            results[Constants.WEEK_FLOW] = Constants.WEEK_FLOW_DOWN
                        else:
                            results[Constants.WEEK_FLOW] = Constants.WEEK_FLOW_DOWN_LOW

                    if abs(media) > active.parameters.weekMEDMinLevel:
                        results[Constants.WEEK_FLOW_MED_LEVEL] = Constants.WEEK_FLOW_MED_LEVEL_HIGH
                    elif abs(media) < active.parameters.weekMEDMinLevel:
                        results[Constants.WEEK_FLOW_MED_LEVEL] = Constants.WEEK_FLOW_MED_LEVEL_LOW
                    else:
                        results[Constants.WEEK_FLOW_MED_LEVEL] = Constants.WEEK_FLOW_MED_LEVEL_MID
                else:
                    # iniciamos con tendencia de indicadores
                    results[Constants.WEEK_FLOW] = Constants.WEEK_FLOW_UNDEF
                    results[Constants.WEEK_FLOW_MED_LEVEL] = Constants.WEEK_FLOW_MED_LEVEL_UNDEF

                results[Constants.WEEK_FLOW_ABSVAL] = desviacion_estandar
                results[Constants.WEEK_FLOW_MED] = media

                # print(
                # f" WEEK media:  {marketAngle} desviacion {desviacion_estandar} fecha {results[Constants.DATE]} WEEK_FLOW {results[Constants.WEEK_FLOW]} level {results[Constants.WEEK_FLOW_MED_LEVEL]}")

            else:
                # iniciamos con tendencia de indicadores
                results[Constants.WEEK_FLOW] = Constants.WEEK_FLOW_UNDEF
                results[Constants.WEEK_FLOW_ABSVAL] = 0
                results[Constants.WEEK_FLOW_MED] = 0
                results[Constants.WEEK_FLOW_MED_LEVEL] = Constants.WEEK_FLOW_MED_LEVEL_UNDEF

        else:
            results[Constants.WEEK_FLOW] = Constants.WEEK_FLOW_UNDEF
            results[Constants.WEEK_FLOW_ABSVAL] = 0
            results[Constants.WEEK_FLOW_MED] = 0
            results[Constants.WEEK_FLOW_MED_LEVEL] = Constants.WEEK_FLOW_MED_LEVEL_UNDEF

    def determinarFlujoSTDMEDIAWEEK(self, data, results, active):
        # DETERMINAMOS ANGULO DE TENDENCIA

        weekdays= active.parameters.weekInterval

        maNEW = data[self.closeValue].rolling(weekdays).mean()

        # Calcular la media móvil de x días
        maNEW_MED = data[self.closeValue].rolling(window=weekdays).mean()
        currentValue = results[Constants.VALUE]
        # Calcular la desviación estándar de x días
        maNEW_STD = data[self.closeValue].rolling(window=weekdays).std()
        # if pd.isna(maNEW_MED) is not True:
        #     print(f" WEEEK MED : {maNEW_MED.values[-1]} WEEEK MED dif : {maNEW_MED.values[-1]-currentValue} WEEK STD {maNEW_STD.values[-1]}")

        # maNEW = data[self.closeValue]
        ma15Size = len(maNEW)
        elements_past =30
        if pd.isna(maNEW) is not True:
            if ma15Size >= elements_past:

                # recorremos X elementos atras
                count = 0
                fin = False
                contador = len(maNEW) - 1
                posicion = elements_past
                valores = list()
                weekLevel = Constants.WEEK_FLOW_MED_LEVEL_UNDEF
                # currentDataValue = data.iloc[[contador]]
                valor = maNEW.iloc[[contador]].values[0]
                if pd.isna(valor) is True:
                    valor = 0
                while fin != True:

                    valorPre = maNEW.iloc[[contador - posicion]].values[0]

                    if pd.isna(valorPre) is not True and valorPre is not None:
                        valores.append(valorPre)
                    # else:
                    #     valores.append(0)

                    if posicion <= 1:
                        break
                    else:
                        posicion = posicion - 1

                # calculamos el angulo
                cambios = [valores[-1] - valor for valor in valores]
                if self.simulation:
                    nada = ""
                    # print(f"valores determinarFlujoSTDMEDIA {valores}")
                    # print(f"cambios determinarFlujoSTDMEDIA {cambios}")

                # ma_past = maNEW[-elements_past]
                # ma_past = maNEW[ma15Size - elements_past]
                if len(valores) > 0:
                    # Calcula la desviacion estandar
                    weekprev = Constants.WEEK_FLOW_UNDEF
                    if Constants.WEEK_FLOW in results:
                        weekprev = results[Constants.WEEK_FLOW]
                        weekprevMed = results[Constants.WEEK_FLOW_MED]
                        results[Constants.WEEK_FLOW_PREV] = weekprev
                        results[Constants.WEEK_FLOW_PREV_MED] = weekprevMed

                    angulo = np.arctan(valores[-1] - valores[0]) * (180 / np.pi)
                    # print(f"WEEK ANGLE: {angulo}")
                    desviacion_estandar = np.std(cambios)
                    media = np.mean(cambios)
                    marketAngle = media
                    # print(f" NEW WEEK_FLOW_STD: {desviacion_estandar} WEEK_FLOW_MED: {media}")


                    indicador_STD = Constants.INDICATOR_TSTD_MID

                    if media > 0:
                        results[Constants.WEEK_FLOW] = Constants.WEEK_FLOW_UP
                    elif media <= 0:
                        results[Constants.WEEK_FLOW] = Constants.WEEK_FLOW_DOWN

                    if abs(media) > desviacion_estandar:
                        results[Constants.WEEK_FLOW_MED_LEVEL] = Constants.WEEK_FLOW_MED_LEVEL_HIGH
                    else:
                        results[Constants.WEEK_FLOW_MED_LEVEL] = Constants.WEEK_FLOW_MED_LEVEL_LOW

                    results[Constants.WEEK_FLOW_STD] = float(desviacion_estandar)
                    results[Constants.WEEK_FLOW_MED] = float(media)

                    # print(
                    # f" WEEK media:  {marketAngle} desviacion {desviacion_estandar} fecha {results[Constants.DATE]} WEEK_FLOW {results[Constants.WEEK_FLOW]} level {results[Constants.WEEK_FLOW_MED_LEVEL]}")

                else:
                    # iniciamos con tendencia de indicadores
                    results[Constants.WEEK_FLOW] = Constants.WEEK_FLOW_UNDEF
                    results[Constants.WEEK_FLOW_PREV] = Constants.WEEK_FLOW_UNDEF
                    results[Constants.WEEK_FLOW_ABSVAL] = 0
                    results[Constants.WEEK_FLOW_MED] = 0
                    results[Constants.WEEK_FLOW_MED_LEVEL] = Constants.WEEK_FLOW_MED_LEVEL_UNDEF

            else:
                results[Constants.WEEK_FLOW] = Constants.WEEK_FLOW_UNDEF
                results[Constants.WEEK_FLOW_PREV] = Constants.WEEK_FLOW_UNDEF
                results[Constants.WEEK_FLOW_ABSVAL] = 0
                results[Constants.WEEK_FLOW_MED] = 0
                results[Constants.WEEK_FLOW_STD] = 0
                results[Constants.WEEK_FLOW_MED_LEVEL] = Constants.WEEK_FLOW_MED_LEVEL_UNDEF

        else:
            results[Constants.WEEK_FLOW] = Constants.WEEK_FLOW_UNDEF
            results[Constants.WEEK_FLOW_PREV] = Constants.WEEK_FLOW_UNDEF
            results[Constants.WEEK_FLOW_ABSVAL] = 0

    def determinarFlujoSTDMEDIAWEEK_HOURLY(self, data, results, active):
        # DETERMINAMOS ANGULO DE TENDENCIA

        weekdays= 5

        maNEW = data[self.closeValue].rolling(weekdays).mean()

        # Calcular la media móvil de x días
        maNEW_MED = data[self.closeValue].rolling(window=weekdays).mean()
        currentValue = results[Constants.VALUE]
        # Calcular la desviación estándar de x días
        maNEW_STD = data[self.closeValue].rolling(window=weekdays).std()
        # if pd.isna(maNEW_MED) is not True:
        #     print(f" WEEEK MED : {maNEW_MED.values[-1]} WEEEK MED dif : {maNEW_MED.values[-1]-currentValue} WEEK STD {maNEW_STD.values[-1]}")

        # maNEW = data[self.closeValue]
        ma15Size = len(maNEW)
        elements_past =10
        if pd.isna(maNEW) is not True:
            if ma15Size >= elements_past:

                # recorremos X elementos atras
                count = 0
                fin = False
                contador = len(maNEW) - 1
                posicion = elements_past
                valores = list()
                weekLevel = Constants.WEEK_FLOW_MED_LEVEL_UNDEF
                # currentDataValue = data.iloc[[contador]]
                valor = maNEW.iloc[[contador]].values[0]
                if pd.isna(valor) is True:
                    valor = 0
                while fin != True:

                    valorPre = maNEW.iloc[[contador - posicion]].values[0]

                    if pd.isna(valorPre) is not True and valorPre is not None:
                        valores.append(valorPre)
                    # else:
                    #     valores.append(0)

                    if posicion <= 1:
                        break
                    else:
                        posicion = posicion - 1

                # calculamos el angulo
                cambios = [valores[-1] - valor for valor in valores]
                if self.simulation:
                    nada = ""
                    # print(f"valores determinarFlujoSTDMEDIA {valores}")
                    # print(f"cambios determinarFlujoSTDMEDIA {cambios}")

                # ma_past = maNEW[-elements_past]
                ma_past = maNEW[ma15Size - elements_past]
                if len(valores) > 0:
                    # Calcula la desviacion estandar
                    weekprev = Constants.WEEK_FLOW_UNDEF
                    if Constants.WEEK_FLOW in results:
                        weekprev = results[Constants.WEEK_FLOW]
                        weekprevMed = results[Constants.WEEK_FLOW_MED]
                        results[Constants.WEEK_FLOW_PREV] = weekprev
                        results[Constants.WEEK_FLOW_PREV_MED] = weekprevMed

                    angulo = np.arctan(valores[-1] - valores[0]) * (180 / np.pi)
                    # print(f"WEEK ANGLE: {angulo}")
                    desviacion_estandar = np.std(cambios)
                    media = np.mean(cambios)
                    marketAngle = media
                    # print(f" NEW WEEK_FLOW_STD: {desviacion_estandar} WEEK_FLOW_MED: {media}")


                    indicador_STD = Constants.INDICATOR_TSTD_MID

                    if media > 0:
                        results[Constants.WEEK_FLOW] = Constants.WEEK_FLOW_UP
                    elif media <= 0:
                        results[Constants.WEEK_FLOW] = Constants.WEEK_FLOW_DOWN

                    if abs(media) > desviacion_estandar:
                        results[Constants.WEEK_FLOW_MED_LEVEL] = Constants.WEEK_FLOW_MED_LEVEL_HIGH
                    else:
                        results[Constants.WEEK_FLOW_MED_LEVEL] = Constants.WEEK_FLOW_MED_LEVEL_LOW

                    results[Constants.WEEK_FLOW_STD] = float(desviacion_estandar)
                    results[Constants.WEEK_FLOW_MED] = float(media)

                    # print(
                    # f" WEEK media:  {marketAngle} desviacion {desviacion_estandar} fecha {results[Constants.DATE]} WEEK_FLOW {results[Constants.WEEK_FLOW]} level {results[Constants.WEEK_FLOW_MED_LEVEL]}")

                else:
                    # iniciamos con tendencia de indicadores
                    results[Constants.WEEK_FLOW] = Constants.WEEK_FLOW_UNDEF
                    results[Constants.WEEK_FLOW_PREV] = Constants.WEEK_FLOW_UNDEF
                    results[Constants.WEEK_FLOW_ABSVAL] = 0
                    results[Constants.WEEK_FLOW_MED] = 0
                    results[Constants.WEEK_FLOW_MED_LEVEL] = Constants.WEEK_FLOW_MED_LEVEL_UNDEF

            else:
                results[Constants.WEEK_FLOW] = Constants.WEEK_FLOW_UNDEF
                results[Constants.WEEK_FLOW_PREV] = Constants.WEEK_FLOW_UNDEF
                results[Constants.WEEK_FLOW_ABSVAL] = 0
                results[Constants.WEEK_FLOW_MED] = 0
                results[Constants.WEEK_FLOW_STD] = 0
                results[Constants.WEEK_FLOW_MED_LEVEL] = Constants.WEEK_FLOW_MED_LEVEL_UNDEF

        else:
            results[Constants.WEEK_FLOW] = Constants.WEEK_FLOW_UNDEF
            results[Constants.WEEK_FLOW_PREV] = Constants.WEEK_FLOW_UNDEF
            results[Constants.WEEK_FLOW_ABSVAL] = 0




    def search_pricesYahoo(self, active):
        data = None
        try:
            nada = ""
            # data = yf.download(tickers=active.parameters.name, period='2d', interval='15m')

        except Exception as e:

            print(f"ERROR search_pricesYahoo {str(e)}")

        return data

    def search_pricesDB(self, active):

        data = None
        try:

            t = time.localtime()
            current_time_h = time.strftime("%H", t)
            current_time_min = time.strftime("%M", t)
            print(f" hora : {current_time_h} minutos: {current_time_min}")

            current_value, day_value = self.alpaca.getCurrentPrice(active.parameters.name)
            invested,profit, open, qty = self.alpaca.is_investedComplete(active.parameters.name)
            weekno = datetime.datetime.today().weekday()
            days = 4
            if weekno == 0 or weekno == 1:
                days = 6

            dif = 0
            acu = 0
            acumulate = 0
            tendence_acu = 0
            tendence_count = 0
            oldvalue = 0
            min_value = 999
            min_acu = 0
            max_value = 0
            max_acu = 0
            direction = Constants.DIR_WAIT
            min_dir = 99999
            max_dir = 0
            indi_dir = ''
            motion_min = 0
            motion_max = 0
            global_min = 0
            global_max = 0
            action_acum = 0
            week_flow = ''
            week_flow_med = 0
            week_flow_std = 0
            rel_fcst = ''
            rel_fcst_std = 0
            rel_fcst_med = 0
            rel_fcst_min = 0
            rel_fcst_max = 0
            action_count = 0
            rel_fcst_percent = 0
            close_nxt_up = 0
            close_nxt_down = 0
            close_nxt_middle = 0
            week_dir = Constants.DIR_WAIT
            week_min_dir = 99999
            week_max_dir = 0
            week_dir_flow = 0
            protect = 0
            revenue =  profit

            action = Constants.ACTION_WAIT
            oldDBvalue = self.dataBDMan.getLastValueWithName(active.parameters.name)
            if oldDBvalue is not None:
                oldvalue = oldDBvalue[0]["value"]

                acumulate = oldDBvalue[0]["acumulate"]
                tendence_acu = oldDBvalue[0]["tendence_acu"]
                tendence_count = oldDBvalue[0]["tendence_count"]
                min_value = oldDBvalue[0]["min_value"]
                min_acu = oldDBvalue[0]["min_acu"]
                max_value = oldDBvalue[0]["max_value"]
                max_acu = oldDBvalue[0]["max_acu"]
                action = oldDBvalue[0]["action"]
                if "CLOSE-SELL" in action:
                    action  = "SELL"
                if "CLOSE-BUY" in action:
                    action  = "BUY"
                if "CLOSE" in action:
                    if invested==True:
                        action = 'BUY'
                else:
                    nada = ""
                    # if invested==False:
                    #     action = 'CLOSE'



                action_count = oldDBvalue[0]["action_count"]
                direction = oldDBvalue[0]["direction"]
                min_dir = oldDBvalue[0]["min_dir"]
                max_dir = oldDBvalue[0]["max_dir"]
                indi_dir = oldDBvalue[0]["indi_dir"]
                motion_min = oldDBvalue[0]["motion_min"]
                motion_max = oldDBvalue[0]["motion_max"]
                global_min = oldDBvalue[0]["global_min"]
                global_max = oldDBvalue[0]["global_max"]
                action_acum = oldDBvalue[0]["action_acum"]
                week_flow = oldDBvalue[0]["week_flow"]
                week_flow_std = oldDBvalue[0]["week_flow_std"]
                week_flow_med = oldDBvalue[0]["week_flow_med"]
                rel_fcst = oldDBvalue[0]["rel_fcst"]
                rel_fcst_std = oldDBvalue[0]["rel_fcst_std"]
                rel_fcst_med = oldDBvalue[0]["rel_fcst_med"]
                rel_fcst_min = oldDBvalue[0]["rel_fcst_min"]
                rel_fcst_max = oldDBvalue[0]["rel_fcst_max"]
                rel_fcst_percent = oldDBvalue[0]["rel_fcst_percent"]
                close_nxt_up = oldDBvalue[0]["close_nxt_up"]
                close_nxt_down = oldDBvalue[0]["close_nxt_down"]
                close_nxt_middle = oldDBvalue[0]["close_nxt_middle"]
                week_dir = oldDBvalue[0]["week_dir"]
                week_min_dir = oldDBvalue[0]["week_min_dir"]
                week_max_dir = oldDBvalue[0]["week_max_dir"]
                week_dir_flow = oldDBvalue[0]["week_dir_flow"]
                angle_ima = oldDBvalue[0]["angle_ima"]
                angle_ima_counter = oldDBvalue[0]["angle_ima_counter"]
                angle = oldDBvalue[0]["angle"]
                angle_counter = oldDBvalue[0]["angle_counter"]

                month_dir_bot_dst = oldDBvalue[0]["month_dir_bot_dst"]
                week_dir_bot_dst = oldDBvalue[0]["week_dir_bot_dst"]
                week_dir_bot_dst_new = oldDBvalue[0]["week_dir_bot_dst_new"]
                protect = oldDBvalue[0]["protect"]
                if "CLOSE" == action:
                    protect = 0
                previous_entry_price = oldDBvalue[0]["openValue"]
                previous_qty = oldDBvalue[0]["qty"]
                # correccion estado por si cerro por stop loss o take profit
                if not invested and action != 'CLOSE':
                    action = 'CLOSE'
                    protect = 0
                    # Posición cerrada, calcular PnL
                    pnl, closed_price = self.alpaca.get_closed_pnl(active.parameters.name, previous_entry_price, previous_qty)
                    if pnl is not None:
                        # Registrar PnL en tu historial
                        self.log.info(f"{active.parameters.name} cerró en {closed_price} con PnL {pnl}")
                        revenue = pnl
                        profit = pnl


            self.dataBDMan.inserValue(active.parameters.name, current_value, oldvalue, dif, acumulate, tendence_acu,
                                      tendence_count, min_value,
                                      max_value, min_acu, max_acu, direction, min_dir, max_dir, indi_dir, motion_min,
                                      motion_max, global_min, global_max, action_acum, action_count,
                                      week_flow, week_flow_std, week_flow_med, rel_fcst, rel_fcst_std, rel_fcst_med,
                                      rel_fcst_min, rel_fcst_max, rel_fcst_percent, close_nxt_up, close_nxt_down,close_nxt_middle,
                                      week_dir, week_min_dir, week_max_dir,week_dir_flow,angle_ima, angle_ima_counter,angle, angle_counter,
                                      month_dir_bot_dst, week_dir_bot_dst, week_dir_bot_dst_new, profit, open, qty, protect, revenue, action )

            data = self.dataBDMan.getAllWithNameForXdaysSpecial(active.parameters.name, days)

            # Verificacion de que hay almenos 3 dias recuperados para procesar
            faltan = self.verify3DaysInData(data)
            start_date_time = None
            if faltan > 0:

                days = days + faltan
                data = self.dataBDMan.getAllWithNameForXdaysSpecial(active.parameters.name, days)


        except Exception as e:
            print(f"ERROR search_pricesDB {str(e)}")

        return data

    def filterActives(self, actives, interval):

        activesFiletered = list();

        dbActives = self.dataBDMan.getActivesforInterval(interval)
        for active in actives:
            if self.findActiveInDB(dbActives, active.parameters.name):
                activesFiletered.append(active)

        return activesFiletered

    def getfirstValueForToday(self,  data, results=None):
        # print(f"getfirstValueForToday")
        today = time.strftime("%Y-%m-%d")
        from datetime import datetime
        if self.simulation:

            temp = results[Constants.DATE].values[0]
            todayDate = datetime.strptime(temp, '%Y-%m-%d %H:%M:%S.%f')
            # todayCeros = todayDate.replace(hour=0, minute=0, second=0, microsecond=0)
            today = todayDate.strftime("%Y-%m-%d")


        df = data.loc[(data['date'] >= today)]

        first = df['date'].iloc[0]
        t = datetime.strptime(first, '%Y-%m-%d %H:%M:%S.%f')
        current_time_h = t.hour * 100
        current_time_min = t.minute
        startTimeForToday = int(current_time_h + current_time_min)
        # print(f"START DATE IS : {startTimeForToday}")
        return startTimeForToday

    def updateTimeZoneValues(self, results=None):
        timedelta = None
        try:
            if self.simulation:
                from datetime import datetime
                temp = results[Constants.DATE].values[0]
                # if np.issubdtype(temp.dtype, np.datetime64):#para los valores de yahoo
                #     t = datetime.strptime(str(temp), '%Y-%m-%dT%H:%M:%S.%f000')
                #     timedelta = int(t.astimezone().utcoffset().seconds / 3600)
                # else:
                t = datetime.strptime(temp, '%Y-%m-%d %H:%M:%S.%f')

                timedelta = int(t.astimezone().utcoffset().seconds / 3600)

            else:
                timedelta = -time.timezone / 3600

            if timedelta and timedelta == 1:
                # print(f"TIMEZONE ES INVIERNO {timedelta}")
                self.prepareInvierno()
            else:
                # print(f"TIMEZONE ES VERANO {timedelta}")
                self.prepareVerano()
        except Exception as e:
            message = f"{self.name}  fallo timedelta "
            self.telegram.enviarMensaje(message, self.telegram.tokenBot, self.errorTelegroup)
            self.addmessages(message, results)
            print(f"ERROR updateTimeZoneValues {str(e)}")

    def prepare1430(self):
        self.closeStart = 2040
        self.closeEnd = 2100

        # caluclos iniciales
        self.iniStart = 1430
        self.iniEnd = 1500

        # retornar intervalo
        self.normalIntervalStart = 1600
        self.normalIntervalEnd = 1605

        self.closeAnalisisIntervalStart = 2040
        self.closeAnalisisIntervalEnd = 2100

        # prepare relative values
        self.prepRelStart = 1430
        self.prepRelEnd = 1500
    def prepareInvierno(self):
        self.closeStart = 2140
        self.closeEnd = 2200

        # caluclos iniciales
        self.iniStart = 1530
        self.iniEnd = 1600

        # retornar intervalo
        self.normalIntervalStart = 1600
        self.normalIntervalEnd = 1605

        self.closeAnalisisIntervalStart = 2140
        self.closeAnalisisIntervalEnd = 2200

        # prepare relative values
        self.prepRelStart = 1530
        self.prepRelEnd = 1535

    def prepareVerano(self):
        self.closeStart = 2140
        self.closeEnd = 2200

        # caluclos iniciales
        self.iniStart = 1530
        self.iniEnd = 1550

        # retornar intervalo
        self.normalIntervalStart = 1600
        self.normalIntervalEnd = 1605

        self.closeAnalisisIntervalStart = 2140
        self.closeAnalisisIntervalEnd = 2200

        # prepare relative values
        self.prepRelStart = 1530
        self.prepRelEnd = 1550

    def updateIntervalForAll(self, actives):

        t = time.localtime()
        current_time_h = time.strftime("%H", t)
        current_time_min = time.strftime("%M", t)
        # print(f" gettime hora sistema: {current_time_h} minutos: {current_time_min}")
        currentTime = int(current_time_h + current_time_min)

        intervalo5MIn = 10
        intervalo10MIn = 10



        mensaje = None
        if (currentTime >= int(self.iniStart) and currentTime < int(self.iniEnd)):
            # cambiamoa a 5 minutos
            for active in actives:
                if active.parameters.name == "BTCUSD" or active.parameters.name == "ETHUSD":
                    return
                self.dataBDMan.updateIntervalForActive(active.parameters.name, intervalo5MIn, 3)
            mensaje = f"updateIntervalForAll {self.name} intervalo de 5 MIN"

        if (currentTime >= int(self.normalIntervalStart) and currentTime < int(self.normalIntervalEnd)):
            # cambiamoa a 10 minutos
            for active in actives:
                if active.parameters.name == "BTCUSD" or active.parameters.name == "ETHUSD":
                    return
                self.dataBDMan.updateIntervalForActive(active.parameters.name, self.intervalTime, -1)
            mensaje = f"updateIntervalForAll {self.name} intervalo de: {self.intervalTime} MIN"

        if (currentTime >= int(self.closeAnalisisIntervalStart) and currentTime < int(self.closeAnalisisIntervalEnd)):
            # cambiamoa a 10 minutos
            for active in actives:
                if active.parameters.name == "BTCUSD" or active.parameters.name == "ETHUSD":
                    return
                self.dataBDMan.updateIntervalForActive(active.parameters.name, intervalo10MIn, 5)
            mensaje = f"updateIntervalForAll {self.name} intervalo de 10 MIN"

        if mensaje is not None:
            self.telegram.enviarMensaje(mensaje, self.telegram.tokenBot, self.importanteslTelegroup)

        enb = True

    def updateCounterForAll(self):
        actives = self.dataBDMan.getALLActivesControlTime()

        for active in actives:
            counter = active['counter']
            name = active['active']
            interval = active['interval']
            initial = active['initial']
            if counter != -1:
                if counter > 1:
                    counter = counter - 1
                    self.dataBDMan.updateIntervalForActive(name, interval, counter)
                elif counter == 1:
                    self.dataBDMan.updateIntervalForActive(name, initial, -1)
        enb = True

    def findActiveInDB(self, dbactives, value):
        for active in dbactives:
            if value == active['active']:
                return True
        return False

    def search_prices_list_local(self, actives):
        interval = self.getInterval(None)
        # if len(interval)>0:
        # actives = self.filterActives(actives, interval)
        for active in actives:
            results = {}

            # if active.parameters.verifyMarketOpen:
            #     if self.alpaca.ismarketOpen() == False:
            #         print(f"market is closed for {active.parameters.name}")
            #         continue

            if self.isDBData:
                data = self.search_pricesDB(active)
            else:
                data = self.search_pricesYahoo(active)
            # self.reviewControls(data, active)
            if data is not None and not data.empty and len(data) > 0:
                fastReview = self.evaluateActions(data, results, active)


            if 'ALERT' in results and results['ALERT']:
                self.processAlerts(True, results, active)
                if self.isDBData:
                    self.drawActiveAction(active)
                else:
                    active.drawInfo(data)

    def search_prices_list(self, actives):
        interval = self.getInterval(None)
        # if len(interval)>0:
        actives = self.filterActives(actives, interval)
        for active in actives:
            results = {}

            if active.parameters.verifyMarketOpen:
                if self.alpaca.ismarketOpen() == False:
                    print(f"market is closed for {active.parameters.name}")
                    continue

            if self.isDBData:
                data = self.search_pricesDB(active)
            else:
                data = self.search_pricesYahoo(active)
            # self.reviewControls(data, active)
            if data.empty == False and len(data) > 0:
                fastReview = self.evaluateActions(data, results, active)
                #en real se añade un start de 5 minutos
                # if fastReview == True:
                #     self.evaluateActions(data, results, active,True)
            if 'ALERT' in results and results['ALERT']:
                self.processAlerts(True, results, active)
                if self.isDBData:
                    self.drawActiveAction(active)
                else:
                    active.drawInfo(data)



    def sendResultsEndDay(self, sendResults=False):
        # grafico
        groupTelegram = self.resultsTelegroup
        t = time.localtime()
        current_time_h = time.strftime("%H", t)
        current_time_min = time.strftime("%M", t)
        # print(f" gettime hora sistema: {current_time_h} minutos: {current_time_min}")
        currentTime = int(current_time_h + current_time_min)

        # if (currentTime >= 2200 and currentTime <= 2204) or \
        #         (currentTime >= 1600 and currentTime <= 1604) or \
        #         (currentTime >= 1800 and currentTime <= 1804) or \
        #         (currentTime >= 2000 and currentTime <= 2004) or sendResults:
        if (currentTime >= 2200 and currentTime <= 2204) or \
                (currentTime >= 900 and currentTime <= 904) or \
                (currentTime >= 1100 and currentTime <= 1104) or \
                (currentTime >= 1600 and currentTime <= 1604) or \
                (currentTime >= 1800 and currentTime <= 1804) or \
                (currentTime >= 2000 and currentTime <= 2004) or sendResults:
            start = datetime.datetime.today()
            start_time = start.replace(hour=0, minute=0, second=0, microsecond=0)

            if start:
                end_timeplus = start + datetime.timedelta(days=+1)
                start = start_time.strftime("%Y-%m-%d %H:%M:%S.%f")
                end = end_timeplus.strftime("%Y-%m-%d %H:%M:%S.%f")
            # start_string = datetime.datetime.strptime(start, "%Y-%m-%d")
            # start_string = str(start)

            # end =  start_string
            # start_string =  '2023-07-20'
            # end = '2023-07-20'
            #recuperar los valores abiertos
            onlyOpen = self.dataBDMan.getCurrentRevenues()
            res = self.dataBDMan.getResumeForRangeDatesExact(start, end)
            print(res)

            if res is not None and len(res):
                total = 0
                messages = f"{self.name} RESULTADOS DEL DIA \n"
                for i in range(len(res)):
                    value = res.iloc[i]['value']
                    if value is None:
                        value =0
                    name = res.iloc[i]['name']
                    total = total + float(value)
                    abierto = None
                    if name in onlyOpen:
                        abierto = f" {str(onlyOpen[name])}"
                        onlyOpen.pop(name)
                    messages = messages + f" <b>{name}</b> : {value}  \n"
                    if abierto is not None:
                        messages = messages + f"        <b>Abierto</b> : {abierto}  \n"
                messages = messages + f"total: {total}"


            if len(onlyOpen) >0:
                for clave, valor in onlyOpen.items():
                    messages = messages + f" <b>{clave}</b> open: {valor}  \n"
            self.telegram.enviarMensaje(messages, self.telegram.tokenBot, groupTelegram)

    def drawActiveAction(self, active, send=True):
        days = 2
        weekno = datetime.datetime.today().weekday()
        if weekno == 0:
            days = 3
        data = None
        if self.start is not None and self.end is not None:
            data = self.dataBDMan.getAllWithNameForXdaysRangeDates(active.parameters.name, self.start, self.end)
        else:
            data = self.dataBDMan.getAllWithNameForXdays(active.parameters.name, days)

        # Verificacion de que hay almenos 3 dias recuperados para procesar
        faltan = self.verify3DaysInData(data)
        start_date_time = None
        if faltan > 0:
            if self.start is not None and self.end is not None:
                try:
                    start_date_time = datetime.datetime.strptime(self.start, "%Y-%m-%d %H:%M:%S.%f")
                except Exception as error:
                    # print("Error getAllWithNameForXdaysRangeDates  date format using second change", error)
                    start_date_time = datetime.datetime.strptime(self.start, "%Y-%m-%d")

                if start_date_time:
                    start_date_timeplus = start_date_time + datetime.timedelta(days=-faltan + 1)
                    start = start_date_timeplus.strftime("%Y-%m-%d %H:%M:%S.%f")

                data = self.dataBDMan.getAllWithNameForXdaysRangeDates(active.parameters.name, self.start, self.end)
            else:
                days = days + faltan-1
                data = self.dataBDMan.getAllWithNameForXdays(active.parameters.name, days)

        rangehours = active.parameters.rangehours
        if active.parameters.name == 'BTCUSD' or active.parameters.name == 'ETHUSD':
            rangehours = None
        buyData = data[((data['action'] == 'BUY') & (data['change_action'] == 1)) | ((data['action'] == 'CLOSE-BUY') & (data['change_action'] == 1))]
        closeData = data[((data['action'] == 'CLOSE') & (data['change_action'] == 1)) | ((data['action'] == 'CLOSE-BUY') & (data['change_action'] == 1)) | ((data['action'] == 'CLOSE-SELL') & (data['change_action'] == 1))]
        sellData = data[((data['action'] == 'SELL') & (data['change_action'] == 1)) | ((data['action'] == 'CLOSE-SELL') & (data['change_action'] == 1))]
        active.drawDataDBActions(data, buyData, sellData, closeData, send, rangehours, self.simulation)

    def addmessages(self, message, results):
        messages = ""
        if Constants.MESSAGES in results:
            messages = results[Constants.MESSAGES]
            messages = messages + "\n"
            messages = messages + message
        else:
            messages = message
        results[Constants.MESSAGES] = messages

    # #@mide_tiempo
    def evaluateNewAction(self, results, active, isFastReview=False, isfcst=False):
        fastReview = isFastReview

        try:
            revenue = 0
            winvalue = 0
            res = None
            if self.simulation == False:
                if (results[Constants.CURRENT_ACTION] != Constants.ACTION_CLOSE):
                    try:
                        # if active.parameters.name == 'BTCUSD':
                        #     res, revenue = self.alpaca.is_invested(active.parameters.second_name)
                        # else:
                        res, revenue = self.alpaca.is_invested(active.parameters.name)
                        print(f" evaluateNewAction  paso1 ")
                        results[Constants.REVENUE] = revenue
                        revenue = float(revenue)
                        tp_step = float(active.parameters.profit)
                        last_tp = float(results.get(Constants.PROTECT, 0))
                        needProfit = False

                        # 1 Solo trabajamos si hay beneficio
                        if revenue > 0:
                            # 2 Si no hay TP aún, o se ha superado el objetivo inicial
                            if last_tp == 0:
                                if revenue >= tp_step:
                                    needProfit = True
                            else:
                                # 3 Solo subir TP si ha aumentado al menos X desde el último TP
                                if revenue >= last_tp + tp_step:
                                    needProfit = True

                            # 4 Nunca permitir que el TP baje
                            if revenue <= last_tp:
                                needProfit = False
                                #poner take profit

                            if needProfit:
                                results[Constants.PROTECT] = revenue
                                if active.parameters.name == 'BTCUSD':
                                    print(f" evaluateNewAction  paso2 ")
                                    data = self.alpaca.add_smart_stop_usd_crypto(active.parameters.name, active.parameters.second_name,max_loss_usd=active.parameters.max_loss_usd,protect_profit_usd=active.parameters.protect_profit_usd)
                                    print(f" evaluateNewAction  paso3 ")
                                elif active.parameters.name == 'ETHUSD':
                                    print(f" evaluateNewAction  paso2 ")
                                    data= self.alpaca.add_smart_stop_usd_crypto(active.parameters.name, active.parameters.second_name,max_loss_usd=active.parameters.max_loss_usd,protect_profit_usd=active.parameters.protect_profit_usd)
                                    print(f" evaluateNewAction  paso3 ")
                                else:
                                    nada = ""
                                    data= self.alpaca.add_smart_stop_usd_stock(active.parameters.name, max_loss_usd=active.parameters.max_loss_usd,
                                                                          protect_profit_usd=active.parameters.protect_profit_usd)
                                message = (
                                    f"🛑 STOP LOSS actualizado\n"
                                    f"Activo: {active.parameters.name}\n\n"
                                    f"📥 Entrada: {data['entry_price']}\n"
                                    f"📊 Precio actual: {data['current_price']}\n"
                                    f"⛔ Stop Loss: {data['stop_price']}\n\n"
                                    f"📦 Cantidad: {data['qty']}\n"
                                    f"💸 Pérdida máxima: {data['max_loss_usd']}$\n"
                                    f"🛡️ Protección beneficio: {data['protect_profit_usd']}$"
                                )

                                self.telegram.enviarMensaje(message, self.telegram.tokenBot, self.newTelegroup)
                        else:
                            #control para negativos
                            if abs(float(revenue)) >= float(active.parameters.profit):
                                #cerramos
                                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                            # else:
                            #     needProfit = True
                            #     if results[Constants.PROTECT] !=0:
                            #         if abs(float(revenue)) < float(results[Constants.PROTECT]):
                            #             #ya hay un profit puesto
                            #             needProfit = False
                            #     #poner take profit
                            #     if needProfit:
                            #         results[Constants.PROTECT] = revenue
                            #         if active.parameters.name == 'BTCUSD':
                            #             print(f" evaluateNewAction  paso2 ")
                            #             self.alpaca.add_smart_stop_usd_crypto(active.parameters.second_name,max_loss_usd=3,protect_profit_usd=3)
                            #             print(f" evaluateNewAction  paso3 ")
                            #         elif active.parameters.name == 'ETHUSD':
                            #             print(f" evaluateNewAction  paso2 ")
                            #             self.alpaca.add_smart_stop_usd_crypto(active.parameters.name,max_loss_usd=3,protect_profit_usd=3)
                            #             print(f" evaluateNewAction  paso3 ")
                            #         else:
                            #             nada = ""
                            #             self.alpaca.add_smart_stop_usd_stock(active.parameters.name, max_loss_usd=3,
                            #                                                   protect_profit_usd=3)
                        # actionAcum = results[Constants.ACTION_ACUM]
                        # if results[Constants.CURRENT_ACTION] == Constants.ACTION_SELL:
                        #     if actionAcum < 0:
                        #         actionAcum = abs(actionAcum)
                        #     elif actionAcum > 0:
                        #         actionAcum = actionAcum * (-1)
                        # results[Constants.REVENUE] = revenue
                        # minimunactionAcum = self.minimunActionAcum
                        # # Control ganancias cerramos si el valor es superior a X
                        # if active.parameters.controlWin or self.enableControlWIN:
                        if isFastReview == True:
                           self.dataBDMan.updateIntervalForActive(active.parameters.name, 5, 1)
                                # self.addmessages(message, results)
                                # self.telegram.enviarMensaje(message, self.telegram.tokenBot, self.newTelegroup)
                                # print(message)
                    except Exception as e:
                        message = f"{self.name} fallo revenue {results[Constants.CURRENT_ACTION]} para {active.parameters.name} ganancia {str(revenue)} error: {str(e)}"
                        self.addmessages(message, results)
                        self.telegram.enviarMensaje(message, self.telegram.tokenBot, self.errorTelegroup)
                        print(f"ERROR1 evaluateNewAction {str(e)}")
                        print(
                            f"fallo en revenue for {active.parameters.name} second: {active.parameters.second_name}")

            elif self.simulation == True and isFastReview == True and self.disableCloseEndRevenue == False:
                nada = ""
                if (results[Constants.CURRENT_ACTION] != Constants.ACTION_CLOSE):
                    try:
                        revenue = results[Constants.ACTION_ACUM]
                        if results[Constants.CURRENT_ACTION] == Constants.ACTION_SELL:
                            if revenue < 0:
                                revenue = abs(revenue)
                            elif revenue > 0:
                                revenue = revenue * (-1)
                        minimunactionAcum = self.minimunActionAcum
                        # Control ganancias cerramos si el valor es superior a X
                        if active.parameters.controlWin or self.enableControlWIN:
                            if isFastReview == True:
                                if float(revenue) >= float(minimunactionAcum):
                                    fastReview = False
                                    message = f"{self.name} Cerramos por regla de ahorro accion: {results[Constants.CURRENT_ACTION]}  para {active.parameters.name} ganancia {str(revenue)}"
                                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                                    # self.addmessages(message, results)
                                    # self.telegram.enviarMensaje(message, self.telegram.tokenBot, self.newTelegroup)
                                    print(message)
                    except Exception as e:
                        message = f"{self.name} fallo revenue {results[Constants.CURRENT_ACTION]} para {active.parameters.name} ganancia {str(revenue)} error: {str(e)}"
                        self.addmessages(message, results)
                        self.telegram.enviarMensaje(message, self.telegram.tokenBot, self.errorTelegroup)
                        print(f"ERROR2 evaluateNewAction {str(e)}")
                        print(
                            f"fallo en revenue for {active.parameters.name} second: {active.parameters.second_name}")

            if Constants.NEW_ACTION in results:
                currentAction = results[Constants.CURRENT_ACTION]

                if results[Constants.NEW_ACTION] == results[Constants.CURRENT_ACTION] and fastReview == False:
                    # NO CAMBIO DE ACCION
                    same = True
                    print(f"no cambio el estado")
                else:
                    isSell = False
                    isBuy = False
                    isClose = False
                    results[Constants.CHANGE_ACTION] = 1
                    amount = 1000
                    newAction = results[Constants.NEW_ACTION]
                    # print(f"changeStatus for {active.parameters.name} second: {active.parameters.second_name} "
                    #       f"current {results[Constants.CURRENT_ACTION]} newAction {newAction}")

                    results[Constants.CURRENT_ACTION] = newAction
                    if Constants.ACTION_BUY == newAction:
                        # self.operations.currentTupla['START'] = results[Constants.VALUE]
                        # self.operations.currentTupla['START_DATE'] = results[Constants.DATE].values[0]

                        isBuy = True
                        self.addStartValues(results, isBuy, active)
                        self.updateMinMaxValues(results=results)
                    elif Constants.ACTION_SELL == newAction:
                        # self.operations.currentTupla['START'] = results[Constants.VALUE]
                        # self.operations.currentTupla['START_DATE'] = results[Constants.DATE].values[0]
                        isSell = True
                        self.addStartValues(results, False, active)
                        self.updateMinMaxValues(results=results)
                    elif Constants.ACTION_CLOSE in newAction:
                        isClose = True
                        wasBuy = True
                        if active.parameters.reevaluateAction:
                            fastReview = True
                        if Constants.ACTION_SELL == currentAction:
                            wasBuy = False
                        self.addStopValues(results, wasBuy, active)

                        results[Constants.ACTION_COUNT] = 0
                        results[Constants.ACTION_ACUM] = 0

                        # if isfcst == False:
                        # self.dataBDMan.updateIntervalForActive(active.parameters.name, 5, 2)

                        self.updateMinMaxValues(results=results)
                    else:
                        print(f"otra accion no esperada !! {results[Constants.CURRENT_ACTION]}")

                    results['ALERT'] = True

                    # ===================== OPERAR MERCADO =====================
                    if self.simulation == False:
                        try:
                            if self.operate and active.parameters.operate:
                                action_map = {
                                    Constants.ACTION_BUY: "LONG",
                                    Constants.ACTION_SELL: "SHORT",
                                    Constants.ACTION_CLOSE: "FLAT"
                                }

                                target_side = action_map.get(results[Constants.CURRENT_ACTION], None)

                                if target_side is not None:
                                    mess = " "
                                    if target_side == "FLAT":
                                        mess = self.alpaca.close_all_positions_and_orders(active.parameters.name)

                                    else:

                                        mess = self.alpaca.execute_target_position(
                                            active.parameters.name,
                                            target_side,
                                            amount
                                        )
                                    print(
                                        f"Operación {results[Constants.CURRENT_ACTION]} ejecutada en {active.parameters.name}: {mess}")

                                    error_keywords = [
                                        "failed",
                                        "error",
                                        "exception",
                                        "insufficient",
                                        "denied",
                                        "rejected"
                                    ]

                                    if any(k in mess.lower() for k in error_keywords):
                                        self.telegram.enviarMensaje(mess, self.telegram.tokenBot,
                                                                    self.errorTelegroup)

                                    # Obtener ganancia si es cierre o cambio de posición
                                    # revenue = 0
                                    if target_side == "FLAT":
                                        invested, revenue = self.alpaca.is_invested(active.parameters.name)
                                        results[Constants.REVENUE] = revenue



                                    # Obtener ganancia actual
                                    # revenue = 0
                                    # invested, revenue = self.alpaca.is_invested(active.parameters.name)
                                    # results[Constants.REVENUE] = revenue

                                    # # Colocar stop inteligente solo si no estamos FLAT
                                    # if target_side != "FLAT" and invested:
                                    #     # Determinar tipo de stop según activo (crypto o stock)
                                    #     if active.parameters.is_crypto:
                                    #         stop_info = self.alpaca.add_smart_stop_usd_crypto(
                                    #             symbol=active.parameters.name,
                                    #             max_loss_usd=active.parameters.max_loss_usd,
                                    #             protect_profit_usd=active.parameters.protect_profit_usd
                                    #         )
                                    #     else:
                                    #         stop_info = self.alpaca.add_smart_stop_usd_stock(
                                    #             symbol=active.parameters.name,
                                    #             max_loss_usd=active.parameters.max_loss_usd,
                                    #             protect_profit_usd=active.parameters.protect_profit_usd
                                    #         )
                                    #
                                    #     print(f"Stop inteligente colocado: {stop_info}")
                                    #     mess += f" | Stop: {stop_info['stop_price']}"

                                    # Mensaje unificado para Telegram
                                    message = (
                                        f"{self.name} operación en ALPACA: {results[Constants.CURRENT_ACTION]} "
                                        f"para {active.parameters.name}, invertido {amount}, "
                                        f"ganancia {revenue}, mensaje: {mess}"
                                    )
                                    self.telegram.enviarMensaje(message, self.telegram.tokenBot, self.newTelegroup)
                                    self.addmessages(message, results)
                                else:
                                    print(f"Acción desconocida: {results[Constants.CURRENT_ACTION]}")
                        except Exception as e:
                            # Captura de errores general
                            revenue = results.get(Constants.REVENUE, 0)
                            message = (
                                f"{self.name} ERROR en operación {results[Constants.CURRENT_ACTION]} "
                                f"para {active.parameters.name}, ganancia {revenue}, error: {str(e)}"
                            )
                            self.telegram.enviarMensaje(message, self.telegram.tokenBot, self.errorTelegroup)
                            self.addmessages(message, results)
                            print(f"ERROR3 evaluateNewAction {str(e)}")
                            print(
                                f"{self.name} operate for {active.parameters.name}, second: {active.parameters.second_name}")



                    # ACUMULAR VALORES PARA DIBUJAR SIMULACION
                    if self.simulation:
                        dataTemp = {}

                        dataTemp['date'] = results[Constants.DATE].values[0]
                        dataTemp['value'] = results[Constants.VALUE]
                        if isSell:
                            self.operations.sellData.append(dataTemp)
                        elif isBuy:
                            self.operations.buyData.append(dataTemp)
                        elif isClose:
                            self.operations.closeData.append(dataTemp)
            else:
                #para guardar logs para analisis
                if self.simulation:
                        if self.allAnalysLogs:
                            nada =""
                            self.addNormaValues(results, active)

        except Exception as e:
            message = f"{self.name}  fallo change state {results[Constants.CURRENT_ACTION]} para {active.parameters.name} ganancia {str(winvalue)} error: {str(e)}"
            self.telegram.enviarMensaje(message, self.telegram.tokenBot, self.errorTelegroup)
            self.addmessages(message, results)
            print(f"ERROR evaluateNewAction {str(e)}")
            print(f"fallo change state for {active.parameters.name} second: {active.parameters.second_name}")

        return fastReview

    def printAnalisis(self, results, active):
        # if self.simulation:
        #     # acumular distancias
        #     # self.prepareBESTDISTANCE(results)
        # print(f"PRINT ANALISIS  {results[Constants.DATE].values[0]} ACCION: {results[Constants.CURRENT_ACTION]} RELAT: {results[Constants.RELATIVE]} ACUM: {results[Constants.ACUMULADO]} ACT_ACUM: {results[Constants.ACTION_ACUM]} FLUJO: {results[Constants.FLUJO]} contador {results[Constants.FLUJO_COUNT]} difference: {active.parameters.difference} INDICATOR_MED_MOMENT {results[Constants.INDICATOR_MED_MOMENT]} MED {results[Constants.INDICATOR_MED]} MED_STD {results[Constants.INDICATOR_MED_STD]} ")
        print(
            f"PRINT ANALISIS  {results[Constants.DATE].values[0]}  ACUM: {results[Constants.ACUMULADO]} \tFLOW_DIFF: {results[Constants.FLOW_DIFF]} \tPREVIUS: {results[Constants.PREVIOUS_DIST]} \tACCION: {results[Constants.CURRENT_ACTION]}  \tRELAT: {results[Constants.RELATIVE]}   ")
        print(
            f"PRINT0 ANALISIS  {results[Constants.DATE].values[0]} ACTION_ACUM: {results[Constants.ACTION_ACUM]} \tACTION_DISTANCE: {results[Constants.ACTION_DISTANCE]} \tACTION_COUNT: {results[Constants.ACTION_COUNT]} \tFLUJO: {results[Constants.FLUJO]} \tFLUJO_COUNT: {results[Constants.FLUJO_COUNT]}  ")

        print(
            f"PRINT00 ANALISIS  {results[Constants.DATE].values[0]} ACTION_ACUM: {results[Constants.ACTION_ACUM]} \tACTION_MIN_DIST: {results[Constants.ACTION_MIN_DIST]} \tACTION_MAX_DIST: {results[Constants.ACTION_MAX_DIST]} \tACTION_MIN: {results[Constants.ACTION_MIN]} \tACTION_MAX: {results[Constants.ACTION_MAX]}  ")

        print(
            f"PRINT1 ANALISIS  {results[Constants.DATE].values[0]} INDICATOR_MED_MOMENT: {results[Constants.INDICATOR_MED_MOMENT]} \tINDICATOR_MED_MOMENT_VALUE: {results[Constants.INDICATOR_MED_MOMENT_VALUE]} \t STD_MOMENT: {results[Constants.STD_MOMENT]}")
        print(
            f"PRINT2 ANALISIS  {results[Constants.DATE].values[0]} IMA1: {results[Constants.IMA1]} \tIMA5MA20: {results[Constants.IMA5MA20]} \tIMA_NEW: {results[Constants.IMA_NEW]} \tIMA1_DIS :{results[Constants.IMA1_DISTANCE]}")
        print(
            f"PRINT3 ANALISIS  {results[Constants.DATE].values[0]} MARKET_TENDENCE: {results[Constants.MARKET_TENDENCE]} \tIND_MED: {results[Constants.INDICATOR_MED]} \tDIRECTION: {results[Constants.DIRECTION]}  \tINDICATOR: {results[Constants.INDICATOR]} \tINDICATOR_TENDENCE: {results[Constants.INDICATOR_TENDENCE]} ")
        print(
            f"PRINT4 ANALISIS  {results[Constants.DATE].values[0]} WEEK_FLOW: {results[Constants.WEEK_FLOW]} \tWEEK_FLOW_STD: {results[Constants.WEEK_FLOW_STD]}  \tWEEK_FLOW_MED: {results[Constants.WEEK_FLOW_MED]} \tWEEK_FLOW_MED_LEVEL: {results[Constants.WEEK_FLOW_MED_LEVEL]}")
        print(
            f"PRINT41 ANALISIS  {results[Constants.DATE].values[0]} WEEK_FLOW: {results[Constants.WEEK_FLOW]} \tWEEK_FLOW_DIFF: {results[Constants.WEEK_FLOW_DIFF]} \tWEEK_FLOW_MED: {results[Constants.WEEK_FLOW_MED]} \tWEEK_FLOW_PREV_MED: {results[Constants.WEEK_FLOW_PREV_MED]} \tWEEK_FLOW_PREV: {results[Constants.WEEK_FLOW_PREV]} ")
        print(
            f"PRINT42 ANALISIS  {results[Constants.DATE].values[0]} WEEK_FLOW: {results[Constants.WEEK_FLOW]} \tWEEK_DIR: {results[Constants.WEEK_DIR]} \tWEEK_DIR_BOT_DST: {results[Constants.WEEK_DIR_BOT_DST]} \tWEEK_DIR_TOP_DST: {results[Constants.WEEK_DIR_TOP_DST]}  \tWEEK_MIN_DIR: {results[Constants.WEEK_MIN_DIR]} \tWEEK_MAX_DIR: {results[Constants.WEEK_MAX_DIR]} ")

        print(
            f"PRINT43 ANALISIS  {results[Constants.DATE].values[0]} WEEK_FLOW: {results[Constants.WEEK_FLOW]} \tWEEK_DIR: {results[Constants.WEEK_DIR]} \tWEEK_DIR_FLOW_DIFF: {results[Constants.WEEK_DIR_FLOW_DIFF]}  \tWEEK_DIR_FLOW: {results[Constants.WEEK_DIR_FLOW]} \tWEEK_DIR_FLOW_PREV: {results[Constants.WEEK_DIR_FLOW_PREV]} \tWEEK_DIR_BOT_DST: {results[Constants.WEEK_DIR_BOT_DST]}   ")

        print(
            f"PRINT5 ANALISIS  {results[Constants.DATE].values[0]} IND_PROB_FLOW: {results[Constants.IND_PROB_FLOW]} \tIND_REL_FCST_PERCENT: {results[Constants.IND_REL_FCST_PERCENT]} \tIND_REL_FCST: {results[Constants.IND_REL_FCST]} \tIND_REL_FCST_STD: {results[Constants.IND_REL_FCST_STD]}  \tIND_REL_FCST_MED: {results[Constants.IND_REL_FCST_MED]} \tIND_REL_FCST_MIN: {results[Constants.IND_REL_FCST_MIN]} \tIND_REL_FCST_MAX: {results[Constants.IND_REL_FCST_MAX]} ")
        print(
            f"PRINT6 ANALISIS  {results[Constants.DATE].values[0]} INDICATOR_MED: {results[Constants.INDICATOR_MED]} \tIND_MED_STD: {results[Constants.INDICATOR_MED_STD]} \tMED: {results[Constants.MEDIA]} \tSTDDESV: {results[Constants.STDDESV]}")
        print(
            f"PRINT7 ANALISIS  {results[Constants.DATE].values[0]} IND_REL_FCST_PERCENT: {results[Constants.IND_REL_FCST_PERCENT]} \tIND_REL_FCST_PREV_PERCENT: {results[Constants.IND_REL_FCST_PREV_PERCENT]} \tIND_REL_FCST: {results[Constants.IND_REL_FCST]} \tIND_REL_FCST_STD: {results[Constants.IND_REL_FCST_STD]}  \tIND_REL_FCST_MED: {results[Constants.IND_REL_FCST_MED]} \tIND_REL_FCST_MIN: {results[Constants.IND_REL_FCST_MIN]} \tIND_REL_FCST_MAX: {results[Constants.IND_REL_FCST_MAX]} ")

        print(
            f"PRINT7.1 ANALISIS  {results[Constants.DATE].values[0]} IND_REL_FCST_STD: {results[Constants.IND_REL_FCST_STD]}  \tIND_REL_FCST_MED: {results[Constants.IND_REL_FCST_MED]} \tIND_REL_FCST_MIN: {results[Constants.IND_REL_FCST_MIN]} \tIND_REL_FCST_MAX: {results[Constants.IND_REL_FCST_MAX]} ")

        print(
            f"PRINT8 ANALISIS  {results[Constants.DATE].values[0]} IND_REL_PERCENT_MED: {results[Constants.IND_REL_PERCENT_MED]} \tIND_REL_PERCENT_STD: {results[Constants.IND_REL_PERCENT_STD]} \tIND_REL_FCST_PERCENT: {results[Constants.IND_REL_FCST_PERCENT]} \tIND_REL_FCST_PREV_PERCENT: {results[Constants.IND_REL_FCST_PREV_PERCENT]}")

        print(
            f"PRINT9 ANALISIS  {results[Constants.DATE].values[0]} VALUE: {results[Constants.VALUE]} \tIND_REL_FCST_MIN: {results[Constants.IND_REL_FCST_MIN]} \tIND_REL_FCST_MAX: {results[Constants.IND_REL_FCST_MAX]} RELATIVE_MIN: {results[Constants.RELATIVE_MIN]} \tRELATIVE_MAX: {results[Constants.RELATIVE_MAX]} ")

        print(
            f"PRINT10 ANALISIS  {results[Constants.DATE].values[0]} \tDIRECTION: {results[Constants.DIRECTION]} \tMIN_DIR: {results[Constants.MIN_DIR]} \tMAX_DIR: {results[Constants.MAX_DIR]} ")
        print(
            f"PRINT11 ANALISIS  {results[Constants.DATE].values[0]} \tINDICATOR_MED_STD: {results[Constants.INDICATOR_MED_STD]}  \tMEDSTDDIFF: {results[Constants.MEDSTDDIFF]} \tMEDIA: {results[Constants.MEDIA]} \tSTDDESV: {results[Constants.STDDESV]} ")
        print(
            f"PRINT12 ANALISIS  {results[Constants.DATE].values[0]} \tRELATIVE: {results[Constants.RELATIVE]} \tIND_REL_FCST_MED: {results[Constants.IND_REL_FCST_MED]} \tIND_REL_FCST_MIN: {results[Constants.IND_REL_FCST_MIN]} \tIND_REL_FCST_MAX: {results[Constants.IND_REL_FCST_MAX]} ")

        print(
            f"PRINT13 ANALISIS  {results[Constants.DATE].values[0]} \tINDICATOR_MED_DAY: {results[Constants.INDICATOR_MED_DAY]} \tINDICATOR_STD_DAY: {results[Constants.INDICATOR_STD_DAY]} \tINDICATOR_MED_DAYS: {results[Constants.INDICATOR_MED_DAYS]} \tINDICATOR_STD_DAYS: {results[Constants.INDICATOR_STD_DAYS]} ")

        print(
            f"PRINT14 ANALISIS  {results[Constants.DATE].values[0]} \tIND_MED_DAY: {results[Constants.IND_MED_DAY]} \t VALUE_DIFFMED: {results[Constants.VALUE_DIFFMED]} \t VALUE: {results[Constants.VALUE]}  \tIND_SUM_UP: {results[Constants.IND_SUM_UP]} \tIND_NUM_UP: {results[Constants.IND_NUM_UP]} \tIND_SUM_DOWN: {results[Constants.IND_SUM_DOWN]} \tIND_NUM_DOWN: {results[Constants.IND_NUM_DOWN]} ")
        print(
            f"PRINT15 ANALISIS  {results[Constants.DATE].values[0]} \tINDICATOR_DISTANCE: {results[Constants.INDICATOR_DISTANCE]} \tINDICATOR: {results[Constants.INDICATOR]} \tIMA5MA20: {results[Constants.IMA5MA20]} ")
        print(
            f"PRINT16 ANALISIS  {results[Constants.DATE].values[0]} \tIND_MED_DAY: {results[Constants.IND_MED_DAY]} \tIND_SUM_UP_DAYS: {results[Constants.IND_SUM_UP_DAYS]} \tIND_NUM_UP_DAYS: {results[Constants.IND_NUM_UP_DAYS]} \tIND_SUM_DOWN_DAYS: {results[Constants.IND_SUM_DOWN_DAYS]} \tIND_NUM_DOWN_DAYS: {results[Constants.IND_NUM_DOWN_DAYS]} ")
        print(
            f"PRINT17 ANALISIS  {results[Constants.DATE].values[0]} \tINDICATOR_EMA: {results[Constants.INDICATOR_EMA]} \tEMA_DST: {results[Constants.EMA_DST]} \tINDICATOR_EMA_CHECK: {results[Constants.INDICATOR_EMA_CHECK]}")
        print(
            f"PRINT18 ANALISIS  {results[Constants.DATE].values[0]} \tIND_BLG: {results[Constants.IND_BLG]} \tIND_BLG_MED_DST: {results[Constants.IND_BLG_MED_DST]} \tIND_BLG_UPPER_DST: {results[Constants.IND_BLG_UPPER_DST]} \tIND_BLG_LOWER_DST: {results[Constants.IND_BLG_LOWER_DST]} \tCLOSE_NXT_UP: {results[Constants.CLOSE_NXT_UP]} \tCLOSE_NXT_DOWN: {results[Constants.CLOSE_NXT_DOWN]}")
        print(
            f"PRINT19 ANALISIS  {results[Constants.DATE].values[0]} \tIND_BLG: {results[Constants.IND_BLG]} \tIND_BLG_UPPER_DST_PERCENT: {results[Constants.IND_BLG_UPPER_DST_PERCENT]} \tIND_BLG_LOWER_DST_PERCENT: {results[Constants.IND_BLG_LOWER_DST_PERCENT]}  \tIND_BLG_MIDDLE_DST_PERCENT: {results[Constants.IND_BLG_MIDDLE_DST_PERCENT]} \tANGLE: {results[Constants.ANGLE]} \tANGLEm1: {results[Constants.ANGLEm1]}")

        print(
            f"PRINT20 ANALISIS  {results[Constants.DATE].values[0]} \tINTERVAL: {results[Constants.INTERVAL]} \tANGLE: {results[Constants.ANGLE]}  \tANGLE_IMA1: {results[Constants.ANGLE_IMA1]} \tANGLE_EMA: {results[Constants.ANGLE_EMA]} \tANGLE_EMA20: {results[Constants.ANGLE_EMA20]} \tANGLE_EMA_FLOW: {results[Constants.ANGLE_EMA_FLOW]}\tANGLEm1: {results[Constants.ANGLEm1]} \tANGLEm21: {results[Constants.ANGLEm21]}\tMARKET_ANGLE_TANG: {results[Constants.MARKET_ANGLE_TANG]}\tMARKET_ANGLE: {results[Constants.MARKET_ANGLE]}\tIND_BLG_UPPER_DST_PERCENT: {results[Constants.IND_BLG_UPPER_DST_PERCENT]} \tIND_BLG_LOWER_DST_PERCENT: {results[Constants.IND_BLG_LOWER_DST_PERCENT]} ")

        print(
            f"PRINT21 ANALISIS  {results[Constants.DATE].values[0]} \tCLOSE_NXT_UP: {results[Constants.CLOSE_NXT_UP]} \tCLOSE_NXT_DOWN: {results[Constants.CLOSE_NXT_DOWN]} \tCLOSE_NXT_MIDDLE: {results[Constants.CLOSE_NXT_MIDDLE]} \tINTERVAL: {results[Constants.INTERVAL]}")

        print(
            f"PRINT22 ANALISIS  {results[Constants.DATE].values[0]} \tWEEK_DIR_BOT_DST: {results[Constants.WEEK_DIR_BOT_DST]} \tWEEK_DIR_TOP_DST: {results[Constants.WEEK_DIR_TOP_DST]}  \tIND_BLG_UPPER_DST_PERCENT: {results[Constants.IND_BLG_UPPER_DST_PERCENT]} \tIND_BLG_LOWER_DST_PERCENT: {results[Constants.IND_BLG_LOWER_DST_PERCENT]}  \tIND_BLG_MIDDLE_DST_PERCENT: {results[Constants.IND_BLG_MIDDLE_DST_PERCENT]} ")


        print(
            f"PRINTCUSTOM ANALISIS  {results[Constants.DATE].values[0]} IMA1: {results[Constants.IMA1]} \tANGLE: {results[Constants.ANGLE]} \tANGLEm1: {results[Constants.ANGLEm1]} \tINDICATOR_MED_MOMENT: {results[Constants.INDICATOR_MED_MOMENT]} \tINDICATOR: {results[Constants.INDICATOR]} \tIND_MED: {results[Constants.INDICATOR_MED]}  \tDIRECTION: {results[Constants.DIRECTION]} \tIMA1_DIS :{results[Constants.IMA1_DISTANCE]}")

        print(
            f"PRINTCUSTOM ANALISIS01  {results[Constants.DATE].values[0]} WEEK_FLOW: {results[Constants.WEEK_FLOW]} \tWEEK_DIR_FLOW_DIFF: {results[Constants.WEEK_DIR_FLOW_DIFF]} \tANGLE: {results[Constants.ANGLE]} \tANGLE_EMA20: {results[Constants.ANGLE_EMA20]}  \tANGLE_IMA1: {results[Constants.ANGLE_IMA1]} \tANGLE_EMA_FLOW: {results[Constants.ANGLE_EMA_FLOW]} \tANGLEm1: {results[Constants.ANGLEm1]} \tANGLE_EMA: {results[Constants.ANGLE_EMA]} \tWEEK_DIR_BOT_DST: {results[Constants.WEEK_DIR_BOT_DST]} \tIND_BLG_LOWER_DST_PERCENT: {results[Constants.IND_BLG_LOWER_DST_PERCENT]} \tDIRECTION: {results[Constants.DIRECTION]} \tIMA1_DIS :{results[Constants.IMA1_DISTANCE]}")

        print(
            f"PRINTCUSTOM ANALISISFLOW01  {results[Constants.DATE].values[0]} WEEK_FLOW: {results[Constants.WEEK_FLOW]} \tWEEK_DIR: {results[Constants.WEEK_DIR]} \tWEEK_DIR_FLOW_DIFF: {results[Constants.WEEK_DIR_FLOW_DIFF]}  \tWEEK_DIR_FLOW: {results[Constants.WEEK_DIR_FLOW]} \tANGLE: {results[Constants.ANGLE]} \tANGLE_EMA20: {results[Constants.ANGLE_EMA20]} \tANGLE_IMA1: {results[Constants.ANGLE_IMA1]} \tIND_BLG_LOWER_DST_PERCENT: {results[Constants.IND_BLG_LOWER_DST_PERCENT]} \tWEEK_DIR_BOT_DST: {results[Constants.WEEK_DIR_BOT_DST]}  \tWEEK_DIR_BOT_DST_PREV: {results[Constants.WEEK_DIR_BOT_DST_PREV]} ")

        print(
            f"PRINTCUSTOM ANALISISFLOW02  {results[Constants.DATE].values[0]} \tIND_PROB_FLOW: {results[Constants.IND_PROB_FLOW]} \tIMA1EMADIFF: {results[Constants.IMA1EMADIFF]} \tANGLE_EMA20: {results[Constants.ANGLE_EMA20]} \tANGLE_IMA1: {results[Constants.ANGLE_IMA1]} \tIND_BLG_LOWER_DST_PERCENT: {results[Constants.IND_BLG_LOWER_DST_PERCENT]} \tWEEK_DIR_BOT_DST: {results[Constants.WEEK_DIR_BOT_DST]}  \tWEEK_DIR_BOT_DST_PREV: {results[Constants.WEEK_DIR_BOT_DST_PREV]} ")

        print(
            f"PRINTCUSTOM ANALISISFLOW03  {results[Constants.DATE].values[0]} \tANGLE: {results[Constants.ANGLE]} \tHOURLY_ANGLE: {results[Constants.HOURLY_ANGLE]} \tHOURLY_ANGLE_MED: {results[Constants.HOURLY_ANGLE_MED]}  \tHOURLY_ANGLE_MED_PREV: {results[Constants.HOURLY_ANGLE_MED_PREV]}\tANGLE_FLOW: {results[Constants.ANGLE_FLOW]} \tANGLE_COUNTER: {results[Constants.ANGLE_COUNTER]} \tANGLE_PREV: {results[Constants.ANGLE_PREV]} \tANGLE_IMA1: {results[Constants.ANGLE_IMA1]} \tANGLE_IMA1_PREV: {results[Constants.ANGLE_IMA1_PREV]} \tANGLE_IMA1_COUNTER: {results[Constants.ANGLE_IMA1_COUNTER]}")

    def prepareBESTDISTANCE(self, results):
        prev = results[Constants.ACUMULADO_ABS]
        if abs(prev) < 2 and abs(prev)!=0:
            self.diffValues.append(abs(prev))

    # #@mide_tiempo
    def calculateBESTDISTANCE(self):
        # cambios = [valor - self.diffValues[-1] for valor in self.diffValues]
        print(f"{self.diffValues}")
        if len(self.diffValues) > 0:
            desviacion_estandar = np.std(self.diffValues)
            media = np.mean(self.diffValues)
            import statistics as stats
            median = stats.median_grouped(self.diffValues)
            print(f" PRINTDIFF ANALISIS DIFF_MED: {media}  DIFF_STD: {desviacion_estandar} median group: {median}")

    def applyNewAction(self, results, active, isFcst=False, doubleAction = False):
        fastReview = self.evaluateNewAction(results, active, False, isFcst)
        if self.useConfig == False:
            # update DATABASE
            if doubleAction==True:
                results[Constants.CURRENT_ACTION]= 'CLOSE-'+results[Constants.CURRENT_ACTION]
            self.dataBDMan.updateValueWithData(results)
        else:
            self.updateConfig(active, results)

    def closeAndNewAction(self, results, active, action, isFcst=False):
        try:
            self.closeAndNewActionRetry(results, active, action, isFcst)

        except Exception as e:
            print(f"ERROR closeAndNewAction {str(e)}")
            message = f"{self.name}  fallo closeAndNewAction  {results[Constants.CURRENT_ACTION]} para {active.parameters.name} error: {str(e)}"
            self.telegram.enviarMensaje(message, self.telegram.tokenBot, self.errorTelegroup)
            try:
                # time.sleep(2)
                self.closeAndNewActionRetry(results, active, action, isFcst)
            except Exception as e:
                print(f"ERROR closeAndNewAction {str(e)}")
                message = f"{self.name}  fallo closeAndNewAction  {results[Constants.CURRENT_ACTION]} para {active.parameters.name} error: {str(e)}"

    def closeAndNewActionRetry(self, results, active, action, isFcst=False):
        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
        self.applyNewAction(results, active, isFcst)
        if self.simulation == False:
            nada = ""
            # time.sleep(4)
        results[Constants.NEW_ACTION] = action
        self.applyNewAction(results, active, isFcst, doubleAction=True)
        if self.simulation == False:
            message = f"{self.name}  EXITO closeAndNewAction  {results[Constants.CURRENT_ACTION]} para {active.parameters.name}"
            self.telegram.enviarMensaje(message, self.telegram.tokenBot, self.errorTelegroup)

    # #@mide_tiempo
    def evaluateFcstPROB(self, results, active):
        try:
            currentTime = self.gettime(results)
            fcst = results[Constants.IND_REL_FCST]
            msg = None
            probFlow = results[Constants.IND_PROB_FLOW]
            if currentTime and currentTime >= int(self.closeStart) and currentTime < int(self.closeEnd):
                if "FINAL_"+ active.parameters.name in results:
                    if results["FINAL_"+ active.parameters.name] =='1':
                        results["FINAL_" + active.parameters.name] = '0'
                        results[Constants.INICIO_NAME] = "PROB_CLOSE_"+active.parameters.endProbDef
                        if (probFlow == Constants.DIR_UP or probFlow == Constants.DIR_PRE_UP):
                            # up

                            if results[Constants.CURRENT_ACTION] == Constants.ACTION_BUY:
                                if active.parameters.continueFlow== False:
                                    # results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                    # print(f"ACTIVO FCST 1530 CLOSE-BUY!!!")
                                    msg = f"{self.name} ACTIVO FCST 2150 CLOSE-BUY for {active.parameters.name} action: {results[Constants.IND_PROB_FLOW]}"
                                    self.closeAndNewAction(results, active, Constants.ACTION_BUY)

                            elif results[Constants.CURRENT_ACTION] == Constants.ACTION_SELL:
                                # results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                # print(f"ACTIVO FCST 2150 BUY!!!")
                                msg = f"{self.name} ACTIVO FCST 2150 CLOSE-BUY for {active.parameters.name} action: {results[Constants.IND_PROB_FLOW]}"
                                self.closeAndNewAction(results, active, Constants.ACTION_BUY)
                            elif Constants.ACTION_CLOSE in results[Constants.CURRENT_ACTION] or results[Constants.CURRENT_ACTION] == Constants.ACTION_WAIT:
                                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                # print(f"ACTIVO FCST 2150 BUY!!!")
                                msg = f"{self.name} ACTIVO FCST 2150 BUY for {active.parameters.name} action: {results[Constants.IND_PROB_FLOW]}"
                                self.applyNewAction(results, active)
                        elif (probFlow == Constants.DIR_DOWN or probFlow == Constants.DIR_PRE_DOWN):
                            if active.parameters.name != 'BTCUSD' and active.parameters.name != 'ETHUSD':
                                # down
                                if results[Constants.CURRENT_ACTION] == Constants.ACTION_BUY:
                                    # print(f"ACTIVO FCST 2150 SELL!!!")
                                    msg = f"{self.name} ACTIVO FCST 2150 CLOSE-SELL for {active.parameters.name} action: {results[Constants.IND_PROB_FLOW]}"
                                    # results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                    self.closeAndNewAction(results, active, Constants.ACTION_SELL)
                                elif results[Constants.CURRENT_ACTION] == Constants.ACTION_SELL:
                                    if active.parameters.continueFlow == False:
                                        # print(f"ACTIVO FCST 1530 CLOSE-SELL!!!")
                                        msg = f"{self.name} ACTIVO FCST 2150 CLOSE-SELL for {active.parameters.name} action: {results[Constants.IND_PROB_FLOW]}"
                                        self.closeAndNewAction(results, active, Constants.ACTION_SELL)

                                elif Constants.ACTION_CLOSE in results[Constants.CURRENT_ACTION] or results[Constants.CURRENT_ACTION] == Constants.ACTION_WAIT:
                                    results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                    # print(f"ACTIVO FCST 2150 SELL!!!")
                                    msg = f"{self.name} ACTIVO FCST 2150 SELL for {active.parameters.name} action: {results[Constants.IND_PROB_FLOW]}"
                                    self.applyNewAction(results, active)

            if currentTime and currentTime >= int(self.iniStart) and currentTime < int(self.iniEnd):
                if "INIT_"+ active.parameters.name in results:
                    if results["INIT_"+ active.parameters.name] =='1':
                        results["INIT_" + active.parameters.name] = '0'
                        results[Constants.INICIO_NAME] = "PROB_START_"+active.parameters.startProbDef
                        if (probFlow == Constants.DIR_UP or probFlow == Constants.DIR_PRE_UP):
                            # up
                            if results[Constants.CURRENT_ACTION] == Constants.ACTION_BUY:
                                if active.parameters.continueFlow == False:
                                    # results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                    # print(f"ACTIVO FCST 1530 CLOSE-BUY!!!")
                                    msg = f"{self.name} ACTIVO FCST 1530 CLOSE-BUY for {active.parameters.name} action: {results[Constants.IND_PROB_FLOW]}"
                                    self.closeAndNewAction(results, active, Constants.ACTION_BUY)


                            elif results[Constants.CURRENT_ACTION] == Constants.ACTION_SELL:
                                # results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                # print(f"ACTIVO FCST 1530 CLOSE-BUY!!!")
                                msg = f"{self.name} ACTIVO FCST 1530 CLOSE-BUY for {active.parameters.name} action: {results[Constants.IND_PROB_FLOW]}"
                                self.closeAndNewAction(results, active, Constants.ACTION_BUY)

                            elif Constants.ACTION_CLOSE in results[Constants.CURRENT_ACTION]:
                                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                # print(f"ACTIVO FCST 1530 BUY!!!")
                                msg = f"{self.name} ACTIVO FCST 1530 BUY for {active.parameters.name} action: {results[Constants.IND_PROB_FLOW]}"
                                self.applyNewAction(results, active)

                        elif (probFlow == Constants.DIR_DOWN or probFlow == Constants.DIR_PRE_DOWN):
                            # down
                            if active.parameters.name != 'BTCUSD' and active.parameters.name != 'ETHUSD':
                                if results[Constants.CURRENT_ACTION] == Constants.ACTION_BUY:
                                    # print(f"ACTIVO FCST 1530 CLOSE-SELL!!!")
                                    msg = f"{self.name} ACTIVO FCST 1530 CLOSE-SELL for {active.parameters.name} action: {results[Constants.IND_PROB_FLOW]}"
                                    self.closeAndNewAction(results, active, Constants.ACTION_SELL)

                                elif results[Constants.CURRENT_ACTION] == Constants.ACTION_SELL:
                                    if active.parameters.continueFlow == False:
                                        # print(f"ACTIVO FCST 1530 CLOSE-SELL!!!")
                                        msg = f"{self.name} ACTIVO FCST 1530 CLOSE-SELL for {active.parameters.name} action: {results[Constants.IND_PROB_FLOW]}"
                                        self.closeAndNewAction(results, active, Constants.ACTION_SELL)

                                elif Constants.ACTION_CLOSE in results[Constants.CURRENT_ACTION]:
                                    results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                    # print(f"ACTIVO FCST 1530 SELL!!!")
                                    msg = f"{self.name} ACTIVO FCST 1530 SELL for {active.parameters.name} action: {results[Constants.IND_PROB_FLOW]}"
                                    self.applyNewAction(results, active)

            if msg is not None and self.simulation == False:
                self.telegram.enviarMensaje(msg, self.telegram.tokenBot, active.parameters.tele_group)
        except Exception as e:
            print(f"ERROR evaluateFcstPROB {str(e)}")
            message = f"{self.name}  fallo enevaluateFcst  {results[Constants.CURRENT_ACTION]} para {active.parameters.name} error: {str(e)}"
            self.telegram.enviarMensaje(message, self.telegram.tokenBot, self.errorTelegroup)
            self.addmessages(message, results)
            print(e)
            print(f"fallo change state for {active.parameters.name} second: {active.parameters.second_name}")

    def evaluateCloseAction(self, active, results):
        fastReview = False
        currentTime = self.gettime(results)

        if currentTime and currentTime >= int(self.closeStart) and currentTime < int(self.closeEnd):
                #solo si no ha hecho predicciones
                active.parameters.controlWin = True
                fastReview = True
        elif currentTime and currentTime >= int(self.iniStart) and currentTime < int(self.iniEnd):
                #solo si no ha hecho predicciones
                active.parameters.controlWin = True
                fastReview = True


        return fastReview

    def isHour(self, results):
        res = False
        currentTime = None
        from datetime import datetime
        if results[Constants.SIMULATION]:
            temp = results[Constants.DATE].values[0]
            t = datetime.strptime(temp, '%Y-%m-%d %H:%M:%S.%f')
            current_time_h = t.hour * 100
            current_time_min = t.minute
            # print(f" gettime hora : {current_time_h} minutos: {current_time_min}")
            currentTime = int(current_time_h + current_time_min)
        else:
            t = time.localtime()
            current_time_h = time.strftime("%H", t)
            current_time_min = time.strftime("%M", t)
            if current_time_min == 0:
                isHour = True
            currentTime = int(current_time_min)
        # Definir un rango de tolerancia en minutos
        tolerancia_minutos = 5

        # Verificar si el valor de t está cerca de una hora en punto
        minutos = t.minute
        segundos = t.second

        # Calcular la diferencia en minutos y segundos con la hora exacta
        if minutos <= tolerancia_minutos:
            res = True
            # print(f"isHour current time hour: {current_time_h} minutes :{current_time_min}")

        return res

    # #@mide_tiempo
    def calculateHourlyFlow(self, data, results, active):
        data2 = data
        if not isinstance(data2.index, pd.DatetimeIndex):
            data2.index = pd.to_datetime(data2['date'])
        df_hourly = data.resample('1H').first()
        # df_half = data.resample('30T').first()
        df_hourly = df_hourly.dropna()



        # Boollinger
        boolinger = active.parameters.bollinger
        blgMA = df_hourly[self.closeValue].rolling(window=boolinger).mean()
        # EMA_10 = talib.EMA(df_hourly[self.closeValue], timeperiod=10)
        EMA_10 = df_hourly[self.closeValue].ewm(span=10, adjust=False).mean()

        blgMAm0 = EMA_10.iloc[[-1]]
        hourlyM0 = df_hourly.iloc[-1]
        hourlyM2 = None
        blgMAm2 = None
        blgMAm3 = None
        anlgeblgm0 = 0
        hourlyM1 = None
        interval = 30

        results[Constants.HOURLY_ANGLE] = 0
        results[Constants.HOURLY_ANGLE_MED] = 0
        results[Constants.HOURLY_ANGLE_MED_PREV] = 0
        # try:
        #     interval = abs(self.calcular_minutos_entre_fechas(df_hourly.iloc[-1]['date'], data.iloc[-2]['date']))
        #     # angleEMA20 = np.arctan(EMA_20.values[-1] - EMA_20.values[-2]) * (180 / np.pi)
        # except Exception as error:
        #     interval = 30

        # if interval > 60:
        #     interval = 1
        # elif interval < 30:
        #     if "BTCUSD" in active.parameters.name or "ETHUSD" in active.parameters.name:
        #         nada = ""
        #     else:
        #         if interval <= 15:
        #             if self.activeHelper.angleExclusion(results, active.parameters.name):
        #                 interval = interval / 1000
        #             else:
        #                 interval = interval / 100
        #         else:
        #             interval = 1

        # results[Constants.INTERVAL] = interval
        try:
            blgMAm1 = EMA_10.iloc[[-2]]
        except Exception as error:
            blgMAm1 = None

        try:
            blgMAm2 = EMA_10.iloc[[-3]]
        except Exception as error:
            blgMAm2 = None

        try:
            hourlyM1 = df_hourly.iloc[-2]
        except Exception as error:
            hourlyM1 = None



        if blgMAm1 is not None:
            if pd.isna(blgMAm1.values[0]) is not True:
                anlgeblgm0 = math.degrees(math.atan2(blgMAm0.values[0] - blgMAm1.values[0], 1))
                nada = ""
            if pd.isna(anlgeblgm0) is True:
                anlgeblgm0 = 0
            # print(f" angle m0 : {anlgeblgm0}")
            results[Constants.HOURLY_ANGLE_MED] = anlgeblgm0

        if blgMAm2 is not None:
            if pd.isna(blgMAm2.values[0]) is not True:
                anlgeblgm0 = math.degrees(math.atan2(blgMAm1.values[0] - blgMAm2.values[0], 1))
                nada = ""
            if pd.isna(anlgeblgm0) is True:
                anlgeblgm0 = 0
            # print(f" angle m0 : {anlgeblgm0}")
            results[Constants.HOURLY_ANGLE_MED_PREV] = anlgeblgm0

        if hourlyM1 is not None:
            if pd.isna(hourlyM1.values[0]) is not True:
                anlgeblgm0 = math.degrees(math.atan2(hourlyM0.values[1] - hourlyM1.values[1], 1))
                nada = ""
            if pd.isna(anlgeblgm0) is True:
                anlgeblgm0 = 0
            # print(f" angle m0 : {anlgeblgm0}")
            results[Constants.HOURLY_ANGLE] = anlgeblgm0

    def collectFlowAnalisis(self, data, results, active):
        dataTemp = {}
        dataTemp['date'] = results[Constants.DATE].values[0]
        dataTemp['value'] = results[Constants.VALUE]

        if self.showAnallisisFlow:
            if self.drawnEMA_UPDOWN:
                if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_BUY:
                    self.operations.tendenceUP.append(dataTemp)
                elif results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
                    self.operations.tendenceDOWN.append(dataTemp)
                else:
                    self.operations.tendenceWAIT.append(dataTemp)

    def postcalculation(self, data, results, active):

        # UPDATE COUNTER
        angleimaPrev = float(results[Constants.ANGLE_IMA1_PREV])
        angleIma1 = float(results[Constants.ANGLE_IMA1])
        angleImaCounter = int(float(results[Constants.ANGLE_IMA1_COUNTER]))
        angle = float(results[Constants.ANGLE])
        anglePrev = float(results[Constants.ANGLE_PREV])
        angleCounter = int(float(results[Constants.ANGLE_COUNTER]))
        if angleimaPrev != 0:
            if angleimaPrev > 0:
                if angleIma1 > 0:
                    angleImaCounter = angleImaCounter + 1
                else:
                    angleImaCounter = 1
            else:
                if angleIma1 < 0:
                    angleImaCounter = angleImaCounter + 1
                else:
                    angleImaCounter = 1

        if anglePrev != 0:
            if anglePrev > 0:
                if angle > 0:
                    angleCounter = angleCounter + 1
                else:
                    angleCounter = 1
            else:
                if angle < 0:
                    angleCounter = angleCounter + 1
                else:
                    angleCounter = 1
        results[Constants.ANGLE_IMA1_COUNTER] = angleImaCounter
        results[Constants.ANGLE_COUNTER] = angleCounter


    def evaluateActions(self, data, results, active, isFastReview=False):
        fastReview = isFastReview
        try:
            #init values
            results[Constants.SIMULATION] = self.simulation
            results[Constants.ISDBDATA] = self.isDBData
            results[Constants.ONLY_START_END] = self.onlyStartEnd




            self.evaluateIndicators(data, results, active)
            self.evaluateActiveIndicators(results,data, active)
            self.review_results(data, results, active)

            results[Constants.HOURLY_ANGLE] = 0
            results[Constants.HOURLY_ANGLE_MED] = 0
            results[Constants.HOURLY_ANGLE_MED_PREV] = 0
            # self.calculateHourlyFlow(data, results, active)
            # if self.isHour(results):
            #     self.calculateHourlyFlow(data, results, active)
            # else:
            self.collectFlowAnalisis(data,results,active)
            self.postcalculation(data,results,active)
            # if self.simulation:
            startTimeForToday= self.getfirstValueForToday(data,results)
            if startTimeForToday < 1500:

                self.prepare1430()
            else:
                self.updateTimeZoneValues(results)

            # self.calculatePrevRelativeValues(results,active)

            # calula la medi y desviacion para el dia y acumulado de dias
            self.calculatePredictionIndicator(data, results, active)

            if active.parameters.name == "BTCUSD" or active.parameters.name == "ETHUSD":
                self.calculateSpecialIndicatorsBTCETH(results, active)
            else:
                self.calculateSpecialIndicators(results, active)

            self.calculateMinMax(results, data, active)
            self.executeAnalisisHelperMINMAXFlow(results, data, active)
            self.evaluateFinalIndicators(results, data, active)



            # calular los valores de probabilidad final
            try:
                probFlow = self.getPROBMEDSTD_NEWFlow(results, active)
                if probFlow:
                    results[Constants.IND_PROB_FLOW] = probFlow
            except Exception as e:
                print(f"error getPROBMEDSTD_NEWFlow {str(e)}")

            # LLAMA AL EVALUADOR
            active.evaluate(results)
            if self.simulation:
                self.prepareBESTDISTANCE(results)
                if self.needAnalsis:
                    self.printAnalisis(results, active)

            # activa cierres de ganancia puntual y evalua la prediccion a ciertas horas
            # isFastReview = self.evaluateCloseAction(active, results)

            fastReview = self.evaluateNewAction(results, active, isFastReview)

            if self.useConfig == False:
                # update DATABASE
                self.dataBDMan.updateValueWithData(results)
            else:
                self.updateConfig(active, results)
                if self.updateDBSimulation:
                    self.dataBDMan.updateSimulationValues(results)
                    # self.dataBDMan.update_market(results)
            # print(f"active {active.parameters.name} ingnoreProb es {active.parameters.ignoreProb}")
            # EJECUTA la nueva accion en caso de ser distinta a la actual lo hace en horarios
            if self.disableInitProb == False and active.parameters.ignoreProb == False:
                if active.parameters.name == "BTCUSD" or active.parameters.name == "ETHUSD":
                    nada = ""
                else:
                    self.evaluateFcstPROB(results, active)


        except Exception as e:
            fastReview = False
            print(f"ERROR evaluateActions {str(e)}")
            message = f"{self.name} fallo evaluateActions  {results[Constants.CURRENT_ACTION]} para {active.parameters.name} error: {str(e)}"
            self.telegram.enviarMensaje(message, self.telegram.tokenBot, self.errorTelegroup)
            self.addmessages(message, results)
            print(e)
            print(f"fallo change state for {active.parameters.name} second: {active.parameters.second_name}")

        return fastReview

    def inserDataPrices(self, value, active):
        data = None
        try:

            t = time.localtime()
            current_time_h = time.strftime("%H", t)
            current_time_min = time.strftime("%M", t)
            print(f" hora : {current_time_h} minutos: {current_time_min}")

            current_value = float(value[self.closeValue])
            fecha = value['date'].values[0]
            weekno = datetime.datetime.today().weekday()
            days = 2
            if weekno == 0:
                days = 3

            dif = 0
            acu = 0
            acumulate = 0
            tendence_acu = 0
            tendence_count = 0
            oldvalue = 0
            min_value = 999
            min_acu = 0
            max_value = 0
            max_acu = 0
            direction = Constants.DIR_WAIT
            min_dir = 99999
            max_dir = 0
            indi_dir = ''
            action = Constants.ACTION_WAIT
            oldDBvalue = self.dataBDMan.getLastValueWithName(active.parameters.name)
            if oldDBvalue is not None:
                oldvalue = oldDBvalue[0]["value"]

                acumulate = oldDBvalue[0]["acumulate"]
                tendence_acu = oldDBvalue[0]["tendence_acu"]
                tendence_count = oldDBvalue[0]["tendence_count"]
                min_value = oldDBvalue[0]["min_value"]
                min_acu = oldDBvalue[0]["min_acu"]
                max_value = oldDBvalue[0]["max_value"]
                max_acu = oldDBvalue[0]["max_acu"]
                action = oldDBvalue[0]["action"]
                direction = oldDBvalue[0]["direction"]
                min_dir = oldDBvalue[0]["min_dir"]
                max_dir = oldDBvalue[0]["max_dir"]
                indi_dir = oldDBvalue[0]["indi_dir"]
                action_acum = oldDBvalue[0]["action_acum"]
                action_count = oldDBvalue[0]["action_count"]

            self.dataBDMan.inserValue(active.parameters.name, current_value, oldvalue, dif, acumulate, tendence_acu,
                                      tendence_count, min_value,
                                      max_value, min_acu, max_acu, direction, min_dir, max_dir, indi_dir, action_acum,
                                      action_count, action, dateValue=fecha)

            data = self.dataBDMan.getAllWithNameForXdays(active.parameters.name, days)
            # if data is not None:
            # self.log.info(data)
            # oldvalue = oldDBvalue[0]["value"]

        except Exception as e:
            print(f"ERROR inserDataPrices {str(e)}")

        return data

    def search_prices_list_data_simulation(self, actives, data):
        res = None
        for active in actives:
            results = {}

            if data.empty == False and len(data) > 0:
                fastReview = self.evaluateActions(data, results, active)
                # if fastReview == True:
                #     self.evaluateActions(data, results, active,True)
            res = results
        return res

    def search_prices_list_data_simulation_INSERT(self, actives, dataSimulate):

        for active in actives:
            results = {}
            # self.reviewControls(data, active)
            data = self.inserDataPrices(dataSimulate, active)
            if data and len(data) > 0:
                self.evaluateActions(data, results, active)
                if active.parameters.reevaluateAction:
                    self.evaluateActions(data, results, active)

    def calcular_angulo(self,x1, y1, x2, y2):
        # Calcula la diferencia en y y en x
        delta_y = y2 - y1
        delta_x = x2 - x1

        # Calcula el arco tangente de la pendiente
        angulo_radianes = math.atan2(delta_y, delta_x)

        # Convertir el ángulo a grados
        angulo_grados = math.degrees(angulo_radianes)

        return angulo_grados

    def calcular_minutos_entre_fechas(str, fecha1_str, fecha2_str):
        # from datetime import datetime
        # Convertir las cadenas de fecha a objetos datetime
        # fecha1 = datetime.strptime(fecha1_str, "%Y-%m-%d %H:%M:%S")
        try:
            fecha1 = datetime.datetime.strptime(fecha1_str, "%Y-%m-%d %H:%M:%S.%f")
        except Exception as error:
            # print("Error getAllWithNameForXdaysRangeDates  date format using second change", error)
            fecha1 = datetime.datetime.strptime(fecha1_str, "%Y-%m-%d")
        # fecha2 = datetime.strptime(fecha2_str, "%Y-%m-%d %H:%M:%S")

        try:
            fecha2 = datetime.datetime.strptime(fecha2_str, "%Y-%m-%d %H:%M:%S.%f")
        except Exception as error:
            # print("Error getAllWithNameForXdaysRangeDates  date format using second change", error)
            fecha2 = datetime.datetime.strptime(fecha2_str, "%Y-%m-%d")

        # Calcular la diferencia de tiempo entre las dos fechas
        diferencia = fecha2 - fecha1

        # Calcular la diferencia en minutos
        minutos = diferencia.total_seconds() / 60
        # Redondear hacia arriba al próximo entero más cercano
        minutos = math.ceil(minutos)

        return abs(minutos)




    # #@mide_tiempo
    def evaluateIndicators(self, data, results, active):
        ima1, ima2, ima3, ima4, ema_10, ema_20, ema_50, passiveDistance, elements_past, boolinger = self._eval_init_parameters(active)
        
        # Base Rolling Means
        ma5, maNEW, ma20, ma4 = self._eval_base_rolling_means(data, ima1, ima2, ima3, ima4)
        
        # Interval
        interval = self._eval_calculate_interval(data, results, active)
        results[Constants.INTERVAL] = interval
        
        # Init Current Value & Base Results
        currentVal = self._eval_init_base_results(data, results, active)
        
        # Bollinger Bands & Angles (also sets Results)
        blgMA, blgMA_m_values, blgUPPER, blgLOWER, blgSTD = self._eval_bollinger_bands_angles(data, results, active, boolinger, interval, currentVal)
        
        # Exponential Moving Averages
        EMA_10, EMA_20, EMA_50 = self._eval_process_emas(data, results, active, ema_10, ema_20, ema_50, interval, currentVal, blgMA_m_values, blgMA)
        
        # Bollinger Distances
        self._eval_bollinger_distances(results, currentVal, blgMA, blgUPPER, blgLOWER)
        
        # SMA and Momentum (also tendency)
        self._eval_process_smas_and_momentum(data, results, active, currentVal, ma5, maNEW, ma20, ma4, passiveDistance, elements_past)
        
        # Final defaults
        self._eval_set_final_defaults(results)

    def _eval_init_parameters(self, active):
        ima1 = 5
        ima2 = 10
        ima3 = 20
        ima4 = 20
        passiveDistance = 0.00012
        elements_past = 10
        boolinger = 20
        if active is not None:
            passiveDistance = active.parameters.tendence_measure
            ima1 = active.parameters.ima1
            ima2 = active.parameters.ima2
            ima3 = active.parameters.ima3
            ima4 = active.parameters.ima4
            elements_past = active.parameters.tendence_distance
            boolinger = active.parameters.bollinger

        ema_10 = active.parameters.ema10
        ema_20 = active.parameters.ema20
        ema_50 = active.parameters.ema50
        
        return ima1, ima2, ima3, ima4, ema_10, ema_20, ema_50, passiveDistance, elements_past, boolinger

    def _eval_base_rolling_means(self, data, ima1, ima2, ima3, ima4):
        ma5 = data[self.closeValue].rolling(ima1).mean()
        maNEW = data[self.closeValue].rolling(ima2).mean()
        ma20 = data[self.closeValue].rolling(ima3).mean()
        ma4 = data[self.closeValue].rolling(ima4).mean()
        return ma5, maNEW, ma20, ma4

    def _eval_calculate_interval(self, data, results, active):
        interval = 30
        try:
            interval = abs(self.calcular_minutos_entre_fechas(data.iloc[-1]['date'], data.iloc[-2]['date']))
        except Exception as error:
            interval = 30
        if interval == 0:
            interval = 1
        intervalCpy = interval

        if interval > 60:
            interval = 1
        elif interval < 30:
            if "BTCUSD" in active.parameters.name or "ETHUSD" in active.parameters.name:
                nada = ""
            else:
                if interval <= 15:
                    if self.activeHelper.angleExclusion(results, active.parameters.name):
                        interval = interval / 1000
                    else:
                        if interval <= 5:
                            interval = (interval / 10) / intervalCpy
                        else:
                            interval = interval / 100
                else:
                    interval = 1
        return interval

    def _eval_init_base_results(self, data, results, active):
        current = data.iloc[[-1]]
        currentVal = float(current[self.closeValue].iloc[0])
        
        if Constants.VALUE not in results:
            results[Constants.VALUE] = currentVal
            if results[Constants.ISDBDATA]:
                results[Constants.DATE] = current['date'].values[0]
            else:
                results[Constants.DATE] = current.index.values[0]

            results[Constants.INDICATOR_DISTANCE] = 0
            results[Constants.CHANGE_ACTION] = 0
            results[Constants.REVENUE] = 0
            results[Constants.MEDIA] = 0
            results[Constants.STDDESV] = 0
            results[Constants.ACTION_COUNT] = 0
            results[Constants.MEDSTDDIFF] = 0
            if Constants.MESSAGES not in results:
                results[Constants.MESSAGES] = " "

            if Constants.INDICATOR_TENDENCE not in results:
                results[Constants.INDICATOR_TENDENCE] = Constants.INDICATOR_T_WAIT
        if Constants.IMA5MA20 not in results:
            results[Constants.IMA5MA20] = Constants.INDICATOR_EMPTY

        price_range_periods = active.parameters.price_range_periods  # 6 horas a 15min/velas
        price_range_percent = 0
        if len(data) >= price_range_periods:
            recent_closes = data[self.closeValue].iloc[-price_range_periods:]
            max_price = recent_closes.max()
            min_price = recent_closes.min()
            if currentVal != 0:
                price_range_percent = ((max_price - min_price) / currentVal) * 100
                
        results[Constants.PRICE_RANGE_PERCENT] = float(price_range_percent)
            
        return currentVal

    def _eval_bollinger_bands_angles(self, data, results, active, boolinger, interval, currentVal):
        import math
        blgMA = data[self.closeValue].rolling(window=boolinger).mean()
        self.analisisHelper.evaluate_MABLG_PERCENT(results, blgMA, active)
        blgSTD = data[self.closeValue].rolling(window=boolinger).std()

        blgMAm0 = blgMA.iloc[[-1]]
        blgMAm1, blgMAm2, blgMAm3, blgMAm5 = None, None, None, None
        anlgeblgm0, anlgeblgm1, anlgeblgm2 = 0, 0, 0

        try: blgMAm1 = blgMA.iloc[[-2]]
        except: pass
        try: blgMAm2 = blgMA.iloc[[-3]]
        except: pass
        try: blgMAm3 = blgMA.iloc[[-4]]
        except: pass
        try:
            madays = int(active.parameters.ma_dist_int) * -1
            blgMAm5 = blgMA.iloc[[madays]]
        except: pass

        if blgMAm1 is not None and not blgMAm1.isna().iloc[0]:
            anlgeblgm0 = math.degrees(math.atan2(blgMAm0.values[0] - blgMAm1.values[0], interval))
        if blgMAm2 is not None and not blgMAm2.isna().iloc[0] and blgMAm1 is not None:
            anlgeblgm1 = math.degrees(math.atan2(blgMAm1.values[0] - blgMAm2.values[0], interval))
        if blgMAm3 is not None and not blgMAm3.isna().iloc[0] and blgMAm2 is not None:
            anlgeblgm2 = math.degrees(math.atan2(blgMAm2.values[0] - blgMAm3.values[0], interval))

        blaMA05_dist = 0
        if blgMAm5 is not None and not blgMAm5.isna().iloc[0]:
            blaMA05_dist = blgMAm0.values[0] - blgMAm5.values[0]

        blaMA03_dist = 0
        if blgMAm3 is not None and not blgMAm3.isna().iloc[0]:
            blaMA03_dist = blgMAm0.values[0] - blgMAm3.values[0]

        results[Constants.BLG_MA_X] = blaMA05_dist
        results[Constants.BLG_MA_VAL] = blgMAm0.values[0]
        
        results[Constants.ANGLE] = anlgeblgm0
        results[Constants.ANGLEm1] = anlgeblgm1
        results[Constants.ANGLEm21] = anlgeblgm2

        blgUPPER = blgMA + 2 * blgSTD
        blgLOWER = blgMA - 2 * blgSTD
        
        blgMA_m_values = {
            'blgMAm0': blgMAm0,
            'blgMAm1': blgMAm1,
            'blgMAm2': blgMAm2,
            'blgMAm3': blgMAm3,
            'blgMAm5': blgMAm5
        }

        return blgMA, blgMA_m_values, blgUPPER, blgLOWER, blgSTD

    def _eval_process_emas(self, data, results, active, ema_10, ema_20, ema_50, interval, currentVal, blgMA_m_values, blgMA):
        import math
        import numpy as np
        EMA_10 = data[self.closeValue].ewm(span=ema_10, adjust=False).mean()
        EMA_20 = data[self.closeValue].ewm(span=ema_20, adjust=False).mean()
        EMA_50 = data[self.closeValue].ewm(span=ema_50, adjust=False).mean()

        emaIndicator = Constants.INDICATOR_EMA_WAIT
        emaIndicatorCheck = Constants.INDICATOR_EMA_WAIT
        angleEMA, angleEMAm1, angleEMA20, emaDst, angleEMA10 = 0, 0, 0, 0, 0
        angle_ema_flow = Constants.FLUJO_MANTIENE

        if not EMA_10.isna().iloc[-1] and not EMA_20.isna().iloc[-1]:
            emaDst = EMA_10.values[-1] - EMA_20.values[-1]
            if EMA_10.values[-1] > EMA_20.values[-1]:
                emaIndicator = Constants.INDICATOR_EMA_BUY
            else:
                emaIndicator = Constants.INDICATOR_EMA_SELL

            n = 5
            if len(EMA_10.dropna()) > n:
                slopeEMA10 = (EMA_10 - EMA_10.shift(n)) / n
                slopeEMA10 = slopeEMA10.dropna()
                if len(slopeEMA10) > n:
                    angleEMA10 = np.degrees(np.arctan(slopeEMA10)).iloc[-1]

            if currentVal > EMA_10.values[-1]:
                emaIndicatorCheck = Constants.INDICATOR_EMA_BUY
            else:
                emaIndicatorCheck = Constants.INDICATOR_EMA_SELL

        results[Constants.EMA_DST] = float(emaDst)
        results[Constants.EMA10_ANGLE] = angleEMA10


        slopeEMA10_val = 0
        if len(EMA_10.dropna()) > n:
            past_ema10 = EMA_10.shift(n)
            diff_ema10 = EMA_10 - past_ema10
            denom_10 = past_ema10.replace(0, 1)
            slopeEMA10_calc = diff_ema10 / denom_10
            slopeEMA10_calc = slopeEMA10_calc.dropna()
            if len(slopeEMA10_calc) > 0:
                slopeEMA10_val = slopeEMA10_calc.iloc[-1]
                
        results[Constants.EMA10_SLOPE] = float(slopeEMA10_val)

        slopeEMA20_val = 0
        if len(EMA_20.dropna()) > n:
            past_ema20 = EMA_20.shift(n)
            diff_ema20 = EMA_20 - past_ema20
            # Evitar división por cero
            denom = past_ema20.replace(0, 1)
            slopeEMA20 = diff_ema20 / denom
            slopeEMA20 = slopeEMA20.dropna()
            if len(slopeEMA20) > 0:
                slopeEMA20_val = slopeEMA20.iloc[-1]
                
        results[Constants.EMA20_SLOPE] = float(slopeEMA20_val)

        emaSpread = 0
        if currentVal != 0 and not EMA_10.isna().iloc[-1] and not EMA_20.isna().iloc[-1]:
            emaSpread = abs(EMA_10.values[-1] - EMA_20.values[-1]) / currentVal
        results[Constants.EMA_SPREAD] = float(emaSpread)

        cross_periods = active.parameters.cross_periods  # 24 periodos de 15 min = 6 horas
        cross_count = 0
        if len(EMA_10.dropna()) > cross_periods and len(EMA_20.dropna()) > cross_periods:
            ema_above = EMA_10 > EMA_20
            # Detectar cambios de estado entre periodos consecutivos (Cruces)
            crosses = ema_above != ema_above.shift(1)
            # ignorar el primer valor NA si estuviera en el corte, sumar el booleano
            cross_count = int(crosses.iloc[-cross_periods:].sum())
            
        results[Constants.EMA_CROSS_COUNT] = cross_count

        currEMA50Dis = 0
        currEMA50Ind = Constants.INDICATOR_EMA_WAIT
        if not EMA_50.isna().iloc[-1]:
            currEMA50Dis = currentVal - EMA_10.values[-1]
            if EMA_50.values[-1] > currentVal:
                currEMA50Ind = Constants.INDICATOR_EMA_SELL
            else:
                currEMA50Ind = Constants.INDICATOR_EMA_BUY

        results[Constants.INDICATOR_EMA50_DST] = float(currEMA50Dis)
        results[Constants.INDICATOR_EMA50] = currEMA50Ind

        valueEMAm1, valueEMA20m1, valueEMAm2, valueEMA20m2, valueEMAm3 = None, None, None, None, None
        try: valueEMAm1 = EMA_10.iloc[[-1]]
        except: pass
        try: valueEMA20m1 = EMA_20.iloc[[-1]]
        except: pass
        try: valueEMAm2 = EMA_10.iloc[[-2]]
        except: pass
        try: valueEMA20m2 = EMA_20.iloc[[-2]]
        except: pass
        try: valueEMAm3 = EMA_10.iloc[[-3]]
        except: pass

        currvalEma10 = 0
        if valueEMAm1 is not None and not valueEMAm1.isna().iloc[0]:
            currvalEma10 = currentVal - float(valueEMAm1.values[0])
        results[Constants.CURRVAL_EMA_DST] = currvalEma10

        ema10_blg_dist, ema20_blg_dist = 0, 0
        blgMAm0 = blgMA_m_values['blgMAm0']
        if not EMA_10.isna().iloc[-1] and not EMA_20.isna().iloc[-1]:
            ema10_blg_dist = float(valueEMAm1.values[0]) - float(blgMAm0.values[0])
            ema20_blg_dist = float(valueEMA20m1.values[0]) - float(blgMAm0.values[0])

        results[Constants.EMA10_BLG_DST] = ema10_blg_dist
        results[Constants.EMA20_BLG_DST] = ema20_blg_dist

        # IMA DIFF (omitted ima angle logic inside ema for brevity, kept exactly as logic was slightly detached, waiting to combine)
        # In original, angleIma1 came from ma5.
        angleIma1 = 0
        ima1 = active.parameters.ima1 if active else 5
        ma5 = data[self.closeValue].rolling(ima1).mean()
        angleima10, angleima11 = None, None
        try: angleima10 = ma5.iloc[[-1]]
        except: pass
        try: angleima11 = ma5.iloc[[-2]]
        except: pass
        if angleima11 is not None and not angleima11.isna().iloc[0]:
            angleIma1 = math.degrees(math.atan2(angleima10.values[0] - angleima11.values[0], interval))
        
        imaEmaDiff = 0
        if valueEMAm1 is not None and angleima10 is not None and not valueEMAm1.isna().iloc[0] and not angleima10.isna().iloc[0]:
            imaEmaDiff = float(angleima10.values[0]) - float(valueEMAm1.values[0])
        results[Constants.IMA1EMADIFF] = imaEmaDiff

        if valueEMA20m2 is not None:
            angleEMA20 = math.degrees(math.atan2(EMA_20.values[-1] - EMA_20.values[-2], interval))
        if valueEMAm2 is not None:
            angleEMA = math.degrees(math.atan2(EMA_10.values[-1] - EMA_10.values[-2], interval))
        if valueEMAm3 is not None:
            angleEMAm1 = math.degrees(math.atan2(EMA_10.values[-2] - EMA_10.values[-3], interval))
            if angleEMA > angleEMAm1:
                angle_ema_flow = Constants.FLUJO_SUBE
            elif angleEMA < angleEMAm1:
                angle_ema_flow = Constants.FLUJO_BAJA

        results[Constants.ANGLE_EMA] = angleEMA
        results[Constants.ANGLE_IMA1] = angleIma1
        results[Constants.ANGLE_IMA1_COUNTER] = 1
        results[Constants.ANGLE_COUNTER] = 1
        results[Constants.ANGLE_EMA20] = angleEMA20
        results[Constants.ANGLE_EMAm1] = angleEMAm1
        results[Constants.ANGLE_EMA_FLOW] = angle_ema_flow
        results[Constants.INDICATOR_EMA] = emaIndicator
        results[Constants.INDICATOR_EMA_CHECK] = emaIndicatorCheck
        
        return EMA_10, EMA_20, EMA_50

    def _eval_bollinger_distances(self, results, currentVal, blgMA, blgUPPER, blgLOWER):
        blgAction = Constants.IND_BLG_MED_WAIT
        if not blgMA.isna().iloc[-1]:
            if currentVal > blgMA.values[-1]:
                blgAction = Constants.IND_BLG_MED_BUY
            else:
                blgAction = Constants.IND_BLG_MED_SELL
        results[Constants.IND_BLG] = blgAction

        blgMedDist = 0
        if not blgMA.isna().iloc[-1]:
            blgMedDist = currentVal - float(blgMA.values[-1])
        results[Constants.IND_BLG_MED_DST] = blgMedDist

        blgUpperDist, blgLowerDist = 0, 0
        if not blgUPPER.isna().iloc[-1]:
            blgUpperDist = float(blgUPPER.values[-1]) - currentVal
        results[Constants.IND_BLG_UPPER_DST] = blgUpperDist

        if not blgLOWER.isna().iloc[-1]:
            blgLowerDist = currentVal - float(blgLOWER.values[-1])
        results[Constants.IND_BLG_LOWER_DST] = blgLowerDist

        totalDst = blgUpperDist + blgLowerDist
        blgupperPercent, blgLowerPercent = 0, 0
        if blgUpperDist != 0:
            blgupperPercent = blgUpperDist * 100 / totalDst
        results[Constants.IND_BLG_UPPER_DST_PERCENT] = blgupperPercent

        if blgLowerDist != 0:
            blgLowerPercent = blgLowerDist * 100 / totalDst
        results[Constants.IND_BLG_LOWER_DST_PERCENT] = blgLowerPercent

        middlePercent = abs(blgLowerPercent) - 50
        results[Constants.IND_BLG_MIDDLE_DST_PERCENT] = middlePercent

        blgBandwidth = 0
        if not blgUPPER.isna().iloc[-1] and not blgLOWER.isna().iloc[-1] and not blgMA.isna().iloc[-1]:
            ma_val = float(blgMA.values[-1])
            if ma_val != 0:
                blgBandwidth = (float(blgUPPER.values[-1]) - float(blgLOWER.values[-1])) / ma_val
        results[Constants.BLG_BANDWIDTH] = float(blgBandwidth)

    def _eval_process_smas_and_momentum(self, data, results, active, currentVal, ma5, maNEW, ma20, ma4, passiveDistance, elements_past):
        ima5ema20 = Constants.INDICATOR_EMA_WAIT
        emaDst = 0
        if not ma5.isna().iloc[-1] and not ma20.isna().iloc[-1]:
            emaDst = ma5.values[-1] - ma20.values[-1]
            if ma5.values[-1] > ma20.values[-1]:
                ima5ema20 = Constants.INDICATOR_EMA_BUY
            else:
                ima5ema20 = Constants.INDICATOR_EMA_SELL
        results[Constants.IMA5MA20] = ima5ema20
        results[Constants.IMA5MA20_DST] = emaDst

        ma20Value = float(ma20.iloc[-1])
        ma5Value = float(ma5.iloc[-1])
        maNEWValue = float(maNEW.iloc[-1])
        ma4Value = float(ma4.iloc[-1])

        results[Constants.IMA_NEW] = Constants.IMA_NEW_WAIT
        if currentVal > maNEWValue:
            results[Constants.IMA_NEW] = Constants.IMA_NEW_BUY
        elif maNEWValue > currentVal:
            results[Constants.IMA_NEW] = Constants.IMA_NEW_SELL

        results[Constants.IMA1] = Constants.IMA1_WAIT
        if currentVal > ma5Value:
            results[Constants.IMA1] = Constants.IMA1_BUY
        elif ma5Value > currentVal:
            results[Constants.IMA1] = Constants.IMA1_SELL
            
        ima1_distance = abs(float(ma5Value) - float(currentVal))
        import pandas as pd
        if pd.isna(ima1_distance):
            ima1_distance = 0
        results[Constants.IMA1_DISTANCE] = ima1_distance
        
        if ma20Value > ma5Value:
            results[Constants.MARKET_TENDENCE] = Constants.MARKET_TENDENCE_DOWN
        elif ma20Value < ma5Value:
            results[Constants.MARKET_TENDENCE] = Constants.MARKET_TENDENCE_UP
        else:
            results[Constants.MARKET_TENDENCE] = Constants.MARKET_TENDENCE_UNDEF

        if not pd.isna(ma20Value):
            current_distance = float(currentVal) - float(ma20Value)
            if ma20Value > currentVal:
                if ma5Value > currentVal:
                    results[Constants.INDICATOR] = Constants.INDICATOR_SELLX
                else:
                    results[Constants.INDICATOR] = Constants.INDICATOR_SELL
            elif ma20Value < currentVal:
                if ma5Value < currentVal:
                    results[Constants.INDICATOR] = Constants.INDICATOR_BUYX
                else:
                    results[Constants.INDICATOR] = Constants.INDICATOR_BUY
            else:
                results[Constants.INDICATOR] = Constants.INDICATOR_WAIT

            results[Constants.INDICATOR_DISTANCE] = current_distance
        else:
            results[Constants.INDICATOR] = Constants.INDICATOR_WAIT

        self.determinarRelativePercent(data, results, active)

        if not pd.isna(ma4Value):
            self.determinarIndicatorTendenceBOTHIma4Best(data, ma4, results, active)
        else:
            results[Constants.INDICATOR_MED] = Constants.INDICATOR_TM_WAIT
            results[Constants.INDICATOR_STD] = Constants.INDICATOR_TSTD_MID
            results[Constants.INDICATOR_MED_STD] = Constants.INDICATOR_M_STD_WAIT
            results[Constants.INDICATOR_MED_MOMENT] = Constants.INDICATOR_TM_UNDEF
            results[Constants.STD_MOMENT] = 0
            results[Constants.MEDIA_MOMENT] = 0
            results[Constants.INDICATOR_MED_MOMENT_VALUE] = 0
            results[Constants.MEDSTDDIFF] = 0

        if not pd.isna(maNEWValue):
            self.determinarIndicatorTendence(maNEW, elements_past, results, maNEWValue, passiveDistance)
            self.determinarIndicatorTendenceMomentBest(maNEW, ma4, results, active)
        else:
            results[Constants.INDICATOR_MED_MOMENT] = Constants.INDICATOR_TM_UNDEF
            results[Constants.STD_MOMENT] = 0
            results[Constants.MEDIA_MOMENT] = 0
            results[Constants.INDICATOR_MED_MOMENT_VALUE] = 0
            results[Constants.MARKET_ANGLE] = 0
            results[Constants.MARKET_ANGLE_TANG] = 0

    def _eval_set_final_defaults(self, results):
        results[Constants.WEEK_FLOW] = Constants.WEEK_FLOW_UNDEF
        results[Constants.WEEK_FLOW_PREV] = Constants.WEEK_FLOW_UNDEF
        results[Constants.WEEK_FLOW_PREV_MED] = 0
        results[Constants.WEEK_FLOW_ABSVAL] = 0
        results[Constants.WEEK_FLOW_MED] = 0
        results[Constants.WEEK_FLOW_MED_LEVEL] = Constants.WEEK_FLOW_MED_LEVEL_UNDEF
        results[Constants.WEEK_DIR] = Constants.WEEK_FLOW_UNDEF
        results[Constants.WEEK_MIN_DIR] = 0
        results[Constants.WEEK_MAX_DIR] = 0
        results[Constants.WEEK_DIR_TOP_DST] = 0
        results[Constants.WEEK_DIR_BOT_DST] = 0
        results[Constants.WEEK_DIR_BOT_DST_PREV] = 0
        results[Constants.WEEK_DIR_FLOW_DIFF] = 0
        results[Constants.WEEK_DIR_FLOW] = Constants.WEEK_FLOW_UNDEF
        results[Constants.IND_PROB_FLOW] = Constants.DIR_WAIT
        results[Constants.RSI] = 0
    # #@mide_tiempo
    def executeAnalisisHelper(self, results, data, active, start, end):
        self.analisisHelper.getWeekDirection(results, data, active, start, end)

    # #@mide_tiempo
    def executeAnalisisHelperMINMAXFlow(self, results, data, active):
        self.analisisHelper.getMinMaxFlow(results, data, active)


    def evaluateActiveIndicators(self, results, data, active):
        self.analisisHelper.evaluateActiveIndicators(results, data, active)
        self.analisisHelper.calculate_rsi_metrics(results, data, active)
        self.analisisHelper.calculate_market_trend(results, data, active)
        # self.analisisHelper.calculate_order_flow_metrics(results, data, active)



    def calculateMinMax(self, results, data, active):
        try:
            param = self.config_obj[active.parameters.name]
            minweek = param['minweek']
            maxweek = param['maxweek']
            minmonth = param['minmonth']
            maxmonth = param['maxmonth']
            results[Constants.MIN_WEEK] = float(minweek)
            results[Constants.MAX_WEEK] = float(maxweek)
            results[Constants.MIN_MONTH] = float(minmonth)
            results[Constants.MAX_MONTH] = float(maxmonth)

        except Exception as e:
            print(f"ERROR calculateMinMax useConfig {str(e)}")
            param = self.createConfig(active)
            act = 'WAIT'
            act_val = 0
        self.analisisHelper.calculateMinMax(results,data,active)
        self.updateConfig(active, results)

    def evaluateFinalIndicators(self, results, data, active):
        self.analisisHelper.determineAngleFlow(results,data,active)

        # # RSI
        # self.analisisHelper.determineRSI(results,data,active)
        #
        # # SMA
        # self.analisisHelper.determineSMA_FAST_SLOW(results, data, active)
        #
        # # MACD
        # self.analisisHelper.determineMACD(results, data, active)
        #
        # RSI_OVERSOLD = 30
        # RSI_OVERBOUGHT = 70
        #
        sma_signal = False
        # if (pd.isna(results[Constants.SMA_FAST]) is not True) and (pd.isna(results[Constants.SMA_FAST]) is not True):
        #     sma_signal = results[Constants.SMA_FAST] > results[Constants.SMA_SLOW]
        rsi_signal = False
        # if (pd.isna(results[Constants.RSI]) is not True):
        #     rsi_signal = results[Constants.RSI] < RSI_OVERSOLD or results[Constants.RSI] > RSI_OVERBOUGHT
        #
        macd_signal = False
        # if (pd.isna(results[Constants.MACD]) is not True) and (pd.isna(results[Constants.MACD_SIGNAL]) is not True):
        #     macd_signal = results[Constants.MACD] > results[Constants.MACD_SIGNAL]
        #
        results[Constants.SMA_SIGNAL] = sma_signal
        # results[Constants.RSI_SIGNAL] = rsi_signal
        results[Constants.MACD_SIGNAL_OK] = macd_signal
        #
        action_test = "NADA"
        # if sma_signal and rsi_signal and macd_signal and results[Constants.RSI] < RSI_OVERSOLD:
        #     action_test =  'BUY'
        # elif (not sma_signal or not macd_signal) and results[Constants.RSI]  > RSI_OVERBOUGHT:
        #     action_test = 'SELL'
        #
        results[Constants.ACTION_TEST] = action_test

    # #@mide_tiempo
    def calculareWeekIndicator(self, results, active):

        end_date_time = datetime.datetime.strptime(results[Constants.DATE].values[0], "%Y-%m-%d %H:%M:%S.%f")
        end_date_time = end_date_time.replace(second=0, microsecond=0)
        end_date_time =end_date_time + datetime.timedelta(minutes=5)

        end_date = end_date_time.strftime("%Y-%m-%d %H:%M:%S.%f")

        start_date_time = end_date_time + datetime.timedelta(days=-6)
        # start_date_time = start_date_time.replace(second=0, microsecond=0)

        start_date = start_date_time.strftime("%Y-%m-%d %H:%M:%S.%f")

        data = self.dataBDMan.getAllWithNameForXdaysRangeDatesExactdays(active.parameters.name, start_date, end_date)

        self.executeAnalisisHelper(results,data, active,start_date, end_date)
        df_hourly = None
        # try:
        #
        #     if not isinstance(data.index, pd.DatetimeIndex):
        #         data.index = pd.to_datetime(data['date'])
        #     df_hourly = data.resample('H').first()
        #     # df_half = data.resample('30T').first()
        #     df_hourly = df_hourly.dropna()

        # except Exception as error:
        #     print("Error df_hourly ", error)

        # end_dateyh= end_date_time.strftime("%Y-%m-%dT%H:%M:%S.%f")
        # start_dateyh = start_date_time.strftime("%Y-%m-%dT%H:%M:%S.%f")
        # dataYahho = yf.download(tickers=active.parameters.name, interval='1h', start=start_date_time, end=end_date_time)


        self.determinarFlujoSTDMEDIAWEEK(data,results, active)
        # self.determinarFlujoSTDMEDIAWEEK_HOURLY(df_hourly,results, active)


    def getDifTimeFromOpen(self, results):
        temp = results[Constants.DATE].values[0]
        t = datetime.datetime.strptime(temp, '%Y-%m-%d %H:%M:%S.%f')
        current_time_h = t.hour * 100
        current_time_min = t.minute
        # print(f" gettime hora : {current_time_h} minutos: {current_time_min}")
        currentTime = int(current_time_h + current_time_min)
        openHour = int(self.iniStart)
        dif = currentTime - openHour
        return dif

    def getProbFlow(self, results, active):
        res = Constants.DIR_WAIT
        try:
            percent = results[Constants.IND_REL_FCST_PERCENT]
            fcst = results[Constants.IND_REL_FCST]
            week = results[Constants.WEEK_FLOW]
            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            diftimeOpen = self.getDifTimeFromOpen(results)
            if diftimeOpen <= 60:
                # menos de 60 minutos de apertura
                if fcst == Constants.IND_REL_FCST_PRE_UP or fcst == Constants.IND_REL_FCST_UP:
                    if percent < 70:
                        res = Constants.DIR_UP
                if fcst == Constants.IND_REL_FCST_DOWN_INV_REL:
                    if percent < 7:
                        res = Constants.DIR_UP
                if fcst == Constants.IND_REL_FCST_PRE_DOWN or fcst == Constants.IND_REL_FCST_DOWN:
                    if percent > 40:
                        res = Constants.DIR_DOWN
                if fcst == Constants.IND_REL_FCST_UP_INV_REL:
                    if percent > 95:
                        res = Constants.DIR_DOWN
            else:
                # mas de 60 minutos de apertura
                if fcst == Constants.IND_REL_FCST_PRE_UP:
                    if percent > 30 and percent < 70:
                        res = Constants.DIR_UP
                    elif percent > 5 and percent <= 30:
                        if med > 0:
                            if absmed > std:
                                res = Constants.DIR_UP
                            else:
                                res = Constants.DIR_PRE_UP
                if fcst == Constants.IND_REL_FCST_UP:
                    if percent > 5 and percent < 70:
                        if med > 0:
                            if absmed > std:
                                res = Constants.DIR_UP
                            else:
                                res = Constants.DIR_PRE_UP
                if fcst == Constants.IND_REL_FCST_DOWN_INV_REL:
                    if percent < 7:
                        if med > 0:
                            if absmed > std:
                                res = Constants.DIR_UP
                            else:
                                res = Constants.DIR_PRE_UP
                    else:
                        if med < 0:
                            if absmed > std:
                                res = Constants.DIR_DOWN

                if fcst == Constants.IND_REL_FCST_PRE_DOWN:
                    if percent > 40 and percent < 90:
                        res = Constants.DIR_DOWN
                    elif percent > 5 and percent <= 40:
                        if med < 0:
                            if absmed > std:
                                res = Constants.DIR_DOWN
                            else:
                                res = Constants.DIR_PRE_DOWN

                if fcst == Constants.IND_REL_FCST_DOWN:
                    if percent > 30 and percent < 95:
                        if med < 0:
                            if absmed > std:
                                res = Constants.DIR_DOWN
                            else:
                                res = Constants.DIR_PRE_DOWN
                if fcst == Constants.IND_REL_FCST_UP_INV_REL:
                    if percent > 95:
                        if med < 0:
                            if absmed > std:
                                res = Constants.DIR_DOWN
                            else:
                                res = Constants.DIR_PRE_DOWN
                    else:
                        if med > 0:
                            if absmed > std:
                                res = Constants.DIR_UP
        except Exception as error:
            print("Error getProbFlow ", error)
        return res

    def determineMedMomentFlow(self, medMoment, absMedMoment, stdMoment, direction):
        res = ""
        if medMoment < 0:
            # baja
            if absMedMoment > stdMoment:
                res = Constants.DIR_DOWN
            else:
                if direction == Constants.DIR_UP or direction == Constants.DIR_PRE_UP:
                    res = Constants.DIR_PRE_UP
                elif direction == Constants.DIR_DOWN or direction == Constants.DIR_PRE_DOWN:
                    res = Constants.DIR_PRE_DOWN
                else:
                    res = Constants.DIR_PRE_DOWN
        else:
            # SUBE
            if absMedMoment > stdMoment:
                res = Constants.DIR_UP
            else:
                if direction == Constants.DIR_UP or direction == Constants.DIR_PRE_UP:
                    res = Constants.DIR_PRE_UP
                elif direction == Constants.DIR_DOWN or direction == Constants.DIR_PRE_DOWN:
                    res = Constants.DIR_PRE_DOWN
                else:
                    res = Constants.DIR_PRE_UP
        return res

    def determine_Direction_percent_Flow(self, direction, percentFlow):

        if direction == Constants.DIR_UP or direction == Constants.DIR_PRE_UP:
            if percentFlow == Constants.DIR_UP:
                res = Constants.DIR_PRE_UP
            else:
                res = Constants.DIR_PRE_DOWN
        else:
            if percentFlow == Constants.DIR_DOWN:
                res = Constants.DIR_PRE_DOWN
            else:
                res = Constants.DIR_PRE_UP
        return res

    def getProMEDSTD_MID(self, results):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            week = results[Constants.WEEK_FLOW]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_med_abs = results[Constants.WEEK_FLOW_MED]
            week_std = results[Constants.WEEK_FLOW_STD]
            direction = Constants.DIR_WAIT
            if Constants.DIRECTION in results:
                direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            if prevPercent is not None:
                prevPercent = float(prevPercent)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]
            if med == 0:
                if direction == Constants.DIR_UP:
                    med = 1
                elif direction == Constants.DIR_DOWN:
                    med = -1
            percentFlow = Constants.DIR_WAIT
            if percent > prevPercent:
                percentFlow = Constants.DIR_UP
            else:
                # baja
                percentFlow = Constants.DIR_DOWN
            # CALCULOS final del dia
            if fcst == Constants.IND_REL_FCST_PRE_UP or fcst == Constants.IND_REL_FCST_UP:
                if percent >= 0 and percent < 95:
                    if med > 0:
                        if absmed > std:
                            res = Constants.DIR_UP
                        else:
                            res = Constants.DIR_PRE_UP
                    else:
                        if absmed > std:
                            res = Constants.DIR_DOWN
                        else:
                            # contradiccion revisar week
                            if week_med > 0:
                                # sube
                                if week_med_abs > week_std:
                                    res = Constants.DIR_UP
                                else:
                                    res = Constants.DIR_PRE_UP
                            else:
                                # baja
                                res = Constants.DIR_PRE_DOWN

                elif percent >= 95:
                    if med < 0:
                        if absmed > std:
                            res = Constants.DIR_DOWN
                        else:
                            res = Constants.DIR_PRE_DOWN
                    if med >= 0:
                        if absmed > std:
                            res = Constants.DIR_UP
                        else:
                            # fix se añade direction
                            if direction == Constants.DIR_UP or direction == Constants.DIR_PRE_UP:
                                res = Constants.DIR_UP
                            else:
                                if percentFlow == Constants.DIR_UP:
                                    res = Constants.DIR_PRE_UP
                                else:
                                    res = Constants.DIR_PRE_DOWN

            if fcst == Constants.IND_REL_FCST_DOWN_INV_REL:
                if percent > 10 and percent <= 100:
                    if med > 0:
                        if absmed > std:
                            res = Constants.DIR_UP
                        else:
                            res = Constants.DIR_PRE_UP
                    else:
                        if absmed > std:
                            res = Constants.DIR_DOWN
                        else:
                            res = Constants.DIR_PRE_DOWN
                elif percent <= 10:
                    if med >= 0:
                        if absmed > std:
                            res = Constants.DIR_UP
                        else:
                            res = Constants.DIR_PRE_UP
                    if med < 0:
                        if absmed > std:
                            res = Constants.DIR_DOWN
                        else:
                            # res = Constants.DIR_PRE_UP
                            # fix se añade direction
                            if direction == Constants.DIR_DOWN or direction == Constants.DIR_PRE_DOWN:
                                res = Constants.DIR_DOWN
                            else:
                                if percentFlow == Constants.DIR_UP:
                                    res = Constants.DIR_PRE_UP
                                else:
                                    res = Constants.DIR_PRE_DOWN

            if fcst == Constants.IND_REL_FCST_PRE_DOWN or fcst == Constants.IND_REL_FCST_DOWN:
                if percent > 10 and percent <= 100:
                    if med < 0:
                        if absmed > std:
                            res = Constants.DIR_DOWN
                        else:
                            res = Constants.DIR_PRE_DOWN
                    elif med > 0:
                        if absmed >= std:
                            res = Constants.DIR_UP
                        else:
                            # contradiccion revisar week
                            if week_med < 0:
                                # baja
                                if week_med_abs > week_std:
                                    res = Constants.DIR_DOWN
                                else:
                                    res = Constants.DIR_PRE_DOWN
                            else:
                                # sube
                                res = Constants.DIR_PRE_UP

                elif percent > 0 and percent <= 10:
                    if med > 0:
                        if absmed > std:
                            res = Constants.DIR_UP
                        else:
                            res = Constants.DIR_PRE_UP
                    elif med < 0:
                        if absmed > std:
                            res = Constants.DIR_DOWN
                        else:
                            if direction == Constants.DIR_DOWN or direction == Constants.DIR_PRE_DOWN:
                                res = Constants.DIR_DOWN
                            else:
                                if percentFlow == Constants.DIR_UP:
                                    res = Constants.DIR_PRE_UP
                                else:
                                    res = Constants.DIR_PRE_DOWN
                elif percent == 0:
                    if medMoment >= 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_UP
                        else:
                            res = Constants.DIR_PRE_UP
                    if medMoment < 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_DOWN
                        else:
                            # res = Constants.DIR_PRE_DOWN
                            if direction == Constants.DIR_DOWN or direction == Constants.DIR_PRE_DOWN:
                                res = Constants.DIR_DOWN
                            else:
                                if percentFlow == Constants.DIR_UP:
                                    res = Constants.DIR_PRE_UP
                                else:
                                    res = Constants.DIR_PRE_DOWN

            if fcst == Constants.IND_REL_FCST_UP_INV_REL:
                if percent >= 0 and percent < 95:
                    if med > 0:
                        if absmed > std:
                            res = Constants.DIR_UP
                        else:
                            res = Constants.DIR_PRE_UP
                    elif med < 0:
                        if absmed > std:
                            res = Constants.DIR_DOWN
                        else:
                            res = Constants.DIR_PRE_DOWN
                elif percent >= 95:
                    if med < 0:
                        if absmed > std:
                            res = Constants.DIR_DOWN
                        else:
                            res = Constants.DIR_PRE_DOWN
                    if med > 0:
                        if absmed > std:
                            res = Constants.DIR_UP
                        else:

                            # fix se añade direction
                            if direction == Constants.DIR_UP or direction == Constants.DIR_PRE_UP:
                                res = Constants.DIR_UP
                            else:
                                if percentFlow == Constants.DIR_UP:
                                    res = Constants.DIR_PRE_UP
                                else:
                                    res = Constants.DIR_PRE_DOWN
        except Exception as error:
            print("Error getProMEDSTD_MID ", error)
        return res


    # #@mide_tiempo
    def getPROBMEDSTD_NEWFlow(self, results, active):
        res = Constants.DIR_WAIT
        try:

            currentTime = self.gettime(results)
            if currentTime >= int(self.iniStart) and currentTime < int(self.iniEnd):
                try:
                    nombre_clase = "ProbEvaluator"
                    # Nombre del método
                    nombre_metodo = active.parameters.startProbDef
                    # Obtener la clase utilizando el nombre de la clase como string
                    clase = globals()[nombre_clase]
                    # Obtener el método de clase utilizando getattr()
                    metodo = getattr(clase, nombre_metodo)
                    # Llamar al método de clase con parámetros
                    res = metodo(results, active)
                    nda = ""
                except Exception as error:
                    # res = self.getProMEDSTD_END_BLG_05(results, active)
                    print("Error getPROBMEDSTD_OKFlow ", error)


            elif currentTime >= self.closeStart and currentTime < self.closeEnd:
                try:
                    nombre_clase = "ProbEvaluator"
                    # Nombre del método
                    nombre_metodo = active.parameters.endProbDef
                    # Obtener la clase utilizando el nombre de la clase como string
                    clase = globals()[nombre_clase]
                    # Obtener el método de clase utilizando getattr()
                    metodo = getattr(clase, nombre_metodo)
                    # Llamar al método de clase con parámetros
                    res = metodo(results,active)
                    nada = ""
                except Exception as error:
                    # res = self.getProMEDSTD_END_BLG_05(results, active)
                    print("Error getPROBMEDSTD_OKFlow ", error)

            else:
                nombre_clase = "ProbEvaluator"
                # Nombre del método
                nombre_metodo = active.parameters.normalProbDef
                # Obtener la clase utilizando el nombre de la clase como string
                clase = globals()[nombre_clase]
                # Obtener el método de clase utilizando getattr()
                metodo = getattr(clase, nombre_metodo)
                # Llamar al método de clase con parámetros
                res = metodo(results, active)
                # res = self.getProMEDSTD_MID(results)

        except Exception as error:
            print("Error getPROBMEDSTD_OKFlow ", error)
        return res

    def calculateSpecialIndicatorsBTCETH(self, results, active):

        try:
            currentTime = self.gettime(results)
            if currentTime >= int(0000) and currentTime < int(30):
                preditValue = self.dataBDMan.getPredictForActive(active.parameters.name)
                if preditValue[0]['initialPredict'] == 0:
                    # print(f"NUEVA PREDICCION initialPredict")
                    # solo si no ha hecho predicciones
                    # if results[Constants.WEEK_FLOW]==Constants.WEEK_FLOW_NOTINIT:
                    self.calculareWeekIndicator(results, active)
                    # self.calculatePrevRelativeValues(results, active)
                    # actualizamos
                    results["INIT_"+active.parameters.name] = '1'
                    self.dataBDMan.updatePredictForActive(active.parameters.name, '1', '0')
                else:
                    results["INIT_" + active.parameters.name] = '0'

            if currentTime >= int(1200) and currentTime < int(1230):
                preditValue = self.dataBDMan.getPredictForActive(active.parameters.name)
                if preditValue[0]['finalPredict'] == 0:
                    # print(f"NUEVA PREDICCION finalPredict")
                    # solo si no ha hecho predicciones
                    self.calculareWeekIndicator(results, active)
                    # self.calculatePrevRelativeValues(results, active)
                    # actualizamos
                    results["FINAL_" + active.parameters.name] = '1'
                    self.dataBDMan.updatePredictForActive(active.parameters.name, '0', '1')
                else:
                    results["FINAL_" + active.parameters.name] = '0'

            # calular percent

            percent = self.calculatePercentFcst(float(results[Constants.IND_REL_FCST_MIN]),
                                                float(results[Constants.IND_REL_FCST_MAX]),
                                                float(results[Constants.VALUE]))
            if percent is not None:
                results[Constants.IND_REL_FCST_PERCENT] = percent
            else:
                results[Constants.IND_REL_FCST_PERCENT] = 0
            # probFlow = self.getPROBMEDSTDFlow(results,active)
            # probFlow = self.getPROBMEDSTD_OKFlow(results, active)
            results[Constants.IND_PROB_FLOW] = Constants.DIR_WAIT
            # calculamos weekDIFF
            weekDiff = abs(results[Constants.WEEK_FLOW_MED]) - abs(results[Constants.WEEK_FLOW_STD])
            results[Constants.WEEK_FLOW_DIFF] = weekDiff

            # probFlow = self.getPROBMEDSTD_NEWFlow(results, active)
            # if probFlow:
            #     results[Constants.IND_PROB_FLOW] = probFlow

            # extremMin = float(results[Constants.WEEK_MIN_DIR])
            # extremMax = float(results[Constants.WEEK_MAX_DIR])
            # currentValue = float(results[Constants.VALUE])
            # fromTopDstPercent = (extremMax - currentValue) * 100 / (extremMax - extremMin)
            # results[Constants.WEEK_DIR_TOP_DST] = fromTopDstPercent
            # results[Constants.WEEK_DIR_BOT_DST] = 100 - fromTopDstPercent


        except Exception as error:
            print("Error calculatepercent ", error)
    # #@mide_tiempo
    def calculateSpecialIndicators(self, results, active):

        message = None
        currentTime = self.gettime(results)
        if currentTime >= int(self.iniStart) and currentTime < int(self.iniEnd):
            preditValue = self.dataBDMan.getPredictForActive(active.parameters.name)
            if preditValue[0]['initialPredict'] == 0:
                # print(f"NUEVA PREDICCION initialPredict")
                # solo si no ha hecho predicciones
                # if results[Constants.WEEK_FLOW]==Constants.WEEK_FLOW_NOTINIT:
                self.calculareWeekIndicator(results, active)
                # self.calculatePrevRelativeValues(results, active)
                # actualizamos
                results["INIT_"+active.parameters.name] = '1'
                self.dataBDMan.updatePredictForActive(active.parameters.name, '1', '0')
                message = f"{self.name} WEEK FLOW START para  {active.parameters.name} WEEK_FLOW: {str(results[Constants.WEEK_FLOW])}"
                # self.telegram.enviarMensaje(message, self.telegram.tokenBot, active.parameters.tele_group)
            else:
                results["INIT_" + active.parameters.name] = '0'

        if currentTime >= int(self.closeStart) and currentTime < int(self.closeEnd):
            preditValue = self.dataBDMan.getPredictForActive(active.parameters.name)
            if preditValue[0]['finalPredict'] == 0:
                # print(f"NUEVA PREDICCION finalPredict")
                # solo si no ha hecho predicciones
                self.calculareWeekIndicator(results, active)
                # self.calculatePrevRelativeValues(results, active)
                # actualizamos
                results["FINAL_" + active.parameters.name] = '1'
                self.dataBDMan.updatePredictForActive(active.parameters.name, '0', '1')
                message = f"{self.name} WEEK FLOW CLOSE para  {active.parameters.name} WEEK_FLOW: {str(results[Constants.WEEK_FLOW])}"
                # self.telegram.enviarMensaje(message, self.telegram.tokenBot, active.parameters.tele_group)

            else:
                results["FINAL_" + active.parameters.name] = '0'

        if message is not None and self.simulation==False:
            self.telegram.enviarMensaje(message, self.telegram.tokenBot, active.parameters.tele_group)

        # calular percent
        try:
            percent = self.calculatePercentFcst(float(results[Constants.IND_REL_FCST_MIN]),
                                                float(results[Constants.IND_REL_FCST_MAX]),
                                                float(results[Constants.VALUE]))
            if percent is not None:
                results[Constants.IND_REL_FCST_PERCENT] = percent
            else:
                results[Constants.IND_REL_FCST_PERCENT] = 0
            # probFlow = self.getPROBMEDSTDFlow(results,active)
            # probFlow = self.getPROBMEDSTD_OKFlow(results, active)
            results[Constants.IND_PROB_FLOW] = Constants.DIR_WAIT
            weekDiff = abs(results[Constants.WEEK_FLOW_MED]) - abs(results[Constants.WEEK_FLOW_STD])
            results[Constants.WEEK_FLOW_DIFF] = weekDiff

            # # calculamos weekDIFF
            # probFlow = self.getPROBMEDSTD_NEWFlow(results, active)
            # if probFlow:
            #     results[Constants.IND_PROB_FLOW] = probFlow

            # extremMin = float(results[Constants.WEEK_MIN_DIR])
            # extremMax = float(results[Constants.WEEK_MAX_DIR])
            # currentValue = float(results[Constants.VALUE])
            # fromTopDstPercent = (extremMax - currentValue) * 100 / (extremMax - extremMin)
            # results[Constants.WEEK_DIR_TOP_DST] = fromTopDstPercent
            # results[Constants.WEEK_DIR_BOT_DST] = 100-fromTopDstPercent





        except Exception as error:
            print("Error calculatepercent ", error)

        # if self.showLog:
        #     print(f'\n\n LOGS INDICADORES '
        #           f'ACTIVO : {active.parameters.name} Valor: {results[Constants.VALUE]} \n'
        #           f'ACTION : {results[Constants.CURRENT_ACTION]}  \n'
        #           f'ACTION_COUNT : {results[Constants.ACTION_COUNT]}  \n'
        #           f'ACTION_DISTANCE : {results[Constants.ACTION_DISTANCE]}  \n'
        #           f'IMA5MA20 : {results[Constants.IMA5MA20]}  \n'
        #           f'IMA_NEW : {results[Constants.IMA_NEW]}  \n'
        #           f'INDICATOR : {results[Constants.INDICATOR]}  \n'
        #           f'INDICATOR_TENDENCE : {results[Constants.INDICATOR_TENDENCE]}  \n'
        #           f'INDICATOR_DISTANCE : {results[Constants.INDICATOR_DISTANCE]}  \n\n'
        #
        #           f'ACUMULADO: {results[Constants.ACUMULADO]} \n'
        #           f'Tendencia: {results[Constants.FLUJO]} \n'
        #           f'tendencia count: {results[Constants.FLUJO_COUNT]} \n\n'
        #
        #           f'ACTION_MIN: {results[Constants.ACTION_MIN]} \n'
        #           f'ACTION_MIN_DIST: {results[Constants.ACTION_MIN_DIST]} \n'
        #           f'ACTION_MAX: {results[Constants.ACTION_MAX]} \n'
        #           f'ACTION_MAX_DIST: {results[Constants.ACTION_MAX_DIST]} \n'
        #           f'MARKET_TENDENCE: {results[Constants.MARKET_TENDENCE]} \n'
        #
        #           f'RSI: {results[Constants.RSI]} \n'
        #
        #           f'MEDIA: {results[Constants.MEDIA]} \n'
        #           f'STD: {results[Constants.STDDESV]} \n'
        #           f'MINSTD: {active.parameters.minSTDNormal} \n'
        #           f'MAXSTD: {active.parameters.maxSTDNormal} \n'
        #           f'MINMED: {active.parameters.minMEDNormal} \n'
        #           f'MAXMED: {active.parameters.maxMEDNormal} \n'
        #
        #           f'INDICATOR_MED : {results[Constants.INDICATOR_MED]}  \n'
        #           f'INDICATOR_MED_MOMENT : {results[Constants.INDICATOR_MED_MOMENT]}  \n'
        #           f'INDICATOR_MED_MOMENT_VALUE : {results[Constants.INDICATOR_MED_MOMENT_VALUE]}  \n'
        #           f'INDICATOR_STD : {results[Constants.INDICATOR_STD]}  \n'
        #           f'INDICATOR_MED_STD : {results[Constants.INDICATOR_MED_STD]}  \n'
        #           f'RELATIVE_MIN : {results[Constants.RELATIVE_MIN]}  \n'
        #           f'RELATIVE_MIN_DIST : {results[Constants.RELATIVE_MIN_DIST]}  \n'
        #           f'RELATIVE_MAX : {results[Constants.RELATIVE_MAX]}  \n'
        #           f'RELATIVE_MAX_DIST : {results[Constants.RELATIVE_MAX_DIST]}  \n'
        #           f'RELATIVE_PREV_MIN : {results[Constants.RELATIVE_PREV_MIN]}  \n'
        #           f'RELATIVE_PREV_MIN_DIST : {results[Constants.RELATIVE_PREV_MIN_DIST]}  \n'
        #           f'RELATIVE_PREV_MAX : {results[Constants.RELATIVE_PREV_MAX]}  \n'
        #           f'RELATIVE_PREV_MAX_DIST : {results[Constants.RELATIVE_PREV_MAX_DIST]}  \n'
        #           f'RELATIVE : {results[Constants.RELATIVE]}  \n'
        #
        #
        #           f'VALUE: : {results[Constants.VALUE]} \n'
        #           f'PREVIOUS_DIST: : {results[Constants.PREVIOUS_DIST]} \n'
        #           f'DIRECTION: {results[Constants.DIRECTION]} \n'
        #           f'MIN_DIR: {results[Constants.MIN_DIR]} \n'
        #           f'MAX_DIR: {results[Constants.MAX_DIR]} \n'
        #           f'INDI_DIR: {results[Constants.INDI_DIR]} \n'
        #           # f'CHANGE_POINT: {changePoint} \n'
        #
        #           f'WEEK_FLOW: {results[Constants.WEEK_FLOW]} \n'
        #           f'WEEK_FLOW_ABSVAL: {results[Constants.WEEK_FLOW_ABSVAL]} \n'
        #           f'WEEK_FLOW_MED: {results[Constants.WEEK_FLOW_MED]} \n'
        #           f'WEEK_FLOW_MED_LEVEL: {results[Constants.WEEK_FLOW_MED_LEVEL]} \n'
        #
        #           f'DATE: {results[Constants.DATE].values[0]} \n'
        #
        #           )

    # #@mide_tiempo
    def calculatePredictionIndicator(self, data, results, active):
        # VALORES SOLO HOY
        todayDate = datetime.datetime.strptime(results[Constants.DATE].values[0], "%Y-%m-%d %H:%M:%S.%f")
        startDate = todayDate.replace(hour=0, minute=0, second=0, microsecond=0)
        endDate = todayDate.replace(hour=23, minute=0, second=0, microsecond=0)

        startStr = startDate.strftime("%Y-%m-%d %H:%M:%S.%f")
        endStr = endDate.strftime("%Y-%m-%d %H:%M:%S.%f")

        maToday = data.loc[(data['date'] >= startStr) & (data['date'] < endStr)]
        maToday = maToday['value'].rolling(1).mean()

        diftimeOpen = self.getDifTimeFromOpen(results)
        results[Constants.TIME_FROM_OPEN] = diftimeOpen

        # calcular la media hasta el momento

        if active is not None:
            ima2 = active.parameters.ima2

        maNEW = data[self.closeValue].rolling(ima2).mean()

        listaDias = maNEW.to_numpy().tolist()
        # eliminamos nan values
        listaDias = [x for x in listaDias if str(x) != 'nan']
        listaDiaToday = maToday.to_numpy().tolist()
        contador = len(maNEW) - 1
        contadorToday = len(maToday) - 1

        valorCurrent = maNEW.iloc[[contador]].values[0]

        desSTDTotal = 0
        desSTDTotalToday = 0
        mediaTotal = 0
        mediaTotalToday = 0

        cambiosDay = [listaDias[-1] - valorCurrent for valorCurrent in listaDias]
        cambiosDayToday = [listaDiaToday[-1] - valorCurrent for valorCurrent in listaDiaToday]

        # contadores
        sumUP = 0
        sumDDWN = 0
        numUp = 0
        numDown = 0

        sumUPDAYS = 0
        sumDDWNDAYS = 0
        numUpDAYS = 0
        numDownDAYS = 0

        midTpday = 0
        if Constants.IND_REL_FCST_MIN in results:
            minToday = float(results[Constants.IND_REL_FCST_MIN])
            maxToday = float(results[Constants.IND_REL_FCST_MAX])
            # print(f"RELATIVE MIN {minToday}  RELATIVE MAX {maxToday}")
            midTpday = minToday + float((maxToday - minToday) / 2)
            for x in listaDiaToday:
                if x > midTpday:
                    sumUP = float(sumUP + x)
                    numUp = numUp + 1
                else:
                    sumDDWN = float(sumDDWN + x)
                    numDown = numDown + 1

            for x in listaDias:
                if x > midTpday:
                    sumUPDAYS = float(sumUPDAYS + x)
                    numUpDAYS = numUpDAYS + 1
                else:
                    sumDDWNDAYS = float(sumDDWNDAYS + x)
                    numDownDAYS = numDownDAYS + 1

        if len(listaDias) > 0:
            # Calcula la desviacion estandar
            desSTDTotal = np.std(cambiosDay)
            mediaTotal = np.mean(cambiosDay)

        if len(listaDiaToday) > 0:
            # Calcula la desviacion estandar
            desSTDTotalToday = np.std(cambiosDayToday)
            mediaTotalToday = np.mean(cambiosDayToday)

        results[Constants.INDICATOR_MED_DAYS] = mediaTotal
        results[Constants.INDICATOR_STD_DAYS] = desSTDTotal

        results[Constants.INDICATOR_MED_DAY] = mediaTotalToday
        results[Constants.INDICATOR_STD_DAY] = desSTDTotalToday

        results[Constants.IND_SUM_UP] = sumUP
        results[Constants.IND_SUM_DOWN] = sumDDWN
        results[Constants.IND_NUM_UP] = numUp
        results[Constants.IND_NUM_DOWN] = numDown

        results[Constants.IND_SUM_UP_DAYS] = sumUPDAYS
        results[Constants.IND_SUM_DOWN_DAYS] = sumDDWNDAYS
        results[Constants.IND_NUM_UP_DAYS] = numUpDAYS
        results[Constants.IND_NUM_DOWN_DAYS] = numDownDAYS

        results[Constants.IND_MED_DAY] = midTpday
        results[Constants.VALUE_DIFFMED] = results[Constants.VALUE] - midTpday

    # #@mide_tiempo
    def calculatePrevRelativeValues(self, results, active):
        try:
            valores = list()
            valoresPrev = list()
            minMax = list()
            cont = 1
            data1, cont = self.getPrevRelativeValues(results, active, cont)
            cont = cont + 1
            data2, cont = self.getPrevRelativeValues(results, active, cont)
            cont = cont + 1
            data3, cont = self.getPrevRelativeValues(results, active, cont)

            rel_val3 = None
            rel_val2 = None
            rel_val1 = None
            med3 = 0
            std3 = 0
            med2 = 0
            std2 = 0
            med1 = 0
            std1 = 0
            flow2 = None
            flow20 = None
            percent20 = None

            flow3 = None
            flow30 = None
            percent30 = None

            flow1 = None
            flow10 = None
            percent10 = None

            percent3 = None
            percent2 = None
            percent1 = None
            rel_min1 = None

            if len(data3) > 0:
                rel_min3 = data3.iloc[[-1]]["relative_min"].values[0]
                rel_max3 = data3.iloc[[-1]]["relative_max"].values[0]
                rel_val3 = data3.iloc[[-1]]["value"].values[0]
                valores.append(rel_val3)
                minMax.append(rel_min3)
                minMax.append(rel_max3)

                cambios3 = [rel_val3 - valor for valor in data3["value"]]
                med3 = np.mean(cambios3)
                std3 = np.std(cambios3)

            if len(data2) > 0:
                rel_min2 = data2.iloc[[-1]]["relative_min"].values[0]
                rel_max2 = data2.iloc[[-1]]["relative_max"].values[0]
                rel_val2 = data2.iloc[[-1]]["value"].values[0]
                valores.append(rel_val2)
                minMax.append(rel_min2)
                minMax.append(rel_max2)

                cambios2 = [rel_val2 - valor for valor in data2["value"]]
                med2 = np.mean(cambios2)
                std2 = np.std(cambios2)

            if len(data1) > 0:
                rel_min1 = data1.iloc[[-1]]["relative_min"].values[0]
                rel_max1 = data1.iloc[[-1]]["relative_max"].values[0]
                rel_val1 = data1.iloc[[-1]]["value"].values[0]
                valores.append(rel_val1)
                minMax.append(rel_min1)
                minMax.append(rel_max1)

                cambios1 = [rel_val1 - valor for valor in data1["value"]]
                med1 = np.mean(cambios1)
                std1 = np.std(cambios1)

            rel_val0 = results[Constants.VALUE]
            rel_min0 = results[Constants.RELATIVE_MIN]
            rel_max0 = results[Constants.RELATIVE_MAX]
            minMax.append(rel_min0)
            minMax.append(rel_max0)
            valores.append(rel_val0)

            min_val = min(minMax)
            max_val = max(minMax)

            # valores prev son valores sin el inicial para determinar flujo ayuda
            if rel_val2:
                valoresPrev.append(rel_val2)
            if rel_val1:
                valoresPrev.append(rel_val1)
            if rel_val0:
                valoresPrev.append(rel_val0)

            if pd.isna(rel_min1) is not True:

                if rel_val3 is not None:
                    flow3, dist_rel3, dist3, percent3 = self.determineFlow(rel_min3, rel_max3, rel_val3)
                    flow_30, dist_rel30, dist_30, percent30 = self.determineFlow(min_val, max_val, rel_val3)
                if rel_val2 is not None:
                    flow2, dist_rel2, dist2, percent2 = self.determineFlow(rel_min2, rel_max2, rel_val2)
                    flow20, dist_rel20, dist_20, percent20 = self.determineFlow(min_val, max_val, rel_val2)

                if rel_val1 is not None:
                    flow1, dist_rel1, dist1, percent1 = self.determineFlow(rel_min1, rel_max1, rel_val1)
                    flow10, dist_rel10, dist_10, percent10 = self.determineFlow(min_val, max_val, rel_val1)

                if rel_val0 is not None:
                    flow0, dist_rel0, dist0, percent0 = self.determineFlow(rel_min0, rel_max0, rel_val0)
                    flow00, dist_rel00, dist_00, percent00 = self.determineFlow(min_val, max_val, rel_val0)

                flow_minMax, dist_relminMax, dist_minMax, percentMinMax = self.determineFlow(min_val, max_val, rel_val0)

                rel_fcst = Constants.IND_REL_FCST_WAIT

                cambios = [valores[-1] - valor for valor in valores]
                desviacion_estandar = np.std(cambios)
                media = np.mean(cambios)

                # calcular valores valoresPrev
                cambiosprev = [valoresPrev[-1] - valor for valor in valoresPrev]
                std_prev = np.std(cambiosprev)
                med_prev = np.mean(cambiosprev)

                # if dist_minMax >= active.parameters.relativeDistance:
                # supero el rango deberia ir a la inversa
                # verificar ultimo flujo que direccion tomo y porcentaje

                print(
                    f"PRINTFCST ANALISIS {results[Constants.DATE].values[0]} \tflow_minMax: {flow_minMax} \tdist_relminMax: {dist_relminMax} \tdist_minMax: {dist_minMax} \tpercentMinMax: {percentMinMax} ")
                print(
                    f"PRINTFCST1 ANALISIS {results[Constants.DATE].values[0]} \tpercent3: {percent3} \tpercent2: {percent2} \tpercent1: {percent1} \tpercent0: {percent0} \tflow3: {flow3} \tflow2: {flow2} \tflow1: {flow1} \tflow0: {flow0} ")
                print(
                    f"PRINTFCST2 ANALISIS {results[Constants.DATE].values[0]} \trel_val3: {rel_val3} \trel_val2: {rel_val2} \trel_val1: {rel_val1} \trel_val0: {rel_val0} ")
                print(
                    f"PRINTFCST3 ANALISIS {results[Constants.DATE].values[0]} \tpercent30: {percent30} \tpercent20: {percent20} \tpercent10: {percent10} \tpercent00: {percent00}  ")
                print(
                    f"PRINTFCST4 ANALISIS {results[Constants.DATE].values[0]} \tmed3: {med3} \tstd3: {std3} \tmed2: {med2} \tstd2: {std2} \tmed1: {med1} \tstd1: {std1}")

                rel_fcst = self.determinePercentDistance(percentMinMax, results, media, desviacion_estandar, med_prev,
                                                         std_prev)

                results[Constants.IND_REL_FCST_STD] = float(desviacion_estandar)
                results[Constants.IND_REL_FCST_MED] = float(media)
                results[Constants.IND_REL_FCST] = rel_fcst
                results[Constants.IND_REL_FCST_MIN] = min_val
                results[Constants.IND_REL_FCST_MAX] = max_val

                print(
                    f"PRINTFCST4 ANALISIS {results[Constants.DATE].values[0]} \trel_fcst: {rel_fcst} \tpercentMinMax: {percentMinMax} \tmedia: {media} \tdesviacion_estandar: {desviacion_estandar} \tmin_val: {min_val} \tmax_val: {max_val} \tmed_prev {med_prev} \tstd_prev {std_prev} ")






        except Exception as error:
            print("Error calculatePrevRelativeValues  date format using second change", error)

    def determinePercentDistance(self, percentMinMax, results, med, std, med_prev, std_prev):
        res = None
        # determinar donde esta
        minMaxABS = abs(percentMinMax)
        week_std = results[Constants.WEEK_FLOW_STD]
        week_med = results[Constants.WEEK_FLOW_MED]
        resMedprev = None
        flujoweek = 0  # 0 indeciso 1 dube -1 baja
        # flujomedprev
        if med_prev > 0:
            # sube
            if abs(med_prev) > std_prev:
                resMedprev = Constants.UP_HIGH
            else:
                resMedprev = Constants.UP_LOW
        else:
            # baja
            if abs(med_prev) > std_prev:
                resMedprev = Constants.DOWN_HIGH
            else:
                resMedprev = Constants.DOWN_LOW

        # flujo week
        if week_med > 0:
            # SUBE
            if abs(week_med) > week_std:
                flujoweek = 1
            else:
                flujoweek = 1
        else:
            # BAJA
            if abs(week_med) > week_std:
                flujoweek = -1
            else:
                flujoweek = -1

        if med > 0:

            # sube
            if abs(med) > std:
                res = Constants.IND_REL_FCST_UP
                if percentMinMax > 80:
                    # ya no puede subir tanto
                    res = Constants.IND_REL_FCST_UP
            else:
                # el valor es pequeño determinar si sube o baja
                if resMedprev == Constants.UP_HIGH:
                    # sube
                    res = Constants.IND_REL_FCST_UP
                    if percentMinMax > 80:
                        # ya no puede subir tanto
                        res = Constants.IND_REL_FCST_UP_INV_REL
                if resMedprev == Constants.UP_LOW:

                    if flujoweek > 0:
                        res = Constants.IND_REL_FCST_UP
                        if abs(week_med) < week_std:
                            res = Constants.IND_REL_FCST_PRE_UP
                        if percentMinMax > 80:
                            # ya no puede subir tanto
                            res = Constants.IND_REL_FCST_UP_INV_REL
                    else:
                        res = Constants.IND_REL_FCST_PRE_DOWN
                if resMedprev == Constants.DOWN_HIGH:
                    # sube
                    res = Constants.IND_REL_FCST_DOWN
                    if percentMinMax < 20:
                        # ya no puede subir tanto
                        res = Constants.IND_REL_FCST_DOWN_INV_REL
                if resMedprev == Constants.DOWN_LOW:
                    if flujoweek > 0:
                        res = Constants.IND_REL_FCST_DOWN
                        if abs(week_med) < week_std:
                            res = Constants.IND_REL_FCST_PRE_DOWN
                        if percentMinMax < 20:
                            # ya no puede subir tanto
                            res = Constants.IND_REL_FCST_DOWN_INV_REL
                    else:
                        res = Constants.IND_REL_FCST_PRE_DOWN
        else:
            # baja
            if abs(med) > std:
                res = Constants.IND_REL_FCST_DOWN
                if percentMinMax < 20:
                    # ya no puede bajar tanto
                    res = Constants.IND_REL_FCST_DOWN
            else:
                # el valor es pequeño determinar si sube o baja
                if resMedprev == Constants.DOWN_HIGH:
                    # baja
                    res = Constants.IND_REL_FCST_DOWN
                    if percentMinMax < 20:
                        # ya no puede subir tanto
                        res = Constants.IND_REL_FCST_DOWN_INV_REL
                if resMedprev == Constants.DOWN_LOW:

                    if flujoweek < 0:
                        res = Constants.IND_REL_FCST_DOWN
                        if abs(week_med) < week_std:
                            res = Constants.IND_REL_FCST_PRE_DOWN
                            if percentMinMax < 20:
                                # ya no puede subir tanto
                                res = Constants.IND_REL_FCST_DOWN_INV_REL
                    else:
                        res = Constants.IND_REL_FCST_PRE_DOWN
                if resMedprev == Constants.UP_HIGH:
                    # sube
                    res = Constants.IND_REL_FCST_UP
                    if percentMinMax > 80:
                        # ya no puede subir tanto
                        res = Constants.IND_REL_FCST_UP_INV_REL
                if resMedprev == Constants.UP_LOW:

                    if flujoweek > 0:
                        res = Constants.IND_REL_FCST_UP
                        if abs(week_med) < week_std:
                            res = Constants.IND_REL_FCST_PRE_UP
                            if percentMinMax > 80:
                                # ya no puede subir tanto
                                res = Constants.IND_REL_FCST_UP_INV_REL
                    else:
                        res = Constants.IND_REL_FCST_PRE_DOWN

        return res

    # #@mide_tiempo
    def calculatePercentFcst(self, min, max, val):

        percent = 0
        try:
            if val < min:
                min = val
            if val > max:
                max = val
            min_dist = val - min
            max_dist = max - val
            if min_dist > max_dist:
                # SUBE
                dist = float(max) - float(min)
                percent = (min_dist * 100) / dist

            elif min_dist < max_dist:
                # BAJA
                dist = float(max) - float(min)
                percent = (min_dist * 100) / dist
        except Exception as error:
            print("Error calculatePerfectFcst ", error)
        return percent

    def determineFlow(self, min, max, val):
        res = Constants.IND_REL_FCST_WAIT
        dist_rel = 0
        dist = 0
        percent = 0
        try:
            if min is None or max is None:
                return Constants.IND_REL_FCST_WAIT
            min_dist = val - min
            max_dist = max - val
            if min_dist > max_dist:
                # SUBE
                dist_rel = float(min_dist) - float(max_dist)
                dist = float(max) - float(min)
                percent = (min_dist * 100) / dist
                if abs(percent) >= 50:
                    res = Constants.IND_REL_FCST_UP
                else:
                    res = Constants.IND_REL_FCST_PRE_UP

            elif min_dist < max_dist:
                # BAJA

                dist_rel = float(min_dist) - float(max_dist)
                dist = float(max) - float(min)
                percent = (min_dist * 100) / dist
                if abs(percent) >= 50:
                    res = Constants.IND_REL_FCST_DOWN
                else:
                    res = Constants.IND_REL_FCST_PRE_DOWN
        except Exception as error:
            print("Error determineFlow ", error)
            return res, dist_rel, dist, percent
        return res, dist_rel, dist, percent

    def getPrevRelativeValues(self, results, active, days):

        value_week = 0

        end_date_time = None
        try:
            eval_date_time = datetime.datetime.strptime(results[Constants.DATE].values[0], "%Y-%m-%d %H:%M:%S.%f")
        except Exception as error:
            # print("Error getAllWithNameForXdaysRangeDates  date format using second change", error)
            eval_date_time = datetime.datetime.strptime(results[Constants.DATE].values[0], "%Y-%m-%d")

        # quitamos los segundos y milisegundos
        # eval_date_time = eval_date_time.replace(hour=0, minute=0, second=0, microsecond=0)
        eval_date_time = eval_date_time.replace(hour=0, minute=0, second=0, microsecond=0)

        end_date = eval_date_time.strftime("%Y-%m-%d %H:%M:%S.%f")
        start_date_time = eval_date_time + datetime.timedelta(days=-days)
        # 1verificar que dia ha caido
        if start_date_time.weekday() == 5:
            ##cayo un sabado
            days = days + 1
            start_date_time = eval_date_time + datetime.timedelta(days=-days)
        if start_date_time.weekday() == 6:
            ##cayo un domingo
            days = days + 2
            start_date_time = eval_date_time + datetime.timedelta(days=-days)

        start_date = start_date_time.strftime("%Y-%m-%d %H:%M:%S.%f")

        if days > 1:
            end_date_time = eval_date_time + datetime.timedelta(days=-days + 1)
            end_date = end_date_time.strftime("%Y-%m-%d %H:%M:%S.%f")

        data = self.dataBDMan.getAllWithNameForXdaysRangeDatesExactdays(active.parameters.name, start_date, end_date)
        return data, days

    def determinarIndicatorTendence(self, maNEW, elements_past, results, maNEWValue, passiveDistance):
        # DETERMINAMOS ANGULO DE TENDENCIA
        ma15Size = len(maNEW)
        marketAngle = 0
        marketAngleTan = 0
        if ma15Size >= elements_past:
            dataTemp = {}
            dataTemp['date'] = results[Constants.DATE]
            dataTemp['value'] = results[Constants.VALUE]

            # ma_past = maNEW[-elements_past]
            ma_past = maNEW[ma15Size - elements_past]

            if pd.isna(ma_past) is not True:
                marketAngle = maNEWValue - ma_past
                # print(f"onld marketAngle {marketAngle}")
                marketAngleTan = np.degrees(np.arctan(maNEWValue-ma_past))
                marketAngleAbs = abs(marketAngle)
                # print(f"indicator tendence value :  {marketAngle} passiveDistante {passiveDistance}")
                # print(f"ma15Value {maNEWValue} ma_past {ma_past} cantidad {elements_past}")
                if marketAngleAbs > passiveDistance:
                    # print(f"ENTRA A EVALUAR")
                    if marketAngle > 0:
                        # sube
                        results[Constants.INDICATOR_TENDENCE] = Constants.INDICATOR_T_UP
                        # self.operations.tendenceUP.append(dataTemp)
                    else:
                        # baja
                        results[Constants.INDICATOR_TENDENCE] = Constants.INDICATOR_T_DOWN
                        # self.operations.tendenceDOWN.append(dataTemp)
                else:
                    # no hay cambios grandes
                    results[Constants.INDICATOR_TENDENCE] = Constants.INDICATOR_T_WAIT
                    # self.operations.tendenceWAIT.append(dataTemp)
            else:
                # iniciamos con tendencia de indicadores

                if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UP:
                    results[Constants.INDICATOR_TENDENCE] = Constants.INDICATOR_T_UP
                    # self.operations.tendenceUP.append(dataTemp)
                elif results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_DOWN:
                    results[Constants.INDICATOR_TENDENCE] = Constants.INDICATOR_T_DOWN
                    # self.operations.tendenceDOWN.append(dataTemp)
                else:
                    results[Constants.INDICATOR_TENDENCE] = Constants.INDICATOR_T_WAIT
                    # self.operations.tendenceWAIT.append(dataTemp)

        results[Constants.MARKET_ANGLE] = marketAngle
        results[Constants.MARKET_ANGLE_TANG] = marketAngleTan

    def determinarRelativePercent(self, data, results, active):
        # DETERMINAMOS ANGULO DE TENDENCIA
        datalen = len(data)
        elements_past = active.parameters.percent_distance
        results[Constants.IND_REL_PERCENT_MED] = 0
        results[Constants.IND_REL_PERCENT_STD] = 0
        media = 0
        desviacion_estandar = 0
        try:
            if datalen > elements_past:
                dataTemp = {}
                dataTemp['date'] = results[Constants.DATE]
                dataTemp['value'] = results[Constants.VALUE]

                # recorremos X elementos atras
                count = 0
                fin = False
                contador = len(data) - 1
                posicion = elements_past
                valores = list()
                # currentDataValue = data.iloc[[contador]]
                valor = data.iloc[[contador]]["rel_fcst_percent"].values[0]
                if pd.isna(valor) is True:
                    nada = True
                while fin != True:

                    valorPre = data.iloc[[contador - posicion]]["rel_fcst_percent"].values[0]

                    if pd.isna(valorPre) is not True and valorPre is not None:
                        if valorPre > 0:
                            valores.append(valorPre)

                    if posicion <= 0:
                        break
                    else:
                        posicion = posicion - 1

                # cambios = [valores[-1] - valor for valor in valores]

                if len(valores) > 0:
                    desviacion_estandar = np.std(valores)
                    media = np.mean(valores)

                results[Constants.IND_REL_PERCENT_MED] = media
                results[Constants.IND_REL_PERCENT_STD] = desviacion_estandar

        except Exception as e:
            print(f"ERROR determinarRelativePercent {str(e)}")

    def determinarIndicatorTendenceBOTHIma4Best(self, data, maNEW, results, active):
        # DETERMINAMOS ANGULO DE TENDENCIA
        ma15Size = len(maNEW)
        elements_past = active.parameters.tendence_distance
        passiveDistance = active.parameters.tendence_measure
        minSTDNormal = active.parameters.minSTDNormal
        maxSTDNormal = active.parameters.maxSTDNormal
        minMEDNormal = active.parameters.minMEDNormal
        maxMEDNormal = active.parameters.maxMEDNormal
        if ma15Size >= elements_past:
            dataTemp = {}
            dataTemp['date'] = results[Constants.DATE]
            dataTemp['value'] = results[Constants.VALUE]

            # recorremos X elementos atras
            count = 0
            fin = False
            contador = len(maNEW) - 1
            posicion = elements_past
            valores = list()
            # currentDataValue = data.iloc[[contador]]
            valor = maNEW.iloc[[contador]].values[0]
            if pd.isna(valor) is True:
                valor = 0
            while fin != True:

                valorPre = maNEW.iloc[[contador - posicion]].values[0]

                if pd.isna(valorPre) is not True and valorPre is not None:
                    valores.append(valorPre)
                # else:
                #     valores.append(0)

                if posicion <= 0:
                    break
                else:
                    posicion = posicion - 1

            # calculamos el angulo
            cambios = [valores[-1] - valor for valor in valores]
            # print(f"valores {valores}")
            # print(f"cambios {cambios}")

            # ma_past = maNEW[-elements_past]
            # ma_past = maNEW[ma15Size - elements_past]
            results[Constants.MEDSTDDIFF] = 0
            if len(valores) > 0:
                # Calcula la desviacion estandar
                desviacion_estandar = np.std(cambios)
                media = np.mean(cambios)
                marketAngle = media

                results[Constants.MEDIA] = media
                results[Constants.STDDESV] = desviacion_estandar
                results[Constants.MEDSTDDIFF] = abs(media) - abs(desviacion_estandar)

                # marketAngle = maNEWValue - ma_past
                marketAngleAbs = abs(marketAngle)
                # print(f"indicator media :  {media} desviacion_estandar {desviacion_estandar} fecha: {results[Constants.DATE]}")

                # print(f"ENTRA A EVALUAR STD")
                indicador_STD = Constants.INDICATOR_TSTD_MID

                if desviacion_estandar > maxSTDNormal:
                    indicador_STD = Constants.INDICATOR_TSTD_HIGH
                elif desviacion_estandar < minSTDNormal:
                    indicador_STD = Constants.INDICATOR_TSTD_LOW

                results[Constants.INDICATOR_STD] = indicador_STD

                # print(f"ENTRA A EVALUAR MEDIA")
                indicador_MED = Constants.INDICATOR_TM_WAIT
                mediaABS = abs(media)

                if media > 0:
                    indicador_MED = Constants.INDICATOR_TM_UP
                elif media <= 0:
                    indicador_MED = Constants.INDICATOR_TM_DOWN

                results[Constants.INDICATOR_MED] = indicador_MED

                # print(f"ENTRA A EVALUAR MEDIA y STD")

                results[Constants.INDICATOR_MED_STD] = Constants.INDICATOR_M_STD_WAIT

                if indicador_MED == Constants.INDICATOR_TM_UP:
                    if mediaABS > desviacion_estandar:
                        results[Constants.INDICATOR_MED_STD] = Constants.INDICATOR_M_STD_UP
                        if self.drawnMedia_UPDOWN:
                            self.operations.tendenceUP.append(dataTemp)
                    else:
                        results[Constants.INDICATOR_MED_STD] = Constants.INDICATOR_M_STD_WAIT
                        if self.drawnMedia_UPDOWN:
                            self.operations.tendenceWAIT.append(dataTemp)


                elif indicador_MED == Constants.INDICATOR_TM_DOWN:
                    # baja
                    if mediaABS > desviacion_estandar:
                        results[Constants.INDICATOR_MED_STD] = Constants.INDICATOR_M_STD_DOWN
                        if self.drawnMedia_UPDOWN:
                            self.operations.tendenceDOWN.append(dataTemp)
                    else:
                        results[Constants.INDICATOR_MED_STD] = Constants.INDICATOR_M_STD_WAIT
                        if self.drawnMedia_UPDOWN:
                            self.operations.tendenceWAIT.append(dataTemp)
                elif indicador_MED == Constants.INDICATOR_TM_WAIT:
                    # no hay cambios grandes
                    results[Constants.INDICATOR_MED_STD] = Constants.INDICATOR_M_STD_WAIT
                    if self.drawnMedia_UPDOWN:
                        self.operations.tendenceWAIT.append(dataTemp)
                else:
                    # no hay cambios grandes
                    results[Constants.INDICATOR_MED_STD] = Constants.INDICATOR_M_STD_WAIT
                    if self.drawnMedia_UPDOWN:
                        self.operations.tendenceWAIT.append(dataTemp)


            else:
                # iniciamos con tendencia de indicadores
                results[Constants.INDICATOR_MED_STD] = Constants.INDICATOR_M_STD_WAIT
                if self.drawnMedia_UPDOWN:
                    self.operations.tendenceWAIT.append(dataTemp)
        else:
            results[Constants.INDICATOR_MED] = Constants.INDICATOR_TM_WAIT
            results[Constants.INDICATOR_STD] = Constants.INDICATOR_TSTD_UNDEF
            results[Constants.INDICATOR_MED_STD] = Constants.INDICATOR_M_STD_WAIT
            results[Constants.MEDSTDDIFF] = 0

    def determinarIndicatorTendenceMomentBest(self, maNEW, ma4, results, active):
        # DETERMINAMOS ANGULO DE TENDENCIA
        ma15Size = len(maNEW)
        elements_past = active.parameters.tendence_distance_moment
        minMEDNormal = active.parameters.minMEDNormal
        maxMEDNormal = active.parameters.maxMEDNormal

        if ma15Size >= elements_past:
            dataTemp = {}
            dataTemp['date'] = results[Constants.DATE]
            dataTemp['value'] = results[Constants.VALUE]

            # recorremos X elementos atras
            count = 0
            fin = False
            contador = len(maNEW) - 1
            posicion = elements_past
            valores = list()
            # currentDataValue = data.iloc[[contador]]
            valor = maNEW.iloc[[contador]].values[0]
            if pd.isna(valor) is True:
                valor = 0
            while fin != True:

                valorPre = maNEW.iloc[[contador - posicion]].values[0]

                if pd.isna(valorPre) is not True and valorPre is not None:
                    valores.append(valorPre)
                else:
                    valores.append(0)

                if posicion <= 0:
                    break
                else:
                    posicion = posicion - 1

            # calculamos el angulo
            cambios = [valores[-1] - valor for valor in valores]
            # print(f"valores LONG {valores}")
            # print(f"cambios LONG {cambios}")

            results[Constants.INDICATOR_MED_MOMENT] = Constants.INDICATOR_TM_UNDEF
            if len(valores) > 0:
                # Calcula la desviacion estandar
                desviacion_estandar = np.std(cambios)
                media = np.mean(cambios)
                marketAngle = media

                results[Constants.MEDIA_MOMENT] = media
                results[Constants.STD_MOMENT] = desviacion_estandar

                # marketAngle = maNEWValue - ma_past
                marketAngleAbs = abs(marketAngle)
                # print(f"indicator mediaLONG :  {media} desviacion_estandar {desviacion_estandar} fecha: {results[Constants.DATE]}")

                # print(f"ENTRA A EVALUAR MEDIA")
                indicador_MED = Constants.INDICATOR_TM_WAIT
                mediaABS = abs(media)

                if media > 0:
                    if mediaABS > desviacion_estandar:
                        indicador_MED = Constants.INDICATOR_TM_UP
                    else:
                        indicador_MED = Constants.INDICATOR_TM_WAIT
                elif media <= 0:
                    if mediaABS > desviacion_estandar:
                        indicador_MED = Constants.INDICATOR_TM_DOWN
                    else:
                        indicador_MED = Constants.INDICATOR_TM_WAIT

                results[Constants.INDICATOR_MED_MOMENT] = indicador_MED
                results[Constants.INDICATOR_MED_MOMENT_VALUE] = media





            else:
                # iniciamos con tendencia de indicadores
                results[Constants.INDICATOR_MED_MOMENT] = Constants.INDICATOR_TM_UNDEF
                results[Constants.INDICATOR_MED_MOMENT_VALUE] = 0
        else:
            # iniciamos con tendencia de indicadores
            results[Constants.INDICATOR_MED_MOMENT] = Constants.INDICATOR_TM_UNDEF
            results[Constants.INDICATOR_MED_MOMENT_VALUE] = 0
            results[Constants.MEDIA_MOMENT] = 0
            results[Constants.STD_MOMENT] = 0

    def calculate_rsi(self, data, period=14):
        return calculate_rsi(data, period)
    def extractResultsDataForAnalisys(self, results, isbuy, active, name = None, isStart = False, isnormal = False):
        res = {}
        fecha = results[Constants.DATE].values[0]
        if name is not None:
            resname = name
        else:
            resname = fecha

        if isnormal:
            resname = " "
        res[Constants.ANALISIS_NAME] = resname
        res[Constants.EVAl_NAME] = results[Constants.EVAl_NAME]
        if Constants.EVAl_CLOSE_ACUM in results:
            res[Constants.EVAl_CLOSE_ACUM] = results[Constants.EVAl_CLOSE_ACUM]
        if Constants.EVAl_CLOSE_DIFF in results:
            res[Constants.EVAl_CLOSE_DIFF] = results[Constants.EVAl_CLOSE_DIFF]
        if Constants.EVAl_ACUM in results:
            res[Constants.EVAl_ACUM] = results[Constants.EVAl_ACUM]

        res[Constants.INTERVAL] = results[Constants.INTERVAL]
        res[Constants.ACTION_MAX_DIST] = results[Constants.ACTION_MAX_DIST]
        res[Constants.ACTION_MIN_DIST] = results[Constants.ACTION_MIN_DIST]

        res[Constants.DATE] = fecha
        if self.showMinMaxLogs:
            res[Constants.MIN_WEEK] = results[Constants.MIN_WEEK]
            res[Constants.MAX_WEEK] = results[Constants.MAX_WEEK]
            res[Constants.MIN_MONTH] = results[Constants.MIN_MONTH]
            res[Constants.MAX_MONTH] = results[Constants.MAX_MONTH]

        if self.showBLGLogs:
            res[Constants.BLG_MA_VAL] = results[Constants.BLG_MA_VAL]
            res[Constants.BLG_MA_MEAN] = results[Constants.BLG_MA_MEAN]
            res[Constants.BLG_MA_X] = results[Constants.BLG_MA_X]


        value = float(results[Constants.ACTION_ACUM])
        # if isStart ==False:
        if isbuy ==False:
            # if isnormal==False:
                value = value*-1

        res[Constants.VALUE] = results[Constants.VALUE]
        if Constants.INICIO_NAME in results:
            res[Constants.INICIO_NAME] = results[Constants.INICIO_NAME]
        else:
            res[Constants.INICIO_NAME] = "NONE"

        res[Constants.CURRENT_ACTION] = results[Constants.CURRENT_ACTION]
        res["IS_BUY"] = isbuy
        res["START"] = isStart
        res[Constants.ACUMULADO] = results[Constants.ACUMULADO]
        res[Constants.ACTION_ACUM] = results[Constants.ACTION_ACUM]
        res[Constants.PROFIT] = results[Constants.PROFIT]
        if self.showMarketTrendLogs:
            res[Constants.MARKET_TREND_DIRECTION] = results[Constants.MARKET_TREND_DIRECTION]
            res[Constants.MARKET_TREND_INTENSITY] = results[Constants.MARKET_TREND_INTENSITY]
            # res[Constants.MARKET_TREND_SCORE] = results[Constants.MARKET_TREND_SCORE]
            # res[Constants.MARKET_TREND_SLOPE_3D] = results[Constants.MARKET_TREND_SLOPE_3D]
            # res[Constants.MARKET_TREND_SLOPE_7D] = results[Constants.MARKET_TREND_SLOPE_7D]
            # res[Constants.MARKET_TREND_PCT_CHANGE_3D] = results[Constants.MARKET_TREND_PCT_CHANGE_3D]
            # res[Constants.MARKET_TREND_PCT_CHANGE_7D] = results[Constants.MARKET_TREND_PCT_CHANGE_7D]
            # res[Constants.MARKET_TREND_CONSISTENCY] = results[Constants.MARKET_TREND_CONSISTENCY]
        if self.showRSILogs:
            res[Constants.RSI] = results[Constants.RSI]
            res[Constants.RSI_PREV5] = results[Constants.RSI_PREV5]
            res[Constants.RSI_DIFF] = results[Constants.RSI_DIFF]
            res[Constants.RSI_SLOPE] = results[Constants.RSI_SLOPE]
            res[Constants.RSI_ACCEL] = results[Constants.RSI_ACCEL]
            res[Constants.RSI_SCORE] = results[Constants.RSI_SCORE]
            res[Constants.RSI_SIGNAL] = results[Constants.RSI_SIGNAL]
        # res[Constants.ORDER_FLOW_SIGNAL] = results[Constants.ORDER_FLOW_SIGNAL]
        res[Constants.ACTION_COUNT] = results[Constants.ACTION_COUNT]
        if isStart == False:
            # res[Constants.ACTION_ACUM] = 0
            res[Constants.ACTION_ACUM_END] = value
        else:
            # res[Constants.ACTION_ACUM] = 0
            res[Constants.ACTION_ACUM_END] = 0
        res[Constants.FLUJO] = results[Constants.FLUJO]
        res[Constants.FLUJO_COUNT] = results[Constants.FLUJO_COUNT]
        if self.showHourlyLogs:
            res[Constants.HOURLY_ANGLE] = results[Constants.HOURLY_ANGLE]
            res[Constants.HOURLY_ANGLE_MED] = results[Constants.HOURLY_ANGLE_MED]
            res[Constants.HOURLY_ANGLE_MED_PREV] = results[Constants.HOURLY_ANGLE_MED_PREV]
        if self.showAngleLogs:
            res[Constants.ANGLE_PREV] = results[Constants.ANGLE_PREV]
            res[Constants.ANGLE] = results[Constants.ANGLE]
            res[Constants.ANGLE_COUNTER] = results[Constants.ANGLE_COUNTER]
            res[Constants.ANGLE_FLOW] = results[Constants.ANGLE_FLOW]
            res[Constants.ANGLE_IMA1] = results[Constants.ANGLE_IMA1]
            res[Constants.ANGLE_IMA1_PREV] = results[Constants.ANGLE_IMA1_PREV]
            res[Constants.ANGLE_EMA] = results[Constants.ANGLE_EMA]
            res[Constants.ANGLE_EMA20] = results[Constants.ANGLE_EMA20]
            res[Constants.ANGLE_IMA1_COUNTER] = results[Constants.ANGLE_IMA1_COUNTER]

        res[Constants.INDICATOR_EMA] = results[Constants.INDICATOR_EMA]
        res[Constants.INDICATOR_EMA_CHECK] = results[Constants.INDICATOR_EMA_CHECK]

        res[Constants.EMA20_SLOPE] = results[Constants.EMA20_SLOPE]
        res[Constants.EMA10_SLOPE] = results[Constants.EMA10_SLOPE]
        res[Constants.BLG_BANDWIDTH] = results[Constants.BLG_BANDWIDTH]
        res[Constants.EMA_SPREAD] = results[Constants.EMA_SPREAD]
        res[Constants.EMA_CROSS_COUNT] = results[Constants.EMA_CROSS_COUNT]
        res[Constants.PRICE_RANGE_PERCENT] = results[Constants.PRICE_RANGE_PERCENT]
        res[Constants.EMA10_ANGLE] = results[Constants.EMA10_ANGLE]
        res[Constants.RSI] = results[Constants.RSI]


        res[Constants.CURRVAL_EMA_DST] = results[Constants.CURRVAL_EMA_DST]
        res[Constants.INDICATOR_EMA50] = results[Constants.INDICATOR_EMA50]
        res[Constants.INDICATOR_EMA50_DST] = results[Constants.INDICATOR_EMA50_DST]
        res[Constants.EMA_DST] = results[Constants.EMA_DST]
        res[Constants.IMA5MA20] = results[Constants.IMA5MA20]
        res[Constants.MEDSTDDIFF] = results[Constants.MEDSTDDIFF]
        varName = "IND_" + active.parameters.name
        res[varName] = results[varName]
        res[Constants.IMA1] = results[Constants.IMA1]
        res[Constants.IMA1EMADIFF] = results[Constants.IMA1EMADIFF]

        if self.showDirBotLog:
            res[Constants.MONTH_DIR_BOT_DST] = results[Constants.MONTH_DIR_BOT_DST]
            res[Constants.MONTH_DIR_BOT_DST_MED] = results[Constants.MONTH_DIR_BOT_DST_MED]
            res["MONTH_DIFF"] = float(results[Constants.MONTH_DIR_BOT_DST])-float(results[Constants.MONTH_DIR_BOT_DST_MED])
            res[Constants.WEEK_DIR_BOT_DST] = results[Constants.WEEK_DIR_BOT_DST]
            res[Constants.WEEK_DIR_BOT_DST_MED] = results[Constants.WEEK_DIR_BOT_DST_MED]
            res["WEEK_DIFF"] = float(results[Constants.WEEK_DIR_BOT_DST]) - float(
                results[Constants.WEEK_DIR_BOT_DST_MED])
            # res[Constants.WEEK_DIR_BOT_DST_NEW] = results[Constants.WEEK_DIR_BOT_DST_NEW]
            # res[Constants.WEEK_DIR_BOT_DST_MED_NEW] = results[Constants.WEEK_DIR_BOT_DST_MED_NEW]
            # res["WEEK_NEW_DIFF"] = float(results[Constants.WEEK_DIR_BOT_DST_NEW]) - float(
            #     results[Constants.WEEK_DIR_BOT_DST_MED_NEW])
            # res[Constants.WEEK_DIR_BOT_DST_MED_NEW_FLOW] = results[Constants.WEEK_DIR_BOT_DST_MED_NEW_FLOW]

        res[Constants.BOT_DST_BLG] = results[Constants.BOT_DST_BLG]
        res[Constants.IND_BLG_LOWER_DST_PERCENT] = results[Constants.IND_BLG_LOWER_DST_PERCENT]
        res[Constants.IND_BLG_MIDDLE_DST_PERCENT] = results[Constants.IND_BLG_MIDDLE_DST_PERCENT]
        res[Constants.IND_BLG] = results[Constants.IND_BLG]
        # res[Constants.INDICATOR_EMA_CHECK] = results[Constants.INDICATOR_EMA_CHECK]
        res[Constants.EMA10_BLG_DST] = results[Constants.EMA10_BLG_DST]
        res[Constants.EMA20_BLG_DST] = results[Constants.EMA20_BLG_DST]


        # res[Constants.MACD_SIGNAL_OK] = results[Constants.MACD_SIGNAL_OK]
        # res[Constants.SMA_SIGNAL] = results[Constants.SMA_SIGNAL]
        # res[Constants.RSI_SIGNAL] = results[Constants.RSI_SIGNAL]
        # res[Constants.ACTION_TEST] = results[Constants.ACTION_TEST]
        # res[Constants.RSI] = results[Constants.RSI]
        if self.showWeekLogs:
            res[Constants.WEEK_DIR_FLOW_DIFF] = results[Constants.WEEK_DIR_FLOW_DIFF]
            res[Constants.WEEK_DIR_FLOW] = results[Constants.WEEK_DIR_FLOW]
            res[Constants.WEEK_FLOW] = results[Constants.WEEK_FLOW]
            res[Constants.WEEK_FLOW_MED] = results[Constants.WEEK_FLOW_MED]
            res[Constants.WEEK_FLOW_STD] = results[Constants.WEEK_FLOW_STD]
            res[Constants.WEEK_FLOW_DIFF] = results[Constants.WEEK_FLOW_DIFF]
            res[Constants.WEEK_DIR] = results[Constants.WEEK_DIR]
            res[Constants.WEEK_DIR_TOP_DST] = results[Constants.WEEK_DIR_TOP_DST]
        if self.showExtraLogs:


            res[Constants.IND_PROB_FLOW] = results[Constants.IND_PROB_FLOW]

            res[Constants.CLOSE_NXT_UP] = results[Constants.CLOSE_NXT_UP]
            res[Constants.CLOSE_NXT_DOWN] = results[Constants.CLOSE_NXT_DOWN]
            res[Constants.CLOSE_NXT_MIDDLE] = results[Constants.CLOSE_NXT_MIDDLE]
            res[Constants.INDICATOR_MED] = results[Constants.INDICATOR_MED]
            res[Constants.ANGLEm1] = results[Constants.ANGLEm1]
            res[Constants.ANGLEm21] = results[Constants.ANGLEm21]

            res[Constants.IND_REL_FCST_PERCENT] = results[Constants.IND_REL_FCST_PERCENT]
            res[Constants.DIRECTION] = results[Constants.DIRECTION]

            res[Constants.MEDIA] = results[Constants.MEDIA]
            res[Constants.STDDESV] = results[Constants.STDDESV]
            res[Constants.IND_SUM_UP] = results[Constants.IND_SUM_UP]
            res[Constants.IND_SUM_DOWN] = results[Constants.IND_SUM_DOWN]
            res[Constants.IND_BLG_UPPER_DST_PERCENT] = results[Constants.IND_BLG_UPPER_DST_PERCENT]
        return res,resname
    def addStopValues(self, results, isBuy, active):
        if 'START' in self.operations.currentTupla:
            value = results[Constants.VALUE]
            date = results[Constants.DATE].values[0]
            self.operations.currentTupla['STOP'] = value
            self.operations.currentTupla['STOP_DATE'] = date
            name =self.operations.currentTupla['NAME']
            res, resname = self.extractResultsDataForAnalisys(results, isBuy, active,name=name)
            self.operations.currentTupla['resData_Stop'] = res
            # update endvalue
            self.operations.currentTupla['resData_Start'][Constants.ACTION_ACUM_END]=self.operations.currentTupla['resData_Stop'][Constants.ACTION_ACUM_END]

            if isBuy:
                self.operations.buyValues.append(self.operations.currentTupla)
            else:
                self.operations.sellValues.append(self.operations.currentTupla)
            self.operations.currentTupla = {}

    def addNormaValues(self, results, active, isBuy=False):
            value = results[Constants.VALUE]
            date = results[Constants.DATE].values[0]
            tupla = {}
            res, resname = self.extractResultsDataForAnalisys(results, isBuy,active,isnormal=True)
            tupla['resData_Normal'] = res
            # update endvalue
            self.operations.normalValues.append(tupla)

    def addStartValues(self, results,isBuy, active):
        # if 'START' in self.operations.currentTupla:
            value = results[Constants.VALUE]
            date = results[Constants.DATE].values[0]
            self.operations.currentTupla['STOP'] = value
            self.operations.currentTupla['STOP_DATE'] = date
            res, resname = self.extractResultsDataForAnalisys(results, isBuy,active, isStart=True)
            self.operations.currentTupla['resData_Start'] =res
            self.operations.currentTupla['NAME']=resname
            if isBuy:
                self.operations.currentTupla['START'] = value
                self.operations.currentTupla['START_DATE'] = date
            else:
                self.operations.currentTupla['START'] = value
                self.operations.currentTupla['START_DATE'] = date

    def drawActiveActions(self, actives):
        for active in actives:
            self.drawActiveAction(active, False)

    def verify3DaysInData(self, data):
        faltan = 0
        onlydates = pd.to_datetime(data['date'])
        newData = onlydates.groupby([onlydates.dt.date])
        size = len(newData.groups)
        if size < 3:
            faltan =3 -size


        print(f"faltan {faltan}")
        return faltan

    def simulateFlowConfigReview(self, active, start=None, end=None, draw=False, isDBData= True, prepareExcel = False):

        useConfig = True
        isDBData = isDBData
        simulation = True
        startSimGroup = 0
        send = False
        showBoolinger = True
        showima1 = True
        showima2 = False
        showima3 = False
        showima4 = False
        sorted = True

        data = None

        # plotty = PlottyService()
        plotty = PlottyService(showMa1=showima1, showMa2=showima2, showMa3=showima3,
                               showMa4=showima4, showBoolinger=showBoolinger)

        period = 2
        if isDBData:
            period = 2
            weekno = datetime.datetime.today().weekday()

            if weekno == 0:
                period = 4

            if start is not None and end is not None:

                data = self.dataBDMan.getAllWithNameForXdaysRangeDates(active.parameters.name, start, end)
                # if not isinstance(data.index, pd.DatetimeIndex):
                #     data.index = pd.to_datetime(data['date'])
                # df_hourly = data.resample('2H').first()
                # # df_half = data.resample('30T').first()
                # data = df_hourly.dropna()
            else:
                data = self.dataBDMan.getAllWithNameForXdays(active.parameters.name, period)
        else:
            # DATA YAHOO
            # data = yf.download(tickers=active.parameters.name, period='3d', interval='15m')
            # data = yf.download(tickers=active.parameters.name, interval='2h', start=start, end=end)
            nada= ""

        #Verificacion de que hay almenos 3 dias recuperados para procesar
        faltan = self.verify3DaysInData(data)
        start_date_time = None
        if faltan >0:
            if start is not None and end is not None:
                try:
                    start_date_time = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S.%f")
                except Exception as error:
                    # print("Error getAllWithNameForXdaysRangeDates  date format using second change", error)
                    start_date_time = datetime.datetime.strptime(start, "%Y-%m-%d")

                if start_date_time:
                    start_date_timeplus = start_date_time + datetime.timedelta(days=-faltan+1)
                    start = start_date_timeplus.strftime("%Y-%m-%d %H:%M:%S.%f")

                data = self.dataBDMan.getAllWithNameForXdaysRangeDates(active.parameters.name, start, end)
            else:
                period = period + faltan
                data = self.dataBDMan.getAllWithNameForXdays(active.parameters.name, period)
        # DATA FROM DB
        if useConfig:
            self.initConfig(active, data)

        size = len(data)
        print(f"TOTAL {size}")
        actives = list()
        actives.append(active)
        results = {}
        for x in range(startSimGroup, size + 1):
            if self.showLog:
                print(f"\nSIMULACION {x}")
            subData = data.head(x)
            results =self.search_prices_list_data_simulation(actives, subData)

        # self.sendResultsEndDay(sendResults=True)
        # self.calculateBESTDISTANCE()
        eval_name = ""
        if Constants.EVAl_NAME in results:
            eval_name = results[Constants.EVAl_NAME]
        # VER RESULTADOS FINALES
        tendence = None
        accumulated = None
        sellData = None
        buyData = None
        closeData = None
        rsiData = None
        tendenceWAIT = None
        tendenceDOWN = None
        tendenceUP = None

        if len(self.operations.sellData) > 0:
            sellData = pd.DataFrame(self.operations.sellData)
            if isDBData == False:
                sellData['date'] = pd.to_datetime(sellData['date'] + pd.DateOffset(hours=active.parameters.hourOffset),
                                                  format='%Y-%m-%d')

        if len(self.operations.buyData) > 0:
            buyData = pd.DataFrame(self.operations.buyData)
            if isDBData == False:
                buyData['date'] = pd.to_datetime(buyData['date'] + pd.DateOffset(hours=active.parameters.hourOffset),
                                                 format='%Y-%m-%d')

        if len(self.operations.closeData) > 0:
            closeData = pd.DataFrame(self.operations.closeData)
            if isDBData == False:
                closeData['date'] = pd.to_datetime(
                    closeData['date'] + pd.DateOffset(hours=active.parameters.hourOffset), format='%Y-%m-%d')

        if len(self.operations.rsiValues) > 0:
            rsiData = pd.DataFrame(self.operations.rsiValues)

        if len(self.operations.tendenceUP) > 0:
            tendenceUP = pd.DataFrame(self.operations.tendenceUP)
            if isDBData == False:
                tendenceUP['date'] = pd.to_datetime(
                    tendenceUP['date'] + pd.DateOffset(hours=active.parameters.hourOffset), format='%Y-%m-%d')
        if len(self.operations.tendenceDOWN) > 0:
            tendenceDOWN = pd.DataFrame(self.operations.tendenceDOWN)
            if isDBData == False:
                tendenceDOWN['date'] = pd.to_datetime(
                    tendenceDOWN['date'] + pd.DateOffset(hours=active.parameters.hourOffset), format='%Y-%m-%d')
        if len(self.operations.tendenceWAIT) > 0:
            tendenceWAIT = pd.DataFrame(self.operations.tendenceWAIT)
            if isDBData == False:
                tendenceWAIT['date'] = pd.to_datetime(
                    tendenceWAIT['date'] + pd.DateOffset(hours=active.parameters.hourOffset), format='%Y-%m-%d')

        if draw:
            if isDBData:
                # plotty.drawDatabaseSimulationClose(data, tendence, accumulated, sellData, buyData, closeData, None,
                #                                    None,
                #                                    None, type=active.parameters.name, send=send,
                #                                    rangehours=active.parameters.rangehours,
                #                                    drawWeekend=active.parameters.weekend, ima1=active.parameters.ima1,
                #                                    ima2=active.parameters.ima2, ima3=active.parameters.ima3,
                #                                    ima4=active.parameters.ima4,
                #                                    bollinger=active.parameters.bollinger,
                #                                    rsiData=rsiData)
                # rsiData = self.calculate_rsi(data)

                plotty.drawDatabaseSimulationClose(data, tendence, accumulated, sellData, buyData, closeData, tendenceUP,
                                                   tendenceDOWN, tendenceWAIT, type=active.parameters.name,send=send,
                                                   rangehours= active.parameters.rangehours, drawWeekend=active.parameters.weekend,
                                                   ima1=active.parameters.ima1, ima2=active.parameters.ima2, ima3=active.parameters.ima3,
                                                   ima4=active.parameters.ima4,bollinger=active.parameters.bollinger, rsiData= rsiData, active=active, eval_name = eval_name)

            else:
                # plotty.drawDataYahooSimulation(data, tendence, accumulated, sellData, buyData, closeData, None, None, None,
                #                                type=active.parameters.name, send=send,
                #                                rangehours=active.parameters.rangehours,
                #                                drawWeekend=active.parameters.weekend, ima1=active.parameters.ima1,
                #                                ima2=active.parameters.ima2, ima3=active.parameters.ima3,
                #                                ima4=active.parameters.ima4, rsiData = rsiData)

                plotty.drawDataYahooSimulation(data, tendence, accumulated, sellData, buyData, closeData,
                                               tendenceUP,
                                               tendenceDOWN, tendenceWAIT, type=active.parameters.name, send=send,
                                               rangehours=active.parameters.rangehours,
                                               drawWeekend=active.parameters.weekend,
                                               ima1=active.parameters.ima1, ima2=active.parameters.ima2,
                                               ima3=active.parameters.ima3,
                                               ima4=active.parameters.ima4, rsiData=rsiData)
            # plotty.drawDataYahooSimulation(data, tendence, accumulated, sellData, buyData, closeData, tendenceUP, tendenceDOWN,tendenceWAIT, type=active, send=send, rangehours=rangehours,drawWeekend=element.weekend, ima1=element.ima1, ima2=element.ima2, ima3=element.ima3)

        if send:
            telegram = TelegramService()
            telegram.enviarDocumento(f"./img/{active.parameters.name}.png", active.parameters.tele_group,
                                     active.parameters.name)
        # plotty.drawDataYahooSimultaion(data)

        totalBuy, totalSell = evaluateMarketMovements(self.operations.buyValues,
                                                      self.operations.sellValues, sorted)
        # generate analissys data
        if prepareExcel:
            generateAnalisysDataColoredOK(self.operations.buyValues, self.operations.sellValues, self.operations.normalValues, active)
        return totalBuy, totalSell

def generateAnalisysData(buyValues, sellvalues, normalValues, active):
    nada = ""
    try:
        from openpyxl import Workbook
        from openpyxl import load_workbook
        from datetime import datetime

        resData = list()
        for x in buyValues:
            if "resData_Start" in x:
                resData.append(x["resData_Start"])
            if "resData_Stop" in x:
                resData.append(x["resData_Stop"])

        for x in sellvalues:
            if "resData_Start" in x:
                resData.append(x["resData_Start"])
            if "resData_Stop" in x:
                resData.append(x["resData_Stop"])
        for x in normalValues:
            resData.append(x["resData_Normal"])
        fecha_hora_actual = datetime.now()

        # Convertir la fecha y hora en una cadena de texto
        fecha_hora_string = fecha_hora_actual.strftime("%Y-%m-%d_%H-%M-%S")
        activeName = active.parameters.name+"_"+str(fecha_hora_string)
        nombre_archivo = f"f:\\SALIDA\\{activeName}.xlsx"
        libro_trabajo_existente = Workbook()
        # Comprobar si el archivo ya existe
        try:
            libro_trabajo_existente = load_workbook(nombre_archivo)
            # Si el archivo existe, elimina todas las hojas excepto la primera (por defecto)
            libro_trabajo_existente.remove(libro_trabajo_existente.active)
            # Obtén la hoja activa del libro de trabajo existente
            # hoja = libro_trabajo_existente.active
        except FileNotFoundError:
            # Si el archivo no existe, crea uno nuevo
            libro_trabajo_existente = Workbook()
            # hoja = libro_trabajo_existente.active
            # Agrega una fila con los títulos de los campos

        hoja = libro_trabajo_existente.active
        titulos = list(resData[0].keys())
        hoja.append(titulos)

        # Llenar la hoja con los datos de los diccionarios
        for fila_dict in resData:
            fila = [fila_dict[titulo] for titulo in titulos]
            hoja.append(fila)

        for columna in hoja.columns:
            max_length = 0
            for celda in columna:
                try:
                    if len(str(celda.value)) > max_length:
                        max_length = len(celda.value)
                except:
                    pass
            adjusted_width = (max_length + 2) * 1.2
            hoja.column_dimensions[columna[0].column_letter].width = adjusted_width

        # Guardar el libro de trabajo en un archivo (sobrescribiendo si ya existe)
        libro_trabajo_existente.save(nombre_archivo)
    except Exception as e:
        print(f"error generateAnalisysData :{str(e)}")
def generateAnalisysDataColoredOK(buyValues, sellvalues, normalValues, active):
    try:
        from openpyxl import Workbook, load_workbook
        from openpyxl.styles import PatternFill
        from openpyxl.formatting.rule import FormulaRule
        from openpyxl.utils import get_column_letter
        from datetime import datetime

        # =========================
        # COLORES
        # =========================
        green_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
        red_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
        yellow_fill = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")

        # =========================
        # RECOLECTAR DATOS
        # =========================
        resData = []

        for x in buyValues:
            if "resData_Start" in x:
                resData.append(x["resData_Start"])
            if "resData_Stop" in x:
                resData.append(x["resData_Stop"])

        for x in sellvalues:
            if "resData_Start" in x:
                resData.append(x["resData_Start"])
            if "resData_Stop" in x:
                resData.append(x["resData_Stop"])

        for x in normalValues:
            resData.append(x["resData_Normal"])

        if not resData:
            print("No hay datos para exportar")
            return

        # =========================
        # NOMBRE ARCHIVO
        # =========================
        fecha_hora_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        activeName = active.parameters.name + "_" + fecha_hora_string
        nombre_archivo = f"f:\\SALIDA\\{activeName}.xlsx"

        # =========================
        # CREAR / CARGAR EXCEL
        # =========================
        try:
            libro = load_workbook(nombre_archivo)
            libro.remove(libro.active)
        except FileNotFoundError:
            libro = Workbook()

        hoja = libro.active

        # =========================
        # CABECERAS
        # =========================
        titulos = list(resData[0].keys())
        hoja.append(titulos)

        # Índices clave
        idx_start = titulos.index("START") if "START" in titulos else None
        idx_is_buy = titulos.index("IS_BUY") if "IS_BUY" in titulos else None

        # =========================
        # INSERTAR DATOS + COLOR FILA
        # =========================
        for fila_dict in resData:
            fila = [fila_dict.get(t, None) for t in titulos]
            hoja.append(fila)

            if idx_start is not None and idx_is_buy is not None:
                start_val = fila[idx_start]
                is_buy_val = fila[idx_is_buy]

                # Normalizar valores por si vienen como string
                start_val = str(start_val).lower() == "true"
                is_buy_val = str(is_buy_val).lower() == "true"

                if start_val:
                    fill = green_fill if is_buy_val else red_fill
                    row_num = hoja.max_row

                    for col in range(1, len(titulos) + 1):
                        hoja.cell(row=row_num, column=col).fill = fill

        # =========================
        # FORMATO CONDICIONAL PRO
        # =========================
        max_row = hoja.max_row
        max_col = hoja.max_column

        for col in range(1, max_col + 1):
            col_letter = get_column_letter(col)
            rango_col = f"{col_letter}2:{col_letter}{max_row}"

            hoja.conditional_formatting.add(
                rango_col,
                FormulaRule(formula=[f'ISNUMBER(SEARCH("BUY",{col_letter}2))'], fill=green_fill)
            )
            hoja.conditional_formatting.add(
                rango_col,
                FormulaRule(formula=[f'ISNUMBER(SEARCH("SELL",{col_letter}2))'], fill=red_fill)
            )
            hoja.conditional_formatting.add(
                rango_col,
                FormulaRule(formula=[f'ISNUMBER(SEARCH("WAIT",{col_letter}2))'], fill=yellow_fill)
            )

        # =========================
        # AUTOAJUSTE COLUMNAS
        # =========================
        for columna in hoja.columns:
            max_length = 0
            for celda in columna:
                try:
                    if celda.value:
                        max_length = max(max_length, len(str(celda.value)))
                except:
                    pass

            adjusted_width = (max_length + 2) * 1.2
            hoja.column_dimensions[columna[0].column_letter].width = adjusted_width

        # =========================
        # GUARDAR
        # =========================
        libro.save(nombre_archivo)

    except Exception as e:
        print(f"error generateAnalisysData :{str(e)}")
def generateAnalisysDataColored(buyValues, sellvalues, normalValues, active):
    try:
        from openpyxl import Workbook, load_workbook
        from openpyxl.styles import PatternFill
        from datetime import datetime

        # Colores
        green_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
        red_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")

        resData = list()
        for x in buyValues:
            if "resData_Start" in x:
                resData.append(x["resData_Start"])
            if "resData_Stop" in x:
                resData.append(x["resData_Stop"])

        for x in sellvalues:
            if "resData_Start" in x:
                resData.append(x["resData_Start"])
            if "resData_Stop" in x:
                resData.append(x["resData_Stop"])

        for x in normalValues:
            resData.append(x["resData_Normal"])

        fecha_hora_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        activeName = active.parameters.name + "_" + fecha_hora_string
        nombre_archivo = f"f:\\SALIDA\\{activeName}.xlsx"

        try:
            libro_trabajo_existente = load_workbook(nombre_archivo)
            libro_trabajo_existente.remove(libro_trabajo_existente.active)
        except FileNotFoundError:
            libro_trabajo_existente = Workbook()

        hoja = libro_trabajo_existente.active

        titulos = list(resData[0].keys())
        hoja.append(titulos)

        # Índices de columnas importantes
        idx_start = titulos.index("START")
        idx_is_buy = titulos.index("IS_BUY")

        # Llenar datos
        for fila_dict in resData:
            fila = [fila_dict[titulo] for titulo in titulos]
            hoja.append(fila)

            # Evaluar condiciones
            start_val = fila[idx_start]
            is_buy_val = fila[idx_is_buy]

            if start_val:  # START == True
                fill = green_fill if is_buy_val else red_fill

                # Aplicar color a toda la fila recién añadida
                row_num = hoja.max_row
                for col in range(1, len(titulos) + 1):
                    hoja.cell(row=row_num, column=col).fill = fill

        # Ajustar ancho de columnas
        for columna in hoja.columns:
            max_length = 0
            for celda in columna:
                try:
                    if len(str(celda.value)) > max_length:
                        max_length = len(str(celda.value))
                except:
                    pass
            adjusted_width = (max_length + 2) * 1.2
            hoja.column_dimensions[columna[0].column_letter].width = adjusted_width

        libro_trabajo_existente.save(nombre_archivo)

    except Exception as e:
        print(f"error generateAnalisysData :{str(e)}")
def evaluateMarketMovements(buyValues, sellValues, sortedList = False):
    buyAccumulated = 0
    sellAccumulated = 0
    if buyValues is not None and len(buyValues) > 0:

        print(f" BUY MOVEMENTS")
        if sortedList:
            mi_lista_ordenada = sorted(buyValues, key=lambda x: float(x['STOP'])-float(x['START']), reverse=True)
        else:
            mi_lista_ordenada = buyValues
        for x in mi_lista_ordenada:
            try:
                start = float(x['START'])
                start_date = x['START_DATE']
                stop = float(x['STOP'])
                stop_date = x['STOP_DATE']
                val = stop - start
                buyAccumulated = buyAccumulated + val
                print(f" start: {start} start_date: {start_date} stop: {stop} stop_date: {stop_date} value :{val}")
            except Exception as e:
                print(f"ERROR evaluateMarketMovements {str(e)}")
        print(f"TOTAL BUY VALUE: {buyAccumulated}")

    if sellValues is not None and len(sellValues) > 0:
        print(f" SELL MOVEMENTS")
        if sortedList:
            mi_lista_ordenada = sorted(sellValues, key=lambda x: float(x['STOP'])-float(x['START']), reverse=True)
        else:
            mi_lista_ordenada = sellValues
        for x in mi_lista_ordenada:
            try:
                start = float(x['START'])
                start_date = x['START_DATE']
                stop = float(x['STOP'])
                stop_date = x['STOP_DATE']
                val = start - stop
                sellAccumulated = sellAccumulated + val
                print(f" start: {start} start_date: {start_date} stop: {stop} stop_date: {stop_date} value :{val}")

            except Exception as e:

                print(f"ERROR sellValues {str(e)}")
        print(f"TOTAL SELL VALUE: {sellAccumulated}")
    print(f"Numero de operaciones BUY {len(buyValues)}")
    print(f"Numero de operaciones SELL {len(sellValues)}")
    if sellAccumulated is not None and buyAccumulated is not None:
        print(f"TOTAL GANANCIAS {buyAccumulated + sellAccumulated}")
    return buyAccumulated, sellAccumulated


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
        if isDBData == False:
            sellData['date'] = pd.to_datetime(sellData['date'] + pd.DateOffset(hours=active.parameters.hourOffset),
                                              format='%Y-%m-%d')

    if len(marketService.operations.buyData) > 0:
        buyData = pd.DataFrame(marketService.operations.buyData)
        if isDBData == False:
            buyData['date'] = pd.to_datetime(buyData['date'] + pd.DateOffset(hours=active.parameters.hourOffset),
                                             format='%Y-%m-%d')

    if len(marketService.operations.closeData) > 0:
        closeData = pd.DataFrame(marketService.operations.closeData)
        if isDBData == False:
            closeData['date'] = pd.to_datetime(closeData['date'] + pd.DateOffset(hours=active.parameters.hourOffset),
                                               format='%Y-%m-%d')

    if len(marketService.operations.tendenceUP) > 0:
        tendenceUP = pd.DataFrame(marketService.operations.tendenceUP)
        if isDBData == False:
            tendenceUP['date'] = pd.to_datetime(tendenceUP['date'] + pd.DateOffset(hours=active.parameters.hourOffset),
                                                format='%Y-%m-%d')

    if len(marketService.operations.tendenceDOWN) > 0:
        tendenceDOWN = pd.DataFrame(marketService.operations.tendenceDOWN)
        if isDBData == False:
            tendenceDOWN['date'] = pd.to_datetime(
                tendenceDOWN['date'] + pd.DateOffset(hours=active.parameters.hourOffset), format='%Y-%m-%d')
    if len(marketService.operations.tendenceWAIT) > 0:
        tendenceWAIT = pd.DataFrame(marketService.operations.tendenceWAIT)
        if isDBData == False:
            tendenceWAIT['date'] = pd.to_datetime(
                tendenceWAIT['date'] + pd.DateOffset(hours=active.parameters.hourOffset), format='%Y-%m-%d')

    if isDBData:
        plotty.drawDatabaseSimulationClose(data, tendence, accumulated, sellData, buyData, closeData, None, None, None,
                                           type=active.parameters.name, send=send,
                                           rangehours=active.parameters.rangehours,
                                           drawWeekend=active.parameters.weekend, ima1=active.parameters.ima1,
                                           ima2=active.parameters.ima2, ima3=active.parameters.ima3,
                                           ima4=active.parameters.ima4,
                                           bollinger=active.parameters.bollinger
                                           )
        # plotty.drawDatabaseSimulationClose(data, tendence, accumulated, sellData, buyData, closeData, tendenceUP, tendenceDOWN, tendenceWAIT, type=active.parameters.name,send=send, rangehours= active.parameters.rangehours, drawWeekend=active.parameters.weekend, ima1=active.parameters.ima1, ima2=active.parameters.ima2, ima3=active.parameters.ima3, ima4=active.parameters.ima4)

    else:
        # plotty.drawDataYahooSimulation(data, tendence, accumulated, sellData, buyData, closeData, None, None, None, type=active.parameters.name,send=send, rangehours= active.parameters.rangehours, drawWeekend=active.parameters.weekend, ima1=active.parameters.ima1, ima2=active.parameters.ima2, ima3=active.parameters.ima3, ima4=active.parameters.ima4)
        plotty.drawDataYahooSimulation(data, tendence, accumulated, sellData, buyData, closeData, tendenceUP,
                                       tendenceDOWN, tendenceWAIT, type=active, send=send,
                                       rangehours=active.parameters.rangehours, drawWeekend=active.parameters.weekend,
                                       ima1=active.parameters.ima1, ima2=active.parameters.ima2,
                                       ima3=active.parameters.ima3)

    if send:
        telegram = TelegramService()
        telegram.enviarDocumento(f"./img/{active.parameters.name}.png", active.parameters.tele_group,
                                 active.parameters.name)
    # plotty.drawDataYahooSimultaion(data)

    evaluateMarketMovements(marketService.operations.buyValues, marketService.operations.sellValues)


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
        current = subData.iloc[[-1]]
        marketService.search_prices_list_data_simulation_INSERT(actives, current)

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
        if isDBData == False:
            sellData['date'] = pd.to_datetime(sellData['date'] + pd.DateOffset(hours=active.parameters.hourOffset),
                                              format='%Y-%m-%d')

    if len(marketService.operations.buyData) > 0:
        buyData = pd.DataFrame(marketService.operations.buyData)
        if isDBData == False:
            buyData['date'] = pd.to_datetime(buyData['date'] + pd.DateOffset(hours=active.parameters.hourOffset),
                                             format='%Y-%m-%d')

    if len(marketService.operations.closeData) > 0:
        closeData = pd.DataFrame(marketService.operations.closeData)
        if isDBData == False:
            closeData['date'] = pd.to_datetime(closeData['date'] + pd.DateOffset(hours=active.parameters.hourOffset),
                                               format='%Y-%m-%d')

    if len(marketService.operations.tendenceUP) > 0:
        tendenceUP = pd.DataFrame(marketService.operations.tendenceUP)
        if isDBData == False:
            tendenceUP['date'] = pd.to_datetime(tendenceUP['date'] + pd.DateOffset(hours=active.parameters.hourOffset),
                                                format='%Y-%m-%d')
    if len(marketService.operations.tendenceDOWN) > 0:
        tendenceDOWN = pd.DataFrame(marketService.operations.tendenceDOWN)
        if isDBData == False:
            tendenceDOWN['date'] = pd.to_datetime(
                tendenceDOWN['date'] + pd.DateOffset(hours=active.parameters.hourOffset), format='%Y-%m-%d')
    if len(marketService.operations.tendenceWAIT) > 0:
        tendenceWAIT = pd.DataFrame(marketService.operations.tendenceWAIT)
        if isDBData == False:
            tendenceWAIT['date'] = pd.to_datetime(
                tendenceWAIT['date'] + pd.DateOffset(hours=active.parameters.hourOffset), format='%Y-%m-%d')

    if isDBData:
        plotty.drawDatabaseSimulationClose(data, tendence, accumulated, sellData, buyData, closeData, None, None, None,
                                           type=active.parameters.name, send=send,
                                           rangehours=active.parameters.rangehours,
                                           drawWeekend=active.parameters.weekend, ima1=active.parameters.ima1,
                                           ima2=active.parameters.ima2, ima3=active.parameters.ima3)

    else:
        # plotty.drawDataYahooSimulation(data, tendence, accumulated, sellData, buyData, closeData, None, None, None, type=active.parameters.name,send=send, rangehours= active.parameters.rangehours, drawWeekend=active.parameters.weekend, ima1=active.parameters.ima1, ima2=active.parameters.ima2, ima3=active.parameters.ima3)
        plotty.drawDataYahooSimulation(data, tendence, accumulated, sellData, buyData, closeData, tendenceUP,
                                       tendenceDOWN, tendenceWAIT, type=active, send=send,
                                       rangehours=active.parameters.rangehours, drawWeekend=active.parameters.weekend,
                                       ima1=active.parameters.ima1, ima2=active.parameters.ima2,
                                       ima3=active.parameters.ima3)

    if send:
        telegram = TelegramService()
        telegram.enviarDocumento(f"./img/{active.parameters.name}.png", active.parameters.tele_group,
                                 active.parameters.name)
    # plotty.drawDataYahooSimultaion(data)

    evaluateMarketMovements(marketService.operations.buyValues, marketService.operations.sellValues)


def RealModeConfig():
    isDBData = False
    useConfig = True
    simulation = True
    marketService = MarketManager(simulation=simulation, isDBData=isDBData, useConfig=useConfig)
    activeHelper = ActiveHelper(isDBData=isDBData)
    actives = activeHelper.prepareActives()
    marketService.search_prices_list(actives)
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
    operate = True
    showLog = True
    disableCloseEndRevenue = True
    disableInitPROB = False
    marketService = MarketManager(simulation=simulation, isDBData=isDBData, useConfig=useConfig, showLog=showLog,
                                  disableInitPROB=disableInitPROB, disableCloseEndRevenue=disableCloseEndRevenue, operate=operate)
    activeHelper = ActiveHelper(isDBData=isDBData)
    actives = activeHelper.prepareActivesRealLocal(skipDayControl)
    allactives = activeHelper.prepareActivesRealLocal(skipDayControl)
    # marketService.updateTimeZoneValues()
    # todos los activos
    marketService.updateIntervalForAll(allactives)
    marketService.search_prices_list_local(actives)
    marketService.updateCounterForAll()
    marketService.sendResultsEndDay()


def drawActive():
    isDBData = True
    useConfig = False
    simulation = False
    marketService = MarketManager(simulation=simulation, isDBData=isDBData, useConfig=useConfig)
    activeHelper = ActiveHelper(isDBData=isDBData)
    # actives = activeHelper.prepareActiveForDraw()
    actives = activeHelper.prepareActives()
    # rangehours = [22, 15]
    marketService.drawActiveActions(actives)


def drawActiveDates(skipDayControl = False):
    isDBData = True
    useConfig = False
    simulation = True
    draw = True
    disableprob = True
    disableCloseEndRevenue = False
    start = '2025-07-01'
    end = '2025-07-20'
    marketService = MarketManager(simulation=simulation, isDBData=isDBData, useConfig=useConfig, start=start, end=end,
                                  showLog=False, disableInitPROB=disableprob,
                                  disableCloseEndRevenue=disableCloseEndRevenue)
    activeHelper = ActiveHelper(simulation=simulation, isDBData=isDBData)
    # actives = activeHelper.prepareActiveForDraw()
    actives = activeHelper.prepareActives(skipDayControl)
    # rangehours = [22, 15]
    marketService.drawActiveActions(actives)

def drawActiveDatesSelected(skipDayControl = False):
    isDBData = True
    useConfig = False
    simulation = True
    draw = True
    disableprob = True
    disableCloseEndRevenue = False
    start = '2026-04-01'
    end = '2026-04-25'
    marketService = MarketManager(simulation=simulation, isDBData=isDBData, useConfig=useConfig, start=start, end=end,
                                  showLog=False, disableInitPROB=disableprob,
                                  disableCloseEndRevenue=disableCloseEndRevenue)
    activeHelper = ActiveHelper(simulation=simulation, isDBData=isDBData)
    # actives = activeHelper.prepareActiveForDraw()
    actives = activeHelper.prepareActivesSelected(skipDayControl)
    # rangehours = [22, 15]
    marketService.drawActiveActions(actives)


def simulateFlowActive():
    useConfig = True
    isDBData = True
    simulation = True
    draw = True

    marketService = MarketManager(simulation=simulation, isDBData=isDBData, useConfig=useConfig, showLog=False)
    activeHelper = ActiveHelper(simulation=simulation, isDBData=isDBData)

    # active = activeHelper.prepareTSLA02()
    # active = activeHelper.prepareBTC()
    # active = activeHelper.prepareAMZN1()
    # active = activeHelper.prepareNFLX1()
    # active = activeHelper.prepareAMZN2()
    # active = activeHelper.prepareAAPL6()
    # active = activeHelper.prepareAAPL1()
    # start = '2023-06-08'
    # end = '2023-06-10'

    # SUBE
    # start = '2023-05-31'
    # end = '2023-06-02'

    # baja
    # start = '2023-05-30'
    # end = '2023-05-31'

    start = '2023-11-09'
    end = '2024-03-17'

    # NOCHANGE
    # start = '2023-04-28'
    # end = '2023-05-04'




    # totaBuy, totalSell = marketService.simulateFlowConfigReview(active,start, end, draw=draw)
    # print(f"valores para active {active.parameters.name} ")
    # print(f"BUY :{totaBuy} SELL :{totalSell} TOTAL: {float(totaBuy + totalSell)}")


def drawRelativeTendence():
    useConfig = True
    isDBData = True
    simulation = True
    draw = True
    disableprob = False
    disableCloseEndRevenue = True
    needAnalsis = False
    # needAnalsis = True

    prepareExcel = False
    # prepareExcel = True

    # logs de valores que no se han convertido en acciones
    allAnalysLogs = False

    showima1 = False
    showima2 = True
    showima3 = False
    showima4 = False
    showBoollinger = True
    showHourly = True

    start = '2024-06-01'
    end = '2024-06-24'

    marketService = MarketManager(simulation=simulation, isDBData=isDBData, useConfig=useConfig, start=start, end=end,
                                  showLog=False, disableInitPROB=disableprob,
                                  disableCloseEndRevenue=disableCloseEndRevenue, needAnalsis=needAnalsis,
                                  allAnalysLogs=allAnalysLogs)
    activeHelper = ActiveHelper(simulation=simulation, isDBData=isDBData)


    dataBDMan = MarketSQLManager(False)

    # active = activeHelper.prepareTSLA()
    # active = activeHelper.prepareKO3()
    # active = activeHelper.prepareAMZN4()
    # active = activeHelper.prepareINTC()
    # active = activeHelper.prepareMSFT04()
    # active = activeHelper.prepareNFLX5()
    # active = activeHelper.prepareGOOG5()
    # active = activeHelper.prepareBTC3()
    # active = activeHelper.prepareETH2()
    active = activeHelper.prepareAAPL6()
    # active = activeHelper.prepareDIS08()
    # active = activeHelper.prepareNVDA06()
    # active = activeHelper.prepareVTI02()
    # active = activeHelper.prepareBABA02()
    # active = activeHelper.prepareMETA02()
    # active = activeHelper.prepareSBUX()
    # active = activeHelper.prepareAMD05()
    # active = activeHelper.prepareMCD02()
    # active = activeHelper.prepareSONY03()
    # active = activeHelper.prepareHD01()



    # data = yf.download(tickers=active.parameters.name, interval='1d', start=start,end=end)
    plotty = PlottyService(showMa1=showima1, showMa2=showima2, showMa3=showima3,
                           showMa4=showima4, showBoolinger=True)
    # plotty.drawDataYahooDays(data,active.parameters.ima1, active.parameters.ima3,active.parameters.weekend,active.parameters.name,False,active.parameters.rangehours)

    data = dataBDMan.getAllWithNameForXdaysRangeDates(active.parameters.name, start, end)
    if showHourly:
        if not isinstance(data.index, pd.DatetimeIndex):
            data.index = pd.to_datetime(data['date'])
        df_hourly = data.resample('2H').first()
        # df_half = data.resample('30T').first()
        data = df_hourly.dropna()

    # data = dataBDMan.getAllWithNameForXdays(active.name, days)

    # plotty.drawDataBaseXDays(data, active.parameters.ima1, active.parameters.ima3, active.parameters.weekend,
    #                          active.parameters.name, False, active.parameters.rangehours)

    # plotty.drawDatabaseSimulation(data, tendence=None, accumulated=None, sellData=None, buyData=None, closeData=None,
    #                        tendenceUP=None, tendenceDOWN=None, tendenceWAIT=None, type=None, send=False,
    #                        rangehours=None, drawWeekend=False, ima1=5, ima2=15, ima3=20)

    plotty.drawDatabaseSimulationClose(data, None, None, None, None, None, None,
                                       None,
                                       None, type=active.parameters.name, send=False,
                                       rangehours=active.parameters.rangehours,
                                       drawWeekend=active.parameters.weekend, ima1=active.parameters.ima1,
                                       ima2=active.parameters.ima2, ima3=active.parameters.ima3,
                                       ima4=active.parameters.ima4,
                                       bollinger=active.parameters.bollinger,
                                       rsiData=None)


#@mide_tiempo
def simulateWeekDirection():
    useConfig = True
    isDBData = True
    simulation = True
    draw = True
    disableprob = False
    disableCloseEndRevenue = True

    # UP


    # start = '2024-01-21'
    # end = '2024-02-21'
    # start = '2024-02-18'
    # start = '2024-02-15'
    # end = '2024-03-15'
    # start = '2024-04-17'
    # end = '2024-04-19'
    # start = '2024-03-28'
    # end = '2024-04-05'
    start = '2024-04-20'
    end = '2024-04-23'
    from service.MarketSQLManager import MarketSQLManager


    symbol = 'TSLA'

    dataBDMan = MarketSQLManager()
    data = dataBDMan.getAllWithNameForXdaysRangeDates(symbol, start, end)
    if not isinstance(data.index, pd.DatetimeIndex):
        data.index = pd.to_datetime(data['date'])
    df_hourly = data.resample('3H').first()
    # df_half = data.resample('30T').first()
    data = df_hourly.dropna()




#@mide_tiempo
def simulateIndicatorDates():
    useConfig = True
    isDBData = True
    simulation = True
    draw = True
    disableprob = False #desactiva probabiliddes inicio dia y fin

    # updateDBSimulation = True
    updateDBSimulation = False

    # disableprob = False
    disableCloseEndRevenue = False
    onlyStartEnd = False
    needAnalsis = False
    # needAnalsis = True

    prepareExcel = True
    # prepareExcel = False

    #logs de valores que no se han convertido en acciones
    allAnalysLogs = True
    # allAnalysLogs = False

    # showAnallisisFlow = True
    showAnallisisFlow = False

    # UP


    # start = '2024-01-21'
    # end = '2024-02-21'
    # start = '2024-02-18'
    # start = '2024-02-15'
    # end = '2024-03-15'
    # start = '2024-11-08'
    # end = '2024-11-19'
    # start = '2024-12-13'
    # end = '2024-12-23'ERROR evaluateActio
    # start = '2024-12-20'
    # end = '2025-01-04'
    # start = '2024-12-30'

    # start = '2025-03-12'
    # start = '2025-04-01'
    # end = '2025-04-14'

    # start = '2025-02-04'
    # end = '2025-02-18'

    # start = '2025-03-26'
    # # end = '2025-04-04'
    # end = '2025-03-31'

    start = '2026-05-14'
    # end = '2025-04-11'
    end = '2026-05-18'

    # start = '2025-01-17'
    # end = '2025-01-21'



    marketService = MarketManager(simulation=simulation, isDBData=isDBData, useConfig=useConfig, start=start, end=end,
                                  showLog=False, disableInitPROB=disableprob,
                                  disableCloseEndRevenue=disableCloseEndRevenue, needAnalsis=needAnalsis, allAnalysLogs=allAnalysLogs, onlyStartEnd= onlyStartEnd,
                                  showAnallisisFlow = showAnallisisFlow, updateDBSimulation=updateDBSimulation)
    activeHelper = ActiveHelper(simulation=simulation, isDBData=isDBData)


    # active = activeHelper.prepareTSLA02()
    # active = activeHelper.prepareKO3()
    # active = activeHelper.prepareAMZN4()
    active = activeHelper.prepareINTC()
    # active = activeHelper.prepareMSFT04()
    # active = activeHelper.prepareNFLX5()
    # active = activeHelper.prepareGOOG5()
    # active = activeHelper.prepareBTC3()
    # active = activeHelper.prepareGLD()
    # active = activeHelper.prepareETH2()
    # active = activeHelper.prepareAAPL7()
    # active = activeHelper.prepareGLD()
    # active = activeHelper.prepareDIS08()
    # active = activeHelper.prepareNVDA06()
    # active = activeHelper.prepareVTI02()
    # active = activeHelper.prepareBABA02()
    # active = activeHelper.prepareMETA02()
    # active = activeHelper.prepareSBUX()
    # active = activeHelper.prepareAMD06()
    # active = activeHelper.prepareMCD02()
    # active = activeHelper.prepareSONY03()
    # active = activeHelper.prepareHD01()

    totaBuy, totalSell = marketService.simulateFlowConfigReview(active, start, end, draw=draw, isDBData=isDBData, prepareExcel = prepareExcel)
    print(f"valores para active {active.parameters.name} ")
    print(f"BUY :{totaBuy} SELL :{totalSell} TOTAL: {float(totaBuy + totalSell)}")


def simulateEvaluatorsForActiveDates():
    useConfig = True
    isDBData = True
    simulation = True
    draw = False
    disableprob = False
    disableCloseEndRevenue = False
    updateDBSimulation = False

    # start = '2023-10-03'
    # end = '2023-10-04'

    # start = '2023-10-09'
    # end = '2023-10-10'
    # start = '2023-10-13'
    # end = '2023-10-19'

    start = '2026-04-20'
    end = '2026-04-25'


    marketService = MarketManager(simulation=simulation, isDBData=isDBData, useConfig=useConfig, start=start, end=end,
                                  showLog=False, disableInitPROB=disableprob,
                                  disableCloseEndRevenue=disableCloseEndRevenue)
    activeHelper = ActiveHelper(simulation=simulation, isDBData=isDBData)

    # active = activeHelper.prepareTSLA02()
    # active = activeHelper.prepareKO3()
    # active = activeHelper.prepareAMZN4()
    active = activeHelper.prepareINTC()
    # active = activeHelper.prepareMSFT04()
    # active = activeHelper.prepareNFLX5()
    # active = activeHelper.prepareGOOG5()
    # active = activeHelper.prepareBTC3()
    # active = activeHelper.prepareETH2()
    # active = activeHelper.prepareAAPL7()
    # active = activeHelper.prepareDIS08()
    # active = activeHelper.prepareNVDA06()
    # active = activeHelper.prepareVTI02()
    # active = activeHelper.prepareBABA02()
    # active = activeHelper.prepareMETA02()
    # active = activeHelper.prepareSBUX()
    # active = activeHelper.prepareAMD06()
    # active = activeHelper.prepareMCD02()
    # active = activeHelper.prepareSONY03()
    # active = activeHelper.prepareHD01()

    activesList = list()
    results = list()

    # activesList = activeHelper.prepareActivesEvaluators(active)
    # activesList = activeHelper.prepareActivesEvaluators2(active)
    # activesList = activeHelper.prepareActivesEvaluators3(active)
    #para optimizar tiene los mejores evaluadores
    # activesList = activeHelper.prepareActivesEvaluators4(active)
    # activesList = activeHelper.prepareActivesEvaluatorsONLYUP(active)
    activesList = activeHelper.prepareActivesEvaluatorsONLYUPNEW(active)
    for x in activesList:
        resValues = {}
        # marketService = MarketManager(simulation=simulation, isDBData=isDBData, useConfig=useConfig, start=start,
        #                               end=end,
        #                               showLog=False)

        marketService = MarketManager(simulation=simulation, isDBData=isDBData, useConfig=useConfig, start=start,
                                      end=end,
                                      showLog=False, disableInitPROB=disableprob,
                                      disableCloseEndRevenue=disableCloseEndRevenue)

        activeHelper = ActiveHelper(simulation=simulation, isDBData=isDBData)

        totaBuy, totalSell = marketService.simulateFlowConfigReview(x, start, end, draw=draw)
        resValues["totalBuy"] = totaBuy
        resValues["totalSell"] = totalSell
        resValues["total"] = float(totaBuy + totalSell)
        resValues["evaluator"] = x.evaluator.name
        results.append(resValues)

        # print(f"valores para active {active.parameters.name} ")
        # print(f"BUY :{totaBuy} SELL :{totalSell} TOTAL: {float(totaBuy + totalSell)}")

    # results.sort(key=lambda x: x.get('total'), reverse=True)
    results.sort(key=lambda x: x.get('total'), reverse=True)
    print(f"\n\nRESULTADOS FINALES ")
    for y in results:
        print(f" EVALUATOR: {y['evaluator']}")
        print(f" TOTAL BUY: {y['totalBuy']}")
        print(f" TOTAL SELL: {y['totalSell']}")
        print(f" TOTAL: {y['total']} \n\n")
    # print(results)

def simulate_Star_Close_ForActiveDates():
    useConfig = True
    isDBData = True
    simulation = True
    draw = False
    disableprob = False
    disableCloseEndRevenue = False

    # start = '2023-10-03'
    # end = '2023-10-04'

    # start = '2023-10-09'
    # end = '2023-10-10'
    # start = '2023-10-13'
    # end = '2023-10-19'


    start = '2026-04-01'
    end = '2026-04-24'


    marketService = MarketManager(simulation=simulation, isDBData=isDBData, useConfig=useConfig, start=start, end=end,
                                  showLog=False, disableInitPROB=disableprob,
                                  disableCloseEndRevenue=disableCloseEndRevenue)
    activeHelper = ActiveHelper(simulation=simulation, isDBData=isDBData)

    # active = activeHelper.prepareTSLA02()
    # active = activeHelper.prepareKO3()
    # active = activeHelper.prepareAMZN4()
    # active = activeHelper.prepareINTC()
    # active = activeHelper.prepareMSFT04()
    active = activeHelper.prepareNFLX5()
    # active = activeHelper.prepareGOOG5()
    # active = activeHelper.prepareBTC3()
    # active = activeHelper.prepareETH2()
    # active = activeHelper.prepareAAPL7()
    # active = activeHelper.prepareDIS08()
    # active = activeHelper.prepareNVDA06()
    # active = activeHelper.prepareVTI02()
    # active = activeHelper.prepareBABA02()
    # active = activeHelper.prepareMETA02()
    # active = activeHelper.prepareSBUX()
    # active = activeHelper.prepareAMD06()
    # active = activeHelper.prepareMCD02()
    # active = activeHelper.prepareSONY03()
    # active = activeHelper.prepareHD01()

    activesList = list()
    results = list()

    activesList = activeHelper.prepare_Actives_Start_CLose_Evaluators(active)

    for x in activesList:
        resValues = {}
        # marketService = MarketManager(simulation=simulation, isDBData=isDBData, useConfig=useConfig, start=start,
        #                               end=end,
        #                               showLog=False)

        marketService = MarketManager(simulation=simulation, isDBData=isDBData, useConfig=useConfig, start=start,
                                      end=end,
                                      showLog=False, disableInitPROB=disableprob,
                                      disableCloseEndRevenue=disableCloseEndRevenue)

        activeHelper = ActiveHelper(simulation=simulation, isDBData=isDBData)

        totaBuy, totalSell = marketService.simulateFlowConfigReview(x, start, end, draw=draw)
        resValues["totalBuy"] = totaBuy
        resValues["totalSell"] = totalSell
        resValues["total"] = float(totaBuy + totalSell)
        resValues["evaluator"] = x.evaluator.name
        resValues["startProbDef"] = x.parameters.startProbDef
        resValues["endProbDef"] = x.parameters.endProbDef
        results.append(resValues)

        # print(f"valores para active {active.parameters.name} ")
        # print(f"BUY :{totaBuy} SELL :{totalSell} TOTAL: {float(totaBuy + totalSell)}")

    # results.sort(key=lambda x: x.get('total'), reverse=True)
    results.sort(key=lambda x: x.get('total'), reverse=True)
    print(f"\n\nRESULTADOS FINALES ")
    for y in results:
        print(f" EVALUATOR: {y['evaluator']}")
        print(f" startProbDef: {y['startProbDef']}")
        print(f" endProbDef: {y['endProbDef']}")
        print(f" TOTAL BUY: {y['totalBuy']}")
        print(f" TOTAL SELL: {y['totalSell']}")
        print(f" TOTAL: {y['total']} \n\n")
    # print(results)


def simulate_EMA_parameters_ForActiveDates():
    useConfig = True
    isDBData = True
    simulation = True
    draw = False
    disableprob = False
    disableCloseEndRevenue = True

    # start = '2023-10-03'
    # end = '2023-10-04'

    # start = '2023-10-09'
    # end = '2023-10-10'
    # start = '2023-10-13'
    # end = '2023-10-19'


    start = '2026-02-11'
    end = '2026-02-15'


    marketService = MarketManager(simulation=simulation, isDBData=isDBData, useConfig=useConfig, start=start, end=end,
                                  showLog=False, disableInitPROB=disableprob,
                                  disableCloseEndRevenue=disableCloseEndRevenue)
    activeHelper = ActiveHelper(simulation=simulation, isDBData=isDBData)

    # active = activeHelper.prepareTSLA02()
    # active = activeHelper.prepareKO3()
    # active = activeHelper.prepareAMZN4()
    # active = activeHelper.prepareINTC()
    # active = activeHelper.prepareMSFT04()
    # active = activeHelper.prepareNFLX5()
    # active = activeHelper.prepareGOOG5()
    active = activeHelper.prepareBTC3()
    # active = activeHelper.prepareETH2()
    # active = activeHelper.prepareAAPL7()
    # active = activeHelper.prepareDIS08()
    # active = activeHelper.prepareNVDA06()
    # active = activeHelper.prepareVTI02()
    # active = activeHelper.prepareBABA02()
    # active = activeHelper.prepareMETA02()
    # active = activeHelper.prepareSBUX()
    # active = activeHelper.prepareAMD06()
    # active = activeHelper.prepareMCD02()
    # active = activeHelper.prepareSONY03()
    # active = activeHelper.prepareHD01()

    activesList = list()
    results = list()

    activesList = activeHelper.prepare_EMA_parameters(active)

    for x in activesList:
        resValues = {}
        # marketService = MarketManager(simulation=simulation, isDBData=isDBData, useConfig=useConfig, start=start,
        #                               end=end,
        #                               showLog=False)

        marketService = MarketManager(simulation=simulation, isDBData=isDBData, useConfig=useConfig, start=start,
                                      end=end,
                                      showLog=False, disableInitPROB=disableprob,
                                      disableCloseEndRevenue=disableCloseEndRevenue)

        activeHelper = ActiveHelper(simulation=simulation, isDBData=isDBData)

        totaBuy, totalSell = marketService.simulateFlowConfigReview(x, start, end, draw=draw)
        resValues["totalBuy"] = totaBuy
        resValues["totalSell"] = totalSell
        resValues["total"] = float(totaBuy + totalSell)
        resValues["evaluator"] = x.evaluator.name
        resValues["ema10"] = x.parameters.ema10
        resValues["ema20"] = x.parameters.ema20
        results.append(resValues)

        # print(f"valores para active {active.parameters.name} ")
        # print(f"BUY :{totaBuy} SELL :{totalSell} TOTAL: {float(totaBuy + totalSell)}")

    # results.sort(key=lambda x: x.get('total'), reverse=True)
    results.sort(key=lambda x: x.get('total'), reverse=True)
    print(f"\n\nRESULTADOS FINALES ")
    for y in results:
        print(f" EVALUATOR: {y['evaluator']}")
        print(f" ema10: {y['ema10']}")
        print(f" ema20: {y['ema20']}")
        print(f" TOTAL BUY: {y['totalBuy']}")
        print(f" TOTAL SELL: {y['totalSell']}")
        print(f" TOTAL: {y['total']} \n\n")
    # print(results)

def simulate_Control_ForActiveDates():
    useConfig = True
    isDBData = True
    simulation = True
    draw = False
    disableprob = False
    disableCloseEndRevenue = True

    # start = '2023-10-03'
    # end = '2023-10-04'

    # start = '2023-10-09'
    # end = '2023-10-10'
    # start = '2023-10-13'
    # end = '2023-10-19'


    start = '2025-04-01'
    end = '2025-05-01'


    marketService = MarketManager(simulation=simulation, isDBData=isDBData, useConfig=useConfig, start=start, end=end,
                                  showLog=False, disableInitPROB=disableprob,
                                  disableCloseEndRevenue=disableCloseEndRevenue)
    activeHelper = ActiveHelper(simulation=simulation, isDBData=isDBData)

    active = activeHelper.prepareTSLA02()
    # active = activeHelper.prepareKO3()
    # active = activeHelper.prepareAMZN4()
    # active = activeHelper.prepareINTC()
    # active = activeHelper.prepareMSFT04()
    # active = activeHelper.prepareNFLX5()
    # active = activeHelper.prepareGOOG5()
    # active = activeHelper.prepareBTC3()
    # active = activeHelper.prepareETH2()
    # active = activeHelper.prepareAAPL6()
    # active = activeHelper.prepareDIS08()
    # active = activeHelper.prepareNVDA06()
    # active = activeHelper.prepareVTI02()
    # active = activeHelper.prepareBABA02()
    # active = activeHelper.prepareMETA02()
    # active = activeHelper.prepareSBUX()
    # active = activeHelper.prepareAMD05()
    # active = activeHelper.prepareMCD02()
    # active = activeHelper.prepareSONY03()
    # active = activeHelper.prepareHD01()

    activesList = list()
    results = list()

    activesList = activeHelper.prepare_Actives_Control_Evaluators(active)

    for x in activesList:
        resValues = {}
        # marketService = MarketManager(simulation=simulation, isDBData=isDBData, useConfig=useConfig, start=start,
        #                               end=end,
        #                               showLog=False)

        marketService = MarketManager(simulation=simulation, isDBData=isDBData, useConfig=useConfig, start=start,
                                      end=end,
                                      showLog=False, disableInitPROB=disableprob,
                                      disableCloseEndRevenue=disableCloseEndRevenue)

        activeHelper = ActiveHelper(simulation=simulation, isDBData=isDBData)

        totaBuy, totalSell = marketService.simulateFlowConfigReview(x, start, end, draw=draw)
        resValues["totalBuy"] = totaBuy
        resValues["totalSell"] = totalSell
        resValues["total"] = float(totaBuy + totalSell)
        resValues["evaluator"] = x.evaluator.name
        resValues["controlBUY"] = x.parameters.controlBUY
        resValues["controlSELL"] = x.parameters.controlSELL
        results.append(resValues)

        # print(f"valores para active {active.parameters.name} ")
        # print(f"BUY :{totaBuy} SELL :{totalSell} TOTAL: {float(totaBuy + totalSell)}")

    # results.sort(key=lambda x: x.get('total'), reverse=True)
    results.sort(key=lambda x: x.get('total'), reverse=True)
    print(f"\n\nRESULTADOS FINALES ")
    for y in results:
        print(f" EVALUATOR: {y['evaluator']}")
        print(f" controlBUY: {y['controlBUY']}")
        print(f" controlSELL: {y['controlSELL']}")
        print(f" TOTAL BUY: {y['totalBuy']}")
        print(f" TOTAL SELL: {y['totalSell']}")
        print(f" TOTAL: {y['total']} \n\n")
    # print(results)

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    try:
        env = config['DEFAULT']['DEF_CONF']
    except Exception as e:
        print("Error defaut LINUX")
        env = "LINUX"


    if "LINUX" in env:
        RealMode()
        # skipDayControl = True
        # RealModeLocal(skipDayControl)
    else:
        skipDayControl = True
            # RealMode()
        # RealModeLocal(skipDayControl)
        # drawActive()
        # drawActiveDates(skipDayControl)
        # drawActiveDatesSelected(skipDayControl)
        # RealModeConfig()n
        # simulateFlow()#simulacion con dos BD
        # simulateFlowConfig()
        # simulateFlowActive()
        # simulateWeekDirection()
        # RealMode()

        simulateIndicatorDates()
        # simulateEvaluatorsForActiveDates()
        # simulate_Star_Close_ForActiveDates()
        # simulate_EMA_parameters_ForActiveDates()
        # simulate_Control_ForActiveDates()
        # drawRelativeTendence()


if __name__ == "__main__":
    main()
