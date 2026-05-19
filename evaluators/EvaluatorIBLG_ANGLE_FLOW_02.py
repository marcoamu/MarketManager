from evaluators.CierreBase import CierreBase
from evaluators.EvaluatorBase import EvaluatorBase
from evaluators.AperturaBase import AperturaBase
from service.Constants import Constants

class EvaluatorIBLG_ANGLE_FLOW_02(EvaluatorBase, AperturaBase, CierreBase):

    def __init__(self):
        self.name = 'EvaluatorIBLG_ANGLE_FLOW_02'

    def cambios(self):
        nada = ''

    def evaluate(self, results, activeParam):
        results[Constants.EVAl_NAME] = self.name
        self.updateTimeZoneValues(results)
        self.multiplicatorClose = activeParam.difference / 2
        self.multiplicadorUP = 1
        self.multiplicatorNXT = 1
        self.evaluateChangeMarketTendence = True
        self.closeAcumValue = activeParam.closeAcumvalue
        self.ima1minDistance = activeParam.ima1minDistance
        self.medstdminDiff = activeParam.medstdminDiff
        self.medstdmaxDiff = activeParam.medstdmaxDiff
        self.BLGDist = activeParam.bollingerDst
        self.closeAcumValue = activeParam.bollingerClose
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
        currentTime = self.gettime(results)
        intime = False
        if currentTime >= int(self.iniStart) and currentTime < int(self.iniEnd):
            intime = True
        if currentTime >= int(self.closeStart) and currentTime < int(self.closeEnd):
            intime = True
        intime = True
        if results[Constants.CURRENT_ACTION] == Constants.ACTION_WAIT or results[Constants.CURRENT_ACTION] == Constants.ACTION_CLOSE:
            if intime:
                self.evaluarApertura(results, activeParam)
            else:
                pass
        elif results[Constants.CURRENT_ACTION] == Constants.ACTION_BUY:
            self.evaluarFlujoBUY_LONG(results, activeParam)
        elif results[Constants.CURRENT_ACTION] == Constants.ACTION_SELL:
            self.evaluarFlujoSELL_LONG(results, activeParam)

    def evaluarApertura(self, results, activeParam):
        flujo_count = results[Constants.FLUJO_COUNT]
        if 'UP' in results[Constants.ANGLE_FLOW]:
            self.evaluarAperturaUP(results, activeParam, flujo_count)
        elif 'DOWN' in results[Constants.ANGLE_FLOW]:
            self.evaluarAperturaDOWN(results, activeParam, flujo_count)
        else:
            nada = ''
            self.evaluarAperturaCHANGE(results, activeParam, flujo_count)

    def evaluarAperturaCHANGE(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0
        self.printDifference('evaluarAperturaCHANGE', difference_optimized, self.closeAcumValue, self.closeDifference)
        if results[Constants.ANGLE] > 0:
            self.evaluarAperturaUP(results, activeParam, flujo_count)
        else:
            self.evaluarAperturaDOWN(results, activeParam, flujo_count)

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
                if self.evalNXT_UP_01(results, activeParam, difference_optimized):
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                    name = 'DOWN_BLG_NXTUP_BUY01'
                    self.printInicioLog(name, results, activeParam)
                    return
        if self.evaluateDownOpen_01(results, activeParam):
            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
            self.printInicioLog('SELL_DOWN_01', results, activeParam)
            return

    def evaluarAperturaUP(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0
        self.printDifference('evaluarAperturaUP', difference_optimized, self.closeAcumValue, self.closeDifference)
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if self.evalNXT_UP_01(results, activeParam, difference_optimized):
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                    name = 'UP_BLG_NXTUP_BUY01'
                    self.printInicioLog(name, results, activeParam)
                    return
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
                    results[Constants.CLOSE_NXT_DOWN] = 0
        if self.evaluateUpOpen_02(results, activeParam):
            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
            self.printInicioLog('BUY_UP_BUY01', results, activeParam)
            return
        if self.evaluateForteUpOpen_01(results, activeParam):
            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
            self.printInicioLog('BUY_UP_FORTE_BUY01', results, activeParam)
            return

    def evaluarFlujoBUY_LONG(self, results, activeParam):
        difference_optimized = activeParam.difference
        unit_diff = 0
        flujo_count = results[Constants.FLUJO_COUNT]
        self.printDifference('evaluarFlujoBUY_LONG', difference_optimized, self.closeAcumValue, self.closeDifference, self.accumulate)
        self.control_BUY_BLG_MID_03(results, activeParam, self.closeAcumValue, self.closeDifference, self.accumulate)

    def evaluarFlujoSELL_LONG(self, results, activeParam):
        difference_optimized = activeParam.difference
        unit_diff = 0
        flujo_count = results[Constants.FLUJO_COUNT]
        self.printDifference('evaluarFlujoSELL_LONG', difference_optimized, self.closeAcumValue, self.closeDifference, self.accumulate)
        self.control_SELL_BLG_MID_02(results, activeParam, self.closeAcumValue, self.closeDifference, self.accumulate)