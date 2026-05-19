from service.ActiveHelper import ActiveHelper
from service.Constants import Constants
from service.MarketSQLManager import MarketSQLManager
import pandas as pd
import math
import datetime
import time
# from datetime import datetime, timedelta
# import talib


class AnalisisHelper:
    def __init__(self):

        self.databaseMan = MarketSQLManager()
        self.closeValue = 'value'

    def mide_tiempo(funcion):
        def funcion_medida(*args, **kwargs):
            inicio = time.time()
            c = funcion(*args, **kwargs)

            print(f"Tiempo para {str(funcion)} es : {time.time() - inicio}")
            return c

        return funcion_medida

    def getWeekDirection(self, results, data, active, start, end):

        # data = self.databaseMan.getAllWithNameForXdaysRangeDatesExactdays(active.parameters.name, start, end)
        if not isinstance(data.index, pd.DatetimeIndex):
            data.index = pd.to_datetime(data['date'])
        # df_hourly = data.resample(active.parameters.weekDirectionInterval).first()
        # df_half = data.resample('30T').first()
        # data2 = df_hourly.dropna(subset=['date'])
        # data2['value'] = data2['value'].rolling(window=5).mean()
        # self.analizeData(data2, results)

    def analizeData(self, data, results):
        min = 999999
        extremMin = 999999
        max = 0
        extremMax = 0
        first = True
        second = True
        flujo = None
        prev_flujo = None
        direction = None
        previusValue = None
        currentValue = 0
        direction = Constants.DIR_WAIT
        for index, row in data.iterrows():
            if first:
                min = max = extremMin = extremMax = float(row[self.closeValue])
                first = False
                previusValue = float(row[self.closeValue])
            else:
                currentValue = float(row[self.closeValue])
                if previusValue > currentValue:
                    flujo = Constants.FLUJO_BAJA

                else:
                    flujo = Constants.FLUJO_SUBE
                previusValue = currentValue

                if second:
                    second = False
                    if flujo == Constants.FLUJO_SUBE:
                        direction = Constants.DIR_UP
                    else:
                        direction = Constants.DIR_DOWN
                    prev_flujo = flujo

                if prev_flujo != flujo:
                    if prev_flujo == Constants.FLUJO_SUBE:
                        if min == extremMin:
                            min = currentValue
                    else:
                        if max == extremMax:
                            max = currentValue

                prev_flujo = flujo
                nda = ""
                # if float(min_dir) >= 99999:
                #     min_dir = currentValue
                #     max_dir = currentValue
                # if direction is None or direction == Constants.DIR_WAIT:
                #
                #     if flujo == Constants.FLUJO_SUBE:
                #         direction = Constants.DIR_UP
                #     elif flujo == Constants.FLUJO_BAJA:
                #         direction = Constants.DIR_DOWN
                #
                # # CAMBIO DE DIRECCION
                # if tendence != flujo:
                #     if flujo == Constants.FLUJO_SUBE:
                #         if changePoint:
                #             min_dir = changePoint
                #         else:
                #             min_dir = min_dir
                #     elif flujo == Constants.FLUJO_BAJA:
                #         if changePoint:
                #             max_dir = changePoint
                #         else:
                #             max_dir = max_dir
                #
                # print(f"NUEVOS MIN {min_dir} MAX  {max_dir}")
                if currentValue < float(min):
                    # BAJA
                    # min_dir = currentValue
                    if direction == Constants.DIR_UP:
                        direction = Constants.DIR_CHANGE_DOWN
                    elif direction == Constants.DIR_DOWN:
                        direction = Constants.DIR_DOWN
                    elif Constants.DIR_CHANGE in direction:
                        direction = Constants.DIR_PRE_DOWN
                    elif direction == Constants.DIR_PRE_DOWN:
                        direction = Constants.DIR_DOWN
                    elif direction == Constants.DIR_PRE_UP:
                        direction = Constants.DIR_CHANGE_DOWN

                    if Constants.DIR_CHANGE in direction:
                        min = currentValue

                if currentValue > float(max):
                    #SUBE
                    # max_dir = currentValue
                    if direction == Constants.DIR_UP:
                        direction = Constants.DIR_UP
                    elif direction == Constants.DIR_DOWN:
                        direction = Constants.DIR_CHANGE_UP
                    elif Constants.DIR_CHANGE in direction:
                        direction = Constants.DIR_PRE_UP
                    elif direction == Constants.DIR_PRE_DOWN:
                        direction = Constants.DIR_CHANGE_UP
                    elif direction == Constants.DIR_PRE_UP:
                        direction = Constants.DIR_UP

                    if Constants.DIR_CHANGE in direction:
                        max = currentValue


                # determinar minimos y maximos
                if currentValue < float(min):
                    min = currentValue
                if currentValue > float(max):
                    max = currentValue
                # los extremos de todo el recorrido
                if currentValue < float(extremMin):
                    extremMin = currentValue
                if currentValue > float(extremMax):
                    extremMax = currentValue
        fromTopDstPercent = (extremMax -currentValue )*100/(extremMax-extremMin)
        directionRes = direction
        #fix para cambiar direccion usando el valor fromtopdstspercent
        if fromTopDstPercent <5:
            #entonces baja
            directionRes = Constants.DIR_DOWN
        if fromTopDstPercent > 90:
            directionRes = Constants.DIR_UP
        results[Constants.WEEK_DIR] = direction
        results[Constants.WEEK_MIN_DIR] = extremMin
        results[Constants.WEEK_MAX_DIR] = extremMax
        # results[Constants.WEEK_DIR_TOP_DST] = fromTopDstPercent

        # print(f"VALORES direction: fecha {results[Constants.DATE].values[0]} {direction} MIN: {min} MAX: {max} extremMIn: {extremMin} extremeMax: {extremMax} fromTopDstPercent:´{fromTopDstPercent}")
        # action_min_dist = abs(float(currentValue) - float(min))
        # action_max_dist = abs(float(currentValue) - float(max))

    def determineMACD(self, results, data, active):
        MACD_FAST = 12
        MACD_SLOW = 26
        MACD_SIGNAL = 9
        exp1 = data['value'].ewm(span=MACD_FAST, adjust=False).mean()
        exp2 = data['value'].ewm(span=MACD_SLOW, adjust=False).mean()
        MACD_DATA = exp1 - exp2
        MACD_SIGNAL_DATA = MACD_DATA.ewm(span=MACD_SIGNAL, adjust=False).mean()
        results[Constants.MACD] = MACD_DATA.iloc[-1]
        results[Constants.MACD_SIGNAL] = MACD_SIGNAL_DATA.iloc[-1]

    def determineSMA_FAST_SLOW(self, results, data, active):
        # SMA
        # SMA_FAST = 12
        SMA_FAST = 8
        SMA_SLOW = 16
        # SMA_SLOW = 25
        SMA_FAST_VALUES = data['value'].rolling(window=SMA_FAST).mean()
        SMA_SLOW_VALUES = data['value'].rolling(window=SMA_SLOW).mean()
        results[Constants.SMA_FAST] = SMA_FAST_VALUES.iloc[-1]
        results[Constants.SMA_SLOW] = SMA_SLOW_VALUES.iloc[-1]

    def determineRSI(self, results, data, active):
        # RSI
        # RSI_PERIOD = 14
        # RSI_PERIOD = 9
        RSI_PERIOD = 5
        delta = data['value'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=RSI_PERIOD).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=RSI_PERIOD).mean()
        rs = gain / loss
        RSI_DATA = 100 - (100 / (1 + rs))
        results[Constants.RSI] = RSI_DATA.iloc[-1]

    def es_primer_dia_habil_del_mes(self, datevalue):
        # Convertir el timestamp a un objeto datetime
        fecha = datetime.datetime.strptime(datevalue, '%Y-%m-%d %H:%M:%S.%f')
        primer_dia_mes = fecha.replace(day=1)
        # Calcular el primer día hábil del mes
        while primer_dia_mes.weekday() > 4:  # Si es sábado (5) o domingo (6)
            primer_dia_mes += datetime.timedelta(days=1)
        # Verificar si la fecha coincide con el primer día hábil del mes
        return fecha.date() == primer_dia_mes.date()


    def calculateMinMax(self, results,data,active):
        angleFlow = Constants.DIR_WAIT

        minWeek =None
        maxWeek =None
        minMonth = None
        maxMonth = None
        currmin = None
        currmax = None
        needUpdate = False
        needInsert = False
        isUpdateDay = False
        dataLocal = None
        if Constants.MIN_WEEK in results:
            if results[Constants.MIN_WEEK] == 0.0:
                if results[Constants.SIMULATION]==True:
                    #borramos la primera vez.
                    self.databaseMan.deleteControlMinMaxByActive(active.parameters.name)
                else:
                    dataLocal = self.databaseMan.getControlMinMaxForActive(active.parameters.name)
                if dataLocal and 'minweek' in dataLocal[0]:
                    minWeek = dataLocal[0]["minweek"]
                    maxWeek = dataLocal[0]["maxweek"]
                    minMonth = dataLocal[0]["minmonth"]
                    maxMonth = dataLocal[0]["maxmonth"]
                else:
                    needInsert = True
                    minWeek, maxWeek, minMonth, maxMonth= self.calculateWeekAndMontMinMax(results, active)
                    # results[Constants.MIN_MONTH] = minMonth
                    # results[Constants.MAX_MONTH] = maxMonth
            else:
                minWeek = results[Constants.MIN_WEEK]
                maxWeek = results[Constants.MAX_WEEK]
                minMonth = results[Constants.MIN_MONTH]
                maxMonth = results[Constants.MAX_MONTH]
            # if dataLocal and 'minweek' in dataLocal[0]:
                # data = self.databaseMan.getControlMinMaxForActive(active.parameters.name)
                fecha = results['DATE'].values[0]
                isfirstDay = self.es_primer_dia_habil_del_mes(fecha)
                if isfirstDay:
                    isUpdateDay = True

                dayresults = datetime.datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S.%f')
                weekno = dayresults.weekday()

                if weekno == 0:
                    isUpdateDay = True


                if isUpdateDay:
                    timeFromOpen = results[Constants.TIME_FROM_OPEN]
                    if timeFromOpen < 10:
                        minWeek, maxWeek, minMonth, maxMonth = self.calculateWeekAndMontMinMax(results, active)

                #verificar si el valor de hoy supera al minimo maximo
                currval = results[Constants.VALUE]
                if currval <minWeek:
                    minWeek = currval
                    needUpdate = True
                if currval < minMonth:
                    minMonth = currval
                    needUpdate = True

                if currval > maxWeek:
                    maxWeek = currval
                    needUpdate = True
                if currval > maxMonth:
                    maxMonth = currval
                    needUpdate = True

            # else:
            #     print("calculateMinMax ERROR NO DATABSE LOCAL")
        else:
            #no tiene valores
            dataLocal = self.databaseMan.getControlMinMaxForActive(active.parameters.name)
            if dataLocal and 'minweek' in dataLocal[0]:
                minWeek = dataLocal[0]["minweek"]
                maxWeek = dataLocal[0]["maxweek"]
                minMonth = dataLocal[0]["minmonth"]
                maxMonth = dataLocal[0]["maxmonth"]
            else:
                needInsert = True
                minWeek, maxWeek, minMonth, maxMonth = self.calculateWeekAndMontMinMax(results, active)
                # results[Constants.MIN_MONTH] = minMonth
                # results[Constants.MAX_MONTH] = maxMonth
        results[Constants.MIN_WEEK] = minWeek
        results[Constants.MAX_WEEK] = maxWeek
        results[Constants.MIN_MONTH] = minMonth
        results[Constants.MAX_MONTH] = maxMonth

        if results[Constants.SIMULATION] != True:
            if needInsert:
                self.databaseMan.insertControlMinMaxWithData(results)

            if needUpdate:
                self.databaseMan.updateControlMinMaxWithData(results)



    def calculateWeekAndMontMinMax(self, results, active):
        # no hay valores calcular WEEK
        start_date_time = datetime.datetime.strptime(results[Constants.DATE].values[0],
                                                     "%Y-%m-%d %H:%M:%S.%f")
        start_date_time = start_date_time + datetime.timedelta(days=-7)
        start_date_time = start_date_time.replace(second=0, microsecond=0)
        start_date = start_date_time.strftime("%Y-%m-%d %H:%M:%S.%f")

        # end_date_time = start_date_time + datetime.timedelta(days=+2)
        # start_date_time = start_date_time.replace(second=0, microsecond=0)

        enb_date_time = datetime.datetime.strptime(results[Constants.DATE].values[0], "%Y-%m-%d %H:%M:%S.%f")
        enb_date_time = enb_date_time + datetime.timedelta(minutes=5)
        end_date = enb_date_time.strftime("%Y-%m-%d %H:%M:%S.%f")
        # df = self.databaseMan.getAllWithNameForXdaysSpecial(active.parameters.name, 7)
        df = self.databaseMan.getAllWithNameForXdaysRangeDatesExactdays(active.parameters.name,
                                                                        start_date,
                                                                        end_date)
        minWeek = df['value'].min()
        maxWeek = df['value'].max()

        # para calcular MONTH
        start_date_time = datetime.datetime.strptime(results[Constants.DATE].values[0],
                                                     "%Y-%m-%d %H:%M:%S.%f")
        start_date_time = start_date_time.replace(hour=0,second=0, microsecond=0)
        start_date_time = start_date_time.replace(day=1)

        start_date_time = start_date_time + datetime.timedelta(minutes=5)

        start_date = start_date_time.strftime("%Y-%m-%d %H:%M:%S.%f")

        # end_date_time = start_date_time + datetime.timedelta(days=+2)
        # start_date_time = start_date_time.replace(second=0, microsecond=0)

        enb_date_time = datetime.datetime.strptime(results[Constants.DATE].values[0],
                                                   "%Y-%m-%d %H:%M:%S.%f")
        enb_date_time = enb_date_time + datetime.timedelta(minutes=5)
        end_date = enb_date_time.strftime("%Y-%m-%d %H:%M:%S.%f")

        data = self.databaseMan.getAllWithNameForXdaysRangeDatesExactdays(active.parameters.name,
                                                                          start_date,
                                                                          end_date)

        if len(data)>5:
            minMonth = data['value'].min()
            maxMonth = data['value'].max()
        else:
            minMonth = minWeek
            maxMonth = maxWeek
        return minWeek, maxWeek, minMonth, maxMonth
    def determineAngleFlow(self, results,data,active):
        angleFlow = Constants.DIR_WAIT
        angle = float(results[Constants.ANGLE])
        angleCounter = float(results[Constants.ANGLE_COUNTER])

        angleIma1 = float(results[Constants.ANGLE_IMA1])
        angleIma1Counter = float(results[Constants.ANGLE_IMA1_COUNTER])

        minAngleFlow = active.parameters.minAngleFlow
        minAngleFlowCounter = active.parameters.minAngleFlowCounter
        angle = float(results[Constants.ANGLE])

        resIma1 = Constants.DIR_WAIT
        if angleIma1 >= 0:
            if angleIma1Counter >= minAngleFlowCounter:
                resIma1 = Constants.DIR_UP
            else:
                resIma1 = Constants.DIR_PRE_UP
        elif angleIma1 < 0:
            if angleIma1Counter >= minAngleFlowCounter:
                resIma1 = Constants.DIR_DOWN
            else:
                resIma1 = Constants.DIR_PRE_DOWN


        if angle > 0:
            if angle > minAngleFlow:
                angleFlow = Constants.DIR_UP
            else:
                #determinar otro indicador
                angleFlow = resIma1
                # if resIma1 == Constants.DIR_UP:
                #     angleFlow = Constants.DIR_UP
                # elif resIma1 == Constants.DIR_DOWN:
                #     angleFlow = Constants.DIR_DOWN
                # elif resIma1 == Constants.DIR_PRE_UP:
                #     nada=""
                #     # otro indicador
                #     angleFlow = resIma1
                # elif resIma1 == Constants.DIR_PRE_DOWN:
                #     nada = ""
                #     # otro indicador
                #     angleFlow = resIma1
                # else:
                #     nada = ""
        elif angle < 0:
            if abs(angle) > minAngleFlow:
                angleFlow = Constants.DIR_DOWN
            else:
                #determinar otro indicador
                angleFlow = resIma1
                # if resIma1 == Constants.DIR_UP:
                #     angleFlow = Constants.DIR_UP
                # elif resIma1 == Constants.DIR_DOWN:
                #     angleFlow = Constants.DIR_DOWN
                #
                # elif resIma1 == Constants.DIR_PRE_UP:
                #     nada=""
                #     angleFlow = resIma1
                #     # otro indicador
                # elif resIma1 == Constants.DIR_PRE_DOWN:
                #     nada = ""
                #     angleFlow = resIma1
                #     # otro indicador
                # else:
                #     nada = ""

        results[Constants.ANGLE_FLOW] = angleFlow

    def calculate_rsi_metrics(self, results, data, active, period=14, lookback=5):
        import numpy as np
        import pandas as pd

        df = data.copy()

        #  Si no hay suficientes datos → salir limpio
        if len(df) < max(period, lookback) + 1:
            results[Constants.RSI] = 50
            results[Constants.RSI_PREV5] = 50
            results[Constants.RSI_SLOPE] = 0
            results[Constants.RSI_DIFF] = 0
            results[Constants.RSI_ACCEL] = 0
            results[Constants.RSI_SCORE] = 0
            results[Constants.RSI_SIGNAL] = "NEUTRAL"
            return

        # =========================
        # 1️⃣ Calcular RSI
        # =========================
        delta = df["value"].diff()

        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)

        gain = pd.Series(gain).rolling(window=period).mean()
        loss = pd.Series(loss).rolling(window=period).mean()

        rs = gain / loss
        df["RSI"] = 100 - (100 / (1 + rs))

        #  Si aún hay NaN en las últimas posiciones
        if df["RSI"].isna().iloc[-1]:
            results[Constants.RSI] = 50
            results[Constants.RSI_PREV5] = 50
            results[Constants.RSI_DIFF] = 0
            results[Constants.RSI_SLOPE] = 0
            results[Constants.RSI_ACCEL] = 0
            results[Constants.RSI_SCORE] = 0
            results[Constants.RSI_SIGNAL] = "NEUTRAL"
            return

        # =========================
        # 2️⃣ Métricas clave
        # =========================
        rsi_now = df["RSI"].iloc[-1]
        rsi_prev5 = df["RSI"].iloc[-lookback]
        rsi_diff = 0
        if not df["RSI"].isna().iloc[-2]:
            rsi_prev1 = df["RSI"].iloc[-2]
            rsi_diff = rsi_now - rsi_prev1

        slope = df["RSI"].diff().rolling(lookback).mean().iloc[-1]

        acceleration = df["RSI"].diff().diff().iloc[-1]

        # =========================
        # 3️⃣ Sistema de SCORE
        # =========================
        score = 0

        if rsi_now > 50:
            score += 1
        else:
            score -= 1

        if rsi_now > rsi_prev5:
            score += 1
        else:
            score -= 1

        if slope > 0:
            score += 1
        else:
            score -= 1

        if rsi_now > 80:
            score -= 1
        if rsi_now < 20:
            score += 1

        # =========================
        # 4️⃣ Interpretación final
        # =========================
        if score >= 2:
            signal = "STRONG_LONG"
        elif score == 1:
            signal = "LONG"
        elif score == -1:
            signal = "SHORT"
        elif score <= -2:
            signal = "STRONG_SHORT"
        else:
            signal = "NEUTRAL"

        results[Constants.RSI] = rsi_now
        results[Constants.RSI_PREV5] = rsi_prev5
        results[Constants.RSI_DIFF] = rsi_diff
        results[Constants.RSI_SLOPE] = slope
        results[Constants.RSI_ACCEL] = acceleration
        results[Constants.RSI_SCORE] = score
        results[Constants.RSI_SIGNAL] = signal


    def calculate_market_trend(self, results, data, active, short_days=3, long_days=7):
        """
        Calcula la tendencia actual del mercado (sube/baja) y su intensidad (ALTA/MEDIA/BAJA).
        Usa dos ventanas temporales: corta (3 días) y larga (7 días) para una señal más robusta.

        Métricas calculadas:
         - Slope (pendiente via regresión lineal) para 3d y 7d
         - Cambio porcentual para 3d y 7d
         - Consistencia direccional (% de velas que van en la dirección dominante)
         - Score compuesto (-100 a 100: positivo=sube, negativo=baja)
         - Dirección: TREND_UP / TREND_DOWN / TREND_NEUTRAL
         - Intensidad: ALTA / MEDIA / BAJA
        """
        import numpy as np

        df = data.copy()

        # ─── Valores por defecto ───
        defaults = {
            Constants.MARKET_TREND_DIRECTION: Constants.TREND_NEUTRAL,
            Constants.MARKET_TREND_INTENSITY: Constants.TREND_INTENSITY_LOW,
            Constants.MARKET_TREND_SCORE: 0,
            Constants.MARKET_TREND_SLOPE_3D: 0,
            Constants.MARKET_TREND_SLOPE_7D: 0,
            Constants.MARKET_TREND_PCT_CHANGE_3D: 0,
            Constants.MARKET_TREND_PCT_CHANGE_7D: 0,
            Constants.MARKET_TREND_CONSISTENCY: 0,
        }

        # Necesitamos al menos long_days * 24 registros (aprox 1 registro/5min -> ~288/día)
        # Pero usamos un mínimo más bajo para ser flexibles con los datos disponibles
        min_records = 50
        if len(df) < min_records:
            for k, v in defaults.items():
                results[k] = v
            return

        prices = df['value'].astype(float).values

        # ─── Determinar cuántos registros equivalen a N días ───
        # Estimamos registros por día contando los datos disponibles
        if 'date' in df.columns:
            try:
                dates_parsed = pd.to_datetime(df['date'])
                total_span_days = (dates_parsed.iloc[-1] - dates_parsed.iloc[0]).total_seconds() / 86400.0
                if total_span_days > 0:
                    records_per_day = len(df) / total_span_days
                else:
                    records_per_day = 288  # fallback: ~5 min intervals
            except Exception:
                records_per_day = 288
        else:
            records_per_day = 288

        n_short = min(int(records_per_day * short_days), len(prices) - 1)
        n_long = min(int(records_per_day * long_days), len(prices) - 1)

        if n_short < 10:
            n_short = min(50, len(prices) - 1)
        if n_long < 20:
            n_long = min(200, len(prices) - 1)

        prices_short = prices[-n_short:]
        prices_long = prices[-n_long:]

        # =========================
        # 1️⃣ Pendiente (Slope) via regresión lineal
        # =========================
        def calc_slope(p):
            """Retorna slope normalizado (% por registro)"""
            if len(p) < 2:
                return 0
            x = np.arange(len(p), dtype=float)
            # Regresión lineal simple
            x_mean = x.mean()
            p_mean = p.mean()
            numerator = np.sum((x - x_mean) * (p - p_mean))
            denominator = np.sum((x - x_mean) ** 2)
            if denominator == 0:
                return 0
            slope = numerator / denominator
            # Normalizar: slope como porcentaje del precio medio
            if p_mean != 0:
                slope_pct = (slope / p_mean) * 100
            else:
                slope_pct = 0
            return slope_pct

        slope_short = calc_slope(prices_short)
        slope_long = calc_slope(prices_long)

        # =========================
        # 2️⃣ Cambio porcentual
        # =========================
        pct_change_short = 0
        if prices_short[0] != 0:
            pct_change_short = ((prices_short[-1] - prices_short[0]) / prices_short[0]) * 100

        pct_change_long = 0
        if prices_long[0] != 0:
            pct_change_long = ((prices_long[-1] - prices_long[0]) / prices_long[0]) * 100

        # =========================
        # 3️⃣ Consistencia direccional
        # =========================
        # ¿Qué porcentaje de cambios consecutivos van en la dirección dominante?
        diffs_short = np.diff(prices_short)
        if len(diffs_short) > 0:
            ups = np.sum(diffs_short > 0)
            downs = np.sum(diffs_short < 0)
            total_moves = ups + downs
            if total_moves > 0:
                if ups > downs:
                    consistency = (ups / total_moves) * 100
                else:
                    consistency = -(downs / total_moves) * 100
            else:
                consistency = 0
        else:
            consistency = 0

        # =========================
        # 4️⃣ Score compuesto (-100 a 100)
        # =========================
        score = 0

        # Contribución del slope corto (peso 30)
        if slope_short > 0:
            score += min(slope_short * 1000, 30)   # escalar para normalizar
        else:
            score += max(slope_short * 1000, -30)

        # Contribución del slope largo (peso 20)
        if slope_long > 0:
            score += min(slope_long * 1000, 20)
        else:
            score += max(slope_long * 1000, -20)

        # Contribución del cambio porcentual corto (peso 20)
        if abs(pct_change_short) > 0.1:
            # > 0.1% es significativo a 3 días
            score += max(min(pct_change_short * 5, 20), -20)

        # Contribución del cambio porcentual largo (peso 15)
        if abs(pct_change_long) > 0.2:
            score += max(min(pct_change_long * 3, 15), -15)

        # Contribución de la consistencia (peso 15)
        score += max(min(consistency * 0.15, 15), -15)

        # Clamp score a [-100, 100]
        score = max(min(score, 100), -100)

        # =========================
        # 5️⃣ Dirección y Intensidad
        # =========================
        # Dirección
        if score > 10:
            direction = Constants.TREND_UP
        elif score < -10:
            direction = Constants.TREND_DOWN
        else:
            direction = Constants.TREND_NEUTRAL

        # Intensidad basada en |score|
        abs_score = abs(score)
        if abs_score >= 60:
            intensity = Constants.TREND_INTENSITY_HIGH
        elif abs_score >= 25:
            intensity = Constants.TREND_INTENSITY_MED
        else:
            intensity = Constants.TREND_INTENSITY_LOW

        # =========================
        # 6️⃣ Guardar resultados
        # =========================
        results[Constants.MARKET_TREND_DIRECTION] = direction
        results[Constants.MARKET_TREND_INTENSITY] = intensity
        results[Constants.MARKET_TREND_SCORE] = round(score, 2)
        results[Constants.MARKET_TREND_SLOPE_3D] = round(slope_short, 6)
        results[Constants.MARKET_TREND_SLOPE_7D] = round(slope_long, 6)
        results[Constants.MARKET_TREND_PCT_CHANGE_3D] = round(pct_change_short, 4)
        results[Constants.MARKET_TREND_PCT_CHANGE_7D] = round(pct_change_long, 4)
        results[Constants.MARKET_TREND_CONSISTENCY] = round(consistency, 2)


    def calculate_order_flow_metrics(self, results, data, active, lookback=20):
        """
        Calcula métricas de Order Flow (Footprint Proxy) basándose en
        volumen (qty) y acción del precio de los últimos registros.
        """
        import numpy as np
        import pandas as pd

        df = data.copy()

        # Requerir al menos lookback datos para cálculos de media/suma
        if len(df) < lookback:
            results[Constants.ORDER_FLOW_DELTA] = 0
            results[Constants.ORDER_FLOW_CUM_DELTA] = 0
            results[Constants.ORDER_FLOW_RATIO] = 0
            results[Constants.ORDER_FLOW_SCORE] = 0
            results[Constants.ORDER_FLOW_SIGNAL] = "NEUTRAL"
            results[Constants.ORDER_FLOW_IMBALANCE] = False
            return

        # 1️⃣ Extracción de columnas necesarias de la base de datos
        # 'value' = Close, 'openValue' = Open, 'min_value' = Low, 'max_value' = High, 'qty' = Volume
        try:
            close = df["value"]
            open_val = df["openValue"]
            high = df["max_value"]
            low = df["min_value"]
            volume = df["qty"]
        except (KeyError, ValueError):
            # Si faltan columnas, inicializar con neutros
            results[Constants.ORDER_FLOW_SIGNAL] = "DATA_MISSING"
            return

        # 2️⃣ Cálculo de Delta (Proxy de agresión)
        # Delta Reflejado = Volumen * ((Close - Open) / (High - Low))
        # Esto estima el net buying/selling pressure dentro del "snapshot"
        range_val = (high - low).replace(0, 0.000001)  # Evitar división por cero
        body_val = (close - open_val)

        # Delta Proxy: Proporción del volumen asignada a la dirección del cierre
        delta_proxy = volume * (body_val / range_val)

        df["of_delta"] = delta_proxy
        df["of_cum_delta"] = df["of_delta"].rolling(window=lookback).sum()

        # 3️⃣ Métricas actuales
        current_delta = df["of_delta"].iloc[-1]
        cum_delta = df["of_cum_delta"].iloc[-1]
        avg_volume = volume.rolling(window=lookback).mean().iloc[-1]

        # Ratio de agresión (Delta / Volumen)
        of_ratio = current_delta / (volume.iloc[-1] + 0.000001)

        results[Constants.ORDER_FLOW_DELTA] = float(np.round(current_delta, 4))
        results[Constants.ORDER_FLOW_CUM_DELTA] = float(np.round(cum_delta, 4))
        results[Constants.ORDER_FLOW_RATIO] = float(np.round(of_ratio, 4))

        # 4️⃣ Score de Order Flow (-100 a 100)
        score = 0
        
        # Dirección del Delta actual
        if current_delta > 0:
            score += 40
        elif current_delta < 0:
            score -= 40

        # Tendencia del Delta Acumulado (Momento del flujo)
        if len(df) > 1:
            if cum_delta > df["of_cum_delta"].iloc[-2]:
                score += 30
            elif cum_delta < df["of_cum_delta"].iloc[-2]:
                score -= 30

        # Detección de Desequilibrios (Imbalance) - Volumen inusual
        is_imbalance = False
        if volume.iloc[-1] > avg_volume * 1.5:
            is_imbalance = True
            if current_delta > 0:
                score += 30
            else:
                score -= 30
        
        results[Constants.ORDER_FLOW_IMBALANCE] = is_imbalance
        results[Constants.ORDER_FLOW_SCORE] = score

        # 5️⃣ Lógica de Señal (Sentiment)
        if score >= 70:
            signal = "STRONG_BUY_PRESSURE"
        elif score >= 30:
            signal = "BUY_PRESSURE"
        elif score <= -70:
            signal = "STRONG_SELL_PRESSURE"
        elif score <= -30:
            signal = "SELL_PRESSURE"
        else:
            signal = "NEUTRAL"

        results[Constants.ORDER_FLOW_SIGNAL] = signal


    def evaluateActiveIndicators(self, results, data, active):
        res = ""
        try:
            varName = "IND_" + active.parameters.name
            value = Constants.INDICATOR_EMA_WAIT
            if Constants.EMA_DST in results:
                ema_dst = results[Constants.EMA_DST]
                ind_ema = results[Constants.INDICATOR_EMA]
                ema_change_dst = active.parameters.ema_change_dst

                if Constants.INDICATOR_EMA_BUY == ind_ema:
                    if ema_dst >0 and ema_dst >=ema_change_dst:
                        value = Constants.INDICATOR_EMA_BUY
                elif Constants.INDICATOR_EMA_SELL == ind_ema:
                    if ema_dst <0 and abs(ema_dst) >=ema_change_dst:
                        value = Constants.INDICATOR_EMA_SELL

            results[varName] = value

        except Exception as e:
            print(f"error evaluateActiveIndicators{str(e)}")
    # #@mide_tiempo
    def getMinMaxFlow(self, results, data, active):
        res = ""
        try:
            extremMin = float(results[Constants.WEEK_MIN_DIR])
            extremMax = float(results[Constants.WEEK_MAX_DIR])
            currentValue = float(results[Constants.VALUE])
            fromTopDstPercent = ((extremMax - currentValue) * 100) / (extremMax - extremMin)
            results[Constants.WEEK_DIR_TOP_DST] = fromTopDstPercent
            botDst = 100 - fromTopDstPercent
            if fromTopDstPercent > 100:
                botDst = fromTopDstPercent - 100
            results[Constants.WEEK_DIR_BOT_DST] = botDst

            if results[Constants.SIMULATION] != True:
                #calcular MIN MAX nuevo
                extremMinNew = float(results[Constants.MIN_WEEK])
                extremMaxNew = float(results[Constants.MAX_WEEK])
                currentValue = float(results[Constants.VALUE])
                fromTopDstPercentNew = ((extremMaxNew - currentValue) * 100) / (extremMaxNew - extremMinNew)
                # results[Constants.WEEK_DIR_TOP_DST] = fromTopDstPercentNew
                botDstNew = 100 - fromTopDstPercentNew
                if fromTopDstPercentNew > 100:
                    botDstNew = fromTopDstPercentNew - 100
                results[Constants.WEEK_DIR_BOT_DST_NEW] = botDstNew

                # calular MINMAX MONTH
                extremMinMonth = float(results[Constants.MIN_MONTH])
                extremMaxMonth = float(results[Constants.MAX_MONTH])
                currentValue = float(results[Constants.VALUE])
                if (extremMinMonth != extremMaxMonth):
                    fromTopDstPercentMonth = ((extremMaxMonth - currentValue) * 100) / (extremMaxMonth - extremMinMonth)
                else:
                    fromTopDstPercentMonth = 0
                results[Constants.MONTH_DIR_TOP_DST] = fromTopDstPercentMonth
                botDstMonth = 100 - fromTopDstPercentMonth
                if fromTopDstPercentMonth > 100:
                    botDstMonth = fromTopDstPercentMonth - 100
                results[Constants.MONTH_DIR_BOT_DST] = botDstMonth
            else:
                results[Constants.WEEK_DIR_BOT_DST_NEW]= data.iloc[-1]['week_dir_bot_dst_new']
                results[Constants.MONTH_DIR_BOT_DST]= data.iloc[-1]['month_dir_bot_dst']

            #DISTANCIA PARA BLG Y MIN MAX
            blgval = float(results[Constants.BLG_MA_VAL])
            fromTopDstPercentBLG = ((extremMax - blgval) * 100) / (extremMax - extremMin)
            # results[Constants.WEEK_DIR_TOP_DST] = fromTopDstPercentNew
            botDstBLG = 100 - fromTopDstPercentBLG
            if fromTopDstPercentBLG > 100:
                botDstBLG = fromTopDstPercentBLG - 100
            results[Constants.BOT_DST_BLG] = botDstBLG

            self.determineMinMaxValuesLastXDays(results, data, active)
            self.reevaluateFLowValue(results, data, active)
        except Exception as e:
            print(f"error getMinMaxFlow {str(e)}")
        # self.determineMinMaxValues(results,data,active)


    # #@mide_tiempo
    def determineMinMaxValues(self, results, data, active):
        distance = active.parameters.MinMaxDistance + 1
        if len(data) >= distance:
            currentValue = float(results[Constants.VALUE])
            dataEval = data.tail(distance)[['value', 'week_dir', 'week_max_dir', 'week_min_dir']]
            # dataEval = dataEval.dropna(subset=['week_dir'])
            dataEval = dataEval[dataEval['week_min_dir'] != 99999]
            if len(dataEval) >= distance:
                ultimo_indice = dataEval.index[-1]
                dataEval['percent'] = 100 - (data['week_max_dir'] - data['value']) * 100 / (
                            data['week_max_dir'] - data['week_min_dir'])
                media = dataEval['value'].mean()
                # mediaPrev = dataEval['value'].mean()
                evalPercent = dataEval['percent']
                mediaPercent = dataEval['percent'].mean()
                currentBotPercent = results[Constants.WEEK_DIR_BOT_DST]
                weekBotDiff = currentBotPercent - mediaPercent
                # weekBotDiffPrev = currentBotPercent - currentBotPercent
                weekBotDiffFlow = Constants.DIR_WAIT
                if weekBotDiff > 0:
                    weekBotDiffFlow = Constants.DIR_UP
                else:
                    weekBotDiffFlow = Constants.DIR_DOWN
                nada = ""
                results[Constants.WEEK_DIR_FLOW_DIFF] = weekBotDiff
                results[Constants.WEEK_DIR_FLOW] = weekBotDiffFlow

                prevDistance = 1
                if distance >= 4:
                    prevDistance = 4
                prevPercent = evalPercent.iloc[-prevDistance]
                results[Constants.WEEK_DIR_BOT_DST_PREV] = prevPercent
            else:
                #no hay valores usamos otro indicador similar
                dataEval = data.tail(distance)[['value', 'week_dir', 'global_max', 'global_min']]
                dataEval['percent'] = 100 - (data['global_max'] - data['value']) * 100 / (
                        data['global_max'] - data['global_min'])
                media = dataEval['value'].mean()
                evalPercent = dataEval['percent']
                mediaPercent = dataEval['percent'].mean()
                currentBotPercent = results[Constants.WEEK_DIR_BOT_DST]
                weekBotDiff = currentBotPercent - mediaPercent
                # weekBotDiffPrev = currentBotPercent - currentBotPercent
                weekBotDiffFlow = Constants.DIR_WAIT
                if weekBotDiff > 0:
                    weekBotDiffFlow = Constants.DIR_UP
                else:
                    weekBotDiffFlow = Constants.DIR_DOWN
                nada = ""
                results[Constants.WEEK_DIR_FLOW_DIFF] = weekBotDiff
                results[Constants.WEEK_DIR_FLOW] = weekBotDiffFlow

                prevDistance = 1
                if distance >=4:
                    prevDistance = 4
                prevPercent = evalPercent.iloc[-prevDistance]
                results[Constants.WEEK_DIR_BOT_DST_PREV] = prevPercent
                # results[Constants.WEEK_DIR_BOT_DST] = evalPercent.iloc[-1]

    # #@mide_tiempo
    def determineMinMaxValuesLastXDays(self, results, data, active):
        distance = active.parameters.MinMaxDistance + 1
        month_media = 0
        week_media = 0
        week_new_media = 0
        week_new_flow_value = 0
        if len(data) >= distance:
            currentValue = float(results[Constants.VALUE])
            dataEval = data.tail(distance)[['value', 'month_dir_bot_dst', 'week_dir_bot_dst', 'week_dir_bot_dst_new']]
            # dataEval = dataEval.dropna(subset=['week_dir'])
            # dataEval = dataEval[dataEval['week_dir_bot_dst'] != 0]
            if len(dataEval) >= distance:
                month_media = dataEval['month_dir_bot_dst'].mean()
                week_media = dataEval['week_dir_bot_dst'].mean()
                week_new_media = dataEval['week_dir_bot_dst_new'].mean()

                currVal0 = dataEval.iloc[-1]['week_dir_bot_dst_new']
                currVal1= dataEval.iloc[-2]['week_dir_bot_dst_new']
                week_new_flow_value = currVal0-currVal1
        else:
            #recuperamos x valores de BD
            start_date_time = datetime.datetime.strptime(results[Constants.DATE].values[0],
                                                         "%Y-%m-%d %H:%M:%S.%f")
            start_date_time = start_date_time + datetime.timedelta(days=-7)
            start_date_time = start_date_time.replace(second=0, microsecond=0)
            start_date = start_date_time.strftime("%Y-%m-%d %H:%M:%S.%f")

            # end_date_time = start_date_time + datetime.timedelta(days=+2)
            # start_date_time = start_date_time.replace(second=0, microsecond=0)

            enb_date_time = datetime.datetime.strptime(results[Constants.DATE].values[0], "%Y-%m-%d %H:%M:%S.%f")
            enb_date_time = enb_date_time + datetime.timedelta(minutes=5)
            end_date = enb_date_time.strftime("%Y-%m-%d %H:%M:%S.%f")
            # df = self.databaseMan.getAllWithNameForXdaysSpecial(active.parameters.name, 7)
            df = self.databaseMan.getAllWithNameForXdaysRangeDatesExactdays(active.parameters.name,
                                                                            start_date,
                                                                            end_date)
            dataEval = df.tail(distance)[['value', 'month_dir_bot_dst', 'week_dir_bot_dst', 'week_dir_bot_dst_new']]
            # dataEval = dataEval.dropna(subset=['week_dir'])
            # dataEval = dataEval[dataEval['week_dir_bot_dst'] != 0]
            if len(dataEval) >= distance:
                month_media = dataEval['month_dir_bot_dst'].mean()
                week_media = dataEval['week_dir_bot_dst'].mean()
                week_new_media = dataEval['week_dir_bot_dst_new'].mean()
                currVal0 = dataEval.iloc[-1]['week_dir_bot_dst_new']
                currVal1 = dataEval.iloc[-2]['week_dir_bot_dst_new']
                week_new_flow_value = currVal0 - currVal1


        results[Constants.MONTH_DIR_BOT_DST_MED] = month_media
        results[Constants.WEEK_DIR_BOT_DST_MED] = week_media
        results[Constants.WEEK_DIR_BOT_DST_MED_NEW] = week_new_media
        results[Constants.WEEK_DIR_BOT_DST_MED_NEW_FLOW] = week_new_flow_value

    # #@mide_tiempo
    def reevaluateFLowValue(self, results, data, active):
        flow = Constants.WEEK_FLOW_NOTINIT
        week_dir_flow = results[Constants.WEEK_DIR_FLOW]
        week_dir_bot_dst = results[Constants.WEEK_DIR_BOT_DST]
        week_dir_flow_diff = float(results[Constants.WEEK_DIR_FLOW_DIFF])
        week_dir_flow_prev = float(results[Constants.WEEK_DIR_FLOW_PREV])
        if math.isnan(week_dir_flow_prev):
            week_dir_flow_prev = 0

        weekFlowMinDiff = float(active.parameters.weekFlowMinDiff)
        if week_dir_flow_diff > 0:
            #posible UP
            if abs(week_dir_flow_diff) >= weekFlowMinDiff:
                flow = Constants.WEEK_FLOW_UP
                if week_dir_flow_prev ==0:
                    week_dir_flow_prev = week_dir_flow_diff
                else:
                    if week_dir_flow_diff > week_dir_flow_prev:
                        week_dir_flow_prev = week_dir_flow_diff
            else:
                nada = ""
                if week_dir_flow_prev < 0:
                    flow = Constants.WEEK_FLOW_DOWN
                else:
                    flow = Constants.WEEK_FLOW_UP
                #mantenemos el flow anterior
        elif  week_dir_flow_diff < 0:
            #posible baja
            if abs(week_dir_flow_diff) >= weekFlowMinDiff:
                flow = Constants.WEEK_FLOW_DOWN
                if week_dir_flow_prev ==0:
                    week_dir_flow_prev = week_dir_flow_diff
                else:
                    if week_dir_flow_diff < week_dir_flow_prev:
                        week_dir_flow_prev = week_dir_flow_diff
            else:
                if week_dir_flow_prev < 0:
                    flow = Constants.WEEK_FLOW_DOWN
                else:
                    flow = Constants.WEEK_FLOW_UP
                #mantenemos el flow anterior
                nada = ""

        results[Constants.WEEK_DIR_FLOW] = flow
        results[Constants.WEEK_DIR_FLOW_PREV] = week_dir_flow_prev


    def evaluate_MABLG_PERCENT(self,results, blgMA, active):
        try:
            res = ""
            blgMAFixed = blgMA.dropna()
            blg_media = 0
            week_new_media = 0
            distance = active.parameters.blgma_dst
            if not blgMAFixed.empty:
                blgMAm0 = blgMAFixed.iloc[-1]
                if len(blgMAFixed) >= distance:
                    dataEval = blgMAFixed.tail(distance)
                    if len(dataEval) >= distance:
                        # week_media = dataEval['week_dir_bot_dst'].mean()
                        blg_media = dataEval.mean()
                        res = blgMAm0-blg_media

            results[Constants.BLG_MA_MEAN] = res
        except Exception as e:
           print(f"error evaluate_MABLG_PERCENT {str(e)}")
           results[Constants.BLG_MA_MEAN] = 0

def main():
    analisis = AnalisisHelper()
    results = {}
    activeHelper = ActiveHelper(simulation=True, isDBData=True)
    # active = activeHelper.prepareBTC3()
    active = activeHelper.prepareTSLA()
    start = '2024-04-03'
    end = '2024-04-09'

    analisis.getWeekDirection(results, active, start, end)


if __name__ == "__main__":
    main()
