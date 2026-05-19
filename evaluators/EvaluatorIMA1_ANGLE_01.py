from evaluators.CierreBase import CierreBase
from evaluators.EvaluatorBase import EvaluatorBase
from evaluators.AperturaBase import AperturaBase
from service.Constants import Constants

class EvaluatorIMA1_ANGLE_01(EvaluatorBase, AperturaBase, CierreBase):

    def __init__(self):
        self.name = 'EvaluatorIMA1_ANGLE_01'

    def cambios(self):
        nada = ''

    def evaluate(self, results, activeParam):
        results[Constants.EVAl_NAME] = self.name
        self.updateTimeZoneValues(results)
        self.multiplicatorClose = activeParam.difference * 1.2
        self.enableControlOpen = False
        self.multiplicadorOpen = 2.2
        self.multiplicadorUP = 1
        self.WEEK_FLOW_MINVAL = 0
        self.evaluateChangeMarketTendence = True
        self.maxAcumValue = activeParam.closeAcumvalue * 3
        self.closeAcumValue = activeParam.closeAcumvalue
        self.ima1minDistance = activeParam.ima1minDistance
        self.ima1maxDistance = activeParam.ima1maxDistance
        self.medstdminDiff = activeParam.medstdminDiff
        self.medstdmaxDiff = activeParam.medstdmaxDiff
        self.BLGDist = activeParam.bollingerDst
        self.closeProfit = activeParam.closeProfit
        self.blgDistPercent = activeParam.blgDistPercent
        self.closeDifference = activeParam.difference + activeParam.difference * 0.1
        self.accumulate = activeParam.accumulate
        self.angleUP = activeParam.angleUp
        self.angleDOWN = activeParam.angleDown
        self.midMinDst = 0.08
        self.emaMinDst = activeParam.emaMinDst
        results[Constants.EVAl_CLOSE_ACUM] = self.closeAcumValue
        results[Constants.EVAl_CLOSE_DIFF] = self.closeDifference
        results[Constants.EVAl_ACUM] = self.accumulate
        if self.closeAcumValue > activeParam.accumulate:
            self.closeAcumValue = activeParam.difference + activeParam.difference * 0.2
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
            nada = ''
            self.evaluarAperturaCHANGE(results, activeParam, flujo_count)
        else:
            pass

    def evaluarAperturaCHANGE(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0
        multiplicador = 2
        self.printDifference('evaluarAperturaCHANGE', difference_optimized, self.closeAcumValue, self.closeDifference)
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if self.evalNXT_UP_01(results, activeParam, difference_optimized):
                    nada = ''
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
                    results[Constants.CLOSE_NXT_DOWN] = 0
        res, action, num = self.evaluateChance_Ima1_01(results, activeParam)
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
            if self.evalNXT_UP_01(results, activeParam, difference_optimized):
                nada = ''
        res, action, num = self.evaluateDownOpen_IMA1_01(results, activeParam)
        if res:
            if 'SELL' in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                self.printInicioLog(f'SELL_DOWN_{num}', results, activeParam)
                return
            elif 'BUY' in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                self.printInicioLog(f'BUY_DOWN_INV_{num}', results, activeParam)
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
                if self.evalNXT_UP_01(results, activeParam, difference_optimized):
                    nada = ''
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
                    results[Constants.CLOSE_NXT_DOWN] = 0
        res, action, num = self.evaluateUpOpen_Ima1_01(results, activeParam)
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
        self.control_BUY_START_CLOSE_01(results, activeParam, self.closeAcumValue, self.closeDifference)

    def evaluarDifferenceSELL(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0
        if results[Constants.INDICATOR_TENDENCE] != Constants.INDICATOR_T_WAIT:
            if results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_UP:
                difference_optimized = activeParam.difference - activeParam.difference / 3
            elif results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_DOWN:
                difference_optimized = activeParam.difference + activeParam.difference / 5
        else:
            difference_optimized = activeParam.difference - activeParam.difference / 4
            pass
        if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
            if results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_UP:
                if flujo_count > 1:
                    unit_diff = activeParam.unit * (flujo_count - 1)
                    unit_diff = unit_diff * -1
            elif results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_DOWN:
                if results[Constants.INDICATOR] == Constants.INDICATOR_SELL:
                    if flujo_count > 2:
                        pass
                        unit_diff = activeParam.unit * flujo_count * 1.2
                        unit_diff = unit_diff * -1
            elif flujo_count > 2:
                unit_diff = activeParam.unit * flujo_count * 1.3
                unit_diff = unit_diff * -1
        difference_optimized = difference_optimized + unit_diff
        return (difference_optimized, unit_diff)

    def evaluarFlujoSELL(self, results, activeParam):
        difference_optimized = activeParam.difference
        self.printDifference('evaluarFlujoSELL', difference_optimized, self.closeAcumValue, self.closeDifference, self.accumulate)
        self.control_SELL_START_CLOSE_01(results, activeParam, self.closeAcumValue, self.closeDifference)