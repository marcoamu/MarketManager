from evaluators.CierreBase import CierreBase
from evaluators.EvaluatorBase import EvaluatorBase
from evaluators.AperturaBase import AperturaBase
from service.Constants import Constants

class EvaluatorOnlyUp02(EvaluatorBase, AperturaBase, CierreBase):

    def __init__(self):
        self.name = 'EvaluatorOnlyUp02'

    def evaluate(self, results, activeParam):
        results[Constants.EVAl_NAME] = self.name
        results['ALERT'] = False
        alert = False
        isTendence = False
        isAccumulated = False
        isSell = False
        isBuy = False
        isClose = False
        flujo_count = results[Constants.FLUJO_COUNT]
        if results[Constants.CURRENT_ACTION] == Constants.ACTION_WAIT or results[Constants.CURRENT_ACTION] == Constants.ACTION_CLOSE:
            if results[Constants.DIRECTION] == Constants.DIR_UP:
                if results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_UP:
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                    pass
        elif results[Constants.CURRENT_ACTION] == Constants.ACTION_BUY:
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
            pass
            if results[Constants.ACTION_MAX_DIST] >= difference_optimized:
                pass
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if results[Constants.ACTION_MAX_DIST] != 0:
                    if results[Constants.ACUMULADO_ABS] >= float(difference_optimized) and results[Constants.FLUJO_COUNT] >= 1:
                        pass
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    if results[Constants.ACTION_DISTANCE] < 0 and abs(results[Constants.ACTION_DISTANCE]) >= float(activeParam.accumulate):
                        pass
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
            if results[Constants.IMA5MA20] == Constants.INDICATOR_SELL:
                pass
                if results[Constants.FLUJO] == Constants.FLUJO_BAJA and results[Constants.ACUMULADO_ABS] >= float(difference_optimized):
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
            if results[Constants.IMA5MA20] == Constants.INDICATOR_SELLX:
                pass
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
        elif results[Constants.CURRENT_ACTION] == Constants.ACTION_SELL:
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
            pass
            if results[Constants.ACTION_MIN_DIST] >= difference_optimized:
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                pass
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.ACUMULADO_ABS] >= float(difference_optimized):
                    pass
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                if results[Constants.ACTION_DISTANCE] > 0 and abs(results[Constants.ACTION_DISTANCE]) > float(activeParam.accumulate):
                    pass
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
            if results[Constants.IMA5MA20] == Constants.INDICATOR_BUY:
                if results[Constants.FLUJO] == Constants.FLUJO_SUBE and results[Constants.ACUMULADO_ABS] >= float(difference_optimized) and (results[Constants.ACTION_DISTANCE] > 0):
                    pass
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
            if results[Constants.IMA5MA20] == Constants.INDICATOR_BUYX:
                pass
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE