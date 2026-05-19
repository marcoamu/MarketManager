from service.Constants import Constants
import time
from datetime import datetime

class AperturaBase:

    def __init__(self):
        pass

    def printInicioLog(self, name, results, activeparameters):
        pass
        results[Constants.INICIO_NAME] = name

    def evaluateUpOpen_01(self, results, activeParam):
        res = False
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MIN_DIST] >= difference_optimized:
            if results[Constants.IND_BLG_UPPER_DST_PERCENT] > blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] == 0:
                if results[Constants.WEEK_DIR_BOT_DST] < 90:
                    if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff:
                        res = True
        return res

    def canOpenUP_BLGDistance(self, results, activeParam):
        res = True
        if results[Constants.IND_BLG_LOWER_DST_PERCENT] > 80:
            if results[Constants.WEEK_DIR_BOT_DST] > 40:
                res = False
        return res

    def aperturaAngle(self, results, activeParam):
        angle = results[Constants.ANGLE]
        angleCount = results[Constants.ANGLE_COUNTER]
        res = Constants.DIR_WAIT
        if angle > 0:
            if angleCount >= 2:
                res = Constants.DIR_UP
        elif angle < 0:
            if angleCount >= 2:
                res = Constants.DIR_DOWN
        return res

    def aperturaAngle_01(self, results, activeParam):
        angle = results[Constants.ANGLE]
        angleCount = results[Constants.ANGLE_COUNTER]
        angleIma1 = results[Constants.ANGLE_IMA1]
        angleIma1Count = results[Constants.ANGLE_IMA1_COUNTER]
        res = Constants.DIR_WAIT
        if angle > 0:
            if angleCount >= 2:
                res = Constants.DIR_UP
                if angleIma1 < 0:
                    if angleIma1Count >= 3:
                        res = Constants.DIR_DOWN
        elif angle < 0:
            if angleCount >= 2:
                res = Constants.DIR_DOWN
                if angleIma1 > 0:
                    if angleIma1Count >= 3:
                        res = Constants.DIR_UP
        return res

    def evaluateUpOpen_02(self, results, activeParam):
        res = (False, 0)
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MIN_DIST] >= difference_optimized:
            if results[Constants.IND_BLG_UPPER_DST_PERCENT] > blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] == 0:
                if results[Constants.WEEK_DIR_BOT_DST] < 90:
                    if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] < 10:
                        res = (True, 1)
                elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                    isRising, angleDiff = self.isRisingAngle(results)
                    if isRising:
                        if results[Constants.ANGLE_IMA1] > 0:
                            if results[Constants.IMA1EMADIFF] > 0:
                                if results[Constants.IMA1EMADIFF] > activeParam.ima1EmaMinValue:
                                    res = (True, 2)
        return res

    def evaluateUpOpen_03(self, results, activeParam):
        res = (False, 0)
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MIN_DIST] >= difference_optimized:
            if results[Constants.IND_BLG_UPPER_DST_PERCENT] > blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] == 0:
                if results[Constants.WEEK_DIR_BOT_DST] < 90:
                    if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] < 10:
                        isRising, angleDiff = self.isRisingAngleIma1(results)
                        if isRising:
                            res = (True, 1)
                elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                    isRising, angleDiff = self.isRisingAngle(results)
                    if isRising:
                        if results[Constants.ANGLE_IMA1] > 0:
                            if results[Constants.IMA1EMADIFF] > 0:
                                if results[Constants.IMA1EMADIFF] > activeParam.ima1EmaMinValue:
                                    res = (True, 2)
        return res

    def evaluateUpOpen_09(self, results, activeParam):
        res = (False, 0)
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MIN_DIST] >= difference_optimized:
            if results[Constants.IND_BLG_UPPER_DST_PERCENT] > blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] == 0:
                if results[Constants.WEEK_DIR_BOT_DST] < 90:
                    if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] < 10:
                        res = (True, 1)
                elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                    isRising, angleDiff = self.isRisingAngle(results)
                    if isRising:
                        if results[Constants.ANGLE_IMA1] > 0:
                            if results[Constants.IMA1EMADIFF] > 0:
                                if results[Constants.IMA1EMADIFF] > activeParam.ima1EmaMinValue:
                                    res = (True, 2)
            elif results[Constants.IND_BLG_UPPER_DST_PERCENT] > 0 and results[Constants.IND_BLG_UPPER_DST_PERCENT] < blgDistPercent:
                if results[Constants.WEEK_DIR_BOT_DST] > 90:
                    if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] > 30:
                        if results[Constants.ANGLE] > 0:
                            if results[Constants.ANGLE_COUNTER] > 5:
                                res = (True, 3)
        return res

    def evaluateUpOpen_04(self, results, activeParam):
        res = (False, 0)
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MIN_DIST] >= difference_optimized:
            if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] == 0:
                if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff:
                    if results[Constants.WEEK_DIR_BOT_DST] < 90:
                        if 'UP' in self.aperturaAngle_01(results, activeParam):
                            res = (True, 1)
        return res

    def evaluateUpOpen_05(self, results, activeParam):
        res = (False, 0)
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MIN_DIST] >= difference_optimized:
            if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] == 0:
                if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff:
                    if results[Constants.WEEK_DIR_BOT_DST] < 90:
                        if 'UP' in self.aperturaAngle_01(results, activeParam):
                            res = (True, 1)
                    elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                        isRising, angleDiff = self.isRisingAngle(results)
                        if isRising:
                            if results[Constants.ANGLE_IMA1] > 0:
                                if results[Constants.IMA1EMADIFF] > 0:
                                    if results[Constants.IMA1EMADIFF] > activeParam.ima1EmaMinValue:
                                        res = (True, 2)
            elif results[Constants.IND_BLG_UPPER_DST_PERCENT] > 0 and results[Constants.IND_BLG_UPPER_DST_PERCENT] < blgDistPercent:
                if results[Constants.WEEK_DIR_BOT_DST] > 90:
                    if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] > 30:
                        if results[Constants.ANGLE] > 0:
                            if results[Constants.ANGLE_COUNTER] > 5:
                                res = (True, 3)
        return res

    def evaluateUpOpen_06(self, results, activeParam):
        res = (False, 0)
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MIN_DIST] >= difference_optimized:
            if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] == 0:
                if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff:
                    if results[Constants.WEEK_DIR_BOT_DST] < 90:
                        isRising, angleDiff = self.isRisingAngleIma1(results)
                        if isRising:
                            if 'UP' in self.aperturaAngle_01(results, activeParam):
                                res = (True, 1)
                    elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                        isRising, angleDiff = self.isRisingAngle(results)
                        if isRising:
                            if results[Constants.ANGLE_IMA1] > 0:
                                if results[Constants.IMA1EMADIFF] > 0:
                                    if results[Constants.IMA1EMADIFF] > activeParam.ima1EmaMinValue:
                                        res = (True, 2)
            elif results[Constants.IND_BLG_UPPER_DST_PERCENT] > 0 and results[Constants.IND_BLG_UPPER_DST_PERCENT] < blgDistPercent:
                if results[Constants.WEEK_DIR_BOT_DST] > 90:
                    if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] > 30:
                        if results[Constants.ANGLE] > 0:
                            if results[Constants.ANGLE_COUNTER] > 5:
                                isRising, angleDiff = self.isRisingAngle(results)
                                if isRising:
                                    res = (True, 3)
        return res

    def evaluateUpOpen_07(self, results, activeParam):
        res = (False, 0)
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MIN_DIST] >= difference_optimized:
            if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] == 0:
                if results[Constants.WEEK_DIR_BOT_DST] < 90:
                    isRising, angleDiff = self.isRisingAngleIma1(results)
                    if isRising:
                        res = (True, 1)
                elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                    isRising, angleDiff = self.isRisingAngle(results)
                    if isRising:
                        if results[Constants.ANGLE_IMA1] > 0:
                            if results[Constants.IMA1EMADIFF] > 0:
                                if results[Constants.IMA1EMADIFF] > activeParam.ima1EmaMinValue:
                                    res = (True, 2)
            elif results[Constants.IND_BLG_UPPER_DST_PERCENT] > 0 and results[Constants.IND_BLG_UPPER_DST_PERCENT] < blgDistPercent:
                if results[Constants.WEEK_DIR_BOT_DST] > 90:
                    if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] > 30:
                        if results[Constants.ANGLE] > 0:
                            if results[Constants.ANGLE_COUNTER] > 5:
                                isRising, angleDiff = self.isRisingAngle(results)
                                if isRising:
                                    res = (True, 3)
        return res

    def evaluateUpOpen_08(self, results, activeParam):
        res = (False, 0)
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MIN_DIST] >= difference_optimized:
            if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] == 0:
                if results[Constants.WEEK_DIR_BOT_DST] < 90:
                    isRising, angleDiff = self.isRisingAngleIma1(results)
                    if isRising:
                        if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] < 30:
                            res = (True, 1)
                        elif results[Constants.ANGLE] > angleUp:
                            res = (True, 1)
                elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                    isRising, angleDiff = self.isRisingAngle(results)
                    if isRising:
                        if results[Constants.ANGLE_IMA1] > 0:
                            if results[Constants.IMA1EMADIFF] > 0:
                                if results[Constants.IMA1EMADIFF] > activeParam.ima1EmaMinValue:
                                    res = (True, 2)
            elif results[Constants.IND_BLG_UPPER_DST_PERCENT] > 0 and results[Constants.IND_BLG_UPPER_DST_PERCENT] < blgDistPercent:
                if results[Constants.WEEK_DIR_BOT_DST] > 90:
                    if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] > 30:
                        if results[Constants.ANGLE] > 0:
                            if results[Constants.ANGLE_COUNTER] > 5:
                                isRising, angleDiff = self.isRisingAngle(results)
                                if isRising:
                                    res = (True, 3)
        return res

    def evaluateUpOpen_08_IMP01(self, results, activeParam):
        res = (False, 0)
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MIN_DIST] >= difference_optimized:
            if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] == 0:
                if results[Constants.WEEK_DIR_BOT_DST] < 90:
                    isRising, angleDiff = self.isRisingAngleIma1(results)
                    if isRising:
                        if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] < 30:
                            res = (True, 1)
                        elif results[Constants.ANGLE] > angleUp:
                            res = (True, 1)
                elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                    isRising, angleDiff = self.isRisingAngle(results)
                    if isRising:
                        if results[Constants.ANGLE_IMA1] > 0:
                            if results[Constants.IMA1EMADIFF] > 0:
                                if results[Constants.IMA1EMADIFF] > activeParam.ima1EmaMinValue:
                                    res = (True, 2)
            elif results[Constants.IND_BLG_UPPER_DST_PERCENT] > 0 and results[Constants.IND_BLG_UPPER_DST_PERCENT] < blgDistPercent:
                if results[Constants.WEEK_DIR_BOT_DST] > 90:
                    if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] > 30:
                        if results[Constants.ANGLE] > 0:
                            if results[Constants.ANGLE_COUNTER] > 5:
                                isRising, angleDiff = self.isRisingAngle(results)
                                if isRising:
                                    res = (True, 3)
        return res

    def evaluateChance_Ima1_01(self, results, activeParam):
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        maxAcumValue = activeParam.closeAcumvalue * 3
        res = (False, 'Nada', 0)
        if 'DOWN' in results[Constants.WEEK_FLOW]:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
                    difOpenHours = self.getDifTimeFromOpen(results)
                    if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0:
                        if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                            res = (True, 'SELL', 1)
            elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MIN_DIST] >= difference_optimized:
                    if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0:
                        if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                            res = (True, 'BUY', 1)
        elif 'UP' in results[Constants.WEEK_FLOW]:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MIN_DIST] >= difference_optimized:
                    if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0:
                        if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                            res = (True, 'BUY', 2)
            elif results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized * self.multiplicadorUP or results[Constants.ACTION_MAX_DIST] >= difference_optimized * self.multiplicadorUP:
                    if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0:
                        if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                            res = (True, 'SELL', 2)
        elif results[Constants.FLUJO] == Constants.FLUJO_BAJA:
            if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
                if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0:
                    if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                        res = (True, 'SELL', 3)
        elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
            if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MIN_DIST] >= difference_optimized:
                if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0:
                    if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                        res = (True, 'BUY', 3)
        return res

    def evaluateChance_Ima1_02(self, results, activeParam):
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        maxAcumValue = activeParam.closeAcumvalue * 3
        res = (False, 'Nada', 0)
        if results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_DOWN:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
                    difOpenHours = self.getDifTimeFromOpen(results)
                    if difOpenHours <= 10:
                        res = (True, 'SELL', 1)
                    elif abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0:
                        if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                            res = (True, 'SELL', 2)
            elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MIN_DIST] >= difference_optimized:
                    if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0:
                        if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                            res = (True, 'BUY', 1)
        elif results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_UP:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MIN_DIST] >= difference_optimized:
                    if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0:
                        if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                            res = (True, 'BUY', 2)
            elif results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
                    difOpenHours = self.getDifTimeFromOpen(results)
                    if difOpenHours <= 10:
                        res = (True, 'SELL', 3)
                    elif abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0:
                        if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                            res = (True, 'SELL', 4)
        elif results[Constants.FLUJO] == Constants.FLUJO_BAJA:
            if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
                if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0:
                    if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                        res = (True, 'SELL', 5)
        elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
            if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MIN_DIST] >= difference_optimized:
                if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0:
                    if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                        res = (True, 'BUY', 4)
        return res

    def evaluateDownOpen_start_close_01(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        angleDOWN = activeParam.angleDown
        maxAcumValue = activeParam.closeAcumvalue * 3
        medstdminDiff = activeParam.medstdminDiff
        multiplicadorUP = 2
        emaMinDst = float(activeParam.emaMinDst)
        if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if abs(float(results[Constants.EMA_DST])) >= emaMinDst:
                    if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT] == 0:
                        if results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_DOWN:
                            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                            res = (True, 'SELL', 1)
                        elif results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_UP:
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            res = (True, 'SELL', 2)
                    elif results[Constants.IND_BLG_LOWER_DST_PERCENT] < 0:
                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                        res = (True, 'SELL', 3)
                    elif results[Constants.IND_BLG_LOWER_DST_PERCENT] < blgDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT] == 0:
                        nada = ''
                        if results[Constants.ANGLE] < 0 or results[Constants.ANGLE] == 0:
                            if abs(results[Constants.ANGLE]) > angleDOWN:
                                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                res = (True, 'SELL', 4)
                            elif results[Constants.ANGLEm1] > 0:
                                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                res = (True, 'SELL', 5)
            else:
                nada = ''
        return res

    def evaluateDownOpen_start_close_02(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        angleDOWN = activeParam.angleDown
        maxAcumValue = activeParam.closeAcumvalue * 3
        medstdminDiff = activeParam.medstdminDiff
        multiplicadorUP = 2
        emaMinDst = float(activeParam.emaMinDst)
        multiplicadorOpen = 2.2
        if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if abs(results[Constants.EMA_DST]) >= emaMinDst:
                    if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT] == 0:
                        if results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_DOWN:
                            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                            res = (True, 'SELL', 1)
                    elif results[Constants.IND_BLG_LOWER_DST_PERCENT] < 0:
                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                        res = (True, 'SELL', 2)
                    elif results[Constants.IND_BLG_LOWER_DST_PERCENT] < blgDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT] == 0:
                        nada = ''
                        if results[Constants.ANGLE] < 0 or results[Constants.ANGLE] == 0:
                            if abs(results[Constants.ANGLE]) > angleDOWN:
                                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                res = (True, 'SELL', 3)
                            elif results[Constants.ANGLEm1] > 0:
                                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                res = (True, 'SELL', 4)
            else:
                nada = ''
        return res

    def evaluateUpOpen_start_close_01(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        angleUP = activeParam.angleUp
        maxAcumValue = activeParam.closeAcumvalue * 3
        medstdminDiff = activeParam.medstdminDiff
        multiplicadorUP = 2
        emaMinDst = activeParam.emaMinDst
        if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MIN_DIST] >= difference_optimized * multiplicadorUP:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if abs(float(results[Constants.EMA_DST])) >= emaMinDst:
                    if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] == 0:
                        res = (True, 'BUY', 1)
                    elif results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        res = (True, 'BUY', 2)
                    elif results[Constants.IND_BLG_UPPER_DST_PERCENT] < blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] == 0:
                        nada = ''
                        if results[Constants.ANGLE] > 0 or results[Constants.ANGLE] == 0:
                            if abs(results[Constants.ANGLE]) > angleUP:
                                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                res = (True, 'BUY', 3)
                            elif results[Constants.ANGLEm1] < 0:
                                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                res = (True, 'BUY', 4)
            else:
                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                res = (True, 'SELL', 1)
        return res

    def evaluateUpOpen_start_close_02(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        angleUP = activeParam.angleUp
        maxAcumValue = activeParam.closeAcumvalue * 3
        medstdminDiff = activeParam.medstdminDiff
        multiplicadorUP = 2
        emaMinDst = activeParam.emaMinDst
        if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MIN_DIST] >= difference_optimized * multiplicadorUP:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] == 0:
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                    res = (True, 'BUY', 1)
                elif results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                    res = (True, 'BUY', 2)
                elif results[Constants.IND_BLG_UPPER_DST_PERCENT] < blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] == 0:
                    nada = ''
                    if results[Constants.ANGLE] > 0 or results[Constants.ANGLE] == 0:
                        if abs(results[Constants.ANGLE]) > angleUP:
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            res = (True, 'BUY', 3)
                        elif results[Constants.ANGLEm1] < 0:
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            res = (True, 'BUY', 4)
            else:
                nada = ''
                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                res = (True, 'SELL', 1)
        return res

    def evaluateUpOpen_start_close_03(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        angleUP = activeParam.angleUp
        maxAcumValue = activeParam.closeAcumvalue * 3
        medstdminDiff = activeParam.medstdminDiff
        multiplicadorUP = 2
        emaMinDst = activeParam.emaMinDst
        if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MIN_DIST] >= difference_optimized * multiplicadorUP:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] == 0:
                    if results[Constants.WEEK_DIR_BOT_DST] < 90:
                        isRising, angleDiff = self.isRisingAngleIma1(results)
                        if isRising:
                            if 'UP' in results[Constants.ANGLE_FLOW]:
                                if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] < 5:
                                    res = (True, 'BUY', 1)
                                elif results[Constants.IND_BLG_MIDDLE_DST_PERCENT] < 20:
                                    if results[Constants.ANGLE] > 0:
                                        res = (True, 'BUY', 2)
                                elif angleDiff > angleUP:
                                    if results[Constants.ANGLE] > angleUP:
                                        res = (True, 'BUY', 3)
                    elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                        isRising, angleDiff = self.isRisingAngle(results)
                        if isRising:
                            if results[Constants.ANGLE_IMA1] > 0:
                                if results[Constants.IMA1EMADIFF] > 0:
                                    if results[Constants.IMA1EMADIFF] > activeParam.ima1EmaMinValue:
                                        res = (True, 'BUY', 4)
                elif results[Constants.IND_BLG_UPPER_DST_PERCENT] > 0 and results[Constants.IND_BLG_UPPER_DST_PERCENT] < blgDistPercent:
                    if results[Constants.WEEK_DIR_BOT_DST] > 90:
                        if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] > 30:
                            if results[Constants.ANGLE] > 0:
                                if results[Constants.ANGLE_COUNTER] > 5:
                                    isRising, angleDiff = self.isRisingAngle(results)
                                    if isRising:
                                        res = (True, 'BUY', 5)
            else:
                nada = ''
        return res

    def evaluateDownOpen_BLG_02(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        multiplicadorUP = 2
        if (abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0) and abs(results[Constants.MEDSTDDIFF]) < medstdmaxDiff:
            if results[Constants.IND_BLG] == Constants.IND_BLG_MED_BUY:
                if results[Constants.ACUMULADO] < 0:
                    if results[Constants.MEDSTDDIFF] < 0:
                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                        res = (True, 'SELL', 1)
                elif results[Constants.MEDSTDDIFF] > 0:
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                    res = (True, 'BUY', 1)
            elif results[Constants.IND_BLG_LOWER_DST] < self.blgLowerDist:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized * self.multiplicadorUP or results[Constants.ACTION_MAX_DIST] >= difference_optimized * self.multiplicadorUP:
                    if results[Constants.ACUMULADO] < 0:
                        if results[Constants.MEDSTDDIFF] < 0:
                            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                            res = (True, 'SELL', 2)
                    elif results[Constants.MEDSTDDIFF] > 0:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        res = (True, 'BUY', 2)
            elif results[Constants.ACUMULADO] > 0:
                if results[Constants.MEDSTDDIFF] > 0:
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                    res = (True, 'BUY', 3)
        return res

    def evaluateUpOpen_EMA_WEEK_OUP_01(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        multiplicadorUP = 1
        blgLowerDistPercent = 10
        isRising, angleDiff = self.isRisingFromWEEK(results)
        if isRising:
            if angleDiff > 0 and angleDiff > closeWeekDiffNew / 2:
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgLowerDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MIN_DIST] >= difference_optimized * multiplicadorUP:
                        if results[Constants.ACUMULADO] > 0:
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            res = (True, 'BUY', 1)
        else:
            pass
            if angleDiff < 0 and abs(angleDiff) > closeWeekDiffNew:
                if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgLowerDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT] < 0:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MAX_DIST] >= difference_optimized * multiplicadorUP:
                        if results[Constants.ACUMULADO] < 0:
                            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                            res = (True, 'SELL', 1)
        return res

    def evaluateDownOpen_BLG_03(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        multiplicadorUP = 1
        blgLowerDistPercent = 20
        if results[Constants.ANGLE_FLOW] == Constants.DIR_DOWN:
            if results[Constants.IND_BLG] == Constants.IND_BLG_MED_BUY:
                nada = ''
            elif results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgLowerDistPercent:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MAX_DIST] >= difference_optimized * multiplicadorUP:
                    if results[Constants.ACUMULADO] < 0:
                        if results[Constants.MEDSTDDIFF] < 0:
                            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                            res = (True, 'SELL', 1)
                    else:
                        nada = ''
        return res

    def evaluateDownOpen_EMA_01(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        multiplicadorUP = 1
        blgLowerDistPercent = 5
        if results[Constants.BLG_MA_X] < 0:
            if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgLowerDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT] < 0:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MAX_DIST] >= difference_optimized * multiplicadorUP:
                    if results[Constants.ACUMULADO] < 0:
                        if results[Constants.MEDSTDDIFF] < 0:
                            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                            res = (True, 'SELL', 1)
        return res

    def evaluateDownOpen_EMA_04(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        multiplicadorUP = 1
        blgLowerDistPercent = 5
        angleEma20 = results[Constants.ANGLE_EMA20]
        if angleEma20 < 0:
            if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgLowerDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT] < 0:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MAX_DIST] >= difference_optimized * multiplicadorUP:
                    results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                    res = (True, 'SELL', 1)
        return res

    def evaluateDownOpen_EMA_02(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        multiplicadorUP = 1
        blgLowerDistPercent = 5
        if results[Constants.BLG_MA_X] <= 0:
            if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgLowerDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT] < 0:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MAX_DIST] >= difference_optimized * multiplicadorUP:
                    if results[Constants.ACUMULADO] < 0:
                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                        res = (True, 'SELL', 1)
        return res

    def evaluateDownOpen_RSI_01(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        multiplicadorUP = 1
        blgLowerDistPercent = 5
        isRising = False
        if not isRising:
            if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MAX_DIST] >= difference_optimized * multiplicadorUP:
                if results[Constants.ACUMULADO] < 0:
                    results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                    res = (True, 'SELL', 1)
        return res

    def evaluateDownOpen_EMA_03(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        multiplicadorUP = 1
        blgLowerDistPercent = 5
        isRising, angleDiff = self.isRisingAngle(results)
        isRisingIma1, angleDiffIm1 = self.isRisingAngleIma1(results)
        if not isRising:
            if not isRisingIma1:
                if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgLowerDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT] < 0:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MAX_DIST] >= difference_optimized * multiplicadorUP:
                        if results[Constants.ACUMULADO] < 0:
                            if results[Constants.ACTION_MIN_DIST] < results[Constants.ACTION_MAX_DIST]:
                                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                res = (True, 'SELL', 1)
            else:
                nada = ''
                if results[Constants.ACTION_MAX_DIST] < results[Constants.ACTION_MIN_DIST]:
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                    res = (True, 'BUY', 1)
        return res

    def evaluateDownOpen_EMA_WEEK_01(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        blg_mid_dst_perc = results[Constants.IND_BLG_MIDDLE_DST_PERCENT]
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        multiplicadorUP = 1
        blgLowerDistPercent = 5
        isRising, angleDiff = self.isRisingFromMonth(results)
        if not isRising:
            pass
            if angleDiff < 0 and abs(angleDiff) > closeWeekDiffNew / 2:
                if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgLowerDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT] < 0:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MAX_DIST] >= difference_optimized * multiplicadorUP:
                        if results[Constants.ACUMULADO] < 0:
                            res = (True, 'SELL', 1)
        else:
            pass
            if angleDiff > 0 and abs(angleDiff) > closeWeekDiffNew:
                if blg_mid_dst_perc < 0 or (blg_mid_dst_perc > 0 and blg_mid_dst_perc < 10):
                    if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgLowerDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT] < 0:
                        if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MIN_DIST] >= difference_optimized * multiplicadorUP:
                            if results[Constants.ACUMULADO] > 0:
                                res = (True, 'BUY', 1)
        return res

    def evaluateDownOpen_EMA_WEEK_02(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        blg_mid_dst_perc = results[Constants.IND_BLG_MIDDLE_DST_PERCENT]
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        multiplicadorUP = 1
        blgLowerDistPercent = -10
        blgLowerInvMaxDistPercent = 40
        ima5ma20 = results[Constants.IMA5MA20]
        isRising, angleDiff = self.isRisingFromMonth(results)
        if not isRising:
            pass
            if angleDiff < 0 and abs(angleDiff) > closeWeekDiffNew / 2:
                if ima5ma20 == Constants.INDICATOR_EMA_SELL:
                    if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgLowerDistPercent and results[Constants.IND_BLG_LOWER_DST_PERCENT] > 0:
                        if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MAX_DIST] >= difference_optimized * multiplicadorUP:
                            if results[Constants.ACUMULADO] < 0:
                                res = (True, 'SELL', 1)
        else:
            pass
            if angleDiff > 0 and abs(angleDiff) > closeWeekDiffNew:
                if results[Constants.IND_BLG_LOWER_DST_PERCENT] < blgLowerInvMaxDistPercent or ima5ma20 == Constants.INDICATOR_EMA_BUY:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MIN_DIST] >= difference_optimized * multiplicadorUP:
                        if results[Constants.ACUMULADO] > 0:
                            res = (True, 'BUY', 1)
        return res

    def evaluateDownOpen_EMA_WEEK_NEW_FLOW_01(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        blg_mid_dst_perc = results[Constants.IND_BLG_MIDDLE_DST_PERCENT]
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        multiplicadorUP = 1
        blgLowerDistPercent = -10
        blgLowerInvMaxDistPercent = 40
        ima5ma20 = results[Constants.IMA5MA20]
        isRising, angleDiff = self.isRisingFromWEEKNEW(results)
        if not isRising:
            if angleDiff < 0 and abs(angleDiff) > closeWeekDiffNew / 2:
                if ima5ma20 == Constants.INDICATOR_EMA_SELL:
                    if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgLowerDistPercent and results[Constants.IND_BLG_LOWER_DST_PERCENT] > 0:
                        if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MAX_DIST] >= difference_optimized * multiplicadorUP:
                            if results[Constants.ACUMULADO] < 0:
                                res = (True, 'SELL', 1)
        else:
            pass
            if angleDiff > 0 and abs(angleDiff) > closeWeekDiffNew:
                if results[Constants.IND_BLG_LOWER_DST_PERCENT] < blgLowerInvMaxDistPercent or ima5ma20 == Constants.INDICATOR_EMA_BUY:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MIN_DIST] >= difference_optimized * multiplicadorUP:
                        if results[Constants.ACUMULADO] > 0:
                            res = (True, 'BUY', 1)
        return res

    def evaluateDownOpen_EMA_WEEK_NEW_FLOW_02(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        blg_mid_dst_perc = results[Constants.IND_BLG_MIDDLE_DST_PERCENT]
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        multiplicadorUP = 1
        blgLowerDistPercent = -10
        blgLowerInvMaxDistPercent = 55
        ima5ma20 = results[Constants.IMA5MA20]
        isRising, angleDiff = self.isRisingFromWEEKNEW(results)
        if not isRising:
            if angleDiff < 0 and abs(angleDiff) > closeWeekDiffNew / 2:
                if ima5ma20 == Constants.INDICATOR_EMA_SELL:
                    if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgLowerDistPercent and results[Constants.IND_BLG_LOWER_DST_PERCENT] > 0:
                        if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MAX_DIST] >= difference_optimized * multiplicadorUP:
                            if results[Constants.ACUMULADO] < 0:
                                res = (True, 'SELL', 1)
        else:
            pass
            if angleDiff > 0 and abs(angleDiff) > closeWeekDiffNew:
                if results[Constants.IND_BLG_LOWER_DST_PERCENT] < blgLowerInvMaxDistPercent:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MIN_DIST] >= difference_optimized * multiplicadorUP:
                        if results[Constants.ACUMULADO] > 0:
                            res = (True, 'BUY', 1)
        return res

    def evaluateDownOpen_EMA_WEEK_NEW_FLOW_03(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        blg_mid_dst_perc = results[Constants.IND_BLG_MIDDLE_DST_PERCENT]
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        multiplicadorUP = 1
        blgLowerDistPercent = -10
        blgLowerInvMaxDistPercent = 40
        ima5ma20 = results[Constants.IMA5MA20]
        isRising, angleDiff = self.isRisingFromWEEKNEW(results)
        if not isRising:
            if angleDiff < 0 and abs(angleDiff) > closeWeekDiffNew / 2:
                if ima5ma20 == Constants.INDICATOR_EMA_SELL or ima5ma20 == Constants.INDICATOR_EMA_WAIT:
                    if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgLowerDistPercent and results[Constants.IND_BLG_LOWER_DST_PERCENT] >= 0:
                        if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MAX_DIST] >= difference_optimized * multiplicadorUP:
                            if results[Constants.ACUMULADO] < 0:
                                res = (True, 'SELL', 1)
        elif angleDiff > 0 and abs(angleDiff) > closeWeekDiffNew:
            if results[Constants.IND_BLG_LOWER_DST_PERCENT] < blgLowerInvMaxDistPercent or ima5ma20 == Constants.INDICATOR_EMA_BUY:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MIN_DIST] >= difference_optimized * multiplicadorUP:
                    if results[Constants.ACUMULADO] > 0:
                        res = (True, 'BUY', 1)
        return res

    def evaluateDownOpen_EMA_OUP_01(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        min_ema_dst = activeParam.min_ema_dst
        ema_dst = results[Constants.EMA_DST]
        multiplicadorUP = 1
        blgLowerDistPercent = 5
        isRising, angleDiff = self.isRisingFromWEEK(results)
        if isRising:
            nada = ''
            if ema_dst > min_ema_dst:
                if angleDiff > 0 and abs(angleDiff) >= closeWeekDiffNew:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MIN_DIST] >= difference_optimized * multiplicadorUP:
                        if results[Constants.ACUMULADO] > 0:
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            res = (True, 'BUY', 1)
        return res

    def evaluateDownOpen_EMA_OUP_03(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        min_ema_dst = activeParam.min_ema_dst
        ema_dst = results[Constants.EMA_DST]
        imaemadst = results[Constants.IMA1EMADIFF]
        ima1EmaMinValue = activeParam.ima1EmaMinValue
        multiplicadorUP = 1
        blgLowerDistPercent = 5
        if (abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0) and abs(results[Constants.MEDSTDDIFF]) < medstdmaxDiff:
            if results[Constants.IND_BLG] == Constants.IND_BLG_MED_BUY:
                if results[Constants.ACUMULADO] < 0:
                    if results[Constants.MEDSTDDIFF] < 0:
                        results[Constants.CLOSE_NXT_DOWN] = 0
                        results[Constants.CLOSE_NXT_UP] = 0
                elif results[Constants.MEDSTDDIFF] > 0:
                    if results[Constants.DIRECTION] == Constants.DIR_UP or results[Constants.DIRECTION] == Constants.DIR_PRE_UP or results[Constants.DIRECTION] == Constants.DIR_CHANGE:
                        if results[Constants.IND_BLG_UPPER_DST_PERCENT] > blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
                            res = (True, 'BUY', 1)
                    results[Constants.CLOSE_NXT_DOWN] = 0
                    results[Constants.CLOSE_NXT_UP] = 0
            elif results[Constants.IND_BLG_UPPER_DST_PERCENT] > blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MAX_DIST] >= difference_optimized * multiplicadorUP:
                    if results[Constants.ACUMULADO] < 0:
                        if results[Constants.MEDSTDDIFF] < 0:
                            results[Constants.CLOSE_NXT_DOWN] = 0
                            results[Constants.CLOSE_NXT_UP] = 0
                    else:
                        if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_UP:
                            res = (True, 'BUY', 2)
                        results[Constants.CLOSE_NXT_UP] = 0
            else:
                nada = ''
                if results[Constants.ACUMULADO] > 0:
                    if results[Constants.MEDSTDDIFF] > 0:
                        results[Constants.CLOSE_NXT_DOWN] = 0
                        results[Constants.CLOSE_NXT_UP] = 0
        return res

    def evaluateDownOpen_EMA_OUP_02(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        min_ema_dst = activeParam.min_ema_dst
        ema_dst = results[Constants.EMA_DST]
        imaemadst = results[Constants.IMA1EMADIFF]
        ima1EmaMinValue = activeParam.ima1EmaMinValue
        multiplicadorUP = 1
        blgLowerDistPercent = 5
        isRising, angleDiff = self.isRisingFromWEEK(results)
        if isRising:
            nada = ''
            if imaemadst > 0 and imaemadst >= ima1EmaMinValue:
                if angleDiff > 0 and abs(angleDiff) >= closeWeekDiffNew:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MIN_DIST] >= difference_optimized * multiplicadorUP:
                        res = (True, 'BUY', 1)
        return res

    def evaluateUpOpen_BLG_01(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUP = activeParam.angleUp
        medstdminDiff = activeParam.medstdminDiff
        multiplicadorUP = 2
        if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MIN_DIST] >= difference_optimized * multiplicadorUP:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] == 0:
                    if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff:
                        res = (True, 'BUY', 1)
                elif results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
                    res = (True, 'BUY', 2)
                elif results[Constants.IND_BLG_UPPER_DST_PERCENT] < blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] == 0:
                    nada = ''
                    if results[Constants.ANGLE] > 0 or results[Constants.ANGLE] == 0:
                        if abs(results[Constants.ANGLE]) > angleUP:
                            res = (True, 'BUY', 3)
                        elif results[Constants.ANGLEm1] < 0:
                            res = (True, 'BUY', 4)
            else:
                nada = ''
                if abs(results[Constants.MEDSTDDIFF]) > self.medstdminDiff:
                    res = (True, 'SELL', 1)
        return res

    def evaluateUpOpen_BLG_02(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        medstdminDiff = activeParam.medstdminDiff
        multiplicadorUP = 2
        if (abs(results[Constants.MEDSTDDIFF]) > self.medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0) and abs(results[Constants.MEDSTDDIFF]) < self.medstdmaxDiff:
            if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
                if results[Constants.ACUMULADO] > 0:
                    if results[Constants.MEDSTDDIFF] > 0:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        res = (True, 'BUY', 1)
                else:
                    nada = ''
                    if results[Constants.MEDSTDDIFF] < 0:
                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                        res = (True, 'SELL', 1)
            elif results[Constants.ACUMULADO_ABS] >= difference_optimized * self.multiplicadorUP or results[Constants.ACTION_MIN_DIST] >= difference_optimized * self.multiplicadorUP:
                if results[Constants.ACUMULADO] > 0:
                    if results[Constants.CLOSE_NXT_DOWN] == 0:
                        if results[Constants.MEDSTDDIFF] > 0:
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            res = (True, 'BUY', 2)
                    elif results[Constants.MEDSTDDIFF] < 0:
                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                        res = (True, 'SELL', 2)
                elif results[Constants.ACUMULADO] < 0:
                    if results[Constants.MEDSTDDIFF] < 0:
                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                        res = (True, 'SELL', 3)
        return res

    def evaluateUpOpen_BLG_03(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        multiplicadorUP = 1
        blgLowerDistPercent = 10
        isRising, angleDiff = self.isRisingAngle(results)
        if isRising:
            if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
                if results[Constants.ACUMULADO] > 0:
                    if results[Constants.MEDSTDDIFF] > 0:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        res = (True, 'BUY', 1)
                else:
                    nada = ''
            elif results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgLowerDistPercent:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MIN_DIST] >= difference_optimized * multiplicadorUP:
                    if results[Constants.ACUMULADO] > 0:
                        if results[Constants.MEDSTDDIFF] > 0:
                            if results[Constants.WEEK_DIR_BOT_DST] <= 90:
                                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                res = (True, 'BUY', 2)
                    else:
                        nada = ''
        return res

    def evaluateUpOpen_EMA_01(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        multiplicadorUP = 1
        blgLowerDistPercent = 10
        isRising, angleDiff = self.isRisingAngle(results)
        if isRising:
            if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgLowerDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MIN_DIST] >= difference_optimized * multiplicadorUP:
                    if results[Constants.ACUMULADO] > 0:
                        if results[Constants.MEDSTDDIFF] > 0:
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            res = (True, 'BUY', 1)
        return res

    def evaluateUpOpen_EMA_05(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        multiplicadorUP = 1
        blgLowerDistPercent = 10
        angleEma20 = results[Constants.ANGLE_EMA20]
        if angleEma20 > 0:
            if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgLowerDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MIN_DIST] >= difference_optimized * multiplicadorUP:
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                    res = (True, 'BUY', 1)
        return res

    def evaluateUpOpen_EMA_02(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        multiplicadorUP = 1
        blgLowerDistPercent = 10
        if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgLowerDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
            if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MIN_DIST] >= difference_optimized * multiplicadorUP:
                if results[Constants.ACUMULADO] > 0:
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                    res = (True, 'BUY', 1)
        return res

    def evaluateUpOpen_EMA_03(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        multiplicadorUP = 1
        blgLowerDistPercent = 10
        isRising, angleDiff = self.isRisingAngle(results)
        if isRising:
            if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgLowerDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MIN_DIST] >= difference_optimized * multiplicadorUP:
                    if results[Constants.ACUMULADO] > 0:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        res = (True, 'BUY', 1)
        return res

    def evaluateUpOpen_RSI_01(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        multiplicadorUP = 1
        blgLowerDistPercent = 10
        isRising = True
        if isRising:
            if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MIN_DIST] >= difference_optimized * multiplicadorUP:
                if results[Constants.ACUMULADO] > 0:
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                    res = (True, 'BUY', 1)
        return res

    def evaluateUpOpen_EMA_WEEK_01(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        multiplicadorUP = 1
        blgLowerDistPercent = 10
        isRising, angleDiff = self.isRisingFromWEEK(results)
        if isRising:
            if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgLowerDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MIN_DIST] >= difference_optimized * multiplicadorUP:
                    if results[Constants.ACUMULADO] > 0:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        res = (True, 'BUY', 1)
        return res

    def evaluateUpOpen_EMA_WEEK_02(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        multiplicadorUP = 1
        blgLowerDistPercent = 10
        isRising, angleDiff = self.isRisingFromWEEK(results)
        if isRising:
            if angleDiff > closeWeekDiffNew / 2:
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgLowerDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MIN_DIST] >= difference_optimized * multiplicadorUP:
                        if results[Constants.ACUMULADO] > 0:
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            res = (True, 'BUY', 1)
        return res

    def evaluateUpOpen_EMA_WEEK_03(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        multiplicadorUP = 1
        blgLowerDistPercent = 10
        isRising, angleDiff = self.isRisingFromMonth(results)
        if isRising:
            if angleDiff > 0 and angleDiff > closeWeekDiffNew / 2:
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgLowerDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MIN_DIST] >= difference_optimized * multiplicadorUP:
                        if results[Constants.ACUMULADO] > 0:
                            res = (True, 'BUY', 1)
        else:
            pass
            if angleDiff < 0 and abs(angleDiff) > closeWeekDiffNew:
                if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgLowerDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT] < 0:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MAX_DIST] >= difference_optimized * multiplicadorUP:
                        if results[Constants.ACUMULADO] < 0:
                            res = (True, 'SELL', 1)
        return res

    def evaluateUpOpen_EMA_WEEK_04(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        multiplicadorUP = 1
        blgLowerDistPercent = -10
        ima5ma20 = results[Constants.IMA5MA20]
        isRising, angleDiff = self.isRisingFromMonth(results)
        if isRising:
            if angleDiff > 0 and angleDiff > closeWeekDiffNew / 2:
                if ima5ma20 == Constants.INDICATOR_EMA_BUY:
                    if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgLowerDistPercent:
                        if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MIN_DIST] >= difference_optimized * multiplicadorUP:
                            if results[Constants.ACUMULADO] > 0:
                                res = (True, 'BUY', 1)
        else:
            pass
            if angleDiff < 0 and abs(angleDiff) > closeWeekDiffNew:
                if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgLowerDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT] < 0:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MAX_DIST] >= difference_optimized * multiplicadorUP:
                        if results[Constants.ACUMULADO] < 0:
                            res = (True, 'SELL', 1)
        return res

    def evaluateUpOpen_EMA_WEEK_NEW_FLOW_01(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        multiplicadorUP = 1
        blgLowerDistPercent = -10
        ima5ma20 = results[Constants.IMA5MA20]
        isRising, angleDiff = self.isRisingFromWEEKNEW(results)
        if isRising:
            if angleDiff > 0 and angleDiff > closeWeekDiffNew / 2:
                if ima5ma20 == Constants.INDICATOR_EMA_BUY:
                    if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgLowerDistPercent:
                        if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MIN_DIST] >= difference_optimized * multiplicadorUP:
                            if results[Constants.ACUMULADO] > 0:
                                res = (True, 'BUY', 1)
        else:
            pass
            if angleDiff < 0 and abs(angleDiff) > closeWeekDiffNew:
                if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgLowerDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT] < 0:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MAX_DIST] >= difference_optimized * multiplicadorUP:
                        if results[Constants.ACUMULADO] < 0:
                            res = (True, 'SELL', 1)
        return res

    def evaluateUpOpen_EMA_WEEK_NEW_FLOW_02(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        multiplicadorUP = 1
        blgLowerDistPercent = -10
        ima5ma20 = results[Constants.IMA5MA20]
        blgmaMean = results[Constants.BLG_MA_MEAN]
        blgma_min_diff = activeParam.blgma_min_diff
        isRising, angleDiff = self.isRisingFromWEEKNEW(results)
        if isRising:
            if angleDiff > 0 and angleDiff > closeWeekDiffNew / 2:
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgLowerDistPercent:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MIN_DIST] >= difference_optimized * multiplicadorUP:
                        if results[Constants.ACUMULADO] > 0:
                            res = (True, 'BUY', 1)
        else:
            invSellCond = False
            pass
            if angleDiff < 0 and abs(angleDiff) > closeWeekDiffNew:
                if blgmaMean < 0 and abs(blgmaMean) > blgma_min_diff:
                    invSellCond = True
                if invSellCond:
                    if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgLowerDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT] < 0:
                        if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MAX_DIST] >= difference_optimized * multiplicadorUP:
                            if results[Constants.ACUMULADO] < 0:
                                res = (True, 'SELL', 1)
        return res

    def evaluateUpOpen_EMA_04(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        multiplicadorUP = 1
        blgLowerDistPercent = 10
        isRising, angleDiff = self.isRisingAngle(results)
        isRisingIma1, angleDiffIm1 = self.isRisingAngleIma1(results)
        if isRising:
            if isRisingIma1:
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgLowerDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MIN_DIST] >= difference_optimized * multiplicadorUP:
                        if results[Constants.ACUMULADO] > 0:
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            res = (True, 'BUY', 1)
            else:
                inversa = ''
                if results[Constants.ACTION_MIN_DIST] < results[Constants.ACTION_MAX_DIST]:
                    results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                    res = (True, 'SELL', 1)
        return res

    def evaluateUpOpen_EMA_OUP_01(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        multiplicadorUP = 1
        blgLowerDistPercent = 10
        isRising, angleDiff = self.isRisingFromWEEK(results)
        if isRising:
            if angleDiff > closeWeekDiffNew / 2:
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgLowerDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MIN_DIST] >= difference_optimized * multiplicadorUP:
                        if results[Constants.ACUMULADO] > 0:
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            res = (True, 'BUY', 1)
        return res

    def evaluateUpOpen_EMA_OUP_02(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        multiplicadorUP = 1
        blgLowerDistPercent = 10
        weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
        flujoBLG = results[Constants.BLG_MA_X]
        isRising, angleDiff = self.isRisingFromWEEK(results)
        if isRising:
            if weekdirBotPercent > 90 and weekdirBotPercent < 100:
                nada = ''
            elif angleDiff > closeWeekDiffNew / 2:
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgLowerDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MIN_DIST] >= difference_optimized * multiplicadorUP:
                        if results[Constants.ACUMULADO] > 0:
                            res = (True, 'BUY', 1)
        else:
            nada = ''
        return res

    def evaluateUpOpen_EMA_OUP_04(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        blgDistPercent = activeParam.blgDistPercent
        multiplicadorUP = 1
        if (abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0) and abs(results[Constants.MEDSTDDIFF]) < medstdmaxDiff:
            if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
                if results[Constants.ACUMULADO] > 0:
                    if results[Constants.MEDSTDDIFF] > 0:
                        if results[Constants.DIRECTION] == Constants.DIR_UP or results[Constants.DIRECTION] == Constants.DIR_PRE_UP or results[Constants.DIRECTION] == Constants.DIR_CHANGE:
                            if results[Constants.IND_BLG_UPPER_DST_PERCENT] > blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
                                res = (True, 'BUY', 1)
                else:
                    nada = ''
                    if results[Constants.MEDSTDDIFF] < 0:
                        nada = ''
                    if results[Constants.INDICATOR_MED_MOMENT] == Constants.INDICATOR_TM_DOWN:
                        nada = ''
            elif results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MIN_DIST] >= difference_optimized * multiplicadorUP:
                if results[Constants.ACUMULADO] > 0:
                    if results[Constants.CLOSE_NXT_DOWN] == 0:
                        if results[Constants.MEDSTDDIFF] > 0:
                            if results[Constants.IND_BLG_UPPER_DST_PERCENT] > blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
                                res = (True, 'BUY', 2)
                        else:
                            nada = ''
                    elif results[Constants.MEDSTDDIFF] < 0:
                        nada = ''
                    else:
                        nada = ''
                        if results[Constants.IND_BLG_UPPER_DST_PERCENT] > blgDistPercent:
                            res = (True, 'BUY', 3)
                        elif results[Constants.INDICATOR_MED_MOMENT] == Constants.INDICATOR_TM_UP:
                            res = (True, 'BUY', 4)
                        if results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0 and abs(results[Constants.IND_BLG_UPPER_DST_PERCENT]) > 1:
                            res = (True, 'BUY', 5)
                elif results[Constants.ACUMULADO] < 0:
                    if results[Constants.MEDSTDDIFF] < 0:
                        nada = ''
        return res

    def evaluateUpOpen_EMA_OUP_03(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        multiplicadorUP = 1
        blgLowerDistPercent = 10
        weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
        flujoBLG = results[Constants.BLG_MA_X]
        blgMaVal = results[Constants.BLG_MA_VAL]
        blg_max_min_value = activeParam.blg_max_min_value
        blgma_min_diff = activeParam.blgma_min_diff
        weekNewFlow = results[Constants.WEEK_DIR_BOT_DST_MED_NEW_FLOW]
        weekNewMinFlow = activeParam.blgma_min_diff
        isRising, angleDiff = self.isRisingFromWEEKNEW(results)
        reglasExtraBuy = False
        if weekNewFlow > 0 and weekNewFlow > weekNewMinFlow:
            reglasExtraBuy = True
        reglasExtraBuy = True
        if isRising:
            if weekdirBotPercent > 90 and weekdirBotPercent < 100:
                nada = ''
            elif angleDiff > closeWeekDiffNew / 2:
                if reglasExtraBuy:
                    if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgLowerDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
                        if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MIN_DIST] >= difference_optimized * multiplicadorUP:
                            if results[Constants.ACUMULADO] > 0:
                                res = (True, 'BUY', 1)
        else:
            nada = ''
        return res

    def evaluateUpOpen_Ima1_01(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        maxAcumValue = activeParam.closeAcumvalue * 3
        medstdminDiff = activeParam.medstdminDiff
        if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
            if results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_UP or results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_UNDEF:
                difOpenHours = self.getDifTimeFromOpen(results)
                if difOpenHours <= 10:
                    res = (True, 'BUY', 1)
                elif abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0:
                    if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                        res = (True, 'BUY', 2)
            elif results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_DOWN:
                nada = ''
                if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0:
                    if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                        res = (True, 'BUY', 3)
        elif results[Constants.FLUJO] == Constants.FLUJO_BAJA:
            if results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_DOWN:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
                    if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0:
                        if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                            res = (True, 'SELL', 1)
        return res

    def evaluateUpOpen_Ima1_02(self, results, activeParam):
        res = (False, 'NADA', 0)
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        maxAcumValue = activeParam.closeAcumvalue * 3
        medstdminDiff = activeParam.medstdminDiff
        if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
            if results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_UP or results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_UNDEF:
                difOpenHours = self.getDifTimeFromOpen(results)
                if difOpenHours <= 10:
                    res = (True, 'BUY', 1)
                elif abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0:
                    if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                        res = (True, 'BUY', 2)
            elif results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_DOWN:
                nada = ''
                if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0:
                    if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                        res = (True, 'BUY', 3)
        elif results[Constants.FLUJO] == Constants.FLUJO_BAJA:
            if results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_DOWN:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
                    if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0:
                        if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                            res = (True, 'SELL', 1)
        return res

    def evaluateUpOpen_10(self, results, activeParam):
        res = (False, 0)
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MIN_DIST] >= difference_optimized:
            if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] == 0:
                if results[Constants.WEEK_DIR_BOT_DST] < 90:
                    isRising, angleDiff = self.isRisingAngleIma1(results)
                    if isRising:
                        if 'UP' in results[Constants.ANGLE_FLOW]:
                            if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] < 5:
                                res = (True, 5)
                            elif results[Constants.IND_BLG_MIDDLE_DST_PERCENT] < 20:
                                if results[Constants.ANGLE] > 0:
                                    res = (True, 1)
                            elif angleDiff > angleUp:
                                if results[Constants.ANGLE] > angleUp:
                                    res = (True, 4)
                elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                    isRising, angleDiff = self.isRisingAngle(results)
                    if isRising:
                        if results[Constants.ANGLE_IMA1] > 0:
                            if results[Constants.IMA1EMADIFF] > 0:
                                if results[Constants.IMA1EMADIFF] > activeParam.ima1EmaMinValue:
                                    res = (True, 2)
            elif results[Constants.IND_BLG_UPPER_DST_PERCENT] > 0 and results[Constants.IND_BLG_UPPER_DST_PERCENT] < blgDistPercent:
                if results[Constants.WEEK_DIR_BOT_DST] > 90:
                    if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] > 30:
                        if results[Constants.ANGLE] > 0:
                            if results[Constants.ANGLE_COUNTER] > 5:
                                isRising, angleDiff = self.isRisingAngle(results)
                                if isRising:
                                    res = (True, 3)
        return res

    def isRisingAngle(self, results):
        res = (False, 0)
        angleDIff = float(results[Constants.ANGLE]) - float(results[Constants.ANGLE_PREV])
        if angleDIff > 0:
            res = (True, angleDIff)
        else:
            res = (False, angleDIff)
        return res

    def isRisingFromWEEK(self, results):
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

    def isRisingFromWEEKNEW(self, results):
        res = (False, 0)
        angleDIff = float(results[Constants.WEEK_DIR_BOT_DST_NEW]) - float(results[Constants.WEEK_DIR_BOT_DST_MED_NEW])
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

    def evaluateForteUpOpen_01(self, results, activeParam):
        res = False
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MIN_DIST] >= difference_optimized:
            if results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0 or results[Constants.IND_BLG_UPPER_DST_PERCENT] == 0:
                if results[Constants.WEEK_DIR_BOT_DST] < 90:
                    if results[Constants.IMA1EMADIFF] > 0:
                        if results[Constants.IMA1EMADIFF] > 0.3:
                            res = True
        return res

    def evaluateDownOpen_01(self, results, activeParam):
        res = (False, 0)
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        angleDown = activeParam.angleDown
        if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
            if results[Constants.IND_BLG_LOWER_DST_PERCENT] > blgDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT] == 0:
                if results[Constants.WEEK_DIR_BOT_DST] > 10:
                    if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff:
                        res = (True, 1)
            elif results[Constants.IND_BLG_LOWER_DST_PERCENT] < blgDistPercent:
                rising, angleDiff = self.isRisingAngle(results)
                if rising == False:
                    if abs(angleDiff) > angleDown:
                        res = (True, 2)
        return res

    def evaluateDownOpen_02(self, results, activeParam):
        res = (False, 0)
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        angleDown = activeParam.angleDown
        if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
            if results[Constants.IND_BLG_LOWER_DST_PERCENT] > blgDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT] == 0:
                if results[Constants.WEEK_DIR_BOT_DST] > 10:
                    if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff:
                        res = (True, 1)
            elif results[Constants.IND_BLG_LOWER_DST_PERCENT] < blgDistPercent:
                rising, angleDiff = self.isRisingAngle(results)
                if rising == False:
                    if abs(angleDiff) > angleDown:
                        res = (True, 2)
        return res

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

    def evaluateDownOpen_BLG_01(self, results, activeParam):
        res = (False, 'nada', 0)
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        angleDown = activeParam.angleDown
        angleUp = activeParam.angleUp
        medstdminDiff = activeParam.medstdminDiff
        if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT] == 0:
                    if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff:
                        res = (True, 'SELL', 1)
                elif results[Constants.IND_BLG_LOWER_DST_PERCENT] < 0:
                    res = (True, 'SELL', 2)
                elif results[Constants.IND_BLG_LOWER_DST_PERCENT] < blgDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT] == 0:
                    nada = ''
                    if results[Constants.ANGLE] < 0 or results[Constants.ANGLE] == 0:
                        if abs(results[Constants.ANGLE]) > angleDown:
                            res = (True, 'SELL', 3)
                        elif results[Constants.ANGLEm1] > 0:
                            res = (True, 'SELL', 4)
            else:
                nada = ''
        return res

    def evaluateDownOpen_IMA1_01(self, results, activeParam):
        res = (False, 'nada', 0)
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        angleDown = activeParam.angleDown
        angleUp = activeParam.angleUp
        maxAcumValue = activeParam.closeAcumvalue * 3
        medstdminDiff = activeParam.medstdminDiff
        risingIma1, angleIma1Diff = self.isRisingAngleIma1(results)
        rising, angleDiff = self.isRisingAngle(results)
        if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
            if results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_DOWN or results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_UNDEF:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
                    difOpenHours = self.getDifTimeFromOpen(results)
                    if difOpenHours <= 60:
                        res = (True, 'SELL', 1)
                    elif abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0:
                        if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                            res = (True, 'SELL', 2)
            elif results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_UP:
                if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0:
                    if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                        res = (True, 'SELL', 3)
        elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
            if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UP:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
                    if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0:
                        if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                            res = (True, 'BUY', 1)
        return res

    def evaluateDownOpen_IMA1_02(self, results, activeParam):
        res = (False, 'nada', 0)
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        angleDown = activeParam.angleDown
        angleUp = activeParam.angleUp
        maxAcumValue = activeParam.closeAcumvalue * 3
        medstdminDiff = activeParam.medstdminDiff
        risingIma1, angleIma1Diff = self.isRisingAngleIma1(results)
        rising, angleDiff = self.isRisingAngle(results)
        if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
            if 'DOWN' in results[Constants.ANGLE_FLOW]:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
                    difOpenHours = self.getDifTimeFromOpen(results)
                    if difOpenHours <= 60:
                        res = (True, 'SELL', 1)
                    elif results[Constants.IND_BLG_LOWER_DST_PERCENT] > blgDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT] == 0:
                        if results[Constants.WEEK_DIR_BOT_DST] > 10:
                            res = (True, 'SELL', 2)
            elif 'UP' in results[Constants.ANGLE_FLOW]:
                res = (True, 'SELL', 3)
        elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
            if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UP:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
                    if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0:
                        if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                            res = (True, 'BUY', 1)
        return res

    def evaluateDownOpen_IMA1_03(self, results, activeParam):
        res = (False, 'nada', 0)
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        angleDown = activeParam.angleDown
        angleUp = activeParam.angleUp
        maxAcumValue = activeParam.closeAcumvalue * 3
        medstdminDiff = activeParam.medstdminDiff
        risingIma1, angleIma1Diff = self.isRisingAngleIma1(results)
        rising, angleDiff = self.isRisingAngle(results)
        if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
            if results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_DOWN or results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_UNDEF:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
                    difOpenHours = self.getDifTimeFromOpen(results)
                    if difOpenHours <= 60:
                        res = (True, 'SELL', 1)
                    elif abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0:
                        if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                            res = (True, 'SELL', 2)
            elif results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_UP:
                if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0:
                    if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                        res = (True, 'SELL', 3)
        elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
            if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UP:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
                    if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0:
                        if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                            res = (True, 'BUY', 1)
        return res

    def evaluateDownOpen_03(self, results, activeParam):
        res = (False, 0)
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        angleDown = activeParam.angleDown
        angleUp = activeParam.angleUp
        risingIma1, angleIma1Diff = self.isRisingAngleIma1(results)
        rising, angleDiff = self.isRisingAngle(results)
        if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
            if results[Constants.IND_BLG_LOWER_DST_PERCENT] > blgDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT] == 0:
                if results[Constants.WEEK_DIR_BOT_DST] > 10:
                    if results[Constants.IMA1EMADIFF] > 0:
                        if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] > 20:
                            if risingIma1 == False:
                                res = (True, 3)
                    elif abs(results[Constants.MEDSTDDIFF]) > medstdminDiff:
                        if risingIma1 == False:
                            res = (True, 1)
                        elif angleIma1Diff > angleUp:
                            res = (False, -1)
            elif results[Constants.IND_BLG_LOWER_DST_PERCENT] < blgDistPercent:
                if rising == False:
                    if abs(angleDiff) > angleDown:
                        res = (True, 2)
        return res

    def evalNXT_UP_01(self, results, activeParam, difference_optimized):
        res = False
        if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MIN_DIST] >= difference_optimized:
            results[Constants.CLOSE_NXT_UP] = 0
            if results[Constants.WEEK_DIR_BOT_DST] < 10:
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] > self.blgDistPercent:
                    if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] < 0:
                        res = True
        return res

    def evalNXT_UP_02(self, results, activeParam, difference_optimized):
        res = False
        if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MIN_DIST] >= difference_optimized:
            results[Constants.CLOSE_NXT_UP] = 0
            if results[Constants.WEEK_DIR_BOT_DST] < 50:
                if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
                    if results[Constants.IND_BLG_UPPER_DST_PERCENT] > self.blgDistPercent:
                        if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] < 0:
                            res = True
            elif results[Constants.WEEK_DIR_BOT_DST] > 50 and results[Constants.WEEK_DIR_BOT_DST] < 90:
                if results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_UP:
                    if results[Constants.IND_BLG_UPPER_DST_PERCENT] > self.blgDistPercent:
                        if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] < 0:
                            res = True
        return res

    def evalNXT_UP_03(self, results, activeParam, difference_optimized):
        res = (False, 1)
        if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MIN_DIST] >= difference_optimized:
            results[Constants.CLOSE_NXT_UP] = 0
            if results[Constants.WEEK_DIR_BOT_DST] < 50:
                if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
                    if results[Constants.IND_BLG_UPPER_DST_PERCENT] > self.blgDistPercent:
                        if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] < 0:
                            res = (True, 1)
                elif results[Constants.ANGLE] < 0 and abs(results[Constants.ANGLE]) < 40:
                    if results[Constants.IND_BLG_UPPER_DST_PERCENT] > self.blgDistPercent:
                        if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] < 0:
                            res = (True, 2)
        return res

    def evalNXT_UP_04(self, results, activeParam, difference_optimized):
        res = (False, 1)
        blgDistPercent = activeParam.blgDistPercent
        if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MIN_DIST] >= difference_optimized:
            results[Constants.CLOSE_NXT_UP] = 0
            if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] > blgDistPercent:
                    res = (True, 1)
        return res

    def evalNXT_UP_05(self, results, activeParam, difference_optimized):
        res = (False, 1)
        blgDistPercent = activeParam.blgDistPercent
        results[Constants.CLOSE_NXT_UP] = 0
        multiplicadorUP = 2
        if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
            if results[Constants.IND_BLG_UPPER_DST_PERCENT] > blgDistPercent:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized * multiplicadorUP or results[Constants.ACTION_MIN_DIST] >= difference_optimized * multiplicadorUP:
                    res = (True, 1)
        return res

    def evalNXT_DOWN_01(self, results, activeParam, difference_optimized):
        res = False
        if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
            results[Constants.CLOSE_NXT_DOWN] = 0
            if results[Constants.WEEK_DIR_BOT_DST] > 50:
                if results[Constants.IND_BLG_LOWER_DST_PERCENT] > self.blgDistPercent:
                    if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] > 0:
                        res = True
            elif results[Constants.WEEK_DIR_BOT_DST] < 50 and results[Constants.WEEK_DIR_BOT_DST] > 10:
                if results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_DOWN:
                    if results[Constants.IND_BLG_LOWER_DST_PERCENT] > self.blgDistPercent:
                        if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] > 0:
                            res = True
        return res