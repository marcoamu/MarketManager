from evaluators.CierreBase import CierreBase
from evaluators.EvaluatorBase import EvaluatorBase
from evaluators.AperturaBase import AperturaBase
from service.Constants import Constants

class EvaluatorBOLLINGER_05(EvaluatorBase, AperturaBase, CierreBase):

    def __init__(self):
        self.name = 'EvaluatorBOLLINGER_05'

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
                self.evaluarAperturaEMA(results, activeParam)
            else:
                pass
        elif results[Constants.CURRENT_ACTION] == Constants.ACTION_BUY:
            self.evaluarFlujoBUY(results, activeParam)
        elif results[Constants.CURRENT_ACTION] == Constants.ACTION_SELL:
            self.evaluarFlujoSELL(results, activeParam)

    def evaluarApertura(self, results, activeParam):
        flujo_count = results[Constants.FLUJO_COUNT]
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_BUY:
            self.evaluarAperturaUP(results, activeParam, flujo_count)
        elif results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
            self.evaluarAperturaDOWN(results, activeParam, flujo_count)
        elif results[Constants.IND_BLG] == Constants.IND_BLG_MED_WAIT:
            pass
        else:
            pass

    def evaluarAperturaEMA(self, results, activeParam):
        flujo_count = results[Constants.FLUJO_COUNT]
        if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_BUY:
            self.evaluarAperturaUP(results, activeParam, flujo_count)
        elif results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
            self.evaluarAperturaDOWN(results, activeParam, flujo_count)
        elif results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_WAIT:
            pass
        else:
            pass

    def evaluarAperturaCHANGEDifference(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0
        if results[Constants.INDICATOR] == Constants.INDICATOR_SELL:
            if results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_WAIT:
                difference_optimized = activeParam.difference
            elif results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_UP:
                if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_DOWN:
                    if flujo_count > 2:
                        unit_diff = activeParam.unit * flujo_count * 1.3
                        unit_diff = unit_diff * -1
                    else:
                        difference_optimized = activeParam.difference / 2
                else:
                    difference_optimized = activeParam.difference + activeParam.difference / 3
            elif flujo_count > 2:
                unit_diff = activeParam.unit * flujo_count * 1.3
                unit_diff = unit_diff * -1
            else:
                difference_optimized = activeParam.difference - activeParam.difference / 2
        elif results[Constants.MARKET_TENDENCE] == Constants.INDICATOR_SELLX:
            if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_DOWN:
                if flujo_count > 2:
                    unit_diff = activeParam.unit * flujo_count * 1.3
                    unit_diff = unit_diff * -1
                else:
                    difference_optimized = activeParam.difference / 2
            elif results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_WAIT:
                difference_optimized = activeParam.difference
            else:
                difference_optimized = activeParam.difference / 2
        difference_optimized = difference_optimized + unit_diff
        return (difference_optimized, unit_diff)

    def evaluarAperturaCHANGE(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0
        multiplicador = 2
        difference_optimized, unit_diff = self.evaluarAperturaCHANGEDifference(results, activeParam, flujo_count)
        pass
        if self.evaluateChangeMarketTendence:
            if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_DOWN:
                if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
                        if results[Constants.PREVIOUS_DIST] <= self.multiplicatorPREVIUS:
                            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                            pass
            elif results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UP:
                if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MIN_DIST] >= difference_optimized:
                        if results[Constants.PREVIOUS_DIST] <= self.multiplicatorPREVIUS:
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            pass
            elif results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UNDEF:
                if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
                        if self.enableControlOpen:
                            if results[Constants.ACUMULADO_ABS] <= self.multiplicatorClose:
                                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                pass
                        elif results[Constants.PREVIOUS_DIST] <= self.multiplicatorPREVIUS:
                            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                            pass
                elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MIN_DIST] >= difference_optimized:
                        if self.enableControlOpen:
                            if results[Constants.ACUMULADO_ABS] <= difference_optimized * self.multiplicadorOpen:
                                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                pass
                        elif results[Constants.PREVIOUS_DIST] <= self.multiplicatorPREVIUS:
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            pass
        elif results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_DOWN:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
                    if self.enableControlOpen:
                        if results[Constants.ACUMULADO_ABS] <= difference_optimized * self.multiplicadorOpen:
                            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                            pass
                    else:
                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                        pass
        elif results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_UP:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
                    if self.enableControlOpen:
                        if results[Constants.ACUMULADO_ABS] <= difference_optimized * self.multiplicadorOpen:
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            pass
                    else:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        pass
        elif results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_WAIT:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
                    if self.enableControlOpen:
                        if results[Constants.ACUMULADO_ABS] <= difference_optimized * self.multiplicadorOpen:
                            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                            pass
                    else:
                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                        pass
            elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
                    if self.enableControlOpen:
                        if results[Constants.ACUMULADO_ABS] <= difference_optimized * self.multiplicadorOpen:
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            pass
                    else:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        pass

    def evaluarAperturaDOWNDifference(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0
        if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
            if flujo_count >= 1:
                unit_diff = activeParam.unit * flujo_count
                unit_diff = unit_diff * -1
        difference_optimized = difference_optimized + unit_diff
        return (difference_optimized, unit_diff)

    def evaluarAperturaPREDOWNDifference(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0
        if results[Constants.INDICATOR] == Constants.INDICATOR_SELL:
            if results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_WAIT:
                difference_optimized = activeParam.difference
            elif results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_UP:
                if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_DOWN:
                    if flujo_count > 2:
                        unit_diff = activeParam.unit * flujo_count * 1.3
                        unit_diff = unit_diff * -1
                    else:
                        difference_optimized = activeParam.difference / 2
                else:
                    difference_optimized = activeParam.difference + activeParam.difference / 3
            elif flujo_count > 2:
                unit_diff = activeParam.unit * flujo_count * 1.3
                unit_diff = unit_diff * -1
            else:
                difference_optimized = activeParam.difference - activeParam.difference / 2
        elif results[Constants.INDICATOR] == Constants.INDICATOR_SELLX:
            if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_DOWN:
                if flujo_count > 2:
                    unit_diff = activeParam.unit * flujo_count * 1.3
                    unit_diff = unit_diff * -1
                else:
                    difference_optimized = activeParam.difference / 2
            elif results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_WAIT:
                difference_optimized = activeParam.difference
            else:
                difference_optimized = activeParam.difference / 2
        difference_optimized = difference_optimized + unit_diff
        return (difference_optimized, unit_diff)

    def evaluarAperturaDOWN(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0
        self.printDifference('evaluarAperturaDOWN', difference_optimized, self.closeAcumValue, self.closeDifference)
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                results[Constants.CLOSE_NXT_DOWN] = 0
                self.printInicioLog('DOWN_NXT_DOWN_01', results, activeParam)
                return
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
                    if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
                        if results[Constants.IND_BLG_LOWER_DST] < self.blgLowerDist:
                            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                            self.printInicioLog('DOWN_NXT_UP_01', results, activeParam)
                            return
                        else:
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            self.printInicioLog('DOWN_NXT_UP_02', results, activeParam)
                            return
                elif results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_UP:
                    if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        self.printInicioLog('DOWN_NXT_UP_03', results, activeParam)
                        return
        res, action, num = self.evaluateDownOpen_BLG_02(results, activeParam)
        if res:
            if 'BUY' in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                self.printInicioLog(f'BUY_DOWN_BUY_{num}', results, activeParam)
                return
            elif 'SELL' in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                self.printInicioLog(f'SELL_DOWN_SELL_{num}', results, activeParam)
                return

    def evaluarAperturaPREDOWN(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0
        difference_optimized, unit_diff = self.evaluarAperturaPREDOWNDifference(results, activeParam, flujo_count)
        pass
        if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
            if self.enableControlOpen:
                if results[Constants.ACUMULADO_ABS] <= difference_optimized * self.multiplicadorOpen:
                    results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                    pass
            elif (abs(results[Constants.MEDSTDDIFF]) > self.medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0) and abs(results[Constants.MEDSTDDIFF]) < self.medstdmaxDiff:
                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                pass
        elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
            nada = ''

    def evaluarDifferencePREUP(self, results, activeParam, flujo_count):
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
        difference_optimized = difference_optimized + unit_diff
        return (difference_optimized, unit_diff)

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

    def evaluarAperturaPREUP(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        difference_optimized, unit_diff = self.evaluarDifferencePREUP(results, activeParam, flujo_count)
        pass
        if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
            if self.enableControlOpen:
                if results[Constants.ACUMULADO_ABS] <= difference_optimized * self.multiplicadorOpen:
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                    pass
            elif (abs(results[Constants.MEDSTDDIFF]) > self.medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0) and abs(results[Constants.MEDSTDDIFF]) < self.medstdmaxDiff:
                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                pass
        elif results[Constants.FLUJO] == Constants.FLUJO_BAJA:
            nada = ''

    def evaluarAperturaUP(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0
        self.printDifference('evaluarAperturaUP', difference_optimized, self.closeAcumValue, self.closeDifference)
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
                    if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_BUY:
                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                        self.printInicioLog('UP_NXT_UP_01', results, activeParam)
                        return
                    results[Constants.CLOSE_NXT_UP] = 0
                elif results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_UP:
                    if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        self.printInicioLog('UP_NXT_UP_02', results, activeParam)
                        return
                    results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized * self.multiplicadorUP or results[Constants.ACTION_MAX_DIST] >= difference_optimized * self.multiplicadorUP:
                    if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                        results[Constants.CLOSE_NXT_DOWN] = 0
                        self.printInicioLog('UP_NXT_DOWN_01', results, activeParam)
                        return
                elif results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_UP:
                    results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                    results[Constants.CLOSE_NXT_DOWN] = 0
                    self.printInicioLog('UP_NXT_DOWN_02', results, activeParam)
                    return
        res, action, num = self.evaluateUpOpen_BLG_02(results, activeParam)
        if res:
            if 'BUY' in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                self.printInicioLog(f'BUY_UP_BUY_{num}', results, activeParam)
                return
            elif 'SELL' in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                self.printInicioLog(f'SELL_UP_SELL_{num}', results, activeParam)
                return

    def evaluarDifferenceBUY(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0
        if results[Constants.INDICATOR] == Constants.INDICATOR_SELL or results[Constants.INDICATOR] == Constants.INDICATOR_SELLX:
            if results[Constants.IMA_NEW] == Constants.IMA_NEW_BUY:
                difference_optimized = activeParam.difference + activeParam.difference / 4
            elif results[Constants.IMA_NEW] == Constants.IMA_NEW_SELL:
                if results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_UP:
                    difference_optimized = activeParam.difference - activeParam.difference / 3
                elif results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_DOWN:
                    difference_optimized = activeParam.difference - activeParam.difference / 3
                else:
                    difference_optimized = activeParam.difference - activeParam.difference / 3
        elif results[Constants.INDICATOR] == Constants.INDICATOR_BUY or results[Constants.INDICATOR] == Constants.INDICATOR_BUYX:
            if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UP:
                if results[Constants.IMA_NEW] == Constants.IMA_NEW_BUY:
                    if flujo_count > 2:
                        unit_diff = activeParam.unit * flujo_count * 1.3
                    else:
                        difference_optimized = activeParam.difference + activeParam.difference / 2
        if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
            if results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_UP:
                controlUP = None
                if results[Constants.INDICATOR] == Constants.INDICATOR_BUY:
                    if flujo_count > 2:
                        pass
                        unit_diff = activeParam.unit * flujo_count
                        unit_diff = unit_diff * -1
            elif results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_DOWN:
                if flujo_count > 2:
                    unit_diff = activeParam.unit * flujo_count * 1.3
                    unit_diff = unit_diff * -1
            elif flujo_count > 2:
                unit_diff = activeParam.unit * flujo_count * 1.3
                unit_diff = unit_diff * -1
        difference_optimized = difference_optimized + unit_diff
        return (difference_optimized, unit_diff)

    def evaluarFlujoBUY(self, results, activeParam):
        difference_optimized = activeParam.difference
        unit_diff = 0
        flujo_count = results[Constants.FLUJO_COUNT]
        self.printDifference('evaluarFlujoBUY', difference_optimized, self.closeAcumValue, self.closeDifference, self.accumulate)
        self.control_BUY_BLG_02(results, activeParam, self.closeAcumValue, self.closeDifference)

    def evaluarDifferenceSELL(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0
        if results[Constants.INDICATOR_TENDENCE] != Constants.INDICATOR_T_WAIT:
            if results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_UP:
                difference_optimized = activeParam.difference - activeParam.difference / 3
            elif results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_DOWN:
                difference_optimized = activeParam.difference + activeParam.difference / 4
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
                        unit_diff = activeParam.unit * flujo_count * 1.3
                        unit_diff = unit_diff * -1
            elif flujo_count > 2:
                unit_diff = activeParam.unit * flujo_count * 1.3
                unit_diff = unit_diff * -1
        difference_optimized = difference_optimized + unit_diff
        return (difference_optimized, unit_diff)

    def evaluarFlujoSELL(self, results, activeParam):
        difference_optimized = activeParam.difference
        unit_diff = 0
        self.printDifference('evaluarFlujoSELL', difference_optimized, self.closeAcumValue, self.closeDifference, self.accumulate)
        self.control_SELL_BLG_02(results, activeParam, self.closeAcumValue, self.closeDifference)
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_BUY:
            if results[Constants.ACTION_ACUM] > 0:
                if results[Constants.ACUMULADO] >= self.closeAcumValue:
                    pass
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
            elif results[Constants.ACTION_ACUM] < 0:
                nada = ''
                if results[Constants.ACUMULADO] >= self.closeAcumValue:
                    pass
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if results[Constants.ACTION_ACUM] > 0:
            if abs(results[Constants.ACTION_ACUM]) >= self.closeAcumValue:
                pass
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return