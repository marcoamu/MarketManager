from evaluators.CierreBase import CierreBase
from evaluators.EvaluatorBase import EvaluatorBase
from evaluators.AperturaBase import AperturaBase
from service.Constants import Constants

class EvaluatorPROBMEDSTD_MEDDIFF_BLG_02(EvaluatorBase, AperturaBase, CierreBase):

    def __init__(self):
        self.name = 'EvaluatorPROBMEDSTD_MEDDIFF_BLG_02'

    def evaluate(self, results, activeParam):
        results[Constants.EVAl_NAME] = self.name
        self.multiplicatorClose = activeParam.difference * 1.2
        self.multiplicatorPREVIUS = activeParam.difference * 1.2
        self.enableControlOpen = False
        self.multiplicadorOpen = 2.2
        self.multiplicadorUP = 1
        self.WEEK_FLOW_MINVAL = activeParam.weekDistanceSTDDistance
        self.medstdminDiff = activeParam.medstdminDiff
        self.medstdmaxDiff = activeParam.medstdmaxDiff
        self.evaluateChangeMarketTendence = True
        self.blgDistPercent = activeParam.blgDistPercent
        self.closeAcumValue = activeParam.bollingerClose
        self.closeProfit = activeParam.closeProfit
        self.closeDifference = activeParam.difference + activeParam.difference * 0.2
        self.flujo_Count = 2
        if results[Constants.CURRENT_ACTION] == Constants.ACTION_WAIT or results[Constants.CURRENT_ACTION] == Constants.ACTION_CLOSE:
            self.evaluarApertura(results, activeParam)
        elif results[Constants.CURRENT_ACTION] == Constants.ACTION_BUY:
            self.evaluarFlujoBUY(results, activeParam)
        elif results[Constants.CURRENT_ACTION] == Constants.ACTION_SELL:
            self.evaluarFlujoSELL(results, activeParam)

    def evaluarApertura(self, results, activeParam):
        flujo_count = results[Constants.FLUJO_COUNT]
        if results[Constants.IND_PROB_FLOW] == Constants.DIR_UP:
            self.evaluarAperturaUP(results, activeParam, flujo_count)
        if results[Constants.IND_PROB_FLOW] == Constants.DIR_PRE_UP:
            nada = ''
            self.evaluarAperturaPREUP(results, activeParam, flujo_count)
        elif results[Constants.IND_PROB_FLOW] == Constants.DIR_DOWN:
            self.evaluarAperturaDOWN(results, activeParam, flujo_count)
        elif results[Constants.IND_PROB_FLOW] == Constants.DIR_PRE_DOWN:
            nada = ''
            self.evaluarAperturaPREDOWN(results, activeParam, flujo_count)
        elif results[Constants.IND_PROB_FLOW] == Constants.DIR_CHANGE:
            nada = ''
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
        difference_optimized, unit_diff = self.evaluarAperturaDOWNDifference(results, activeParam, flujo_count)
        pass
        if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
            if self.enableControlOpen:
                if results[Constants.ACUMULADO_ABS] <= difference_optimized * self.multiplicadorOpen:
                    results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                    pass
            else:
                difOpenHours = self.getDifTimeFromOpen(results)
                pass
                if difOpenHours <= 60:
                    if self.getProbFlow(results, activeParam) == Constants.DIR_DOWN:
                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                        pass
                elif results[Constants.ACUMULADO_ABS] >= difference_optimized * self.multiplicadorUP or results[Constants.ACTION_MAX_DIST] >= difference_optimized * self.multiplicadorUP:
                    if results[Constants.IND_BLG_LOWER_DST_PERCENT] > self.blgDistPercent:
                        if (abs(results[Constants.MEDSTDDIFF]) > self.medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0) and abs(results[Constants.MEDSTDDIFF]) < self.medstdmaxDiff:
                            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                            pass
                    elif results[Constants.ANGLE] < 0 and abs(results[Constants.ANGLE]) >= 0.18:
                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                        pass
        elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
            if results[Constants.ACUMULADO_ABS] >= difference_optimized * self.multiplicadorUP or results[Constants.ACTION_MIN_DIST] >= difference_optimized * self.multiplicadorUP:
                if (abs(results[Constants.MEDSTDDIFF]) > self.medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0) and abs(results[Constants.MEDSTDDIFF]) < self.medstdmaxDiff:
                    if results[Constants.IND_BLG_UPPER_DST_PERCENT] > self.blgDistPercent:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        pass

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
        difference_optimized, unit_diff = self.evaluarDifferenceUP(results, activeParam, flujo_count)
        pass
        if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
            if self.enableControlOpen:
                if results[Constants.ACUMULADO_ABS] <= difference_optimized * self.multiplicadorOpen:
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                    pass
            else:
                difOpenHours = self.getDifTimeFromOpen(results)
                if difOpenHours <= 10:
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                    pass
                elif results[Constants.ACUMULADO_ABS] >= difference_optimized * self.multiplicadorUP or results[Constants.ACTION_MIN_DIST] >= difference_optimized * self.multiplicadorUP:
                    if results[Constants.IND_BLG_UPPER_DST_PERCENT] > self.blgDistPercent:
                        if (abs(results[Constants.MEDSTDDIFF]) > self.medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0) and abs(results[Constants.MEDSTDDIFF]) < self.medstdmaxDiff:
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            pass
                    elif results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
                        if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UP:
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            pass
        elif results[Constants.FLUJO] == Constants.FLUJO_BAJA:
            if results[Constants.ACUMULADO_ABS] >= difference_optimized * self.multiplicadorUP or results[Constants.ACTION_MAX_DIST] >= difference_optimized * self.multiplicadorUP:
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] > self.blgDistPercent:
                    if (abs(results[Constants.MEDSTDDIFF]) > self.medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0) and abs(results[Constants.MEDSTDDIFF]) < self.medstdmaxDiff:
                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                        pass

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
        difference_optimized, unit_diff = self.evaluarDifferenceBUY(results, activeParam, flujo_count)
        pass
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.ACTION_ACUM] < 0:
            if results[Constants.ACUMULADO] >= self.closeAcumValue:
                pass
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
            if results[Constants.ACUMULADO] <= 0:
                if abs(results[Constants.ACUMULADO]) >= self.closeDifference:
                    pass
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if results[Constants.ACTION_ACUM] < 0:
            if abs(results[Constants.ACTION_MAX_DIST]) >= self.closeAcumValue:
                pass
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.ACTION_ACUM] <= 0:
            if abs(results[Constants.ACTION_ACUM]) >= self.closeProfit:
                pass
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.ACTION_ACUM] > 0:
            if results[Constants.ACTION_ACUM] >= self.closeProfit:
                if results[Constants.ACUMULADO] <= 0:
                    if results[Constants.ACTION_MAX_DIST] >= self.closeProfit:
                        pass
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return

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
        flujo_count = results[Constants.FLUJO_COUNT]
        difference_optimized, unit_diff = self.evaluarDifferenceSELL(results, activeParam, flujo_count)
        pass
        pass
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_DOWN] = 0
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_BUY:
            if results[Constants.ACUMULADO] > 0:
                if abs(results[Constants.ACUMULADO]) >= self.closeDifference:
                    pass
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if results[Constants.ACTION_ACUM] > 0:
            if abs(results[Constants.ACTION_ACUM]) >= self.closeProfit:
                pass
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.ACUMULADO] > 0:
            if results[Constants.ACTION_MIN_DIST] >= self.closeAcumValue:
                pass
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.ACTION_ACUM] < 0:
            if abs(results[Constants.ACTION_ACUM]) >= self.closeProfit:
                if results[Constants.ACUMULADO] > 0:
                    if results[Constants.ACTION_MIN_DIST] >= difference_optimized:
                        pass
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return