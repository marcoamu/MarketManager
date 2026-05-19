from evaluators.CierreBase import CierreBase
from evaluators.EvaluatorBase import EvaluatorBase
from evaluators.AperturaBase import AperturaBase
from service.Constants import Constants

class EvaluatorIMA1Optimiz_MEDDIFF_01(EvaluatorBase, AperturaBase, CierreBase):

    def __init__(self):
        self.name = 'EvaluatorIMA1Optimiz_MEDDIFF_01'

    def evaluate(self, results, activeParam):
        results[Constants.EVAl_NAME] = self.name
        self.updateTimeZoneValues(results)
        self.multiplicatorClose = activeParam.difference * 1.2
        self.enableControlOpen = False
        self.multiplicadorOpen = 2.2
        self.multiplicadorUP = 1
        self.WEEK_FLOW_MINVAL = 0
        self.evaluateChangeMarketTendence = True
        self.medstdminDiff = activeParam.medstdminDiff
        self.maxAcumValue = activeParam.closeAcumvalue * 3
        self.closeAcumValue = activeParam.closeAcumvalue
        self.ima1minDistance = activeParam.ima1minDistance
        self.ima1maxDistance = activeParam.ima1maxDistance
        self.closeDifference = activeParam.difference + activeParam.difference * 0.1
        self.accumulate = activeParam.accumulate
        self.angleUP = activeParam.angleUp
        self.angleDOWN = activeParam.angleDown
        if self.closeAcumValue > activeParam.accumulate:
            self.closeAcumValue = activeParam.difference + activeParam.difference * 0.2
        results[Constants.EVAl_CLOSE_ACUM] = self.closeAcumValue
        results[Constants.EVAl_CLOSE_DIFF] = self.closeDifference
        results[Constants.EVAl_ACUM] = self.accumulate
        currentTime = self.gettime(results)
        intime = False
        if currentTime >= int(self.iniStart) and currentTime < int(self.iniEnd):
            intime = True
        if currentTime >= int(self.closeStart) and currentTime < int(self.closeEnd):
            intime = True
        if Constants.ONLY_START_END in results:
            if results[Constants.ONLY_START_END] == False:
                intime = True
        if results[Constants.CURRENT_ACTION] == Constants.ACTION_WAIT or results[Constants.CURRENT_ACTION] == Constants.ACTION_CLOSE:
            if intime:
                self.evaluarApertura(results, activeParam)
            else:
                pass
        elif results[Constants.CURRENT_ACTION] == Constants.ACTION_BUY:
            self.evaluarFlujoBUY(results, activeParam)
        elif results[Constants.CURRENT_ACTION] == Constants.ACTION_SELL:
            self.evaluarFlujoSELL(results, activeParam)

    def evaluarApertura(self, results, activeParam):
        flujo_count = results[Constants.FLUJO_COUNT]
        if results[Constants.IMA1] == Constants.IMA1_BUY:
            self.evaluarAperturaUP(results, activeParam, flujo_count)
        elif results[Constants.IMA1] == Constants.IMA1_SELL:
            self.evaluarAperturaDOWN(results, activeParam, flujo_count)
        elif results[Constants.IMA1] == Constants.IMA1_WAIT:
            self.evaluarAperturaCHANGE(results, activeParam, flujo_count)
        else:
            pass

    def evaluarAperturaOPT(self, results, activeParam):
        flujo_count = results[Constants.FLUJO_COUNT]
        blg_bandwidth = results[Constants.BLG_BANDWIDTH]
        ema_spread = results[Constants.EMA_SPREAD]
        if blg_bandwidth is None or ema_spread is None:
            return
        if blg_bandwidth < 0.02:
            return
        if ema_spread < 0.04:
            return
        ema10_slope = results[Constants.EMA10_SLOPE]
        ema20_slope = results[Constants.EMA20_SLOPE]
        week_flow = results[Constants.WEEK_FLOW]
        tendencia_alcista = ema10_slope > 0 and ema20_slope > 0 and (week_flow == Constants.UP)
        tendencia_bajista = ema10_slope < 0 and ema20_slope < 0 and (week_flow == Constants.DOWN)
        if not tendencia_alcista and (not tendencia_bajista):
            return
        angle_ema = results[Constants.ANGLE_EMA]
        if angle_ema is None or abs(angle_ema) < 10:
            return
        ema_dist = results[Constants.CURRVAL_EMA_DST]
        if ema_dist is None:
            return
        if abs(ema_dist) > 0.01:
            return
        rsi = results[Constants.RSI]
        if rsi is None:
            return
        ima1 = results[Constants.IMA1]
        if tendencia_alcista:
            if ima1 == Constants.IMA1_BUY:
                if 50 <= rsi <= 65:
                    self.evaluarAperturaUP(results, activeParam, flujo_count)
        elif tendencia_bajista:
            if ima1 == Constants.IMA1_SELL:
                if 35 <= rsi <= 50:
                    self.evaluarAperturaDOWN(results, activeParam, flujo_count)
        elif ima1 == Constants.IMA1_WAIT:
            self.evaluarAperturaCHANGE(results, activeParam, flujo_count)

    def evaluarAperturaCHANGE(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0
        multiplicador = 2
        self.printDifference('evaluarAperturaCHANGE', difference_optimized, self.closeAcumValue, self.closeDifference)
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MIN_DIST] >= difference_optimized:
                    results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
                    results[Constants.CLOSE_NXT_DOWN] = 0
        res, action, num = self.evaluateChance_Ima1_02(results, activeParam)
        if res:
            if 'BUY' in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                self.printInicioLog(f'BUY_CHANGE_BUY_{num}', results, activeParam)
                return
            elif 'SELL' in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                self.printInicioLog(f'SELL_CHANGE_BUY_{num}', results, activeParam)
                return

    def evaluarAperturaDOWN(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0
        self.printDifference('evaluarAperturaDOWN', difference_optimized, self.closeAcumValue, self.closeDifference)
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
                    results[Constants.CLOSE_NXT_DOWN] = 0
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MIN_DIST] >= difference_optimized:
                    results[Constants.CLOSE_NXT_UP] = 0
        res, action, num = self.evaluateDownOpen_IMA1_03(results, activeParam)
        if res:
            if 'SELL' in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                self.printInicioLog(f'SELL_DOWN_{num}', results, activeParam)
                return
            elif 'BUY' in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                self.printInicioLog(f'BUY_DOWN_INV_{num}', results, activeParam)
                return

    def evaluarAperturaUP(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0
        self.printDifference('evaluarAperturaUP', difference_optimized, self.closeAcumValue, self.closeDifference)
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MIN_DIST] >= difference_optimized:
                    results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
                    results[Constants.CLOSE_NXT_DOWN] = 0
        res, action, num = self.evaluateUpOpen_Ima1_02(results, activeParam)
        if res:
            if 'BUY' in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                self.printInicioLog(f'BUY_UP_BUY_{num}', results, activeParam)
                return
            elif 'SELL' in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                self.printInicioLog(f'SELL_UP_BUY_{num}', results, activeParam)
                return

    def evaluarFlujoBUY(self, results, activeParam):
        difference_optimized = activeParam.difference
        unit_diff = 0
        flujo_count = results[Constants.FLUJO_COUNT]
        self.printDifference('evaluarFlujoBUY', difference_optimized, self.closeAcumValue, self.closeDifference, self.accumulate)
        self.control_BUY_IMA_02(results, activeParam, self.closeAcumValue, self.closeDifference, self.accumulate)

    def evaluarFlujoSELL(self, results, activeParam):
        difference_optimized = activeParam.difference
        unit_diff = 0
        flujo_count = results[Constants.FLUJO_COUNT]
        self.printDifference('evaluarFlujoSELL', difference_optimized, self.closeAcumValue, self.closeDifference, self.accumulate)
        self.control_SELL_IMA1_02(results, activeParam, self.closeAcumValue, self.closeDifference, self.accumulate)