from evaluators.CierreBase import CierreBase
from evaluators.EvaluatorBase import EvaluatorBase
from evaluators.AperturaBase import AperturaBase
from service.Constants import Constants

class EvaluatorEMA_IA_LONG_02(EvaluatorBase, AperturaBase, CierreBase):

    def __init__(self):
        self.name = 'EvaluatorEMA_IA_LONG_02'

    def evaluate(self, results, activeParam):
        results[Constants.EVAl_NAME] = self.name
        self.updateTimeZoneValues(results)
        self.multiplicatorClose = activeParam.difference * 1.2
        self.multiplicatorPREVIUS = activeParam.difference * 1.2
        self.enableControlOpen = False
        self.multiplicadorOpen = 1
        self.multiplicadorUP = 1
        self.WEEK_FLOW_MINVAL = activeParam.weekDistanceSTDDistance
        self.medstdminDiff = activeParam.medstdminDiff
        self.medstdmaxDiff = activeParam.medstdmaxDiff
        self.evaluateChangeMarketTendence = True
        self.BLGDist = activeParam.bollingerDst
        self.blgLowerDist = 1.5
        self.blgLowerDistPercemt = 10
        self.bollingerClose = activeParam.bollingerClose
        self.closeAcumValue = activeParam.closeProfit
        self.closeDifference = activeParam.difference + activeParam.difference * 0.1
        self.accumulate = activeParam.accumulate
        self.angleUP = activeParam.angleUp
        self.angleDOWN = activeParam.angleDown
        results[Constants.EVAl_CLOSE_ACUM] = self.closeAcumValue
        results[Constants.EVAl_CLOSE_DIFF] = self.closeDifference
        results[Constants.EVAl_ACUM] = self.accumulate
        self.flujo_Count = 2
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

    def evaluarAperturaEMA(self, results, activeParam):
        flujo_count = results[Constants.FLUJO_COUNT]
        if results[Constants.INDICATOR_EMA50] == Constants.INDICATOR_EMA_BUY:
            self.evaluarAperturaUP(results, activeParam, flujo_count)
        elif results[Constants.INDICATOR_EMA50] == Constants.INDICATOR_EMA_SELL:
            self.evaluarAperturaDOWN(results, activeParam, flujo_count)
        elif results[Constants.INDICATOR_EMA50] == Constants.INDICATOR_EMA_WAIT:
            pass
        else:
            pass

    def evaluarApertura(self, results, activeParam):
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

    def evaluarAperturaDOWN(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0
        self.printDifference('evaluarAperturaDOWN', difference_optimized, self.closeAcumValue, self.closeDifference)
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
                    if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
                        if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= activeParam.blgDistPercent:
                            nada = ''
                        else:
                            nada = ''
        cross_count = results.get(Constants.EMA_CROSS_COUNT, 0)
        price_range = results.get(Constants.PRICE_RANGE_PERCENT, 100)
        bandwidth = results.get(Constants.BLG_BANDWIDTH, 100)
        ema20_slope = float(results.get(Constants.EMA20_SLOPE))
        is_lateral = False
        pass
        if abs(ema20_slope) < 0.001:
            is_lateral = True
        res, action, num = self.evaluateDownOpen_EMA_02(results, activeParam)
        if res:
            if is_lateral:
                pass
                return
            if 'BUY' in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                self.printInicioLog(f'BUY_DOWN_BUY_{num}', results, activeParam)
                return
            elif 'SELL' in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                self.printInicioLog(f'SELL_DOWN_SELL_{num}', results, activeParam)
                return

    def evaluarDifferenceUP(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0
        if results[Constants.INDICATOR] == Constants.INDICATOR_BUY:
            if results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_WAIT:
                difference_optimized = activeParam.difference
            elif results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_DOWN:
                difference_optimized = activeParam.difference + activeParam.difference / 3
            else:
                difference_optimized = activeParam.difference - activeParam.difference / 3
        elif results[Constants.INDICATOR] == Constants.INDICATOR_BUYX:
            if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UP:
                difference_optimized = activeParam.difference / 2
            elif results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_WAIT:
                difference_optimized = activeParam.difference
            else:
                difference_optimized = activeParam.difference / 2
        return (difference_optimized, unit_diff)

    def evaluarAperturaUP(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0
        self.printDifference('evaluarAperturaUP', difference_optimized, self.closeAcumValue, self.closeDifference)
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
                    if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_BUY:
                        nada = ''
                    results[Constants.CLOSE_NXT_UP] = 0
                elif results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_UP:
                    if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
                        nada = ''
            results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
                    results[Constants.CLOSE_NXT_DOWN] = 0
                elif results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_UP:
                    results[Constants.CLOSE_NXT_DOWN] = 0
        cross_count = results.get(Constants.EMA_CROSS_COUNT, 0)
        price_range = results.get(Constants.PRICE_RANGE_PERCENT, 100)
        bandwidth = results.get(Constants.BLG_BANDWIDTH, 100)
        ema20_slope = results.get(Constants.EMA20_SLOPE, 100)
        pass
        is_lateral = False
        if abs(ema20_slope) < 0.001:
            is_lateral = True
        res, action, num = self.evaluateUpOpen_EMA_03(results, activeParam)
        if res:
            if is_lateral:
                pass
                return
            if 'BUY' in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                self.printInicioLog(f'BUY_UP_BUY_{num}', results, activeParam)
                return
            elif 'SELL' in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                self.printInicioLog(f'SELL_UP_SELL_{num}', results, activeParam)
                return

    def evaluarFlujoBUY(self, results, activeParam):
        difference_optimized = activeParam.difference
        unit_diff = 0
        flujo_count = results[Constants.FLUJO_COUNT]
        self.printDifference('evaluarFlujoBUY', difference_optimized, self.closeAcumValue, self.closeDifference, self.accumulate)
        self.control_BUY_EMA_02(results, activeParam, self.closeAcumValue, self.closeDifference)

    def evaluarFlujoSELL(self, results, activeParam):
        difference_optimized = activeParam.difference
        unit_diff = 0
        flujo_count = results[Constants.FLUJO_COUNT]
        self.printDifference('evaluarFlujoSELL', difference_optimized, self.closeAcumValue, self.closeDifference, self.accumulate)
        self.control_SELL_EMA_01(results, activeParam, self.closeAcumValue, self.closeDifference)