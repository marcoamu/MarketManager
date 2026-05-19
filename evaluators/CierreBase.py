from service.Constants import Constants
import time
from datetime import datetime

class CierreBase:

    def __init__(self):
        pass

    def gettime(self, results):
        currentTime = None
        try:
            import time
            from datetime import datetime
            simulation = results[Constants.SIMULATION]
            if simulation:
                temp = results[Constants.DATE].values[0]
                t = datetime.strptime(temp, '%Y-%m-%d %H:%M:%S.%f')
                current_time_h = t.hour * 100
                current_time_min = t.minute
                currentTime = int(current_time_h + current_time_min)
            else:
                t = time.localtime()
                current_time_h = time.strftime('%H', t)
                current_time_min = time.strftime('%M', t)
                currentTime = int(current_time_h + current_time_min)
        except Exception as e:
            nada = ''
        return currentTime

    def getDifTimeFromOpen(self, results):
        if results[Constants.SIMULATION] is True:
            temp = results[Constants.DATE].values[0]
            t = datetime.strptime(temp, '%Y-%m-%d %H:%M:%S.%f')
            current_time_h = t.hour * 100
            current_time_min = t.minute
            currentTime = int(current_time_h + current_time_min)
            openHour = 1530
            dif = currentTime - openHour
        else:
            t = time.localtime()
            current_time_h = time.strftime('%H', t)
            current_time_min = time.strftime('%M', t)
            currentTime = int(current_time_h + current_time_min)
            openHour = 1530
            dif = currentTime - openHour
        return dif

    def printFinLog(self, name, methodName, results, activeparameters):
        pass
        results[Constants.INICIO_NAME] = name

    def control_SELL_BLG_02(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_SELL_BLG_02'
        difference_optimized = activeParam.difference
        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] = 0
                self.printFinLog('CLOSE_SELL_BLG_MID_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MIN_DIST] >= difference_optimized:
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    self.printFinLog('CLOSE_SELL_NXT_UP_01', name, results, activeParam)
                    results[Constants.CLOSE_NXT_UP] = 0
                return
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_BUY:
            if results[Constants.ACTION_ACUM] > 0:
                if results[Constants.ACUMULADO] >= closeAcumValue:
                    self.printFinLog('CLOSE_SELL_IND_BLG_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
            elif results[Constants.ACTION_ACUM] < 0:
                nada = ''
                if results[Constants.ACUMULADO] >= closeAcumValue:
                    self.printFinLog('CLOSE_SELL_IND_BLG_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if results[Constants.ACTION_ACUM] > 0:
            if abs(results[Constants.ACTION_ACUM]) >= closeAcumValue:
                self.printFinLog('CLOSE_SELL_ACTION_ACUM_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

    def control_SELL_BLG_03(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_SELL_BLG_03'
        difference_optimized = activeParam.difference
        bollingerClose = activeParam.bollingerClose
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_BUY:
            if results[Constants.ACUMULADO] > 0:
                if abs(results[Constants.ACUMULADO]) >= closeAcumValue:
                    self.printFinLog('CLOSE_SELL_IND_BLG_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if results[Constants.ACTION_ACUM] > 0:
            if abs(results[Constants.ACTION_ACUM]) >= bollingerClose:
                self.printFinLog('CLOSE_SELL_IND_BLG_02', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.ACUMULADO] > 0:
            if results[Constants.ACTION_MIN_DIST] >= bollingerClose:
                self.printFinLog('CLOSE_SELL_ACUMULADO_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

    def control_SELL_EMA_WEEK_01(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_SELL_EMA_WEEK_01'
        difference_optimized = activeParam.difference
        bollingerClose = activeParam.bollingerClose
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_BUY:
            self.printFinLog('CLOSE_SELL_EMA_CHANGE_01', name, results, activeParam)
            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
            return
        rising, angleDiff = self.isRisingFromWeek(results)
        if rising:
            if angleDiff < 0:
                if abs(angleDiff) >= closeWeekDiffNew:
                    pass
                    self.printFinLog('CLOSE_SELL_EMA_WEEK_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
            elif abs(angleDiff) >= closeWeekDiffNew / 2:
                pass
                self.printFinLog('CLOSE_SELL_EMA_WEEK_02', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

    def control_SELL_EMA_WEEK_02(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_SELL_EMA_WEKK_02'
        difference_optimized = activeParam.difference
        bollingerClose = activeParam.bollingerClose
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_BUY:
            self.printFinLog('CLOSE_SELL_EMA_CHANGE_01', name, results, activeParam)
            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
            return
        rising, angleDiff = self.isRisingFromWeek(results)
        if rising:
            if angleDiff < 0:
                if abs(angleDiff) >= closeWeekDiffNew:
                    pass
                    self.printFinLog('CLOSE_SELL_EMA_WEEK_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

    def control_SELL_EMA_WEEK_03(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_SELL_EMA_WEEK_03'
        difference_optimized = activeParam.difference
        bollingerClose = activeParam.bollingerClose
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        rising, angleDiff = self.isRisingFromWeek(results)
        if rising:
            if angleDiff < 0:
                if abs(angleDiff) >= closeWeekDiffNew:
                    pass
                    self.printFinLog('CLOSE_SELL_EMA_WEEK_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
            elif abs(angleDiff) >= closeWeekDiffNew / 2:
                pass
                self.printFinLog('CLOSE_SELL_EMA_WEEK_02', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

    def control_SELL_EMA_WEEK_04(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_SELL_EMA_WEEK_03'
        difference_optimized = activeParam.difference
        bollingerClose = activeParam.bollingerClose
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        rising, angleDiff = self.isRisingFromMonth(results)
        if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_BUY:
            if results[Constants.ACUMULADO] > 0:
                self.printFinLog('CLOSE_SELL_EMA_CHANGE_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if rising:
            if angleDiff > 0:
                if abs(angleDiff) >= closeWeekDiffNew:
                    pass
                    self.printFinLog('CLOSE_SELL_EMA_WEEK_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
            else:
                nada = ''
                if abs(angleDiff) >= closeWeekDiffNew:
                    pass
                    self.printFinLog('CLOSE_SELL_EMA_WEEK_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

    def control_SELL_EMA_WEEK_05(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_SELL_EMA_WEEK_03'
        difference_optimized = activeParam.difference
        bollingerClose = activeParam.bollingerClose
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        rising, angleDiff = self.isRisingFromMonth(results)
        if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_BUY:
            if results[Constants.ACUMULADO] > 0:
                if rising and abs(angleDiff) > closeWeekDiffNew:
                    self.printFinLog('CLOSE_SELL_EMA_CHANGE_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if rising:
            if angleDiff > 0:
                if abs(angleDiff) >= closeWeekDiffNew:
                    pass
                    self.printFinLog('CLOSE_SELL_EMA_WEEK_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
            elif abs(angleDiff) >= closeWeekDiffNew:
                pass
                self.printFinLog('CLOSE_SELL_EMA_WEEK_02', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

    def updateCLoseForSell(self, result, activeParam, closeWeekDiffNew):
        res = closeWeekDiffNew
        indicatorEma = result[Constants.INDICATOR_EMA]
        blgLowDst = result[Constants.IND_BLG_LOWER_DST_PERCENT]
        if Constants.INDICATOR_EMA_BUY == indicatorEma:
            if blgLowDst < 30:
                res = closeWeekDiffNew / 2
            else:
                res = closeWeekDiffNew
        elif Constants.INDICATOR_EMA_SELL == indicatorEma:
            if blgLowDst < 10:
                res = closeWeekDiffNew
            elif blgLowDst > 40:
                res = closeWeekDiffNew / 2
        return res

    def updateCLoseForSell2(self, result, activeParam, closeWeekDiffNew):
        res = closeWeekDiffNew
        indicatorEma = result[Constants.INDICATOR_EMA]
        blgLowDst = result[Constants.IND_BLG_LOWER_DST_PERCENT]
        rising, angleDiff = self.isRisingFromWeekNew(result)
        ima1emadiff = float(result[Constants.IMA1EMADIFF])
        if rising:
            if ima1emadiff <= 0:
                res = closeWeekDiffNew
            else:
                res = closeWeekDiffNew / 2
        else:
            res = closeWeekDiffNew * 1.2
        return res

    def control_SELL_EMA_WEEK_NEW_FLOW_04(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_SELL_EMA_WEEK_NEW_FLOW_04'
        difference_optimized = activeParam.difference
        bollingerClose = activeParam.bollingerClose
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        closeWeekDiffNew = self.updateCLoseForSell2(results, activeParam, closeWeekDiffNew)
        rising, angleDiff = self.isRisingFromWeekNew(results)
        currentTime = self.gettime(results)
        actionCount = 0
        if currentTime >= 2100:
            actionCount = 1
        difference_optimized = activeParam.difference
        bollingerClose = activeParam.bollingerClose
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        closeWeekDiffNew = self.updateCLoseForSell2(results, activeParam, closeWeekDiffNew)
        rising, angleDiff = self.isRisingFromWeekNew(results)
        currentTime = self.gettime(results)
        actionCount = 0
        if currentTime >= 2100:
            actionCount = 1
        if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_BUY:
            if results[Constants.ACUMULADO] > 0:
                if results[Constants.ACTION_COUNT] > actionCount:
                    if rising and abs(angleDiff) > closeWeekDiffNew / 2:
                        self.printFinLog('CLOSE_SELL_EMA_CHANGE_01', name, results, activeParam)
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return
        if rising:
            if angleDiff > 0:
                if abs(angleDiff) >= closeWeekDiffNew:
                    pass
                    self.printFinLog('CLOSE_SELL_EMA_WEEK_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
            elif abs(angleDiff) >= closeWeekDiffNew:
                pass
                self.printFinLog('CLOSE_SELL_EMA_WEEK_02', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
            if results[Constants.ACUMULADO] > 0:
                if results[Constants.ACUMULADO_ABS] >= closeAcumValue * 1.2:
                    self.printFinLog('CLOSE_SELL_ACUMULADO_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

    def control_SELL_EMA_WEEK_NEW_FLOW_01(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_SELL_EMA_WEEK_NEW_FLOW_01'
        difference_optimized = activeParam.difference
        bollingerClose = activeParam.bollingerClose
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        closeWeekDiffNew = self.updateCLoseForSell2(results, activeParam, closeWeekDiffNew)
        rising, angleDiff = self.isRisingFromWeekNew(results)
        currentTime = self.gettime(results)
        actionCount = 0
        if currentTime >= 2100:
            actionCount = 1
        if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_BUY:
            if results[Constants.ACUMULADO] > 0:
                if results[Constants.ACTION_COUNT] > actionCount:
                    if rising and abs(angleDiff) > closeWeekDiffNew / 2:
                        self.printFinLog('CLOSE_SELL_EMA_CHANGE_01', name, results, activeParam)
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return
        if rising:
            if angleDiff > 0:
                if abs(angleDiff) >= closeWeekDiffNew:
                    pass
                    self.printFinLog('CLOSE_SELL_EMA_WEEK_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
            elif abs(angleDiff) >= closeWeekDiffNew:
                pass
                self.printFinLog('CLOSE_SELL_EMA_WEEK_02', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

    def control_SELL_EMA_WEEK_NEW_FLOW_02(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_SELL_EMA_WEEK_NEW_FLOW_02'
        difference_optimized = activeParam.difference
        bollingerClose = activeParam.bollingerClose
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        closeWeekDiffNew = self.updateCLoseForSell2(results, activeParam, closeWeekDiffNew)
        rising, angleDiff = self.isRisingFromWeekNew(results)
        currentTime = self.gettime(results)
        actionCount = 0
        if currentTime >= 2100:
            actionCount = 1
        if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_BUY:
            if results[Constants.ACUMULADO] > 0:
                if results[Constants.ACTION_COUNT] > actionCount:
                    if rising and abs(angleDiff) > closeWeekDiffNew / 2:
                        self.printFinLog('CLOSE_SELL_EMA_CHANGE_01', name, results, activeParam)
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return
        if rising:
            if angleDiff > 0:
                if results[Constants.ACUMULADO] > 0:
                    if abs(angleDiff) >= closeWeekDiffNew:
                        pass
                        self.printFinLog('CLOSE_SELL_EMA_WEEK_01', name, results, activeParam)
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return
            elif abs(angleDiff) >= closeWeekDiffNew:
                pass
                self.printFinLog('CLOSE_SELL_EMA_WEEK_02', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

    def control_SELL_EMA_WEEK_NEW_FLOW_03(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_SELL_EMA_WEEK_NEW_FLOW_03'
        difference_optimized = activeParam.difference
        bollingerClose = activeParam.bollingerClose
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        closeWeekDiffNew = self.updateCLoseForSell2(results, activeParam, closeWeekDiffNew)
        rising, angleDiff = self.isRisingFromWeekNew(results)
        currentTime = self.gettime(results)
        actionCount = 0
        if currentTime >= 2100:
            actionCount = 1
        if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_BUY:
            if results[Constants.ACUMULADO] > 0:
                if results[Constants.ACTION_COUNT] > actionCount:
                    if rising and abs(angleDiff) > closeWeekDiffNew / 2:
                        self.printFinLog('CLOSE_SELL_EMA_CHANGE_01', name, results, activeParam)
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return
        if rising:
            if angleDiff > 0:
                if abs(angleDiff) >= closeWeekDiffNew:
                    pass
                    self.printFinLog('CLOSE_SELL_EMA_WEEK_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
            elif abs(angleDiff) >= closeWeekDiffNew:
                pass
                self.printFinLog('CLOSE_SELL_EMA_WEEK_02', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

    def control_SELL_EMA_WEEK_NEW_FLOW_02(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_SELL_EMA_WEEK_NEW_FLOW_01'
        difference_optimized = activeParam.difference
        bollingerClose = activeParam.bollingerClose
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        closeWeekDiffNew = self.updateCLoseForSell(results, activeParam, closeWeekDiffNew)
        rising, angleDiff = self.isRisingFromWeekNew(results)
        currentTime = self.gettime(results)
        actionCount = 0
        if currentTime >= 2100:
            actionCount = 1
        if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_BUY:
            if results[Constants.ACUMULADO] > 0:
                if results[Constants.ACTION_COUNT] > actionCount:
                    if rising and abs(angleDiff) > closeWeekDiffNew / 2:
                        self.printFinLog('CLOSE_SELL_EMA_CHANGE_01', name, results, activeParam)
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return
        if rising:
            if angleDiff > 0:
                if abs(angleDiff) >= closeWeekDiffNew:
                    pass
                    self.printFinLog('CLOSE_SELL_EMA_WEEK_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
            else:
                nada = ''

    def control_SELL_RSI_01(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_SELL_RSI_01'
        difference_optimized = activeParam.difference
        bollingerClose = activeParam.bollingerClose
        max_loss = 0.006 * float(results[Constants.VALUE])
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if (results[Constants.RSI] > 30 and results[Constants.RSI] < 40) and results[Constants.RSI_DIFF] >= 2:
            if results[Constants.ACTION_COUNT] > 1:
                self.printFinLog('CLOSE_SELL_ACTION_RSI_DIFF_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if (results[Constants.RSI] > 50 and results[Constants.RSI] < 60) and results[Constants.RSI_DIFF] >= 2:
            if results[Constants.ACTION_COUNT] > 1:
                self.printFinLog('CLOSE_SELL_ACTION_RSI_DIFF_02', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.ACTION_MIN_DIST] > 0:
            if abs(results[Constants.ACTION_MIN_DIST]) >= max_loss:
                self.printFinLog('CLOSE_SELL_ACTION_ACUM_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

    def control_SELL_EMA_01(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_SELL_EMA_01'
        difference_optimized = activeParam.difference
        bollingerClose = activeParam.bollingerClose
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_BUY:
            self.printFinLog('CLOSE_SELL_EMA_CHANGE_01', name, results, activeParam)
            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
            return

    def control_SELL_EMA_02(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_SELL_EMA_02'
        difference_optimized = activeParam.difference
        bollingerClose = activeParam.bollingerClose
        minmaxClose = closeAcumValue * 2.5
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_BUY:
            if results[Constants.ACTION_MIN_DIST] >= minmaxClose:
                self.printFinLog('CLOSE_SELL_EMA_CHANGE_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.ACTION_MIN_DIST] >= minmaxClose:
            self.printFinLog('CLOSE_SELL_ACTION_MIN_DIST_01', name, results, activeParam)
            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
            return

    def control_SELL_BLG_01(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_SELL_BLG_01'
        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] = 0
                self.printFinLog('CLOSE_SELL_BLG_MID_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_BUY:
            if results[Constants.ACTION_COUNT] > 5:
                if results[Constants.ACTION_ACUM] > 0:
                    self.printFinLog('CLOSE_SELL_BLG_MED_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
                elif abs(results[Constants.ACTION_MIN_DIST]) >= closeAcumValue:
                    self.printFinLog('CLOSE_SELL_BLG_MED_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if results[Constants.ACTION_ACUM] > 0:
            if abs(results[Constants.ACTION_ACUM]) >= closeDifference:
                self.printFinLog('CLOSE_SELL_ACTION_ACUM_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.ACUMULADO] > 0:
            if abs(results[Constants.IND_BLG_MED_DST]) <= self.midMinDst:
                self.printFinLog('CLOSE_SELL_ACUM_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.IND_BLG_LOWER_DST_PERCENT] < 0:
            if results[Constants.ACTION_COUNT] > 3:
                if abs(results[Constants.IND_BLG_LOWER_DST_PERCENT]) > 1:
                    self.printFinLog('CLOSE_SELL_IND_BLG_LOWER_DST_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

    def control_SELL_START_CLOSE_01(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_SELL_START_CLOSE_01'
        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] = 0
                self.printFinLog('CLOSE_SELL_BLG_MID_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_BUY:
            if results[Constants.ACTION_COUNT] > 2:
                if results[Constants.ACTION_ACUM] > 0:
                    self.printFinLog('CLOSE_SELL_BLG_MED_BUY_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
                else:
                    self.printFinLog('CLOSE_SELL_BLG_MED_BUY_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if results[Constants.ACTION_ACUM] > 0:
            if results[Constants.ACTION_COUNT] > 3:
                if abs(results[Constants.ACTION_ACUM]) >= closeDifference:
                    self.printFinLog('CLOSE_SELL_ACT_ACUM_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
            elif results[Constants.ACTION_COUNT] >= 2:
                if abs(results[Constants.ACTION_ACUM]) >= closeDifference:
                    self.printFinLog('CLOSE_SELL_ACT_ACUM_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if results[Constants.ACUMULADO] > 0:
            if results[Constants.ACTION_ACUM] < 0:
                if abs(results[Constants.ACTION_ACUM]) > closeAcumValue:
                    if abs(results[Constants.ACTION_MIN_DIST]) >= closeAcumValue:
                        self.printFinLog('CLOSE_SELL_ACUM_01', name, results, activeParam)
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return

    def control_SELL_START_CLOSE_02(self, results, activeParam, closeAcumValue, closeDifference, accumulate):
        name = 'control_SELL_START_CLOSE_02'
        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] = 0
                self.printFinLog('CLOSE_SELL_BLG_MID_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_BUY:
            if results[Constants.ACTION_COUNT] > 5:
                if results[Constants.ACTION_ACUM] > 0:
                    self.printFinLog('CLOSE_SELL_BLG_MED_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
                elif abs(results[Constants.ACTION_MIN_DIST]) >= closeAcumValue:
                    self.printFinLog('CLOSE_SELL_BLG_MED_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if results[Constants.ACTION_ACUM] > 0:
            if results[Constants.ACTION_COUNT] > 2:
                if abs(results[Constants.ACTION_ACUM]) >= closeDifference:
                    self.printFinLog('CLOSE_SELL_ACTION_ACUM_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if results[Constants.ACUMULADO] > 0:
            if results[Constants.ACTION_ACUM] < 0:
                if abs(results[Constants.ACTION_ACUM]) > closeAcumValue:
                    if abs(results[Constants.ACTION_MIN_DIST]) >= closeAcumValue:
                        self.printFinLog('CLOSE_SELL_ACUMULATE_01', name, results, activeParam)
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return

    def control_SELL_BLG_MID_01(self, results, activeParam, closeAcumValue, closeDifference, accumulate):
        name = 'control_SELL_BLG_MID_01'
        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] = 0
                pass
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
            if results[Constants.ACTION_COUNT] > 2:
                pass
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_BUY:
            if results[Constants.ACTION_COUNT] > 2:
                if results[Constants.ACTION_ACUM] > 0:
                    pass
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
                else:
                    pass
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if results[Constants.ACUMULADO] > 0:
            if results[Constants.ACTION_ACUM] < 0:
                if results[Constants.ACTION_COUNT] >= 3:
                    if results[Constants.ACUMULADO_ABS] > accumulate:
                        if abs(results[Constants.ACTION_MIN_DIST]) >= accumulate:
                            pass
                            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                            return
            else:
                nada = ''

    def control_SELL_BLG_MID_02(self, results, activeParam, closeAcumValue, closeDifference, accumulate):
        name = 'control_SELL_BLG_MID_02'
        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] = 0
                self.printFinLog('CLOSE_SELL_NXT_MID_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
            if results[Constants.ACTION_COUNT] > 2:
                self.printFinLog('CLOSE_SELL_BLG_MID_PERCENT_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_BUY:
            if results[Constants.ACTION_COUNT] > 2:
                if results[Constants.ACTION_ACUM] > 0:
                    self.printFinLog('CLOSE_SELL_BLG_BUY_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
                else:
                    self.printFinLog('CLOSE_SELL_BLG_BUY_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if results[Constants.ACUMULADO] > 0:
            if results[Constants.ACTION_ACUM] < 0:
                if results[Constants.ACTION_COUNT] >= 3:
                    if results[Constants.ACUMULADO_ABS] > accumulate:
                        if abs(results[Constants.ACTION_MIN_DIST]) >= accumulate:
                            self.printFinLog('CLOSE_SELL_ACUM_01', name, results, activeParam)
                            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                            return
            else:
                nada = ''
                if results[Constants.ACTION_COUNT] >= 1:
                    if results[Constants.ANGLE_IMA1] > 0:
                        if results[Constants.ANGLE_IMA1_COUNTER] >= 2:
                            if abs(results[Constants.ACTION_MIN_DIST]) >= accumulate:
                                self.printFinLog('CLOSE_SELL_ACUM_02', name, results, activeParam)
                                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                                return

    def control_SELL_BLG_LONG_01(self, results, activeParam, closeAcumValue, closeDifference, accumulate):
        name = 'control_SELL_BLG_LONG_01'
        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] = 0
                self.printFinLog('CLOSE_SELL_NXT_MID_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
            if results[Constants.ACTION_COUNT] > 2:
                self.printFinLog('CLOSE_SELL_BLG_MID_PERCENT_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_BUY:
            if results[Constants.ACTION_COUNT] > 2:
                if results[Constants.ACTION_ACUM] > 0:
                    self.printFinLog('CLOSE_SELL_BLG_BUY_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
                else:
                    self.printFinLog('CLOSE_SELL_BLG_BUY_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

    def control_SELL_IMA1_01(self, results, activeParam, closeAcumValue, closeDifference, accumulate):
        name = 'control_SELL_IMA1_01'
        angle = float(results[Constants.ANGLE])
        anglePrev = float(results[Constants.ANGLE_PREV])
        angleDiff = angle - anglePrev
        closeAngleDiff = int(activeParam.closeAngleDiff)
        difference_optimized = activeParam.difference
        closeAcumValue = activeParam.closeAcumvalue
        name = 'control_SELL_START_CLOSE_01'
        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] = 0
                pass
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if results[Constants.ACTION_ACUM] > 0:
            if abs(results[Constants.ACTION_ACUM]) >= closeAcumValue:
                self.printFinLog('CLOSE_SELL_ACTION_ACUM_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.ACUMULADO] > 0:
            if results[Constants.ACUMULADO_ABS] >= closeAcumValue:
                self.printFinLog('CLOSE_SELL_ACUMULADO_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.ACTION_ACUM] < 0:
            if abs(results[Constants.ACTION_ACUM]) >= closeAcumValue * 2:
                if results[Constants.ACUMULADO] > 0:
                    if results[Constants.ACUMULADO_ABS] >= closeAcumValue / 2:
                        self.printFinLog('CLOSE_SELL_ACTION_ACUM2_01', name, results, activeParam)
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return

    def control_SELL_IMA1_02(self, results, activeParam, closeAcumValue, closeDifference, accumulate):
        name = 'control_SELL_IMA1_02'
        angle = float(results[Constants.ANGLE])
        anglePrev = float(results[Constants.ANGLE_PREV])
        angleDiff = angle - anglePrev
        closeAngleDiff = int(activeParam.closeAngleDiff)
        difference_optimized = activeParam.difference
        closeAcumValue = activeParam.closeAcumvalue
        if results[Constants.ACTION_ACUM] > 0:
            if abs(results[Constants.ACTION_ACUM]) >= closeAcumValue:
                self.printFinLog('CLOSE_SELL_ACTION_ACUM_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.ACUMULADO] > 0:
            if results[Constants.ACUMULADO_ABS] >= closeAcumValue:
                self.printFinLog('CLOSE_SELL_ACUM_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.ACTION_ACUM] < 0:
            if abs(results[Constants.ACTION_ACUM]) >= closeAcumValue * 2:
                if results[Constants.ACUMULADO] > 0:
                    if results[Constants.ACUMULADO_ABS] >= closeAcumValue / 2:
                        self.printFinLog('CLOSE_SELL_ACTION_ACUM_02', name, results, activeParam)
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return

    def control_SELL_BLG_LONG_02(self, results, activeParam, closeAcumValue, closeDifference, accumulate):
        name = 'control_SELL_BLG_LONG_02'
        closeAngleDiff = int(activeParam.closeAngleDiff)
        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] = 0
                self.printFinLog('CLOSE_SELL_NXT_MID_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] >= activeParam.middleDstPercent:
            if results[Constants.ACTION_COUNT] > 2:
                self.printFinLog('CLOSE_SELL_BLG_MID_PERCENT_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_BUY:
            openTimeFromOpen = self.getDifTimeFromOpen(results)
            if results[Constants.ACTION_COUNT] > 2 or openTimeFromOpen < 30:
                if results[Constants.ACTION_ACUM] > 0:
                    self.printFinLog('CLOSE_SELL_BLG_BUY_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
                else:
                    self.printFinLog('CLOSE_SELL_BLG_BUY_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        rising, angleDiff = self.isRisingAngleIma1(results)
        if rising == True and abs(angleDiff) >= closeAngleDiff:
            if results[Constants.ACTION_COUNT] > 3:
                if results[Constants.ACUMULADO] > 0:
                    if results[Constants.ACUMULADO] >= accumulate:
                        if float(results[Constants.IMA1EMADIFF]) < 0:
                            self.printFinLog('CLOSE_SELL_ANGLE_IMA_EMA_01', name, results, activeParam)
                            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                            return

    def control_SELL_BLG_LONG_04(self, results, activeParam, closeAcumValue, closeDifference, accumulate):
        name = 'control_SELL_BLG_LONG_04'
        closeAngleDiff = int(activeParam.closeAngleDiff)
        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] = 0
                self.printFinLog('CLOSE_SELL_NXT_MID_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] >= activeParam.middleDstPercent:
            if results[Constants.ACTION_COUNT] > 2:
                self.printFinLog('CLOSE_SELL_BLG_MID_PERCENT_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_BUY:
            if results[Constants.ACTION_COUNT] > 2:
                if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] >= activeParam.middleDstPercent:
                    if results[Constants.ACTION_ACUM] > 0:
                        self.printFinLog('CLOSE_SELL_BLG_BUY_01', name, results, activeParam)
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return
                    else:
                        self.printFinLog('CLOSE_SELL_BLG_BUY_02', name, results, activeParam)
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return
        rising, angleDiff = self.isRisingAngleIma1(results)
        if rising == True and abs(angleDiff) >= closeAngleDiff:
            if results[Constants.ACTION_COUNT] > 3:
                if results[Constants.ACUMULADO] > 0:
                    if results[Constants.ACUMULADO] > accumulate:
                        if float(results[Constants.IMA1EMADIFF]) < 0:
                            self.printFinLog('CLOSE_SELL_ANGLE_IMA_EMA_01', name, results, activeParam)
                            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                            return

    def control_SELL_BLG_LONG_03(self, results, activeParam, closeAcumValue, closeDifference, accumulate):
        name = 'control_SELL_BLG_LONG_03'
        closeAngleDiff = int(activeParam.closeAngleDiff)
        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] = 0
                self.printFinLog('CLOSE_SELL_NXT_MID_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
            if results[Constants.ACTION_COUNT] > 2:
                self.printFinLog('CLOSE_SELL_BLG_MID_PERCENT_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_BUY:
            if results[Constants.ACTION_COUNT] > 2:
                if results[Constants.ACTION_ACUM] > 0:
                    self.printFinLog('CLOSE_SELL_BLG_BUY_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
                else:
                    self.printFinLog('CLOSE_SELL_BLG_BUY_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        rising, angleDiff = self.isRisingAngleIma1(results)
        if rising == True and abs(angleDiff) >= closeAngleDiff:
            self.printFinLog('CLOSE_SELL_ANGLE_IMA_EMA_02', name, results, activeParam)
            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
            return
            if results[Constants.ACTION_COUNT] > 3:
                if results[Constants.ACUMULADO] > 0:
                    if results[Constants.ACUMULADO] >= accumulate:
                        if float(results[Constants.IMA1EMADIFF]) < 0:
                            self.printFinLog('CLOSE_SELL_ANGLE_IMA_EMA_01', name, results, activeParam)
                            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                            return

    def control_BUY_BLG_01(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_BUY_BLG_01'
        difference_optimized = activeParam.difference
        midMinDst = 0.08
        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] = 0
                self.printFinLog('CLOSE_BUY_NXT_MIDDLE_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
            if results[Constants.ACTION_COUNT] > 5:
                if results[Constants.ACTION_ACUM] < 0:
                    self.printFinLog('CLOSE_BUY_IND_BLG_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
                elif abs(results[Constants.ACTION_MAX_DIST]) >= closeAcumValue:
                    self.printFinLog('CLOSE_BUY_IND_BLG_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if results[Constants.ACUMULADO] <= 0:
            if abs(results[Constants.ACUMULADO]) > difference_optimized:
                if abs(results[Constants.IND_BLG_MED_DST]) <= midMinDst:
                    self.printFinLog('CLOSE_BUY_ACUM_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if results[Constants.ACTION_ACUM] <= 0:
            if abs(results[Constants.ACTION_ACUM]) >= closeDifference:
                self.printFinLog('CLOSE_BUY_ACTION_ACUM_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
            if results[Constants.ACTION_COUNT] > 3:
                if abs(results[Constants.IND_BLG_UPPER_DST_PERCENT]) > 1:
                    self.printFinLog('CLOSE_BUY_BLG_UPP_DST_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if abs(results[Constants.IND_BLG_UPPER_DST_PERCENT]) > 0 and abs(results[Constants.IND_BLG_UPPER_DST_PERCENT]) < 2:
            if results[Constants.ACTION_COUNT] > 3:
                self.printFinLog('CLOSE_BUY_BLG_UPP_DST_02', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

    def control_BUY_BLG_02(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_BUY_BLG_02'
        multiplicadorUP = 1
        difference_optimized = activeParam.difference
        closeAcumValue = activeParam.closeProfit
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MIN_DIST] >= difference_optimized * multiplicadorUP:
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    self.printFinLog('CLOSE_BUY_NXT_DOWN_01', name, results, activeParam)
                results[Constants.CLOSE_NXT_DOWN] = 0
                return
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
            if results[Constants.ACTION_ACUM] < 0 or results[Constants.ACUMULADO] <= 0:
                self.printFinLog('CLOSE_BUY_MED_SELL_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.ACTION_ACUM] < 0:
            if results[Constants.ACUMULADO] >= closeAcumValue:
                self.printFinLog('CLOSE_BUY_ACTION_ACUM_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.ACTION_ACUM] < 0:
            if abs(results[Constants.ACTION_ACUM]) >= closeAcumValue:
                self.printFinLog('CLOSE_BUY_ACTION_ACUM_02', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

    def control_BUY_BLG_03(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_BUY_BLG_03'
        multiplicadorUP = 1
        difference_optimized = activeParam.difference
        closeAcumValue = activeParam.closeProfit
        bollingerClose = activeParam.bollingerClose
        currentTime = self.gettime(results)
        actionCount = 0
        if currentTime >= 2100:
            actionCount = 1
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
            if results[Constants.ACUMULADO] < 0 or results[Constants.ACUMULADO] <= 0:
                if results[Constants.ACTION_COUNT] > actionCount:
                    if abs(results[Constants.ACUMULADO]) >= closeAcumValue:
                        self.printFinLog('CLOSE_BUY_MED_SELL_01', name, results, activeParam)
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return
        if results[Constants.ACTION_ACUM] < 0:
            if results[Constants.ACTION_COUNT] > actionCount:
                if abs(results[Constants.ACTION_ACUM]) >= bollingerClose:
                    self.printFinLog('CLOSE_BUY_ACTION_ACUM_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if results[Constants.ACTION_ACUM] < 0:
            if results[Constants.ACTION_COUNT] > actionCount:
                if abs(results[Constants.ACTION_ACUM]) >= closeAcumValue:
                    self.printFinLog('CLOSE_BUY_ACTION_ACUM_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if results[Constants.ACUMULADO] <= 0:
            if results[Constants.ACTION_COUNT] > actionCount:
                if results[Constants.ACTION_MAX_DIST] >= bollingerClose:
                    self.printFinLog('CLOSE_BUY_ACUMULADO_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

    def control_BUY_EMA_04(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_BUY_EMA_04'
        multiplicadorUP = 1
        difference_optimized = activeParam.difference
        closeAcumValue = activeParam.closeProfit
        bollingerClose = activeParam.bollingerClose
        currentTime = self.gettime(results)
        actionCount = 0
        if currentTime >= 2100:
            actionCount = 1
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        isRising, angleDiff = self.isRisingFromWEEK(results)
        if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
            pass
            if not isRising:
                nada = ''
                if abs(angleDiff) >= closeWeekDiffNew / 2:
                    self.printFinLog('CLOSE_BUY_EMA_CHANGE_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if results[Constants.ACTION_ACUM] < 0:
            if results[Constants.ACTION_COUNT] > actionCount:
                if abs(results[Constants.ACTION_ACUM]) >= closeAcumValue:
                    self.printFinLog('CLOSE_BUY_ACTION_ACUM_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

    def control_BUY_EMA_01(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_BUY_EMA_01'
        multiplicadorUP = 1
        difference_optimized = activeParam.difference
        closeAcumValue = activeParam.closeProfit
        bollingerClose = activeParam.bollingerClose
        currentTime = self.gettime(results)
        actionCount = 0
        if currentTime >= 2100:
            actionCount = 1
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
            self.printFinLog('CLOSE_BUY_EMA_CHANGE_01', name, results, activeParam)
            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
            return
        if results[Constants.ACTION_ACUM] < 0:
            if results[Constants.ACTION_COUNT] > actionCount:
                if abs(results[Constants.ACTION_ACUM]) >= closeAcumValue:
                    self.printFinLog('CLOSE_BUY_ACTION_ACUM_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

    def control_BUY_EMA_OUP_02(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_BUY_EMA_OUP_02'
        multiplicadorUP = 1
        difference_optimized = activeParam.difference
        closeAcumValue = activeParam.closeProfit
        bollingerClose = activeParam.bollingerClose
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        currentTime = self.gettime(results)
        actionCount = 0
        if currentTime >= 2100:
            actionCount = 1
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        rising, angleDiff = self.isRisingFromWeekNew(results)
        if not rising:
            if angleDiff > 0:
                if abs(angleDiff) <= closeWeekDiffNew:
                    pass
                    self.printFinLog('CLOSE_BUY_EMA_WEEK_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
            elif abs(angleDiff) >= closeWeekDiffNew / 2:
                pass
                self.printFinLog('CLOSEBUY_EMA_WEEK_02', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.ACTION_ACUM] < 0:
            if results[Constants.ACTION_COUNT] > actionCount:
                if abs(results[Constants.ACTION_ACUM]) >= closeAcumValue:
                    self.printFinLog('CLOSE_BUY_ACTION_ACUM_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

    def control_BUY_EMA_OUP_04(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_BUY_EMA_OUP_04'
        multiplicadorUP = 1
        multiplicatorNXT = 1
        difference_optimized = activeParam.difference
        closeAcumValue = activeParam.closeProfit
        bollingerClose = activeParam.bollingerClose
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        week_new_flow = results[Constants.WEEK_DIR_BOT_DST_MED_NEW_FLOW]
        closeProfit = activeParam.closeProfit
        closeBollingerValue = activeParam.bollingerClose
        currentTime = self.gettime(results)
        actionCount = 0
        if currentTime >= 2100:
            actionCount = 1
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if results[Constants.INDICATOR_MED_MOMENT] == Constants.INDICATOR_TM_UP:
                    multiplicator = multiplicadorUP * multiplicatorNXT
                else:
                    multiplicator = multiplicadorUP
                if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicator or results[Constants.ACTION_MAX_DIST] >= difference_optimized * multiplicator:
                    results[Constants.CLOSE_NXT_DOWN] = 0
                    results[Constants.CLOSE_NXT_UP] = 0
                return
        if results[Constants.ACTION_ACUM] > 0:
            if results[Constants.ACTION_ACUM] >= closeProfit:
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] <= 5:
                    self.printFinLog('CLOSE_BUY_ACTION_ACUM_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
            if results[Constants.ACTION_ACUM] < 0:
                if abs(results[Constants.ACTION_ACUM]) >= closeProfit:
                    self.printFinLog('CLOSE_BUY_BLG_MED_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
            if results[Constants.ACTION_ACUM] < 0:
                if abs(results[Constants.ACUMULADO]) >= closeDifference:
                    self.printFinLog('CLOSE_BUY_BLG_MED_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
            elif results[Constants.ACUMULADO] <= 0:
                if abs(results[Constants.ACUMULADO]) >= closeBollingerValue:
                    self.printFinLog('CLOSE_BUY_ACUM_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if results[Constants.ACTION_ACUM] < 0:
            if results[Constants.ACUMULADO] >= closeBollingerValue:
                self.printFinLog('CLOSE_BUY_ACUM_02', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.ACTION_ACUM] < 0:
            if abs(results[Constants.ACTION_ACUM]) >= closeBollingerValue:
                self.printFinLog('CLOSE_BUY_ACTION_ACUM_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

    def control_BUY_EMA_OUP_03(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_BUY_EMA_OUP_03'
        multiplicadorUP = 1
        difference_optimized = activeParam.difference
        closeAcumValue = activeParam.closeProfit
        bollingerClose = activeParam.bollingerClose
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        week_new_flow = results[Constants.WEEK_DIR_BOT_DST_MED_NEW_FLOW]
        currentTime = self.gettime(results)
        actionCount = 0
        if currentTime >= 2100:
            actionCount = 1
        if week_new_flow < 0 and abs(week_new_flow) > 1:
            self.printFinLog('CLOSE_BUY_week_new_flow_01', name, results, activeParam)
            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
            return
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        rising, angleDiff = self.isRisingFromWeekNew(results)
        if not rising:
            if angleDiff > 0:
                if abs(angleDiff) <= closeWeekDiffNew:
                    self.printFinLog('CLOSE_BUY_EMA_WEEK_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
            elif abs(angleDiff) >= closeWeekDiffNew / 2:
                self.printFinLog('CLOSEBUY_EMA_WEEK_02', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.ACTION_ACUM] < 0:
            if results[Constants.ACTION_COUNT] > actionCount:
                if abs(results[Constants.ACTION_ACUM]) >= closeAcumValue:
                    self.printFinLog('CLOSE_BUY_ACTION_ACUM_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

    def control_BUY_EMA_OUP_01(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_BUY_EMA_OUP_01'
        multiplicadorUP = 1
        difference_optimized = activeParam.difference
        closeAcumValue = activeParam.closeProfit
        bollingerClose = activeParam.bollingerClose
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        currentTime = self.gettime(results)
        actionCount = 0
        if currentTime >= 2100:
            actionCount = 1
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        rising, angleDiff = self.isRisingFromWeek(results)
        if not rising:
            if angleDiff > 0:
                if abs(angleDiff) <= closeWeekDiffNew:
                    pass
                    self.printFinLog('CLOSE_BUY_EMA_WEEK_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
            elif abs(angleDiff) >= closeWeekDiffNew / 2:
                pass
                self.printFinLog('CLOSEBUY_EMA_WEEK_02', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.ACTION_ACUM] < 0:
            if results[Constants.ACTION_COUNT] > actionCount:
                if abs(results[Constants.ACTION_ACUM]) >= closeAcumValue:
                    self.printFinLog('CLOSE_BUY_ACTION_ACUM_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

    def control_BUY_WEEK_01(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_BUY_WEEK_01'
        multiplicadorUP = 1
        difference_optimized = activeParam.difference
        closeAcumValue = activeParam.closeProfit
        bollingerClose = activeParam.bollingerClose
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        currentTime = self.gettime(results)
        actionCount = 0
        if currentTime >= 2100:
            actionCount = 1
        if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
            self.printFinLog('CLOSE_BUY_EMA_CHANGE_01', name, results, activeParam)
            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
            return
        rising, angleDiff = self.isRisingFromWeek(results)
        if not rising:
            if angleDiff > 0:
                if abs(angleDiff) <= closeWeekDiffNew:
                    pass
                    self.printFinLog('CLOSE_BUY_EMA_WEEK_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
            elif abs(angleDiff) >= closeWeekDiffNew / 2:
                pass
                self.printFinLog('CLOSEBUY_EMA_WEEK_02', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

    def control_BUY_WEEK_02(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_BUY_WEEK_02'
        multiplicadorUP = 1
        difference_optimized = activeParam.difference
        closeAcumValue = activeParam.closeProfit
        bollingerClose = activeParam.bollingerClose
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        currentTime = self.gettime(results)
        actionCount = 0
        if currentTime >= 2100:
            actionCount = 1
        if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
            self.printFinLog('CLOSE_BUY_EMA_CHANGE_01', name, results, activeParam)
            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
            return
        rising, angleDiff = self.isRisingFromWeek(results)
        if not rising:
            if angleDiff > 0:
                if abs(angleDiff) <= closeWeekDiffNew:
                    pass
                    self.printFinLog('CLOSE_BUY_EMA_WEEK_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

    def control_BUY_WEEK_03(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_BUY_WEEK_03'
        multiplicadorUP = 1
        difference_optimized = activeParam.difference
        closeAcumValue = activeParam.closeProfit
        bollingerClose = activeParam.bollingerClose
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        currentTime = self.gettime(results)
        actionCount = 0
        if currentTime >= 2100:
            actionCount = 1
        rising, angleDiff = self.isRisingFromWeek(results)
        if not rising:
            if angleDiff > 0:
                if abs(angleDiff) <= closeWeekDiffNew:
                    pass
                    self.printFinLog('CLOSE_BUY_EMA_WEEK_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
            elif abs(angleDiff) >= closeWeekDiffNew / 2:
                pass
                self.printFinLog('CLOSEBUY_EMA_WEEK_02', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

    def control_BUY_WEEK_04(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_BUY_WEEK_03'
        multiplicadorUP = 1
        difference_optimized = activeParam.difference
        closeAcumValue = activeParam.closeProfit
        bollingerClose = activeParam.bollingerClose
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        currentTime = self.gettime(results)
        actionCount = 0
        if currentTime >= 2100:
            actionCount = 1
        rising, angleDiff = self.isRisingFromMonth(results)
        if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
            if not rising:
                if angleDiff < 0:
                    if abs(angleDiff) > closeWeekDiffNew:
                        if results[Constants.ACUMULADO] < 0:
                            self.printFinLog('CLOSE_BUY_EMA_CHANGE_01', name, results, activeParam)
                            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                            return
        if not rising:
            if angleDiff > 0:
                if abs(angleDiff) <= closeWeekDiffNew:
                    pass
                    self.printFinLog('CLOSE_BUY_EMA_WEEK_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
            elif abs(angleDiff) >= closeWeekDiffNew:
                pass
                self.printFinLog('CLOSEBUY_EMA_WEEK_02', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

    def updateCLoseForBuy(self, result, activeParam, closeWeekDiffNew):
        res = closeWeekDiffNew
        indicatorEma = result[Constants.INDICATOR_EMA]
        blgLowDst = result[Constants.IND_BLG_LOWER_DST_PERCENT]
        rising, angleDiff = self.isRisingFromWeekNew(result)
        if Constants.INDICATOR_EMA_BUY == indicatorEma:
            if blgLowDst >= 90:
                res = closeWeekDiffNew / 2
            else:
                res = closeWeekDiffNew
        elif Constants.INDICATOR_EMA_SELL == indicatorEma:
            if blgLowDst < 30:
                res = closeWeekDiffNew
            else:
                res = closeWeekDiffNew / 2
        return res

    def updateCLoseForBuy2(self, result, activeParam, closeWeekDiffNew):
        res = closeWeekDiffNew
        indicatorEma = result[Constants.INDICATOR_EMA]
        blgLowDst = result[Constants.IND_BLG_LOWER_DST_PERCENT]
        ima1emadiff = float(result[Constants.IMA1EMADIFF])
        rising, angleDiff = self.isRisingFromWeekNew(result)
        if rising:
            res = closeWeekDiffNew * 1.2
        elif ima1emadiff >= 0:
            res = closeWeekDiffNew
        else:
            res = closeWeekDiffNew / 2
        return res

    def control_BUY_WEEK_NEW_DIFF_03(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_BUY_WEEK_NEW_DIFF_03'
        multiplicadorUP = 1
        difference_optimized = activeParam.difference
        closeAcumValue = activeParam.closeProfit
        bollingerClose = activeParam.bollingerClose
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        closeAcumValue = activeParam.closeProfit
        closeWeekDiffNew = self.updateCLoseForBuy2(results, activeParam, closeWeekDiffNew)
        currentTime = self.gettime(results)
        actionCount = 0
        if currentTime >= 2100:
            actionCount = 1
        rising, angleDiff = self.isRisingFromWeekNew(results)
        if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
            if not rising:
                if angleDiff < 0:
                    if results[Constants.ACTION_COUNT] > actionCount:
                        if abs(angleDiff) > closeWeekDiffNew:
                            if results[Constants.ACUMULADO] < 0:
                                self.printFinLog('CLOSE_BUY_EMA_CHANGE_01', name, results, activeParam)
                                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                                return
                        if abs(results[Constants.ACUMULADO]) >= closeAcumValue:
                            self.printFinLog('CLOSE_BUY_MAX_ACUM_01', name, results, activeParam)
                            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                            return
        if results[Constants.ACTION_ACUM] > 0:
            if results[Constants.ACTION_ACUM] >= closeAcumValue:
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] <= 5:
                    self.printFinLog('CLOSE_BUY_ACTION_ACUM_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if not rising:
            if angleDiff > 0:
                if abs(angleDiff) <= closeWeekDiffNew:
                    pass
                    self.printFinLog('CLOSE_BUY_EMA_WEEK_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
            else:
                if abs(angleDiff) >= closeWeekDiffNew:
                    pass
                    self.printFinLog('CLOSEBUY_EMA_WEEK_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
                if abs(results[Constants.ACUMULADO]) >= closeAcumValue:
                    self.printFinLog('CLOSE_BUY_MAX_ACUM_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

    def control_BUY_WEEK_NEW_DIFF_01(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_BUY_WEEK_NEW_DIFF_01'
        multiplicadorUP = 1
        difference_optimized = activeParam.difference
        closeAcumValue = activeParam.closeProfit
        bollingerClose = activeParam.bollingerClose
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        closeWeekDiffNew = self.updateCLoseForBuy2(results, activeParam, closeWeekDiffNew)
        currentTime = self.gettime(results)
        actionCount = 0
        if currentTime >= 2100:
            actionCount = 1
        rising, angleDiff = self.isRisingFromWeekNew(results)
        if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
            if not rising:
                if angleDiff < 0:
                    if results[Constants.ACTION_COUNT] > actionCount:
                        if abs(angleDiff) > closeWeekDiffNew:
                            if results[Constants.ACUMULADO] < 0:
                                self.printFinLog('CLOSE_BUY_EMA_CHANGE_01', name, results, activeParam)
                                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                                return
                        if abs(results[Constants.ACUMULADO]) >= closeAcumValue:
                            self.printFinLog('CLOSE_BUY_MAX_ACUM_01', name, results, activeParam)
                            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                            return
        if not rising:
            if angleDiff > 0:
                if abs(angleDiff) <= closeWeekDiffNew:
                    pass
                    self.printFinLog('CLOSE_BUY_EMA_WEEK_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
            else:
                if abs(angleDiff) >= closeWeekDiffNew:
                    pass
                    self.printFinLog('CLOSEBUY_EMA_WEEK_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
                if abs(results[Constants.ACUMULADO]) >= closeAcumValue:
                    self.printFinLog('CLOSE_BUY_MAX_ACUM_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

    def control_BUY_WEEK_NEW_DIFF_02(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_BUY_WEEK_NEW_DIFF_02'
        multiplicadorUP = 1
        difference_optimized = activeParam.difference
        closeAcumValue = activeParam.closeProfit
        bollingerClose = activeParam.bollingerClose
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        closeWeekDiffNew = self.updateCLoseForBuy2(results, activeParam, closeWeekDiffNew)
        currentTime = self.gettime(results)
        actionCount = 0
        if currentTime >= 2100:
            actionCount = 1
        rising, angleDiff = self.isRisingFromWeekNew(results)
        if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
            if not rising:
                if angleDiff < 0:
                    if results[Constants.ACTION_COUNT] > actionCount:
                        if abs(angleDiff) > closeWeekDiffNew:
                            if results[Constants.ACUMULADO] < 0:
                                self.printFinLog('CLOSE_BUY_EMA_CHANGE_01', name, results, activeParam)
                                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                                return
                        if abs(results[Constants.ACUMULADO]) >= closeAcumValue:
                            self.printFinLog('CLOSE_BUY_MAX_ACUM_01', name, results, activeParam)
                            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                            return
        if not rising:
            if angleDiff > 0:
                if abs(angleDiff) <= closeWeekDiffNew:
                    pass
                    self.printFinLog('CLOSE_BUY_EMA_WEEK_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
            elif results[Constants.ACUMULADO] < 0:
                if abs(angleDiff) >= closeWeekDiffNew:
                    pass
                    self.printFinLog('CLOSEBUY_EMA_WEEK_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
                if abs(results[Constants.ACUMULADO]) >= closeAcumValue:
                    self.printFinLog('CLOSE_BUY_MAX_ACUM_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

    def control_BUY_RSI_01(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_BUY_RSI_01'
        multiplicadorUP = 1
        difference_optimized = activeParam.difference
        closeAcumValue = activeParam.closeProfit
        bollingerClose = activeParam.bollingerClose
        max_loss = 0.006 * float(results[Constants.VALUE])
        currentTime = self.gettime(results)
        actionCount = 0
        if currentTime >= 2100:
            actionCount = 1
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if results[Constants.ACTION_ACUM] < 0:
            if abs(results[Constants.ACTION_ACUM]) >= max_loss:
                self.printFinLog('CLOSE_BUY_ACTION_ACUM_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if (results[Constants.RSI] > 60 and results[Constants.RSI] < 70) and results[Constants.RSI_DIFF] < 0:
            if results[Constants.ACTION_COUNT] > 1 and abs(results[Constants.RSI_DIFF]) >= 2:
                self.printFinLog('CLOSE_BUY_ACTION_RSI_DIFF_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if (results[Constants.RSI] > 40 and results[Constants.RSI] < 50) and results[Constants.RSI_DIFF] < 0:
            if results[Constants.ACTION_COUNT] > 1 and abs(results[Constants.RSI_DIFF]) >= 2:
                self.printFinLog('CLOSE_BUY_ACTION_RSI_DIFF_02', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

    def control_BUY_EMA_02(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_BUY_EMA_02'
        multiplicadorUP = 1
        difference_optimized = activeParam.difference
        closeAcumValue = activeParam.closeProfit
        bollingerClose = activeParam.bollingerClose
        currentTime = self.gettime(results)
        actionCount = 0
        if currentTime >= 2100:
            actionCount = 1
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
            self.printFinLog('CLOSE_BUY_EMA_CHANGE_01', name, results, activeParam)
            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
            return

    def control_BUY_EMA_03(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_BUY_EMA_03'
        multiplicadorUP = 1
        difference_optimized = activeParam.difference
        closeAcumValue = activeParam.closeProfit
        bollingerClose = activeParam.bollingerClose
        minmaxClose = closeAcumValue * 2.5
        currentTime = self.gettime(results)
        actionCount = 0
        if currentTime >= 2100:
            actionCount = 1
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
            if results[Constants.ACTION_MAX_DIST] >= minmaxClose:
                self.printFinLog('CLOSE_BUY_EMA_CHANGE_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.ACTION_MAX_DIST] >= minmaxClose:
            self.printFinLog('CLOSE_SELL_ACTION_MAX_DIST_01', name, results, activeParam)
            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
            return

    def control_BUY_START_CLOSE_01(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_BUY_START_CLOSE_01'
        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] = 0
                self.printFinLog('CLOSE_BUY_NXT_MIDDLE_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
            if results[Constants.ACTION_COUNT] > 5:
                if results[Constants.ACTION_ACUM] < 0:
                    self.printFinLog('CLOSE_BUY_MED_SELL_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
                elif abs(results[Constants.ACTION_MAX_DIST]) >= closeAcumValue:
                    self.printFinLog('CLOSE_BUY_MED_SELL_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if results[Constants.ACUMULADO] < 0:
            if results[Constants.ACTION_ACUM] > 0:
                if results[Constants.ACTION_ACUM] > closeAcumValue:
                    if abs(results[Constants.ACTION_MAX_DIST]) >= closeAcumValue:
                        self.printFinLog('CLOSE_BUY_ACT_ACUM_01', name, results, activeParam)
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return
        if results[Constants.ACTION_ACUM] <= 0:
            if results[Constants.ACTION_COUNT] > 3:
                if abs(results[Constants.ACTION_ACUM]) >= closeDifference:
                    self.printFinLog('CLOSE_BUY_ACT_ACUM_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if abs(results[Constants.IND_BLG_UPPER_DST_PERCENT]) > 0 and abs(results[Constants.IND_BLG_UPPER_DST_PERCENT]) < 2:
            if results[Constants.ACTION_COUNT] > 3:
                self.printFinLog('CLOSE_BUY_UPPER_DST_PERCENT_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

    def control_BUY_START_CLOSE_03(self, results, activeParam, closeAcumValue, closeDifference):
        angleDown = activeParam.angleDown
        name = 'control_BUY_START_CLOSE_03'
        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] = 0
                pass
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
            if results[Constants.ACTION_COUNT] > 6:
                if results[Constants.ACTION_ACUM] < 0:
                    pass
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
                elif abs(results[Constants.ACTION_MAX_DIST]) >= closeDifference:
                    pass
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if results[Constants.ACUMULADO] < 0:
            if results[Constants.ACTION_ACUM] > 0:
                if results[Constants.ACTION_ACUM] > closeAcumValue:
                    if abs(results[Constants.ACTION_MAX_DIST]) >= closeAcumValue:
                        pass
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return
        if results[Constants.ACTION_ACUM] <= 0:
            if results[Constants.ACTION_COUNT] >= 3:
                if abs(results[Constants.ACTION_ACUM]) >= closeDifference:
                    pass
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
            elif results[Constants.ANGLE] < 0:
                if results[Constants.ACTION_COUNT] >= 2:
                    if results[Constants.ANGLE] < angleDown:
                        if abs(results[Constants.ACTION_ACUM]) >= closeDifference:
                            pass
                            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                            return
        if abs(results[Constants.IND_BLG_UPPER_DST_PERCENT]) > 0 and abs(results[Constants.IND_BLG_UPPER_DST_PERCENT]) < 2:
            if results[Constants.ACTION_COUNT] > 3:
                pass
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

    def control_BUY_START_CLOSE_04(self, results, activeParam, closeAcumValue, closeDifference):
        angleDown = activeParam.angleDown
        name = 'control_BUY_START_CLOSE_04'
        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] = 0
                self.printFinLog('CLOSE_NXT_BLG_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
            if results[Constants.ACTION_COUNT] > 5:
                if results[Constants.ACTION_ACUM] < 0:
                    self.printFinLog('CLOSE_IND_BLG_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
                elif abs(results[Constants.ACTION_MAX_DIST]) >= closeAcumValue:
                    self.printFinLog('CLOSE_IND_BLG_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if results[Constants.ACUMULADO] < 0:
            if results[Constants.ACTION_ACUM] > 0:
                if results[Constants.ACTION_ACUM] > closeAcumValue:
                    if abs(results[Constants.ACTION_MAX_DIST]) >= closeAcumValue:
                        self.printFinLog('CLOSE_ACUMULADO_01', name, results, activeParam)
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return

    def control_BUY_START_CLOSE_05(self, results, activeParam, closeAcumValue, closeDifference, accumulate):
        angleDown = activeParam.angleDown
        name = 'control_BUY_START_CLOSE_04'
        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] = 0
                self.printFinLog('CLOSE_NXT_BLG_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
            if results[Constants.ACTION_COUNT] > 5:
                if results[Constants.ACTION_ACUM] < 0:
                    self.printFinLog('CLOSE_IND_BLG_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
                elif abs(results[Constants.ACTION_MAX_DIST]) >= closeAcumValue:
                    self.printFinLog('CLOSE_IND_BLG_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if results[Constants.ACUMULADO] < 0:
            if results[Constants.ACTION_ACUM] > 0:
                if results[Constants.ACTION_ACUM] > closeAcumValue:
                    if abs(results[Constants.ACTION_MAX_DIST]) >= closeAcumValue:
                        self.printFinLog('CLOSE_ACUMULADO_01', name, results, activeParam)
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return
        if results[Constants.ACTION_ACUM] <= 0:
            if results[Constants.ACTION_COUNT] > 2:
                if abs(results[Constants.ACTION_ACUM]) >= closeDifference:
                    self.printFinLog('CLOSE_ACUMULADO_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

    def control_BUY_BLG_MID_01(self, results, activeParam, closeAcumValue, closeDifference, accumulate):
        angleDown = activeParam.angleDown
        name = 'control_BUY_BLG_MID_01'
        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] = 0
                pass
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
            if results[Constants.ACTION_COUNT] > 2:
                pass
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
            if results[Constants.ACTION_COUNT] > 3:
                if results[Constants.ACTION_ACUM] < 0:
                    pass
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
                elif abs(results[Constants.ACTION_MAX_DIST]) >= closeDifference:
                    pass
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if results[Constants.ACUMULADO] < 0:
            if results[Constants.ACTION_ACUM] > 0:
                if results[Constants.ACTION_COUNT] >= 3:
                    if results[Constants.ACUMULADO_ABS] > accumulate:
                        if abs(results[Constants.ACTION_MAX_DIST]) >= accumulate:
                            pass
                            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                            return
            else:
                nada = ''

    def control_BUY_BLG_MID_03(self, results, activeParam, closeAcumValue, closeDifference, accumulate):
        angleDown = activeParam.angleDown
        name = 'control_BUY_BLG_MID_01'
        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] = 0
                self.printFinLog('CLOSE_NXT_MID_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
            if results[Constants.ACTION_COUNT] > 2:
                self.printFinLog('CLOSE_BLG_MID_PERCENT_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
            if results[Constants.ACTION_COUNT] > 3:
                if results[Constants.ACTION_ACUM] < 0:
                    self.printFinLog('CLOSE_BLG_SELL_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
                elif abs(results[Constants.ACTION_MAX_DIST]) >= closeDifference:
                    self.printFinLog('CLOSE_BLG_SELL_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if results[Constants.ACUMULADO] < 0:
            if results[Constants.ACTION_ACUM] > 0:
                if results[Constants.ACTION_COUNT] >= 3:
                    if results[Constants.ACUMULADO_ABS] > accumulate:
                        if abs(results[Constants.ACTION_MAX_DIST]) >= accumulate:
                            self.printFinLog('CLOSE_ACUM_01', name, results, activeParam)
                            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                            return
            else:
                nada = ''
                if results[Constants.ACTION_COUNT] >= 1:
                    if results[Constants.ANGLE_IMA1] < 0:
                        if results[Constants.ANGLE_IMA1_COUNTER] >= 2:
                            if abs(results[Constants.ACTION_MAX_DIST]) >= accumulate:
                                self.printFinLog('CLOSE_ACUM_02', name, results, activeParam)
                                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                                return

    def control_BUY_BLG_MID_04(self, results, activeParam, closeAcumValue, closeDifference, accumulate):
        angleDown = activeParam.angleDown
        name = 'control_BUY_BLG_MID_01'
        angle = float(results[Constants.ANGLE])
        anglePrev = float(results[Constants.ANGLE_PREV])
        angleDiff = angle - anglePrev
        closeAngleDiff = int(activeParam.closeAngleDiff) * -1
        difference_optimized = activeParam.difference
        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] = 0
                self.printFinLog('CLOSE_NXT_MID_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
            if results[Constants.ACTION_COUNT] > 2:
                self.printFinLog('CLOSE_BLG_MID_PERCENT_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
            if results[Constants.ACTION_COUNT] >= 3:
                if results[Constants.ACTION_ACUM] < 0:
                    self.printFinLog('CLOSE_BLG_SELL_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
                elif abs(results[Constants.ACTION_MAX_DIST]) >= closeDifference:
                    self.printFinLog('CLOSE_BLG_SELL_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if anglePrev > angle and angleDiff < closeAngleDiff:
            if results[Constants.ACTION_COUNT] > 3:
                if float(results[Constants.IMA1EMADIFF]) > 0:
                    self.printFinLog('CLOSE_ANGLE_IMA_EMA_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if results[Constants.ACUMULADO] < 0:
            if results[Constants.ACTION_ACUM] > 0:
                if results[Constants.ACTION_COUNT] >= 3:
                    if results[Constants.ACUMULADO_ABS] > accumulate:
                        if abs(results[Constants.ACTION_MAX_DIST]) >= accumulate:
                            self.printFinLog('CLOSE_ACUM_01', name, results, activeParam)
                            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                            return
            else:
                nada = ''
                if results[Constants.ACTION_COUNT] >= 1:
                    if results[Constants.ANGLE_IMA1] < 0:
                        if results[Constants.ANGLE_IMA1_COUNTER] >= 2:
                            if abs(results[Constants.ACTION_MAX_DIST]) >= accumulate:
                                self.printFinLog('CLOSE_ACUM_02', name, results, activeParam)
                                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                                return

    def control_BUY_BLG_LONG_01(self, results, activeParam, closeAcumValue, closeDifference, accumulate):
        angleDown = activeParam.angleDown
        name = 'control_BUY_BLG_LONG_01'
        angle = float(results[Constants.ANGLE])
        anglePrev = float(results[Constants.ANGLE_PREV])
        angleDiff = angle - anglePrev
        closeAngleDiff = int(activeParam.closeAngleDiff) * -1
        difference_optimized = activeParam.difference
        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] = 0
                self.printFinLog('CLOSE_NXT_MID_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
            if results[Constants.ACTION_COUNT] > 2:
                self.printFinLog('CLOSE_BLG_MID_PERCENT_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
            if results[Constants.ACTION_COUNT] >= 3:
                if results[Constants.ACTION_ACUM] < 0:
                    self.printFinLog('CLOSE_BLG_SELL_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
                elif abs(results[Constants.ACTION_MAX_DIST]) >= closeDifference:
                    self.printFinLog('CLOSE_BLG_SELL_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

    def control_BUY_IMA1_01(self, results, activeParam, closeAcumValue, closeDifference, accumulate):
        name = 'control_BUY_IMA1_01'
        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] = 0
                self.printFinLog('CLOSE_BUY_NXT_MIDDLE_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        angleDown = activeParam.angleDown
        name = 'control_BUY_IMA1_01'
        angle = float(results[Constants.ANGLE])
        anglePrev = float(results[Constants.ANGLE_PREV])
        angleDiff = angle - anglePrev
        closeAngleDiff = int(activeParam.closeAngleDiff)
        difference_optimized = activeParam.difference
        closeAcumValue = activeParam.closeAcumvalue
        if closeAcumValue > activeParam.accumulate:
            closeAcumValue = activeParam.difference + activeParam.difference * 0.2
        if results[Constants.ACTION_ACUM] < 0:
            if abs(results[Constants.ACTION_ACUM]) >= closeAcumValue:
                self.printFinLog('CLOSE_BUY_ACTION_ACUM_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.ACUMULADO] <= 0:
            if results[Constants.ACUMULADO_ABS] >= closeAcumValue:
                self.printFinLog('CLOSE_BUY_ACUMULADO_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.ACTION_ACUM] > 0:
            if results[Constants.ACTION_ACUM] >= closeAcumValue * 2:
                if results[Constants.ACUMULADO] <= 0:
                    if results[Constants.ACUMULADO_ABS] >= closeAcumValue / 2:
                        self.printFinLog('CLOSE_BUY_ACTION_ACUM2_01', name, results, activeParam)
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return

    def control_BUY_IMA_02(self, results, activeParam, closeAcumValue, closeDifference, accumulate):
        angleDown = activeParam.angleDown
        name = 'control_BUY_BLG_LONG_02'
        angle = float(results[Constants.ANGLE])
        anglePrev = float(results[Constants.ANGLE_PREV])
        angleDiff = angle - anglePrev
        closeAngleDiff = int(activeParam.closeAngleDiff)
        if results[Constants.ACTION_ACUM] < 0:
            if abs(results[Constants.ACTION_ACUM]) >= closeAcumValue:
                self.printFinLog('CLOSE_ACTION_ACUM_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.ACUMULADO] <= 0:
            if results[Constants.ACUMULADO_ABS] >= closeAcumValue:
                self.printFinLog('CLOSE_ACUM_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.ACTION_ACUM] > 0:
            if results[Constants.ACTION_ACUM] >= closeAcumValue * 2:
                if results[Constants.ACUMULADO] <= 0:
                    if results[Constants.ACUMULADO_ABS] >= closeAcumValue / 2:
                        self.printFinLog('CLOSE_ACTION_ACUM_02', name, results, activeParam)
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return

    def control_BUY_BLG_LONG_02(self, results, activeParam, closeAcumValue, closeDifference, accumulate):
        angleDown = activeParam.angleDown
        name = 'control_BUY_BLG_LONG_02'
        angle = float(results[Constants.ANGLE])
        anglePrev = float(results[Constants.ANGLE_PREV])
        angleDiff = angle - anglePrev
        closeAngleDiff = int(activeParam.closeAngleDiff)
        difference_optimized = activeParam.difference
        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] = 0
                self.printFinLog('CLOSE_NXT_MID_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
            if results[Constants.ACTION_COUNT] > 2:
                self.printFinLog('CLOSE_BUY_BLG_MID_PERCENT_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
            openTimeFromOpen = self.getDifTimeFromOpen(results)
            if results[Constants.ACTION_COUNT] > 2 or openTimeFromOpen < 30:
                if results[Constants.ACTION_ACUM] < 0:
                    if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                        self.printFinLog('CLOSE_BUY_BLG_SELL_01', name, results, activeParam)
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return
                elif abs(results[Constants.ACTION_MAX_DIST]) >= closeDifference:
                    self.printFinLog('CLOSE_BUY_BLG_SELL_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        rising, angleDiff = self.isRisingAngleIma1(results)
        if rising == False and abs(angleDiff) >= closeAngleDiff:
            if results[Constants.ACTION_COUNT] > 3:
                if results[Constants.ACUMULADO] < 0:
                    if results[Constants.ACUMULADO_ABS] >= accumulate:
                        if float(results[Constants.IMA1EMADIFF]) > 0:
                            self.printFinLog('CLOSE_ANGLE_IMA_EMA_01', name, results, activeParam)
                            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                            return

    def control_BUY_BLG_MID_02(self, results, activeParam, closeAcumValue, closeDifference, accumulate):
        angleDown = activeParam.angleDown
        name = 'control_BUY_BLG_MID_02'
        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] = 0
                self.printFinLog('CLOSE_NXT_MID_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
            if results[Constants.ACTION_COUNT] > 2:
                self.printFinLog('CLOSE_BLG_MID_DST_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
            if results[Constants.ACTION_COUNT] >= 2:
                if results[Constants.ACTION_ACUM] < 0:
                    self.printFinLog('CLOSE_BUY_MEDSELL_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
                elif abs(results[Constants.ACTION_MAX_DIST]) >= closeDifference:
                    self.printFinLog('CLOSE_BUY_MEDSELL_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
            elif results[Constants.ACTION_COUNT] >= 1:
                if abs(results[Constants.ACTION_ACUM]) > closeAcumValue:
                    self.printFinLog('CLOSE_BUY_MEDSELL_03', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if results[Constants.ACUMULADO] < 0:
            if results[Constants.ACTION_ACUM] > 0:
                if results[Constants.ACTION_COUNT] >= 3:
                    if results[Constants.ACUMULADO_ABS] > closeAcumValue:
                        self.printFinLog('CLOSE_BUY_ACUM_01', name, results, activeParam)
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return

    def nextUpControl_01(self, results, activeParam):
        res = False
        if results[Constants.ANGLE_FLOW] == Constants.DIR_DOWN:
            if results[Constants.WEEK_DIR_BOT_DST] <= 10:
                res = True
        if results[Constants.ANGLE_FLOW] == Constants.DIR_UP:
            res = True
        return res

    def control_BUY_LONG_ONLYUP_01(self, results, activeParam, closeAcumValue, closeDifference, accumulate):
        angleDown = activeParam.angleDown
        name = 'control_BUY_LONG_ONLYUP_01'
        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] = 0
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
            if results[Constants.ACTION_COUNT] > 5:
                self.printFinLog('CLOSE_BLG_SELL_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

    def control_BUY_LONG_ONLYUP_02(self, results, activeParam, closeAcumValue, closeDifference, accumulate):
        angleDown = activeParam.angleDown
        name = 'control_BUY_LONG_ONLYUP_02'
        angle = float(results[Constants.ANGLE])
        anglePrev = float(results[Constants.ANGLE_PREV])
        closeAngleDiff = int(activeParam.closeAngleDiff) * -1
        difference_optimized = activeParam.difference
        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] = 0
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        rising, angleDiff = self.isRisingAngle(results)
        if rising == False and angleDiff < closeAngleDiff:
            if results[Constants.ACTION_COUNT] > 3:
                if float(results[Constants.IMA1EMADIFF]) > 0:
                    self.printFinLog('CLOSE_ANGLE_IMA_EMA_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
            if results[Constants.ANGLE_IMA1] < 0:
                if results[Constants.ANGLE_IMA1_COUNTER] >= 2:
                    if results[Constants.ACTION_ACUM] < 0:
                        if abs(results[Constants.ACTION_ACUM]) >= accumulate:
                            self.printFinLog('CLOSE_BLG_SELL_ACUMNEG_03', name, results, activeParam)
                            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                            return
                if results[Constants.ACTION_COUNT] > 5:
                    self.printFinLog('CLOSE_BLG_SELL_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

    def control_BUY_LONG_ONLYUP_05(self, results, activeParam, closeAcumValue, closeDifference, accumulate):
        angleDown = activeParam.angleDown
        name = 'control_BUY_LONG_ONLYUP_05'
        angle = float(results[Constants.ANGLE])
        anglePrev = float(results[Constants.ANGLE_PREV])
        closeAngleDiff = int(activeParam.closeAngleDiff) * -1
        difference_optimized = activeParam.difference
        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] = 0
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if results[Constants.ACTION_ACUM] < 0:
            if abs(results[Constants.ACTION_ACUM]) > closeDifference:
                self.printFinLog('CLOSE_ANGLE_IMA_EMA_03', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        rising, angleDiff = self.isRisingAngle(results)
        if rising == False and angleDiff >= closeAngleDiff:
            if results[Constants.ACTION_ACUM] < 0:
                if abs(results[Constants.ACTION_ACUM]) > closeDifference:
                    self.printFinLog('CLOSE_ANGLE_IMA_EMA_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
            if results[Constants.ACTION_COUNT] > 3:
                if float(results[Constants.IMA1EMADIFF]) < 0:
                    self.printFinLog('CLOSE_ANGLE_IMA_EMA_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
            if results[Constants.ANGLE_IMA1] < 0:
                if results[Constants.ANGLE_IMA1_COUNTER] >= 2:
                    if results[Constants.ACTION_ACUM] < 0:
                        if abs(results[Constants.ACTION_ACUM]) >= accumulate:
                            self.printFinLog('CLOSE_BLG_SELL_ACUMNEG_03', name, results, activeParam)
                            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                            return
                if results[Constants.ACTION_COUNT] > 5:
                    self.printFinLog('CLOSE_BLG_SELL_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

    def control_BUY_LONG_ONLYUP_06(self, results, activeParam, closeAcumValue, closeDifference, accumulate):
        angleDown = activeParam.angleDown
        name = 'control_BUY_LONG_ONLYUP_05'
        angle = float(results[Constants.ANGLE])
        anglePrev = float(results[Constants.ANGLE_PREV])
        closeAngleDiff = int(activeParam.closeAngleDiff)
        difference_optimized = activeParam.difference
        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] = 0
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if results[Constants.ACTION_ACUM] < 0:
            if abs(results[Constants.ACTION_ACUM]) > closeDifference:
                self.printFinLog('CLOSE_ANGLE_IMA_EMA_03', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        rising, angleDiff = self.isRisingAngle(results)
        if rising == False and abs(angleDiff) >= closeAngleDiff:
            if results[Constants.ACTION_ACUM] < 0:
                if abs(results[Constants.ACTION_ACUM]) > closeDifference:
                    self.printFinLog('CLOSE_ANGLE_IMA_EMA_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
            if results[Constants.ACTION_COUNT] > 3:
                if 'DOWN' in results[Constants.ANGLE_FLOW]:
                    if float(results[Constants.IMA1EMADIFF]) > 0:
                        self.printFinLog('CLOSE_ANGLE_IMA_EMA_01', name, results, activeParam)
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
            if results[Constants.ANGLE_IMA1] < 0:
                if results[Constants.ANGLE_IMA1_COUNTER] >= 2:
                    if results[Constants.ACTION_ACUM] < 0:
                        if abs(results[Constants.ACTION_ACUM]) >= accumulate:
                            self.printFinLog('CLOSE_BLG_SELL_ACUMNEG_03', name, results, activeParam)
                            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                            return
                if results[Constants.ACTION_COUNT] > 5:
                    self.printFinLog('CLOSE_BLG_SELL_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

    def control_BUY_LONG_ONLYUP_07(self, results, activeParam, closeAcumValue, closeDifference, accumulate):
        angleDown = activeParam.angleDown
        name = 'control_BUY_LONG_ONLYUP_05'
        angle = float(results[Constants.ANGLE])
        anglePrev = float(results[Constants.ANGLE_PREV])
        closeAngleDiff = int(activeParam.closeAngleDiff)
        difference_optimized = activeParam.difference
        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] = 0
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if results[Constants.ACTION_ACUM] < 0:
            if abs(results[Constants.ACTION_ACUM]) > closeDifference:
                self.printFinLog('CLOSE_ANGLE_IMA_EMA_03', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        rising, angleDiff = self.isRisingAngle(results)
        if rising == False and abs(angleDiff) >= closeAngleDiff:
            if results[Constants.ACTION_ACUM] < 0:
                if abs(results[Constants.ACTION_ACUM]) > closeDifference:
                    self.printFinLog('CLOSE_ANGLE_IMA_EMA_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
            if results[Constants.ACTION_COUNT] > 3:
                if Constants.FLUJO_BAJA in results[Constants.FLUJO]:
                    if float(results[Constants.IMA1EMADIFF]) > 0:
                        self.printFinLog('CLOSE_ANGLE_IMA_EMA_01', name, results, activeParam)
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
            if results[Constants.ANGLE_IMA1] < 0:
                if results[Constants.ANGLE_IMA1_COUNTER] >= 2:
                    if results[Constants.ACTION_ACUM] < 0:
                        if abs(results[Constants.ACTION_ACUM]) >= accumulate:
                            self.printFinLog('CLOSE_BLG_SELL_ACUMNEG_03', name, results, activeParam)
                            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                            return
                if results[Constants.ACTION_COUNT] > 5:
                    self.printFinLog('CLOSE_BLG_SELL_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

    def control_BUY_LONG_ONLYUP_08(self, results, activeParam, closeAcumValue, closeDifference, accumulate):
        angleDown = activeParam.angleDown
        name = 'control_BUY_LONG_ONLYUP_08'
        angle = float(results[Constants.ANGLE])
        anglePrev = float(results[Constants.ANGLE_PREV])
        closeAngleDiff = int(activeParam.closeAngleDiff)
        difference_optimized = activeParam.difference
        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] = 0
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
                if results[Constants.ACUMULADO] < 0:
                    if results[Constants.FLUJO_COUNT] >= 1:
                        if results[Constants.ACUMULADO_ABS] > closeAcumValue:
                            self.printFinLog('CLOSE_ANGLE_IMA_EMA_03', name, results, activeParam)
                            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                            return
        if results[Constants.ACTION_ACUM] < 0:
            if abs(results[Constants.ACTION_ACUM]) > closeDifference:
                self.printFinLog('CLOSE_ANGLE_IMA_EMA_03', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
            if results[Constants.ANGLE_IMA1] < 0:
                if results[Constants.ANGLE_IMA1_COUNTER] >= 2:
                    if results[Constants.ACTION_ACUM] < 0:
                        if abs(results[Constants.ACTION_ACUM]) >= accumulate:
                            self.printFinLog('CLOSE_BLG_SELL_ACUMNEG_03', name, results, activeParam)
                            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                            return
                if results[Constants.ACTION_COUNT] > 5:
                    self.printFinLog('CLOSE_BLG_SELL_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

    def control_BUY_LONG_ONLYUP_04(self, results, activeParam, closeAcumValue, closeDifference, accumulate):
        angleDown = activeParam.angleDown
        name = 'control_BUY_LONG_ONLYUP_04'
        angle = float(results[Constants.ANGLE])
        anglePrev = float(results[Constants.ANGLE_PREV])
        angleDiff = angle - anglePrev
        closeAngleDiff = int(activeParam.closeAngleDiff) * -1
        difference_optimized = activeParam.difference
        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] = 0
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if anglePrev > angle and angleDiff < closeAngleDiff:
            if results[Constants.ACTION_ACUM] < 0:
                if abs(results[Constants.ACTION_ACUM]) > closeAcumValue:
                    self.printFinLog('CLOSE_ANGLE_IMA_EMA_02', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
            if results[Constants.ACTION_COUNT] >= 2:
                if results[Constants.ACUMULADO] < 0:
                    if results[Constants.ACUMULADO_ABS] > accumulate:
                        if float(results[Constants.IMA1EMADIFF]) > 0:
                            self.printFinLog('CLOSE_ANGLE_IMA_EMA_01', name, results, activeParam)
                            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                            return
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
            if results[Constants.ANGLE_IMA1] < 0:
                if results[Constants.ANGLE_IMA1_COUNTER] >= 2:
                    if results[Constants.ACTION_ACUM] < 0:
                        if abs(results[Constants.ACTION_ACUM]) >= accumulate:
                            self.printFinLog('CLOSE_BLG_SELL_ACUMNEG_03', name, results, activeParam)
                            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                            return
                if results[Constants.ACTION_COUNT] > 5:
                    self.printFinLog('CLOSE_BLG_SELL_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

    def control_BUY_LONG_ONLYUP_03(self, results, activeParam, closeAcumValue, closeDifference, accumulate):
        angleDown = activeParam.angleDown
        name = 'control_BUY_LONG_ONLYUP_03'
        angle = float(results[Constants.ANGLE])
        anglePrev = float(results[Constants.ANGLE_PREV])
        angleDiff = angle - anglePrev
        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] = 0
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if anglePrev > angle and angleDiff < -5:
            if results[Constants.EMA_DST] >= 80:
                if float(results[Constants.ANGLE_IMA1]) > float(results[Constants.ANGLE_EMA]):
                    self.printFinLog('CLOSE_ANGLE_IMA_EMA_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
            if results[Constants.ANGLE_IMA1] < 0:
                if results[Constants.ANGLE_IMA1_COUNTER] >= 2:
                    if results[Constants.ACTION_ACUM] < 0:
                        if abs(results[Constants.ACTION_ACUM]) >= accumulate:
                            self.printFinLog('CLOSE_BLG_SELL_ACUMNEG_03', name, results, activeParam)
                            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                            return
                if results[Constants.ACTION_COUNT] > 5:
                    self.printFinLog('CLOSE_BLG_SELL_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

    def control_SELL_LONG_ONLYUP_01(self, results, activeParam, closeAcumValue, closeDifference, accumulate):
        angleDown = activeParam.angleDown
        name = 'control_SELL_LONG_ONLYUP_01'
        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] = 0
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_BUY:
            if results[Constants.ACTION_COUNT] > 5:
                self.printFinLog('CLOSE_BLG_BUY_01', name, results, activeParam)
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

    def control_SELL_LONG_ONLYUP_02(self, results, activeParam, closeAcumValue, closeDifference, accumulate):
        angleDown = activeParam.angleDown
        name = 'control_SELL_LONG_ONLYUP_02'
        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] = 0
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_BUY:
            if results[Constants.ANGLE] < 0:
                if results[Constants.ACTION_COUNT] > 5:
                    self.printFinLog('CLOSE_BLG_BUY_01', name, results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
                if results[Constants.ANGLE_COUNTER] >= 4:
                    if abs(results[Constants.ANGLE]) < activeParam.maxAngleDown:
                        self.printFinLog('CLOSE_BLG_BUY_02', name, results, activeParam)
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return

    def control_BUY_START_CLOSE_02(self, results, activeParam, closeAcumValue, closeDifference):
        name = 'control_BUY_START_CLOSE_02'
        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] = 0
                pass
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
            if results[Constants.ACTION_COUNT] > 5:
                if results[Constants.ACTION_ACUM] < 0:
                    pass
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
                elif abs(results[Constants.ACTION_MAX_DIST]) >= closeAcumValue:
                    pass
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if results[Constants.ACUMULADO] < 0:
            if results[Constants.ACTION_ACUM] > 0:
                if results[Constants.ACTION_ACUM] > closeAcumValue:
                    if abs(results[Constants.ACTION_MAX_DIST]) >= closeAcumValue:
                        pass
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return
        if results[Constants.ACTION_ACUM] <= 0:
            if results[Constants.ACTION_COUNT] >= 2:
                if abs(results[Constants.ACTION_ACUM]) >= closeDifference:
                    pass
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if abs(results[Constants.IND_BLG_UPPER_DST_PERCENT]) > 0 and abs(results[Constants.IND_BLG_UPPER_DST_PERCENT]) < 2:
            if results[Constants.ACTION_COUNT] > 3:
                pass
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

    def isRisingAngle(self, results):
        res = (False, 0)
        angleDIff = float(results[Constants.ANGLE]) - float(results[Constants.ANGLE_PREV])
        if angleDIff > 0:
            res = (True, angleDIff)
        else:
            res = (False, angleDIff)
        return res

    def isRisingFromWeekNew(self, results):
        res = (False, 0)
        angleDIff = float(results[Constants.WEEK_DIR_BOT_DST_NEW]) - float(results[Constants.WEEK_DIR_BOT_DST_MED_NEW])
        if angleDIff > 0:
            res = (True, angleDIff)
        else:
            res = (False, angleDIff)
        return res

    def isRisingFromWeek(self, results):
        res = (False, 0)
        angleDIff = float(results[Constants.WEEK_DIR_BOT_DST]) - float(results[Constants.WEEK_DIR_BOT_DST_MED])
        if angleDIff > 0:
            res = (True, angleDIff)
        else:
            res = (False, angleDIff)
        return res

    def isRisingFromMonth(self, results):
        res = (False, 0)
        angleDIff = float(results[Constants.MONTH_DIR_BOT_DST]) - float(results[Constants.MONTH_DIR_BOT_DST_MED])
        if angleDIff > 0:
            res = (True, angleDIff)
        else:
            res = (False, angleDIff)
        return res

    def isRisingAngleIma1(self, results):
        res = (False, 0)
        angleDIff = float(results[Constants.ANGLE_IMA1]) - float(results[Constants.ANGLE_IMA1_PREV])
        if angleDIff > 0:
            res = (True, angleDIff)
        else:
            res = (False, angleDIff)
        return res