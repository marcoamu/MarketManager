from service.Constants import Constants
import time
from datetime import datetime


class AperturaBase:

    def __init__(self):
        print("iniciando")

    def printInicioLog(self, name, results, activeparameters):
        print(
            f" INICIO MERCADO {name} {results[Constants.DATE].values[0]} \tACUMULADO_ABS: {results[Constants.ACUMULADO_ABS]} \tWEEK_DIR_FLOW {results[Constants.WEEK_DIR_FLOW]} \tANGLE_EMA20: {results[Constants.ANGLE_EMA20]} \tANGLE: {results[Constants.ANGLE]}  \tANGLE_IMA1: {results[Constants.ANGLE_IMA1]} \tANGLE_IMA1_COUNTER: {results[Constants.ANGLE_IMA1_COUNTER]}  \tWEEK_DIR_BOT_DST {results[Constants.WEEK_DIR_BOT_DST]} \tIND_BLG_LOWER_DST_PERCENT {results[Constants.IND_BLG_LOWER_DST_PERCENT]} \tANGLE_EMA: {results[Constants.ANGLE_EMA]} \tWEEK_DIR_FLOW_DIFF {results[Constants.WEEK_DIR_FLOW_DIFF]} \tWEEK_DIR_FLOW_PREV {results[Constants.WEEK_DIR_FLOW_PREV]}  \tMEDSTDDIFF {results[Constants.MEDSTDDIFF]} \tINDICATOR_EMA: {results[Constants.INDICATOR_EMA]}  \tDIRECTION {results[Constants.DIRECTION]} \tINDICATOR_MED_MOMENT {results[Constants.INDICATOR_MED_MOMENT]}")
        results[Constants.INICIO_NAME] = name

    def evaluateUpOpen_01(self, results,activeParam):
        res = False
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference

        if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
            Constants.ACTION_MIN_DIST] >= (difference_optimized):
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] > blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT]==0:
                    if results[Constants.WEEK_DIR_BOT_DST] < 90:
                        if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff:
                            # if self.canOpenUP_BLGDistance(results,activeParam):
                                res = True
        return  res


    def canOpenUP_BLGDistance(self, results, activeParam):
        #evalua si puede abrir teniendo en cuenta las posiciones bot percent y blg bot percent
        res = True
        if results[Constants.IND_BLG_LOWER_DST_PERCENT] > 80:
            if results[Constants.WEEK_DIR_BOT_DST]> 40:
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
                    # if abs(angleIma1) > activeParam.angleDown:
                    if angleIma1Count >= 3:
                        res = Constants.DIR_DOWN

        elif angle < 0:
            if angleCount >= 2:
                res = Constants.DIR_DOWN
                if angleIma1 > 0:
                    # if angleIma1 > activeParam.angleUp:
                    if angleIma1Count >= 3:
                        res = Constants.DIR_UP
        return res


    def evaluateUpOpen_02(self, results,activeParam):
        res = False, 0
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference

        if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
            Constants.ACTION_MIN_DIST] >= (difference_optimized):
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] > blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT]==0:
                    if results[Constants.WEEK_DIR_BOT_DST] < 90:
                        if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] < 10:
                        # if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff:
                            # if self.canOpenUP_BLGDistance(results,activeParam):
                                res = True, 1
                    else:
                        if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                            isRising, angleDiff = self.isRisingAngle(results)
                            if isRising:
                                if results[Constants.ANGLE_IMA1]>0:
                                    if results[Constants.IMA1EMADIFF] > 0:
                                        if results[Constants.IMA1EMADIFF] > activeParam.ima1EmaMinValue:
                                            res = True, 2
        return  res

    def evaluateUpOpen_03(self, results,activeParam):
        res = False, 0
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference

        if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
            Constants.ACTION_MIN_DIST] >= (difference_optimized):
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] > blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT]==0:
                    if results[Constants.WEEK_DIR_BOT_DST] < 90:
                        if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] < 10:
                            isRising, angleDiff = self.isRisingAngleIma1(results)
                            if isRising:
                                res = True, 1
                    else:
                        if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                            isRising, angleDiff = self.isRisingAngle(results)
                            if isRising:
                                if results[Constants.ANGLE_IMA1]>0:
                                    if results[Constants.IMA1EMADIFF] > 0:
                                        if results[Constants.IMA1EMADIFF] > activeParam.ima1EmaMinValue:
                                            res = True, 2
        return  res


    def evaluateUpOpen_09(self, results,activeParam):
        res = False, 0
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference

        if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
            Constants.ACTION_MIN_DIST] >= (difference_optimized):
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] > blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT]==0:
                    if results[Constants.WEEK_DIR_BOT_DST] < 90:
                        if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] < 10:
                        # if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff:
                            # if self.canOpenUP_BLGDistance(results,activeParam):
                                res = True, 1
                    else:
                        if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                            isRising, angleDiff = self.isRisingAngle(results)
                            if isRising:
                                if results[Constants.ANGLE_IMA1]>0:
                                    if results[Constants.IMA1EMADIFF] > 0:
                                        if results[Constants.IMA1EMADIFF] > activeParam.ima1EmaMinValue:
                                            res = True, 2
                else:
                    if results[Constants.IND_BLG_UPPER_DST_PERCENT] >0 and results[Constants.IND_BLG_UPPER_DST_PERCENT]  < blgDistPercent:
                        if results[Constants.WEEK_DIR_BOT_DST] > 90:
                            if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] > 30:
                                if results[Constants.ANGLE]>0:
                                    if results[Constants.ANGLE_COUNTER] > 5:
                                        # if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff:
                                        # if self.canOpenUP_BLGDistance(results,activeParam):
                                        res = True, 3
        return  res

    def evaluateUpOpen_04(self, results,activeParam):
        res = False, 0
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference

        if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
            Constants.ACTION_MIN_DIST] >= (difference_optimized):
            if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT]==0:
                if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff:
                    if results[Constants.WEEK_DIR_BOT_DST] < 90:
                        if "UP" in self.aperturaAngle_01(results,activeParam):
                            res = True,1
        return res

    def evaluateUpOpen_05(self, results,activeParam):
        res = False, 0
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference

        if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
            Constants.ACTION_MIN_DIST] >= (difference_optimized):
            if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT]==0:
                if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff:

                    if results[Constants.WEEK_DIR_BOT_DST] < 90:
                        # isRising, angleDiff = self.isRisingAngleIma1(results)
                        # if isRising:
                            if "UP" in self.aperturaAngle_01(results,activeParam):
                                res = True,1
                    else:
                        if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                            isRising, angleDiff = self.isRisingAngle(results)
                            if isRising:
                                if results[Constants.ANGLE_IMA1]>0:
                                    if results[Constants.IMA1EMADIFF] > 0:
                                        if results[Constants.IMA1EMADIFF] > activeParam.ima1EmaMinValue:
                                            res = True, 2
            else:
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] > 0 and results[
                    Constants.IND_BLG_UPPER_DST_PERCENT] < blgDistPercent:
                    if results[Constants.WEEK_DIR_BOT_DST] > 90:
                        if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] > 30:
                            if results[Constants.ANGLE] > 0:
                                if results[Constants.ANGLE_COUNTER] > 5:
                                    # if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff:
                                    # if self.canOpenUP_BLGDistance(results,activeParam):
                                    res = True, 3
        return res

    def evaluateUpOpen_06(self, results,activeParam):
        res = False, 0
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        #control penup3


        if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
            Constants.ACTION_MIN_DIST] >= (difference_optimized):
            if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT]==0:
                if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff:

                    if results[Constants.WEEK_DIR_BOT_DST] < 90:
                        isRising, angleDiff = self.isRisingAngleIma1(results)
                        if isRising:
                            if "UP" in self.aperturaAngle_01(results,activeParam):
                                res = True,1
                    else:
                        if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                            isRising, angleDiff = self.isRisingAngle(results)
                            if isRising:
                                if results[Constants.ANGLE_IMA1]>0:
                                    if results[Constants.IMA1EMADIFF] > 0:
                                        if results[Constants.IMA1EMADIFF] > activeParam.ima1EmaMinValue:
                                            res = True, 2
            else:
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] > 0 and results[
                    Constants.IND_BLG_UPPER_DST_PERCENT] < blgDistPercent:
                    if results[Constants.WEEK_DIR_BOT_DST] > 90:
                        if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] > 30:
                            if results[Constants.ANGLE] > 0:
                                if results[Constants.ANGLE_COUNTER] > 5:
                                    isRising, angleDiff = self.isRisingAngle(results)
                                    if isRising:
                                        # if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff:
                                        # if self.canOpenUP_BLGDistance(results,activeParam):
                                        res = True, 3
        return res

    def evaluateUpOpen_07(self, results,activeParam):
        res = False, 0
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        #control penup3


        if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
            Constants.ACTION_MIN_DIST] >= (difference_optimized):
            if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT]==0:
                # if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff:

                    if results[Constants.WEEK_DIR_BOT_DST] < 90:
                        isRising, angleDiff = self.isRisingAngleIma1(results)
                        if isRising:
                            # if "UP" in self.aperturaAngle_01(results,activeParam):
                                res = True,1
                    else:
                        if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                            isRising, angleDiff = self.isRisingAngle(results)
                            if isRising:
                                if results[Constants.ANGLE_IMA1]>0:
                                    if results[Constants.IMA1EMADIFF] > 0:
                                        if results[Constants.IMA1EMADIFF] > activeParam.ima1EmaMinValue:
                                            res = True, 2
            else:
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] > 0 and results[
                    Constants.IND_BLG_UPPER_DST_PERCENT] < blgDistPercent:
                    if results[Constants.WEEK_DIR_BOT_DST] > 90:
                        if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] > 30:
                            if results[Constants.ANGLE] > 0:
                                if results[Constants.ANGLE_COUNTER] > 5:
                                    isRising, angleDiff = self.isRisingAngle(results)
                                    if isRising:
                                        # if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff:
                                        # if self.canOpenUP_BLGDistance(results,activeParam):
                                        res = True, 3
        return res

    def evaluateUpOpen_08(self, results,activeParam):
        res = False, 0
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        #control penup3


        if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
            Constants.ACTION_MIN_DIST] >= (difference_optimized):
            if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT]==0:
                # if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff:

                    if results[Constants.WEEK_DIR_BOT_DST] < 90:
                        isRising, angleDiff = self.isRisingAngleIma1(results)
                        if isRising:
                            #que no este muy arriba
                            if results[Constants.IND_BLG_MIDDLE_DST_PERCENT]<30:

                            # if "UP" in self.aperturaAngle_01(results,activeParam):
                                res = True,1
                            else:
                                if results[Constants.ANGLE] > angleUp:
                                    res = True, 1
                    else:
                        if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                            isRising, angleDiff = self.isRisingAngle(results)
                            if isRising:
                                if results[Constants.ANGLE_IMA1]>0:
                                    if results[Constants.IMA1EMADIFF] > 0:
                                        if results[Constants.IMA1EMADIFF] > activeParam.ima1EmaMinValue:
                                            res = True, 2
            else:
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] > 0 and results[
                    Constants.IND_BLG_UPPER_DST_PERCENT] < blgDistPercent:
                    if results[Constants.WEEK_DIR_BOT_DST] > 90:
                        if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] > 30:
                            if results[Constants.ANGLE] > 0:
                                if results[Constants.ANGLE_COUNTER] > 5:
                                    isRising, angleDiff = self.isRisingAngle(results)
                                    if isRising:
                                        # if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff:
                                        # if self.canOpenUP_BLGDistance(results,activeParam):
                                        res = True, 3
        return res

    def evaluateUpOpen_08_IMP01(self, results,activeParam):
        res = False, 0
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        #control penup3


        if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
            Constants.ACTION_MIN_DIST] >= (difference_optimized):
            if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT]==0:
                # if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff:

                    if results[Constants.WEEK_DIR_BOT_DST] < 90:
                        isRising, angleDiff = self.isRisingAngleIma1(results)
                        if isRising:
                            #que no este muy arriba
                            if results[Constants.IND_BLG_MIDDLE_DST_PERCENT]<30:

                            # if "UP" in self.aperturaAngle_01(results,activeParam):
                                res = True,1
                            else:
                                if results[Constants.ANGLE] > angleUp:
                                    res = True, 1
                    else:
                        if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                            isRising, angleDiff = self.isRisingAngle(results)
                            if isRising:
                                if results[Constants.ANGLE_IMA1]>0:
                                    if results[Constants.IMA1EMADIFF] > 0:
                                        if results[Constants.IMA1EMADIFF] > activeParam.ima1EmaMinValue:
                                            res = True, 2
            else:
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] > 0 and results[
                    Constants.IND_BLG_UPPER_DST_PERCENT] < blgDistPercent:
                    if results[Constants.WEEK_DIR_BOT_DST] > 90:
                        if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] > 30:
                            if results[Constants.ANGLE] > 0:
                                if results[Constants.ANGLE_COUNTER] > 5:
                                    isRising, angleDiff = self.isRisingAngle(results)
                                    if isRising:
                                        # if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff:
                                        # if self.canOpenUP_BLGDistance(results,activeParam):
                                        res = True, 3
        return res


    def evaluateChance_Ima1_01(self, results, activeParam):
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        maxAcumValue = activeParam.closeAcumvalue * 3
        res = False, "Nada", 0
        if "DOWN" in results[Constants.WEEK_FLOW]:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized):
                    difOpenHours = self.getDifTimeFromOpen(results)

                    if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(
                            results[Constants.MEDSTDDIFF]) == 0:
                        if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                            res = True, "SELL", 1


            elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
                    Constants.ACTION_MIN_DIST] >= (difference_optimized):
                    if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(
                            results[Constants.MEDSTDDIFF]) == 0:
                        if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                            res = True, "BUY", 1

        elif "UP" in results[Constants.WEEK_FLOW]:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
                    Constants.ACTION_MIN_DIST] >= (difference_optimized):
                    if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(
                            results[Constants.MEDSTDDIFF]) == 0:
                        if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                            res = True, "BUY", 2

            elif results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP):


                    if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(
                            results[Constants.MEDSTDDIFF]) == 0:
                        if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                            res = True, "SELL", 2

        else:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized):

                    if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(
                            results[Constants.MEDSTDDIFF]) == 0:
                        if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                            res = True, "SELL", 3

            elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
                    Constants.ACTION_MIN_DIST] >= (difference_optimized):

                    if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(
                            results[Constants.MEDSTDDIFF]) == 0:
                        if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                            res = True, "BUY", 3
        return  res


    def evaluateChance_Ima1_02(self, results, activeParam):
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        maxAcumValue = activeParam.closeAcumvalue * 3
        res = False, "Nada", 0

        if results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_DOWN:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized):
                    difOpenHours = self.getDifTimeFromOpen(results)
                    if difOpenHours <= 10:
                        res = True, "SELL", 1
                    else:
                        if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(
                                results[Constants.MEDSTDDIFF]) == 0:
                            if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                                res = True, "SELL", 2

            elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
                    Constants.ACTION_MIN_DIST] >= (difference_optimized):
                    if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(
                            results[Constants.MEDSTDDIFF]) == 0:
                        if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                            res = True, "BUY", 1
        elif results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_UP:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
                    Constants.ACTION_MIN_DIST] >= (difference_optimized):
                    if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(
                            results[Constants.MEDSTDDIFF]) == 0:
                        if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                            res = True, "BUY", 2
            elif results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized):
                    difOpenHours = self.getDifTimeFromOpen(results)
                    if difOpenHours <= 10:
                        res = True, "SELL", 3
                    else:
                        if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(
                                results[Constants.MEDSTDDIFF]) == 0:
                            if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                                res = True, "SELL", 4

        else:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized):
                        if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(
                                results[Constants.MEDSTDDIFF]) == 0:
                            if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                                res = True, "SELL", 5
            elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
                    Constants.ACTION_MIN_DIST] >= (difference_optimized):
                        if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(
                                results[Constants.MEDSTDDIFF]) == 0:
                            if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                                res = True, "BUY", 4

        return  res

    def evaluateDownOpen_start_close_01(self, results, activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        angleDOWN = activeParam.angleDown
        maxAcumValue = activeParam.closeAcumvalue * 3
        medstdminDiff = activeParam.medstdminDiff
        multiplicadorUP = 2
        emaMinDst = float(activeParam.emaMinDst)

        if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
            Constants.ACTION_MAX_DIST] >= (difference_optimized):
            if results[Constants.FLUJO]==Constants.FLUJO_BAJA:
                if abs(float(results[Constants.EMA_DST])) >= emaMinDst:
                    if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT] ==0:
                        if results[Constants.WEEK_FLOW] ==Constants.WEEK_FLOW_DOWN:
                            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                            res = True, "SELL", 1
                        elif results[Constants.WEEK_FLOW] ==Constants.WEEK_FLOW_UP:
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            res = True, "SELL", 2

                    elif results[Constants.IND_BLG_LOWER_DST_PERCENT] <0:
                        # if abs(results[Constants.EMA_DST]) >= self.emaMinDst:
                            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                            res = True, "SELL", 3

                    elif results[Constants.IND_BLG_LOWER_DST_PERCENT] < blgDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT]==0:
                        nada=""
                        if results[Constants.ANGLE] < 0 or results[
                            Constants.ANGLE] == 0:
                            # if abs(results[Constants.EMA_DST]) >= self.emaMinDst:
                                # BAJA
                                if abs(results[Constants.ANGLE]) > angleDOWN:
                                    results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                    res = True, "SELL", 4
                                else:
                                    if results[Constants.ANGLEm1] > 0:
                                        # esta bajando o haciendo el cambio
                                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                        res = True, "SELL", 5
            else:
                nada = ""
        return res

    def evaluateDownOpen_start_close_02(self, results, activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        angleDOWN = activeParam.angleDown
        maxAcumValue = activeParam.closeAcumvalue * 3
        medstdminDiff = activeParam.medstdminDiff
        multiplicadorUP = 2
        emaMinDst = float(activeParam.emaMinDst)
        multiplicadorOpen = 2.2

        if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
            Constants.ACTION_MAX_DIST] >= (difference_optimized):

            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if abs(results[Constants.EMA_DST]) >= emaMinDst:
                    if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgDistPercent or results[
                        Constants.IND_BLG_LOWER_DST_PERCENT] == 0:
                        if results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_DOWN:
                            # if (results[Constants.ANGLE]<0 and abs(results[Constants.ANGLE])>1) or results[Constants.ANGLE]==0:
                            # if abs(results[Constants.EMA_DST]) >= self.emaMinDst:
                            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                            res = True, "SELL", 1

                        # elif results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_UP:
                        #     results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        #     res = True, "BUY", 1

                    elif results[Constants.IND_BLG_LOWER_DST_PERCENT] < 0:
                        # if abs(results[Constants.EMA_DST]) >= self.emaMinDst:
                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                        res = True, "SELL", 2

                    elif results[Constants.IND_BLG_LOWER_DST_PERCENT] < blgDistPercent or results[
                        Constants.IND_BLG_LOWER_DST_PERCENT] == 0:
                        nada = ""
                        if results[Constants.ANGLE] < 0 or results[
                            Constants.ANGLE] == 0:
                            # if abs(results[Constants.EMA_DST]) >= self.emaMinDst:
                            # BAJA
                            if abs(results[Constants.ANGLE]) > angleDOWN:
                                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                res = True, "SELL", 3

                            else:
                                if results[Constants.ANGLEm1] > 0:
                                    # esta bajando o haciendo el cambio
                                    results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                    res = True, "SELL", 4
            else:
                nada = ""

        return res

    def evaluateUpOpen_start_close_01(self, results, activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        angleUP = activeParam.angleUp
        maxAcumValue = activeParam.closeAcumvalue * 3
        medstdminDiff = activeParam.medstdminDiff
        multiplicadorUP = 2
        emaMinDst = activeParam.emaMinDst

        if results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or results[
            Constants.ACTION_MIN_DIST] >= (difference_optimized * multiplicadorUP):
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if abs(float(results[Constants.EMA_DST])) >= emaMinDst:
                    if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgDistPercent or results[
                        Constants.IND_BLG_UPPER_DST_PERCENT] == 0:
                        res = True, "BUY", 1
                    elif results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        res = True, "BUY", 2

                    elif results[Constants.IND_BLG_UPPER_DST_PERCENT] < blgDistPercent or results[
                        Constants.IND_BLG_UPPER_DST_PERCENT] == 0:
                        nada = ""
                        if results[Constants.ANGLE] > 0 or results[
                            Constants.ANGLE] == 0:
                            # SUBE
                            if abs(results[Constants.ANGLE]) > angleUP:
                                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                res = True, "BUY", 3
                            else:
                                if results[Constants.ANGLEm1] < 0:
                                    # esta subiendo o haciendo el cambio
                                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                    res = True, "BUY", 4
            else:

                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                res = True, "SELL", 1

        return res

    def evaluateUpOpen_start_close_02(self, results, activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        angleUP = activeParam.angleUp
        maxAcumValue = activeParam.closeAcumvalue * 3
        medstdminDiff = activeParam.medstdminDiff
        multiplicadorUP = 2
        emaMinDst = activeParam.emaMinDst

        # if results[Constants.IMA1_DISTANCE] >= self.ima1minDistance:
        if results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or results[
            Constants.ACTION_MIN_DIST] >= (difference_optimized * multiplicadorUP):

            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                # if abs(results[Constants.EMA_DST]) >= emaMinDst:
                    if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgDistPercent or results[
                        Constants.IND_BLG_UPPER_DST_PERCENT] == 0:

                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        res = True, "BUY", 1

                    elif results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        res = True, "BUY", 2

                    elif results[Constants.IND_BLG_UPPER_DST_PERCENT] < blgDistPercent or results[
                        Constants.IND_BLG_UPPER_DST_PERCENT] == 0:
                        nada = ""
                        if results[Constants.ANGLE] > 0 or results[
                            Constants.ANGLE] == 0:
                            # SUBE
                            if abs(results[Constants.ANGLE]) > angleUP:
                                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                res = True, "BUY", 3

                            else:
                                if results[Constants.ANGLEm1] < 0:
                                    # esta subiendo o haciendo el cambio
                                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                    res = True, "BUY", 4
            else:
                # BAJA
                nada = ""

                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                res = True, "SELL", 1

        return res

    def evaluateUpOpen_start_close_03(self, results, activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        angleUP = activeParam.angleUp
        maxAcumValue = activeParam.closeAcumvalue * 3
        medstdminDiff = activeParam.medstdminDiff
        multiplicadorUP = 2
        emaMinDst = activeParam.emaMinDst

        # if results[Constants.IMA1_DISTANCE] >= self.ima1minDistance:
        if results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or results[
            Constants.ACTION_MIN_DIST] >= (difference_optimized * multiplicadorUP):

            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                # if abs(results[Constants.EMA_DST]) >= emaMinDst:
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgDistPercent or results[
                    Constants.IND_BLG_UPPER_DST_PERCENT] == 0:
                    # if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff:

                    if results[Constants.WEEK_DIR_BOT_DST] < 90:
                        isRising, angleDiff = self.isRisingAngleIma1(results)
                        if isRising:
                            if "UP" in results[Constants.ANGLE_FLOW]:
                                # que no este muy arriba
                                if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] < 5:
                                    res = True, "BUY", 1
                                else:
                                    if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] < 20:
                                        if results[Constants.ANGLE] > 0:
                                            # if "UP" in self.aperturaAngle_01(results,activeParam):
                                            res = True, "BUY", 2
                                    else:
                                        if angleDiff > angleUP:
                                            if results[Constants.ANGLE] > angleUP:
                                                res = True, "BUY", 3
                    else:
                        if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                            isRising, angleDiff = self.isRisingAngle(results)
                            if isRising:
                                if results[Constants.ANGLE_IMA1] > 0:
                                    if results[Constants.IMA1EMADIFF] > 0:
                                        if results[Constants.IMA1EMADIFF] > activeParam.ima1EmaMinValue:
                                            res = True, "BUY", 4
                else:
                    if results[Constants.IND_BLG_UPPER_DST_PERCENT] > 0 and results[
                        Constants.IND_BLG_UPPER_DST_PERCENT] < blgDistPercent:
                        if results[Constants.WEEK_DIR_BOT_DST] > 90:
                            if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] > 30:
                                if results[Constants.ANGLE] > 0:
                                    if results[Constants.ANGLE_COUNTER] > 5:
                                        isRising, angleDiff = self.isRisingAngle(results)
                                        if isRising:
                                            # if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff:
                                            # if self.canOpenUP_BLGDistance(results,activeParam):
                                            res = True, "BUY", 5
            else:
                # BAJA
                nada = ""

                # results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                # res = True, "SELL", 1

        return res

    def evaluateDownOpen_BLG_02(self, results,activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        multiplicadorUP = 2

        if (abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) ==0) and abs(results[Constants.MEDSTDDIFF]) < medstdmaxDiff:
            # if results[Constants.INDICATOR_MED]==Constants.INDICATOR_TM_DOWN:
                if results[Constants.IND_BLG] == Constants.IND_BLG_MED_BUY:
                    ##ESTAMOS SOBRE LA MEDIA
                    if results[Constants.ACUMULADO] < 0:
                        if results[Constants.MEDSTDDIFF] < 0:
                            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                            res = True, "SELL", 1
                    else:
                        if results[Constants.MEDSTDDIFF] > 0:
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            res = True, "BUY", 1

                else:
                    ##ESTAMOS BAJO LA MEDIA
                    if results[Constants.IND_BLG_LOWER_DST] < self.blgLowerDist:
                        if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or
                                results[Constants.ACTION_MAX_DIST] >= (
                                        difference_optimized * self.multiplicadorUP)):
                            if results[Constants.ACUMULADO] < 0:
                                if results[Constants.MEDSTDDIFF] < 0:
                                    results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                    res = True, "SELL", 2

                            else:
                                if results[Constants.MEDSTDDIFF] >0:
                                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                    res = True, "BUY", 2

                    else:
                        if results[Constants.ACUMULADO] > 0:
                            if results[Constants.MEDSTDDIFF] > 0:
                                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                res = True, "BUY", 3
        return res

    def evaluateUpOpen_EMA_WEEK_OUP_01(self, results,activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        multiplicadorUP= 1
        blgLowerDistPercent = 10

        # isRising, angleDiff = self.isRisingFromWEEKNEW(results)
        isRising, angleDiff = self.isRisingFromWEEK(results)
        if isRising:
            if angleDiff >0 and (angleDiff > closeWeekDiffNew/2):
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgLowerDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
                    if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                            results[Constants.ACTION_MIN_DIST] >= (
                                    difference_optimized * multiplicadorUP)):
                        if results[Constants.ACUMULADO] > 0:
                            # if results[Constants.MEDSTDDIFF] > 0:
                                # if results[Constants.WEEK_DIR_BOT_DST] <= 90:
                                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                    res = True, "BUY", 1
        else:
            #inversa
            print(f" isrising INV: {isRising} angleDiff: {angleDiff}")
            if angleDiff < 0 and (abs(angleDiff) > closeWeekDiffNew):
                if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgLowerDistPercent or results[
                    Constants.IND_BLG_LOWER_DST_PERCENT] < 0:
                    if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                            results[Constants.ACTION_MAX_DIST] >= (
                                    difference_optimized * multiplicadorUP)):
                        if results[Constants.ACUMULADO] < 0:
                            # if results[Constants.MEDSTDDIFF] < 0:
                                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                res = True, "SELL", 1

        return res
    def evaluateDownOpen_BLG_03(self, results,activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        multiplicadorUP = 1
        blgLowerDistPercent = 20

        if results[Constants.ANGLE_FLOW] == Constants.DIR_DOWN:
        # if results[Constants.IMA1EMADIFF] <0:
            if results[Constants.IND_BLG] == Constants.IND_BLG_MED_BUY:
                ##ESTAMOS SOBRE LA MEDIA
                nada = ""
                # if results[Constants.ACUMULADO] < 0:
                #     if results[Constants.MEDSTDDIFF] < 0:
                #         results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                #         res = True, "BUY", 1

            else:
                ##ESTAMOS BAJO LA MEDIA
                if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgLowerDistPercent:
                    if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                            results[Constants.ACTION_MAX_DIST] >= (
                                    difference_optimized * multiplicadorUP)):
                        if results[Constants.ACUMULADO] < 0:
                            if results[Constants.MEDSTDDIFF] < 0:
                                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                res = True, "SELL", 1
                        else:
                            nada = ""
                            # if results[Constants.MEDSTDDIFF] > 0:
                            #     results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            #     res = True, "BUY", 1


        return res

    def evaluateDownOpen_EMA_01(self, results,activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        multiplicadorUP = 1
        blgLowerDistPercent = 5

        # isRising, angleDiff = self.isRisingAngle(results)
        # if not isRising:
        if results[Constants.BLG_MA_X]<0:

                if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgLowerDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT]< 0:
                    if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                            results[Constants.ACTION_MAX_DIST] >= (
                                    difference_optimized * multiplicadorUP)):
                        if results[Constants.ACUMULADO] < 0:
                            if results[Constants.MEDSTDDIFF] < 0:
                                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                res = True, "SELL", 1

        return res

    def evaluateDownOpen_EMA_04(self, results,activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        multiplicadorUP = 1
        blgLowerDistPercent = 5
        angleEma20 = results[Constants.ANGLE_EMA20]

        # isRising, angleDiff = self.isRisingAngle(results)
        # if not isRising:
        if angleEma20<0:

                if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgLowerDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT]< 0:
                    if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                            results[Constants.ACTION_MAX_DIST] >= (
                                    difference_optimized * multiplicadorUP)):
                        # if results[Constants.ACUMULADO] < 0:
                        #     if results[Constants.MEDSTDDIFF] < 0:
                                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                res = True, "SELL", 1

        return res

    def evaluateDownOpen_EMA_02(self, results, activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        multiplicadorUP = 1
        blgLowerDistPercent = 5

        # isRising, angleDiff = self.isRisingAngle(results)
        # if not isRising:
        if results[Constants.BLG_MA_X] <= 0:

            if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgLowerDistPercent or results[
                Constants.IND_BLG_LOWER_DST_PERCENT] < 0:
                if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                        results[Constants.ACTION_MAX_DIST] >= (
                                difference_optimized * multiplicadorUP)):
                    if results[Constants.ACUMULADO] < 0:
                        # if results[Constants.MEDSTDDIFF] < 0:
                            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                            res = True, "SELL", 1

        return res
    def evaluateDownOpen_RSI_01(self, results, activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        multiplicadorUP = 1
        blgLowerDistPercent = 5

        # isRising, angleDiff = self.isRisingAngle(results)
        isRising = False
        if not isRising:
                if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                        results[Constants.ACTION_MAX_DIST] >= (
                                difference_optimized * multiplicadorUP)):
                    if results[Constants.ACUMULADO] < 0:
                        # if results[Constants.MEDSTDDIFF] < 0:
                            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                            res = True, "SELL", 1

        return res

    def evaluateDownOpen_EMA_03(self, results, activeParam):
        res = False, "NADA", 0
        #abrir cuanto antes pero con controles max min
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
        # if results[Constants.BLG_MA_X] < 1:
            if not isRisingIma1:

                if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgLowerDistPercent or results[
                    Constants.IND_BLG_LOWER_DST_PERCENT] < 0:
                    if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                            results[Constants.ACTION_MAX_DIST] >= (
                                    difference_optimized * multiplicadorUP)):
                        if results[Constants.ACUMULADO] < 0:
                            if results[Constants.ACTION_MIN_DIST]<results[Constants.ACTION_MAX_DIST]:
                            # if results[Constants.MEDSTDDIFF] < 0:

                                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                res = True, "SELL", 1
            else:
                #inversa
                nada = ""
                if results[Constants.ACTION_MAX_DIST] < results[Constants.ACTION_MIN_DIST]:
                # if results[Constants.ACTION_MAX_DIST] >=3:
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                    res = True, "BUY", 1

        return res

    def evaluateDownOpen_EMA_WEEK_01(self, results, activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        blg_mid_dst_perc = results[Constants.IND_BLG_MIDDLE_DST_PERCENT]
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        multiplicadorUP = 1
        blgLowerDistPercent = 5

        # isRising, angleDiff = self.isRisingAngle(results)
        # if not isRising:
        # isRising, angleDiff = self.isRisingFromWEEKNEW(results)
        isRising, angleDiff = self.isRisingFromMonth(results)
        # isRising, angleDiff = self.isRisingFromWEEK(results)
        if not isRising:
            print(f" isrising: {isRising} angleDiff: {angleDiff}")
            if angleDiff <0 and (abs(angleDiff) > closeWeekDiffNew / 2):

                if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgLowerDistPercent or results[
                    Constants.IND_BLG_LOWER_DST_PERCENT] < 0:
                    if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                            results[Constants.ACTION_MAX_DIST] >= (
                                    difference_optimized * multiplicadorUP)):
                        if results[Constants.ACUMULADO] < 0:
                            # if results[Constants.MEDSTDDIFF] < 0:
                            #     results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                res = True, "SELL", 1
        else:
            #inversa
            print(f" isrising INV: {isRising} angleDiff: {angleDiff}")
            if angleDiff > 0 and (abs(angleDiff) > closeWeekDiffNew):
                if blg_mid_dst_perc <0 or (blg_mid_dst_perc >0 and blg_mid_dst_perc < 10):
                    if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgLowerDistPercent or results[
                        Constants.IND_BLG_LOWER_DST_PERCENT] < 0:
                        if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                                results[Constants.ACTION_MIN_DIST] >= (
                                        difference_optimized * multiplicadorUP)):
                            if results[Constants.ACUMULADO] > 0:
                                # if results[Constants.MEDSTDDIFF] < 0:
                                #     results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                    res = True, "BUY", 1

        return res

    def evaluateDownOpen_EMA_WEEK_02(self, results, activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        blg_mid_dst_perc = results[Constants.IND_BLG_MIDDLE_DST_PERCENT]
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        multiplicadorUP = 1
        blgLowerDistPercent = -10
        blgLowerInvMaxDistPercent = 40#no abrir si es inversa y esta sobre este valor
        ima5ma20 = results[Constants.IMA5MA20]

        # isRising, angleDiff = self.isRisingAngle(results)
        # if not isRising:
        # isRising, angleDiff = self.isRisingFromWEEKNEW(results)
        isRising, angleDiff = self.isRisingFromMonth(results)
        # isRising, angleDiff = self.isRisingFromWEEK(results)
        if not isRising:
            print(f" isrising: {isRising} angleDiff: {angleDiff}")
            if angleDiff < 0 and (abs(angleDiff) > closeWeekDiffNew / 2):
                if ima5ma20 == Constants.INDICATOR_EMA_SELL:
                    if (results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgLowerDistPercent)  and results[
                        Constants.IND_BLG_LOWER_DST_PERCENT] > 0:
                        if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                                results[Constants.ACTION_MAX_DIST] >= (
                                        difference_optimized * multiplicadorUP)):
                            if results[Constants.ACUMULADO] < 0:
                                # if results[Constants.MEDSTDDIFF] < 0:
                                #     results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                res = True, "SELL", 1
        else:
            # inversa
            print(f" isrising INV: {isRising} angleDiff: {angleDiff}")
            if angleDiff > 0 and (abs(angleDiff) > closeWeekDiffNew):
                # if blg_mid_dst_perc < 0 or (blg_mid_dst_perc > 0 and blg_mid_dst_perc < 10):
                    if (results[Constants.IND_BLG_LOWER_DST_PERCENT] < blgLowerInvMaxDistPercent) or ima5ma20 == Constants.INDICATOR_EMA_BUY:
                        if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                                results[Constants.ACTION_MIN_DIST] >= (
                                        difference_optimized * multiplicadorUP)):
                            if results[Constants.ACUMULADO] > 0:
                                # if results[Constants.MEDSTDDIFF] < 0:
                                #     results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                res = True, "BUY", 1

        return res

    def evaluateDownOpen_EMA_WEEK_NEW_FLOW_01(self, results, activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        blg_mid_dst_perc = results[Constants.IND_BLG_MIDDLE_DST_PERCENT]
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        multiplicadorUP = 1
        blgLowerDistPercent = -10
        blgLowerInvMaxDistPercent = 40#no abrir si es inversa y esta sobre este valor
        ima5ma20 = results[Constants.IMA5MA20]

        # isRising, angleDiff = self.isRisingAngle(results)
        # if not isRising:
        isRising, angleDiff = self.isRisingFromWEEKNEW(results)
        # isRising, angleDiff = self.isRisingFromMonth(results)
        # isRising, angleDiff = self.isRisingFromWEEK(results)
        if not isRising:
            # print(f" isrising: {isRising} angleDiff: {angleDiff}")
            if angleDiff < 0 and (abs(angleDiff) > closeWeekDiffNew / 2):
                if ima5ma20 == Constants.INDICATOR_EMA_SELL:
                    if (results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgLowerDistPercent)  and results[
                        Constants.IND_BLG_LOWER_DST_PERCENT] > 0:
                        if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                                results[Constants.ACTION_MAX_DIST] >= (
                                        difference_optimized * multiplicadorUP)):
                            if results[Constants.ACUMULADO] < 0:
                                # if results[Constants.MEDSTDDIFF] < 0:
                                #     results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                res = True, "SELL", 1
        else:
            # inversa
            print(f" isrising INV: {isRising} angleDiff: {angleDiff}")
            if angleDiff > 0 and (abs(angleDiff) > closeWeekDiffNew):
                # if blg_mid_dst_perc < 0 or (blg_mid_dst_perc > 0 and blg_mid_dst_perc < 10):
                    if (results[Constants.IND_BLG_LOWER_DST_PERCENT] < blgLowerInvMaxDistPercent) or ima5ma20 == Constants.INDICATOR_EMA_BUY:
                        if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                                results[Constants.ACTION_MIN_DIST] >= (
                                        difference_optimized * multiplicadorUP)):
                            if results[Constants.ACUMULADO] > 0:
                                # if results[Constants.MEDSTDDIFF] < 0:
                                #     results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                res = True, "BUY", 1

        return res

    def evaluateDownOpen_EMA_WEEK_NEW_FLOW_02(self, results, activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        blg_mid_dst_perc = results[Constants.IND_BLG_MIDDLE_DST_PERCENT]
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        multiplicadorUP = 1
        blgLowerDistPercent = -10
        blgLowerInvMaxDistPercent = 55  # no abrir si es inversa y esta sobre este valor
        ima5ma20 = results[Constants.IMA5MA20]

        # isRising, angleDiff = self.isRisingAngle(results)
        # if not isRising:
        isRising, angleDiff = self.isRisingFromWEEKNEW(results)
        # isRising, angleDiff = self.isRisingFromMonth(results)
        # isRising, angleDiff = self.isRisingFromWEEK(results)
        if not isRising:
            # print(f" isrising: {isRising} angleDiff: {angleDiff}")
            if angleDiff < 0 and (abs(angleDiff) > closeWeekDiffNew / 2):
                if ima5ma20 == Constants.INDICATOR_EMA_SELL:
                    if (results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgLowerDistPercent) and results[
                        Constants.IND_BLG_LOWER_DST_PERCENT] > 0:
                        if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                                results[Constants.ACTION_MAX_DIST] >= (
                                        difference_optimized * multiplicadorUP)):
                            if results[Constants.ACUMULADO] < 0:
                                # if results[Constants.MEDSTDDIFF] < 0:
                                #     results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                res = True, "SELL", 1
        else:
            # inversa
            print(f" isrising INV: {isRising} angleDiff: {angleDiff}")
            if angleDiff > 0 and (abs(angleDiff) > closeWeekDiffNew):
                # if blg_mid_dst_perc < 0 or (blg_mid_dst_perc > 0 and blg_mid_dst_perc < 10):
                if (results[Constants.IND_BLG_LOWER_DST_PERCENT] < blgLowerInvMaxDistPercent):  # or ima5ma20 == Constants.INDICATOR_EMA_BUY:
                    if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                            results[Constants.ACTION_MIN_DIST] >= (
                                    difference_optimized * multiplicadorUP)):
                        if results[Constants.ACUMULADO] > 0:
                            # if results[Constants.MEDSTDDIFF] < 0:
                            #     results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            res = True, "BUY", 1

        return res

    def evaluateDownOpen_EMA_WEEK_NEW_FLOW_03(self, results, activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        blg_mid_dst_perc = results[Constants.IND_BLG_MIDDLE_DST_PERCENT]
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        multiplicadorUP = 1
        blgLowerDistPercent = -10
        blgLowerInvMaxDistPercent = 40#no abrir si es inversa y esta sobre este valor
        ima5ma20 = results[Constants.IMA5MA20]

        # isRising, angleDiff = self.isRisingAngle(results)
        # if not isRising:
        isRising, angleDiff = self.isRisingFromWEEKNEW(results)
        # isRising, angleDiff = self.isRisingFromMonth(results)
        # isRising, angleDiff = self.isRisingFromWEEK(results)
        if not isRising:
            # print(f" isrising: {isRising} angleDiff: {angleDiff}")
            if angleDiff < 0 and (abs(angleDiff) > closeWeekDiffNew / 2):
                if ima5ma20 == Constants.INDICATOR_EMA_SELL or ima5ma20== Constants.INDICATOR_EMA_WAIT:
                    if (results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgLowerDistPercent)  and results[
                        Constants.IND_BLG_LOWER_DST_PERCENT] >= 0:
                        if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                                results[Constants.ACTION_MAX_DIST] >= (
                                        difference_optimized * multiplicadorUP)):
                            if results[Constants.ACUMULADO] < 0:
                                # if results[Constants.MEDSTDDIFF] < 0:
                                #     results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                res = True, "SELL", 1
        else:
            # inversa
            # print(f" isrising INV: {isRising} angleDiff: {angleDiff}")
            if angleDiff > 0 and (abs(angleDiff) > closeWeekDiffNew):
                # if blg_mid_dst_perc < 0 or (blg_mid_dst_perc > 0 and blg_mid_dst_perc < 10):
                    if (results[Constants.IND_BLG_LOWER_DST_PERCENT] < blgLowerInvMaxDistPercent) or ima5ma20 == Constants.INDICATOR_EMA_BUY:
                        if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                                results[Constants.ACTION_MIN_DIST] >= (
                                        difference_optimized * multiplicadorUP)):
                            if results[Constants.ACUMULADO] > 0:
                                # if results[Constants.MEDSTDDIFF] < 0:
                                #     results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                res = True, "BUY", 1

        return res
    def evaluateDownOpen_EMA_OUP_01(self, results, activeParam):
        res = False, "NADA", 0
        #abrir cuanto antes pero con controles max min
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
        # isRising, angleDiff = self.isRisingFromWEEKNEW(results)
        if isRising:
                #inversa
                nada = ""
                if ema_dst > min_ema_dst:
                    if angleDiff > 0 and (abs(angleDiff) >=closeWeekDiffNew):
                        if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                                results[Constants.ACTION_MIN_DIST] >= (
                                        difference_optimized * multiplicadorUP)):
                            if results[Constants.ACUMULADO] > 0:
                            # if results[Constants.ACTION_MAX_DIST] >=3:
                                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                res = True, "BUY", 1

        return res

    def evaluateDownOpen_EMA_OUP_03(self, results, activeParam):
        res = False, "NADA", 0
        # abrir cuanto antes pero con controles max min
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

        if (abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) ==0) and abs(results[Constants.MEDSTDDIFF]) < medstdmaxDiff:
            # if results[Constants.INDICATOR_MED]==Constants.INDICATOR_TM_DOWN:
                if results[Constants.IND_BLG] == Constants.IND_BLG_MED_BUY:
                    ##ESTAMOS SOBRE LA MEDIA
                    if results[Constants.ACUMULADO] < 0:
                        if results[Constants.MEDSTDDIFF] < 0:
                            # results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                            # print(
                            #     f" INICIO MERCADO {results[Constants.DATE].values[0]} DOWN_DOWN_SELL01 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} IND_BLG_UPPER_DST_PERCENT: {results[Constants.IND_BLG_UPPER_DST_PERCENT]} angle: {results[Constants.ANGLE]} direction {results[Constants.DIRECTION]} INDICATOR_MED_MOMENT {results[Constants.INDICATOR_MED_MOMENT]} ")
                            results[Constants.CLOSE_NXT_DOWN] = 0
                            results[Constants.CLOSE_NXT_UP] = 0

                    else:
                        if results[Constants.MEDSTDDIFF] > 0:
                            if results[Constants.DIRECTION]==Constants.DIR_UP or results[Constants.DIRECTION]==Constants.DIR_PRE_UP or results[
                                            Constants.DIRECTION] == Constants.DIR_CHANGE:
                                if results[Constants.IND_BLG_UPPER_DST_PERCENT] > blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] <0:
                                    # results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                    res = True, "BUY", 1


                            results[Constants.CLOSE_NXT_DOWN] = 0
                            results[Constants.CLOSE_NXT_UP] = 0

                else:
                    ##ESTAMOS BAJO LA MEDIA
                    if results[Constants.IND_BLG_UPPER_DST_PERCENT] > blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] <0:
                        if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                                results[Constants.ACTION_MAX_DIST] >= (
                                        difference_optimized * multiplicadorUP)):
                            if results[Constants.ACUMULADO] < 0:
                                if results[Constants.MEDSTDDIFF] < 0:
                                    # results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                    # print(f" INICIO MERCADO {results[Constants.DATE].values[0]} DOWN_DOWN_SELL02 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} IND_BLG_UPPER_DST_PERCENT: {results[Constants.IND_BLG_UPPER_DST_PERCENT]} angle: {results[Constants.ANGLE]} direction {results[Constants.DIRECTION]} INDICATOR_MED_MOMENT {results[Constants.INDICATOR_MED_MOMENT]} ")
                                    results[Constants.CLOSE_NXT_DOWN] = 0
                                    results[Constants.CLOSE_NXT_UP] = 0

                            else:
                                # if results[Constants.MEDSTDDIFF] >0:
                                #     if results[Constants.DIRECTION] == Constants.DIR_UP or results[
                                #         Constants.DIRECTION] == Constants.DIR_PRE_UP or results[
                                #             Constants.DIRECTION] == Constants.DIR_CHANGE:
                                if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_UP:
                                    # if results[Constants.IND_BLG_UPPER_DST_PERCENT] > self.blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] <0:
                                    res = True, "BUY", 2

                                results[Constants.CLOSE_NXT_UP] = 0

                    else:
                        nada=""
                        if results[Constants.ACUMULADO] > 0:
                            if results[Constants.MEDSTDDIFF] > 0:
                                # results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                # print(
                                #     f" INICIO MERCADO {results[Constants.DATE].values[0]} DOWN_DOWN_SELLBUY04 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} IND_BLG_UPPER_DST_PERCENT: {results[Constants.IND_BLG_UPPER_DST_PERCENT]} angle: {results[Constants.ANGLE]} direction {results[Constants.DIRECTION]} INDICATOR_MED_MOMENT {results[Constants.INDICATOR_MED_MOMENT]} ")
                                results[Constants.CLOSE_NXT_DOWN] = 0
                                results[Constants.CLOSE_NXT_UP] = 0
        return res

    def evaluateDownOpen_EMA_OUP_02(self, results, activeParam):
        res = False, "NADA", 0
        #abrir cuanto antes pero con controles max min
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
        # isRising, angleDiff = self.isRisingFromWEEKNEW(results)
        if isRising:
                #inversa
                nada = ""
                if imaemadst > 0 and imaemadst >=ima1EmaMinValue:
                    if angleDiff > 0 and (abs(angleDiff) >=closeWeekDiffNew):
                        if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                                results[Constants.ACTION_MIN_DIST] >= (
                                        difference_optimized * multiplicadorUP)):
                            # if results[Constants.ACUMULADO] > 0:
                            # if results[Constants.ACTION_MAX_DIST] >=3:
                            #     results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                res = True, "BUY", 1

        return res
    def evaluateUpOpen_BLG_01(self, results,activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUP = activeParam.angleUp
        medstdminDiff = activeParam.medstdminDiff
        multiplicadorUP = 2

        # if results[Constants.IMA1_DISTANCE] >= self.ima1minDistance:
        if results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or results[
            Constants.ACTION_MIN_DIST] >= (difference_optimized * multiplicadorUP):

            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgDistPercent or results[
                    Constants.IND_BLG_UPPER_DST_PERCENT] == 0:
                    if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff:
                        res = True, "BUY",1
                elif results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
                    res = True, "BUY", 2

                elif results[Constants.IND_BLG_UPPER_DST_PERCENT] < blgDistPercent or results[
                    Constants.IND_BLG_UPPER_DST_PERCENT] == 0:
                    nada = ""
                    if results[Constants.ANGLE] > 0 or results[
                        Constants.ANGLE] == 0:
                        # SUBE
                        if abs(results[Constants.ANGLE]) > angleUP:
                            res = True, "BUY", 3
                        else:
                            if results[Constants.ANGLEm1] < 0:
                                res = True, "BUY", 4
            else:
                # BAJA
                nada = ""
                if abs(results[Constants.MEDSTDDIFF]) > self.medstdminDiff:
                    res = True, "SELL", 1
        return res


    def evaluateUpOpen_BLG_02(self, results,activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        medstdminDiff = activeParam.medstdminDiff
        multiplicadorUP = 2

        if (abs(results[Constants.MEDSTDDIFF]) > self.medstdminDiff or abs(results[Constants.MEDSTDDIFF]) ==0) and abs(results[Constants.MEDSTDDIFF]) < self.medstdmaxDiff:
            # if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_UP:
                if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
                # if results[Constants.IND_BLG_UPPER_DST] >= self.BLGDist:
                #     if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or
                #             results[Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP)):
                       if results[Constants.ACUMULADO] > 0:
                           if results[Constants.MEDSTDDIFF] > 0:
                                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                res = True, "BUY", 1

                       else:
                           nada = ""
                           if results[Constants.MEDSTDDIFF] < 0:
                               results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                               res = True, "SELL", 1

                else:
                    ##ESTAMOS SOBRE LA MEDIA
                    # if results[Constants.IND_BLG_UPPER_DST] < self.blgLowerDist:
                        if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or
                                results[Constants.ACTION_MIN_DIST] >= (
                                        difference_optimized * self.multiplicadorUP)):
                            if results[Constants.ACUMULADO] > 0:
                                #sube
                                if results[Constants.CLOSE_NXT_DOWN]==0:
                                    #que no este con la marca de cerrar proxima bajada
                                    if results[Constants.MEDSTDDIFF] > 0:
                                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                        res = True, "BUY", 2
                                else:
                                    if results[Constants.MEDSTDDIFF] < 0:
                                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                        res = True, "SELL", 2
                            else:
                                if results[Constants.ACUMULADO] < 0:
                                    if results[Constants.MEDSTDDIFF] < 0:
                                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                        res = True, "SELL", 3

        return res

    def evaluateUpOpen_BLG_03(self, results,activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        multiplicadorUP= 1
        blgLowerDistPercent = 10

        isRising, angleDiff = self.isRisingAngle(results)
        if isRising:
        # if (abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0) and abs(
        #         results[Constants.MEDSTDDIFF]) < medstdmaxDiff:
        #     if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_UP:
                if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
                    if results[Constants.ACUMULADO] > 0:
                        if results[Constants.MEDSTDDIFF] > 0:
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            res = True, "BUY", 1
                    else:
                        nada = ""
                else:
                    ##ESTAMOS SOBRE LA MEDIA
                    # if results[Constants.IND_BLG_UPPER_DST] < blgLowerDist:
                    if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgLowerDistPercent:
                        if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                                results[Constants.ACTION_MIN_DIST] >= (
                                        difference_optimized * multiplicadorUP)):
                            if results[Constants.ACUMULADO] > 0:
                                if results[Constants.MEDSTDDIFF] > 0:
                                    if results[Constants.WEEK_DIR_BOT_DST]<=90:
                                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                        res = True, "BUY", 2
                            else:
                                nada = ""
                                # if results[Constants.MEDSTDDIFF] < 0:
                                #     results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                #     res = True, "SELL", 1

        return res


    def evaluateUpOpen_EMA_01(self, results,activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        multiplicadorUP= 1
        blgLowerDistPercent = 10

        isRising, angleDiff = self.isRisingAngle(results)
        if isRising:
        # if results[Constants.BLG_MA_X] > 0:
            if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgLowerDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
                if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                        results[Constants.ACTION_MIN_DIST] >= (
                                difference_optimized * multiplicadorUP)):
                    if results[Constants.ACUMULADO] > 0:
                        if results[Constants.MEDSTDDIFF] > 0:
                            # if results[Constants.WEEK_DIR_BOT_DST] <= 90:
                                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                res = True, "BUY", 1

        return res

    def evaluateUpOpen_EMA_05(self, results,activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        multiplicadorUP= 1
        blgLowerDistPercent = 10
        angleEma20 = results[Constants.ANGLE_EMA20]

        # isRising, angleDiff = self.isRisingAngle(results)
        # if isRising:
        if angleEma20 > 0:
        # if results[Constants.BLG_MA_X] > 0:
            if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgLowerDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
                if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                        results[Constants.ACTION_MIN_DIST] >= (
                                difference_optimized * multiplicadorUP)):
                    # if results[Constants.ACUMULADO] > 0:
                    #     if results[Constants.MEDSTDDIFF] > 0:
                            # if results[Constants.WEEK_DIR_BOT_DST] <= 90:
                                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                res = True, "BUY", 1

        return res

    def evaluateUpOpen_EMA_02(self, results,activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        multiplicadorUP= 1
        blgLowerDistPercent = 10

        # isRising, angleDiff = self.isRisingAngle(results)
        # if isRising:
        if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgLowerDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] <0:
            if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                    results[Constants.ACTION_MIN_DIST] >= (
                            difference_optimized * multiplicadorUP)):
                if results[Constants.ACUMULADO] > 0:
                    # if results[Constants.ANGLE_FLOW] != Constants.DIR_DOWN:
                    # if results[Constants.ANGLE_FLOW] == Constants.DIR_UP:
                    #     if results[Constants.BLG_MA_X] > 0:
                                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                res = True, "BUY", 1

        return res


    def evaluateUpOpen_EMA_03(self, results,activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        multiplicadorUP= 1
        blgLowerDistPercent = 10

        isRising, angleDiff = self.isRisingAngle(results)
        if isRising:
        # if results[Constants.BLG_MA_X] > 0:
            if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgLowerDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
                if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                        results[Constants.ACTION_MIN_DIST] >= (
                                difference_optimized * multiplicadorUP)):
                    if results[Constants.ACUMULADO] > 0:
                        # if results[Constants.MEDSTDDIFF] > 0:
                            # if results[Constants.WEEK_DIR_BOT_DST] <= 90:
                                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                res = True, "BUY", 1

        return res

    def evaluateUpOpen_RSI_01(self, results,activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        multiplicadorUP= 1
        blgLowerDistPercent = 10

        # isRising, angleDiff = self.isRisingAngle(results)
        isRising = True
        if isRising:
        # if results[Constants.BLG_MA_X] > 0:
        #     if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgLowerDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
                if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                        results[Constants.ACTION_MIN_DIST] >= (
                                difference_optimized * multiplicadorUP)):
                    if results[Constants.ACUMULADO] > 0:
                        # if results[Constants.MEDSTDDIFF] > 0:
                            # if results[Constants.WEEK_DIR_BOT_DST] <= 90:
                                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                res = True, "BUY", 1

        return res

    def evaluateUpOpen_EMA_WEEK_01(self, results,activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        multiplicadorUP= 1
        blgLowerDistPercent = 10

        # isRising, angleDiff = self.isRisingFromWEEKNEW(results)
        isRising, angleDiff = self.isRisingFromWEEK(results)
        if isRising:
        # if results[Constants.BLG_MA_X] > 0:
            if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgLowerDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
                if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                        results[Constants.ACTION_MIN_DIST] >= (
                                difference_optimized * multiplicadorUP)):
                    if results[Constants.ACUMULADO] > 0:
                        # if results[Constants.MEDSTDDIFF] > 0:
                            # if results[Constants.WEEK_DIR_BOT_DST] <= 90:
                                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                res = True, "BUY", 1

        return res
    def evaluateUpOpen_EMA_WEEK_02(self, results,activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        multiplicadorUP= 1
        blgLowerDistPercent = 10

        # isRising, angleDiff = self.isRisingFromWEEKNEW(results)
        isRising, angleDiff = self.isRisingFromWEEK(results)
        if isRising:
            if angleDiff > closeWeekDiffNew/2:
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgLowerDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
                    if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                            results[Constants.ACTION_MIN_DIST] >= (
                                    difference_optimized * multiplicadorUP)):
                        if results[Constants.ACUMULADO] > 0:
                            # if results[Constants.MEDSTDDIFF] > 0:
                                # if results[Constants.WEEK_DIR_BOT_DST] <= 90:
                                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                    res = True, "BUY", 1

        return res

    def evaluateUpOpen_EMA_WEEK_03(self, results,activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        multiplicadorUP= 1
        blgLowerDistPercent = 10

        isRising, angleDiff = self.isRisingFromMonth(results)
        # isRising, angleDiff = self.isRisingFromWEEK(results)
        # isRising, angleDiff = self.isRisingFromWEEKNEW(results)
        if isRising:
            if angleDiff >0 and (angleDiff > closeWeekDiffNew/2):
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgLowerDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
                    if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                            results[Constants.ACTION_MIN_DIST] >= (
                                    difference_optimized * multiplicadorUP)):
                        if results[Constants.ACUMULADO] > 0:
                            # if results[Constants.MEDSTDDIFF] > 0:
                                # if results[Constants.WEEK_DIR_BOT_DST] <= 90:
                                #     results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                    res = True, "BUY", 1
        else:
            #inversa
            print(f" isrising INV: {isRising} angleDiff: {angleDiff}")
            if angleDiff < 0 and (abs(angleDiff) > closeWeekDiffNew):
                if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgLowerDistPercent or results[
                    Constants.IND_BLG_LOWER_DST_PERCENT] < 0:
                    if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                            results[Constants.ACTION_MAX_DIST] >= (
                                    difference_optimized * multiplicadorUP)):
                        if results[Constants.ACUMULADO] < 0:
                            # if results[Constants.MEDSTDDIFF] < 0:
                            #     results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                res = True, "SELL", 1

        return res

    def evaluateUpOpen_EMA_WEEK_04(self, results,activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        multiplicadorUP= 1
        blgLowerDistPercent = -10
        ima5ma20 = results[Constants.IMA5MA20]



        isRising, angleDiff = self.isRisingFromMonth(results)
        # isRising, angleDiff = self.isRisingFromWEEK(results)
        # isRising, angleDiff = self.isRisingFromWEEKNEW(results)
        if isRising:
            if angleDiff >0 and (angleDiff > closeWeekDiffNew/2):

                if ima5ma20 == Constants.INDICATOR_EMA_BUY:
                    if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgLowerDistPercent:
                        if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                                results[Constants.ACTION_MIN_DIST] >= (
                                        difference_optimized * multiplicadorUP)):
                            if results[Constants.ACUMULADO] > 0:
                                # if results[Constants.MEDSTDDIFF] > 0:
                                    # if results[Constants.WEEK_DIR_BOT_DST] <= 90:
                                    #     results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                        res = True, "BUY", 1
        else:
            #inversa
            print(f" isrising INV: {isRising} angleDiff: {angleDiff}")
            if angleDiff < 0 and (abs(angleDiff) > closeWeekDiffNew):
                # if ima5ma20 == Constants.INDICATOR_EMA_SELL:
                    if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgLowerDistPercent or results[
                        Constants.IND_BLG_LOWER_DST_PERCENT] < 0:
                        if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                                results[Constants.ACTION_MAX_DIST] >= (
                                        difference_optimized * multiplicadorUP)):
                            if results[Constants.ACUMULADO] < 0:
                                # if results[Constants.MEDSTDDIFF] < 0:
                                #     results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                    res = True, "SELL", 1

        return res


    def evaluateUpOpen_EMA_WEEK_NEW_FLOW_01(self, results,activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        multiplicadorUP= 1
        blgLowerDistPercent = -10
        ima5ma20 = results[Constants.IMA5MA20]



        # isRising, angleDiff = self.isRisingFromMonth(results)
        # isRising, angleDiff = self.isRisingFromWEEK(results)
        isRising, angleDiff = self.isRisingFromWEEKNEW(results)
        if isRising:
            if angleDiff >0 and (angleDiff > closeWeekDiffNew/2):

                if ima5ma20 == Constants.INDICATOR_EMA_BUY:
                    if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgLowerDistPercent:
                        if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                                results[Constants.ACTION_MIN_DIST] >= (
                                        difference_optimized * multiplicadorUP)):
                            if results[Constants.ACUMULADO] > 0:
                                # if results[Constants.MEDSTDDIFF] > 0:
                                    # if results[Constants.WEEK_DIR_BOT_DST] <= 90:
                                    #     results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                        res = True, "BUY", 1
        else:
            #inversa
            print(f" isrising INV: {isRising} angleDiff: {angleDiff}")
            if angleDiff < 0 and (abs(angleDiff) > closeWeekDiffNew):
                # if ima5ma20 == Constants.INDICATOR_EMA_SELL:
                    if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgLowerDistPercent or results[
                        Constants.IND_BLG_LOWER_DST_PERCENT] < 0:
                        if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                                results[Constants.ACTION_MAX_DIST] >= (
                                        difference_optimized * multiplicadorUP)):
                            if results[Constants.ACUMULADO] < 0:
                                # if results[Constants.MEDSTDDIFF] < 0:
                                #     results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                    res = True, "SELL", 1

        return res

    def evaluateUpOpen_EMA_WEEK_NEW_FLOW_02(self, results,activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        multiplicadorUP= 1
        blgLowerDistPercent = -10
        ima5ma20 = results[Constants.IMA5MA20]
        blgmaMean = results[Constants.BLG_MA_MEAN]
        blgma_min_diff = activeParam.blgma_min_diff


        # isRising, angleDiff = self.isRisingFromMonth(results)
        # isRising, angleDiff = self.isRisingFromWEEK(results)
        isRising, angleDiff = self.isRisingFromWEEKNEW(results)
        if isRising:
            if angleDiff >0 and (angleDiff > closeWeekDiffNew/2):

                # if ima5ma20 == Constants.INDICATOR_EMA_BUY:
                    if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgLowerDistPercent:
                        if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                                results[Constants.ACTION_MIN_DIST] >= (
                                        difference_optimized * multiplicadorUP)):
                            if results[Constants.ACUMULADO] > 0:
                                # if results[Constants.MEDSTDDIFF] > 0:
                                    # if results[Constants.WEEK_DIR_BOT_DST] <= 90:
                                    #     results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                        res = True, "BUY", 1
        else:
            #inversa
            invSellCond = False
            print(f" isrising INV: {isRising} angleDiff: {angleDiff}")
            if angleDiff < 0 and (abs(angleDiff) > closeWeekDiffNew):
                if blgmaMean < 0 and abs(blgmaMean) > blgma_min_diff:
                    invSellCond = True
                # elif blgmaMean > 0 and blgmaMean < blgma_min_diff)-0.2:
                #     invSellCond = True


                if invSellCond:
                    # if ima5ma20 == Constants.INDICATOR_EMA_SELL:
                        if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgLowerDistPercent or results[
                            Constants.IND_BLG_LOWER_DST_PERCENT] < 0:
                            if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                                    results[Constants.ACTION_MAX_DIST] >= (
                                            difference_optimized * multiplicadorUP)):
                                if results[Constants.ACUMULADO] < 0:
                                    # if results[Constants.MEDSTDDIFF] < 0:
                                    #     results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                        res = True, "SELL", 1




        return res

    def evaluateUpOpen_EMA_04(self, results,activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        multiplicadorUP= 1
        blgLowerDistPercent = 10

        isRising, angleDiff = self.isRisingAngle(results)
        isRisingIma1, angleDiffIm1 = self.isRisingAngleIma1(results)
        if isRising:
            if isRisingIma1:
        # if results[Constants.BLG_MA_X] > 0:
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgLowerDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
                    if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                            results[Constants.ACTION_MIN_DIST] >= (
                                    difference_optimized * multiplicadorUP)):
                        if results[Constants.ACUMULADO] > 0:
                            # if results[Constants.MEDSTDDIFF] > 0:
                                # if results[Constants.WEEK_DIR_BOT_DST] <= 90:
                            # if results[Constants.ACTION_MAX_DIST] < results[Constants.ACTION_MIN_DIST]:
                                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                    res = True, "BUY", 1
            else:
                inversa=""
                if results[Constants.ACTION_MIN_DIST] < results[Constants.ACTION_MAX_DIST]:
                # if results[Constants.ACTION_MIN_DIST] >= 3:
                    results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                    res = True, "SELL", 1
        return res

    def evaluateUpOpen_EMA_OUP_01(self, results,activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        multiplicadorUP= 1
        blgLowerDistPercent = 10

        # isRising, angleDiff = self.isRisingFromWEEKNEW(results)
        isRising, angleDiff = self.isRisingFromWEEK(results)
        if isRising:
            if angleDiff > closeWeekDiffNew / 2:
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgLowerDistPercent or results[
                    Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
                    if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                            results[Constants.ACTION_MIN_DIST] >= (
                                    difference_optimized * multiplicadorUP)):
                        if results[Constants.ACUMULADO] > 0:
                            # if results[Constants.MEDSTDDIFF] > 0:
                            # if results[Constants.WEEK_DIR_BOT_DST] <= 90:
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            res = True, "BUY", 1
        return res

    def evaluateUpOpen_EMA_OUP_02(self, results,activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        multiplicadorUP= 1
        blgLowerDistPercent = 10
        weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
        flujoBLG = results[Constants.BLG_MA_X]

        # isRising, angleDiff = self.isRisingFromWEEKNEW(results)
        isRising, angleDiff = self.isRisingFromWEEK(results)
        if isRising:
            if weekdirBotPercent > 90 and weekdirBotPercent <100:
                nada = ""
            else:
                if angleDiff > closeWeekDiffNew / 2:

                    if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgLowerDistPercent or results[
                        Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
                        if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                                results[Constants.ACTION_MIN_DIST] >= (
                                        difference_optimized * multiplicadorUP)):
                            if results[Constants.ACUMULADO] > 0:
                                # if results[Constants.MEDSTDDIFF] > 0:
                                # if results[Constants.WEEK_DIR_BOT_DST] <= 90:
                                # results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                res = True, "BUY", 1
        else:
            nada = ""
            # if flujoBLG > 0:
            #     if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgLowerDistPercent or results[
            #         Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
            #         if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
            #                 results[Constants.ACTION_MIN_DIST] >= (
            #                         difference_optimized * multiplicadorUP)):
            #             if results[Constants.ACUMULADO] > 0:
            #                 # if results[Constants.MEDSTDDIFF] > 0:
            #                 # if results[Constants.WEEK_DIR_BOT_DST] <= 90:
            #                 results[Constants.NEW_ACTION] = Constants.ACTION_BUY
            #                 res = True, "BUY", 2
        return res

    def evaluateUpOpen_EMA_OUP_04(self, results, activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        blgDistPercent = activeParam.blgDistPercent
        multiplicadorUP = 1

        if (abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) ==0) and abs(results[Constants.MEDSTDDIFF]) < medstdmaxDiff:
            # if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_UP:
                if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
                # if results[Constants.IND_BLG_UPPER_DST] >= self.BLGDist:
                #     if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or
                #             results[Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP)):
                       if results[Constants.ACUMULADO] > 0:
                           if results[Constants.MEDSTDDIFF] > 0:
                               if results[Constants.DIRECTION] == Constants.DIR_UP or results[
                                   Constants.DIRECTION] == Constants.DIR_PRE_UP or results[
                                            Constants.DIRECTION] == Constants.DIR_CHANGE:
                                   if results[Constants.IND_BLG_UPPER_DST_PERCENT] > blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] <0:
                                        #     if results[Constants.IND_BLG_UPPER_DST_PERCENT] > 60:
                                        res = True, "BUY", 1

                       else:
                           nada = ""
                           if results[Constants.MEDSTDDIFF] < 0:
                               nada =""


                           if results[Constants.INDICATOR_MED_MOMENT] ==Constants.INDICATOR_TM_DOWN:
                               nada = ""

                else:
                    ##ESTAMOS SOBRE LA MEDIA
                    # if results[Constants.IND_BLG_UPPER_DST] < self.blgLowerDist:
                        if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                                results[Constants.ACTION_MIN_DIST] >= (
                                        difference_optimized * multiplicadorUP)):
                            if results[Constants.ACUMULADO] > 0:
                                #sube
                                if results[Constants.CLOSE_NXT_DOWN]==0:
                                    #que no este con la marca de cerrar proxima bajada
                                    if results[Constants.MEDSTDDIFF] > 0:
                                        # if results[Constants.DIRECTION] == Constants.DIR_UP or results[
                                        #     Constants.DIRECTION] == Constants.DIR_PRE_UP or results[
                                        #     Constants.DIRECTION] == Constants.DIR_CHANGE:

                                            if results[Constants.IND_BLG_UPPER_DST_PERCENT] > blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] <0:
                                                res = True, "BUY", 2


                                    else:
                                        nada =""

                                else:
                                    if results[Constants.MEDSTDDIFF] < 0:
                                        nada = ""


                                    else:
                                        nada = ""
                                        if results[Constants.IND_BLG_UPPER_DST_PERCENT] > blgDistPercent:
                                            res = True, "BUY", 3


                                        else:
                                            #entra a comprar si esta en tendencia
                                            if results[Constants.INDICATOR_MED_MOMENT]==Constants.INDICATOR_TM_UP:
                                                res = True, "BUY", 4

                                        if results[Constants.IND_BLG_UPPER_DST_PERCENT] <0 and abs(results[Constants.IND_BLG_UPPER_DST_PERCENT])>1:
                                            res = True, "BUY", 5

                            else:
                                if results[Constants.ACUMULADO] < 0:
                                    if results[Constants.MEDSTDDIFF] < 0:
                                        nada = ""
        return res

    def evaluateUpOpen_EMA_OUP_03(self, results,activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        blgLowerDist = 1.5
        medstdminDiff = activeParam.medstdminDiff
        medstdmaxDiff = activeParam.medstdmaxDiff
        closeWeekDiffNew = activeParam.closeWeekDiffNew
        multiplicadorUP= 1
        blgLowerDistPercent = 10
        weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
        flujoBLG = results[Constants.BLG_MA_X]
        blgMaVal = results[Constants.BLG_MA_VAL]
        blg_max_min_value = activeParam.blg_max_min_value
        blgma_min_diff = activeParam.blgma_min_diff
        weekNewFlow = results[Constants.WEEK_DIR_BOT_DST_MED_NEW_FLOW]
        weekNewMinFlow = activeParam.blgma_min_diff

        isRising, angleDiff = self.isRisingFromWEEKNEW(results)
        # isRising, angleDiff = self.isRisingFromWEEK(results)

        reglasExtraBuy= False
        # if flujoBLG < 0 and abs(flujoBLG) < blg_max_min_value:
        #     flujoBLGEValBuy = True
        if weekNewFlow > 0 and weekNewFlow > weekNewMinFlow:
            reglasExtraBuy = True

        # reglasExtraBuy = False
        # if blgMaVal < 0 and abs(flujoBLG) < blg_max_min_value:
        #     reglasExtraBuy = True
        # if flujoBLG > 0:
        #     reglasExtraBuy = True
        reglasExtraBuy = True
        if isRising:
            if weekdirBotPercent > 90 and weekdirBotPercent <100:
                nada = ""
            else:
                if angleDiff > closeWeekDiffNew /2:
                    if reglasExtraBuy:
                        if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgLowerDistPercent or results[
                            Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
                            if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                                    results[Constants.ACTION_MIN_DIST] >= (
                                            difference_optimized * multiplicadorUP)):
                                if results[Constants.ACUMULADO] > 0:
                                    # if results[Constants.MEDSTDDIFF] > 0:
                                    # if results[Constants.WEEK_DIR_BOT_DST] <= 90:
                                    # results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                    res = True, "BUY", 1
        else:
            nada = ""
            # if flujoBLG > 0:
            #     if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgLowerDistPercent or results[
            #         Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
            #         if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
            #                 results[Constants.ACTION_MIN_DIST] >= (
            #                         difference_optimized * multiplicadorUP)):
            #             if results[Constants.ACUMULADO] > 0:
            #                 # if results[Constants.MEDSTDDIFF] > 0:
            #                 # if results[Constants.WEEK_DIR_BOT_DST] <= 90:
            #                 results[Constants.NEW_ACTION] = Constants.ACTION_BUY
            #                 res = True, "BUY", 2
        return res

    def evaluateUpOpen_Ima1_01(self, results,activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        maxAcumValue = activeParam.closeAcumvalue * 3
        medstdminDiff = activeParam.medstdminDiff


        #control penup3
        if results[Constants.FLUJO] == Constants.FLUJO_SUBE :
            if results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_UP or results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_UNDEF:
                #para abrir sin restricciones ya que es inicio mercado
                difOpenHours = self.getDifTimeFromOpen(results)
                if difOpenHours <=10:
                    res = True, "BUY",1
                else:
                    if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF])==0:
                        if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                            res = True, "BUY",2
            elif results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_DOWN:
                nada = ""
                if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF])==0:
                    if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                        res = True, "BUY", 3
        # EVALUADORES A LA INVERSA VENTA
        elif results[Constants.FLUJO] == Constants.FLUJO_BAJA:
            if results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_DOWN:
                # if results[Constants.FLUJO_COUNT]>1:
                    if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
                        Constants.ACTION_MAX_DIST] >= (difference_optimized):

                        if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF])==0:
                            if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                               res = True, "SELL", 1
        return res

    def evaluateUpOpen_Ima1_02(self, results,activeParam):
        res = False, "NADA", 0
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        maxAcumValue = activeParam.closeAcumvalue * 3
        medstdminDiff = activeParam.medstdminDiff

        if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
            if results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_UP or results[
                Constants.WEEK_FLOW] == Constants.WEEK_FLOW_UNDEF:

                # para abrir sin restricciones ya que es inicio mercado
                difOpenHours = self.getDifTimeFromOpen(results)
                if difOpenHours <= 10:
                    res = True, "BUY", 1
                else:
                    if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(
                            results[Constants.MEDSTDDIFF]) == 0:
                        if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                            res = True, "BUY", 2
            elif results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_DOWN:
                nada = ""
                if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0:
                    if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                        res = True, "BUY", 3
        # EVALUADORES A LA INVERSA VENTA
        elif results[Constants.FLUJO] == Constants.FLUJO_BAJA:
            if results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_DOWN:
                # if results[Constants.FLUJO_COUNT]>1:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized):
                        if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(
                                results[Constants.MEDSTDDIFF]) == 0:
                            if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                                res = True, "SELL", 1

        return res
    def evaluateUpOpen_10(self, results,activeParam):
        res = False, 0
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        angleUp = activeParam.angleUp
        #control penup3


        if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
            Constants.ACTION_MIN_DIST] >= (difference_optimized):
            if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT]==0:
                # if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff:

                    if results[Constants.WEEK_DIR_BOT_DST] < 90:
                        isRising, angleDiff = self.isRisingAngleIma1(results)
                        if isRising:
                            if "UP" in results[Constants.ANGLE_FLOW]:
                                #que no este muy arriba
                                if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] < 5:
                                    res = True, 5
                                else:
                                    if results[Constants.IND_BLG_MIDDLE_DST_PERCENT]<20:
                                        if results[Constants.ANGLE] >0:
                                        # if "UP" in self.aperturaAngle_01(results,activeParam):
                                            res = True,1
                                    else:
                                        if angleDiff > angleUp:
                                            if results[Constants.ANGLE] > angleUp:
                                                res = True, 4
                    else:
                        if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                            isRising, angleDiff = self.isRisingAngle(results)
                            if isRising:
                                if results[Constants.ANGLE_IMA1]>0:
                                    if results[Constants.IMA1EMADIFF] > 0:
                                        if results[Constants.IMA1EMADIFF] > activeParam.ima1EmaMinValue:
                                            res = True, 2
            else:
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] > 0 and results[
                    Constants.IND_BLG_UPPER_DST_PERCENT] < blgDistPercent:
                    if results[Constants.WEEK_DIR_BOT_DST] > 90:
                        if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] > 30:
                            if results[Constants.ANGLE] > 0:
                                if results[Constants.ANGLE_COUNTER] > 5:
                                    isRising, angleDiff = self.isRisingAngle(results)
                                    if isRising:
                                        # if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff:
                                        # if self.canOpenUP_BLGDistance(results,activeParam):
                                        res = True, 3
        return res

    def isRisingAngle(self, results):
        res = False, 0
        angleDIff = float(results[Constants.ANGLE]) -float(results[Constants.ANGLE_PREV])
        if angleDIff > 0:
            res = True, angleDIff
        else:
            res = False, angleDIff
        return res

    def isRisingFromWEEK(self, results):
        res = False, 0
        angleDIff = float(results[Constants.WEEK_DIR_BOT_DST]) -float(results[Constants.WEEK_DIR_BOT_DST_MED])
        if angleDIff > 0:
            res = True, angleDIff
        else:
            res = False, angleDIff
        return res

    def isRisingFromMonth(self, results):
        res = False, 0
        angleDIff = float(results[Constants.MONTH_DIR_BOT_DST]) -float(results[Constants.MONTH_DIR_BOT_DST_MED])
        if angleDIff > 0:
            res = True, angleDIff
        else:
            res = False, angleDIff
        return res

    def isRisingFromWEEKNEW(self, results):
        res = False, 0
        angleDIff = float(results[Constants.WEEK_DIR_BOT_DST_NEW]) - float(results[Constants.WEEK_DIR_BOT_DST_MED_NEW])
        if angleDIff > 0:
            res = True, angleDIff
        else:
            res = False, angleDIff
        return res

    def isRisingAngleIma1(self, results):
        res = False, 0
        angleDIff = float(results[Constants.ANGLE_IMA1]) - float(results[Constants.ANGLE_IMA1_PREV])
        if angleDIff > 0:
            res = True, angleDIff
        else:
            res = False, angleDIff
        return res


    def evaluateForteUpOpen_01(self, results,activeParam):
        res = False
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference

        if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
            Constants.ACTION_MIN_DIST] >= (difference_optimized):
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0 or results[Constants.IND_BLG_UPPER_DST_PERCENT]==0:
                    if results[Constants.WEEK_DIR_BOT_DST] < 90:
                        if results[Constants.IMA1EMADIFF] > 0:
                            if results[Constants.IMA1EMADIFF] > 0.3:
                                # if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff:
                                    # if self.canOpenUP_BLGDistance(results,activeParam):
                                        res = True
        return  res

    def evaluateDownOpen_01(self, results,activeParam):
        res = False, 0
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        angleDown = activeParam.angleDown

        if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
            Constants.ACTION_MAX_DIST] >= (difference_optimized):
                if results[Constants.IND_BLG_LOWER_DST_PERCENT] > blgDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT]==0:
                    if results[Constants.WEEK_DIR_BOT_DST] > 10:
                        if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff:
                            # if self.canOpenUP_BLGDistance(results,activeParam):
                                res = True, 1
                elif results[Constants.IND_BLG_LOWER_DST_PERCENT] < blgDistPercent:
                    rising, angleDiff = self.isRisingAngle(results)
                    if rising == False:
                        if abs(angleDiff) > angleDown:
                            res = True, 2
        return  res

    def evaluateDownOpen_02(self, results,activeParam):
        res = False, 0
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        angleDown = activeParam.angleDown

        if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
            Constants.ACTION_MAX_DIST] >= (difference_optimized):
                if results[Constants.IND_BLG_LOWER_DST_PERCENT] > blgDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT]==0:
                    if results[Constants.WEEK_DIR_BOT_DST] > 10:
                        if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff:
                            # if self.canOpenUP_BLGDistance(results,activeParam):
                                res = True, 1
                elif results[Constants.IND_BLG_LOWER_DST_PERCENT] < blgDistPercent:
                    rising, angleDiff = self.isRisingAngle(results)
                    if rising == False:
                        if abs(angleDiff) > angleDown:
                            res = True, 2
        return  res
    def getDifTimeFromOpen(self, results):

        if results[Constants.SIMULATION] is True:
            temp = results[Constants.DATE].values[0]
            t = datetime.strptime(temp, '%Y-%m-%d %H:%M:%S.%f')
            current_time_h = t.hour * 100
            current_time_min = t.minute
            # print(f" gettime hora : {current_time_h} minutos: {current_time_min}")
            currentTime = int(current_time_h + current_time_min)
            openHour = 1530
            dif = currentTime - openHour
        else:
            t = time.localtime()
            current_time_h = time.strftime("%H", t)
            current_time_min = time.strftime("%M", t)
            # print(f" gettime hora sistema: {current_time_h} minutos: {current_time_min}")
            currentTime = int(current_time_h + current_time_min)
            openHour = 1530
            dif = currentTime - openHour
        return dif

    def evaluateDownOpen_BLG_01(self, results,activeParam):
        res = False,"nada", 0
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        angleDown = activeParam.angleDown
        angleUp = activeParam.angleUp
        medstdminDiff = activeParam.medstdminDiff

        if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
            Constants.ACTION_MAX_DIST] >= (difference_optimized):

            if results[Constants.FLUJO]==Constants.FLUJO_BAJA:
                if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= blgDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT] ==0:
                    if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff:
                        # if (results[Constants.ANGLE]<0 and abs(results[Constants.ANGLE])>1) or results[Constants.ANGLE]==0:
                        res = True, "SELL", 1
                elif results[Constants.IND_BLG_LOWER_DST_PERCENT] <0:
                    res = True, "SELL", 2

                elif results[Constants.IND_BLG_LOWER_DST_PERCENT] < blgDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT]==0:
                    nada=""
                    if results[Constants.ANGLE] < 0 or results[
                        Constants.ANGLE] == 0:
                        # BAJA
                        if abs(results[Constants.ANGLE]) > angleDown:
                            res = True, "SELL", 3
                        else:
                            if results[Constants.ANGLEm1] > 0:
                                res = True, "SELL", 4
            else:
                nada = ""

        return res

    def evaluateDownOpen_IMA1_01(self, results,activeParam):
        res = False,"nada", 0
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
            if results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_DOWN or results[
                Constants.WEEK_FLOW] == Constants.WEEK_FLOW_UNDEF:

                if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized):

                        difOpenHours = self.getDifTimeFromOpen(results)
                        if difOpenHours <= 60:
                            res = True, "SELL", 1

                        else:
                            #no abrir si la diferencia anterior es superior a difference
                            if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF])==0:
                                if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                                    res = True, "SELL", 2
            elif results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_UP:
                if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF])==0:
                    if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                        res = True, "SELL", 3


        # inversa COMPRA
        elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
            if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UP:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized):
                    if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF])==0:
                        if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                            res = True, "BUY", 1

        return  res

    def evaluateDownOpen_IMA1_02(self, results, activeParam):
        res = False, "nada", 0
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
            if "DOWN" in results[Constants.ANGLE_FLOW]:

                if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized):

                    difOpenHours = self.getDifTimeFromOpen(results)
                    if difOpenHours <= 60:
                        res = True, "SELL", 1

                    else:
                        if results[Constants.IND_BLG_LOWER_DST_PERCENT] > blgDistPercent or results[
                            Constants.IND_BLG_LOWER_DST_PERCENT] == 0:
                            if results[Constants.WEEK_DIR_BOT_DST] > 10:

                                # no abrir si la diferencia anterior es superior a difference
                                # if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(
                                #         results[Constants.MEDSTDDIFF]) == 0:
                                    #     if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                                    res = True, "SELL", 2

            elif "UP" in results[Constants.ANGLE_FLOW]:
                # if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0:
                #     if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                        res = True, "SELL", 3

        # inversa COMPRA
        elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
            if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UP:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized):
                    if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0:
                        if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                            res = True, "BUY", 1
        return res

    def evaluateDownOpen_IMA1_03(self, results,activeParam):
        res = False,"nada", 0
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
            if results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_DOWN or results[
                Constants.WEEK_FLOW] == Constants.WEEK_FLOW_UNDEF:

                if results[Constants.ACUMULADO_ABS] >= (difference_optimized ) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized):

                        difOpenHours = self.getDifTimeFromOpen(results)
                        # print(f"difOpenHours {difOpenHours}")
                        if difOpenHours <= 60:
                            res = True, "SELL", 1
                        else:
                            # no abrir si la diferencia anterior es superior a difference
                            if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(
                                    results[Constants.MEDSTDDIFF]) == 0:
                                if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                                    # if abs(results[Constants.PREVIOUS_DIST]) <= activeParam.difference:
                                    res = True, "SELL", 2

            elif results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_UP:
                if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(results[Constants.MEDSTDDIFF]) == 0:
                    if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                        # if results[Constants.ACUMULADO_ABS]>= (difference_optimized * self.multiplicadorUP):
                        res = True, "SELL", 3


        # inversa COMPRA
        elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
            if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UP:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized ) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized):
                    if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff or abs(
                            results[Constants.MEDSTDDIFF]) == 0:
                        if abs(results[Constants.PREVIOUS_DIST]) <= maxAcumValue:
                            res = True, "BUY", 1

        return  res

    def evaluateDownOpen_03(self, results,activeParam):
        res = False, 0
        blgDistPercent = activeParam.blgDistPercent
        medstdminDiff = activeParam.medstdminDiff
        difference_optimized = activeParam.difference
        angleDown = activeParam.angleDown
        angleUp = activeParam.angleUp

        risingIma1, angleIma1Diff = self.isRisingAngleIma1(results)
        rising, angleDiff = self.isRisingAngle(results)

        if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
            Constants.ACTION_MAX_DIST] >= (difference_optimized):
                if results[Constants.IND_BLG_LOWER_DST_PERCENT] > blgDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT]==0:
                    if results[Constants.WEEK_DIR_BOT_DST] > 10:
                        if results[Constants.IMA1EMADIFF]> 0:
                            #solo abrir down si esta sobre mid
                            if results[Constants.IND_BLG_MIDDLE_DST_PERCENT]>20:
                                if risingIma1 == False:
                                    res = True, 3
                        else:
                            if abs(results[Constants.MEDSTDDIFF]) > medstdminDiff:
                                if risingIma1 == False:
                                    res = True, 1
                                else:
                                    if angleIma1Diff > angleUp:
                                        res = False, -1
                elif results[Constants.IND_BLG_LOWER_DST_PERCENT] < blgDistPercent:

                    if rising == False:
                        if abs(angleDiff) > angleDown:
                            res = True, 2
        return  res

    def evalNXT_UP_01(self, results, activeParam,difference_optimized):
        res = False
        if (results[Constants.ACUMULADO_ABS] >= (difference_optimized) or
                results[Constants.ACTION_MIN_DIST] >= (
                        difference_optimized)):
            results[Constants.CLOSE_NXT_UP] = 0
            if results[Constants.WEEK_DIR_BOT_DST] < 10:
                # if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
                    if results[Constants.IND_BLG_UPPER_DST_PERCENT] > self.blgDistPercent:
                        if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] < 0:
                            res = True


        return res

    def evalNXT_UP_02(self, results, activeParam, difference_optimized):
        res = False
        if (results[Constants.ACUMULADO_ABS] >= (difference_optimized) or
                results[Constants.ACTION_MIN_DIST] >= (
                        difference_optimized)):
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
        res = False, 1
        if (results[Constants.ACUMULADO_ABS] >= (difference_optimized) or
                results[Constants.ACTION_MIN_DIST] >= (
                        difference_optimized)):
            results[Constants.CLOSE_NXT_UP] = 0
            if results[Constants.WEEK_DIR_BOT_DST] < 50:
                if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
                    if results[Constants.IND_BLG_UPPER_DST_PERCENT] > self.blgDistPercent:
                        if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] < 0:
                            res = True,1
                else:
                    if results[Constants.ANGLE] < 0 and abs(results[Constants.ANGLE])< 40:
                        if results[Constants.IND_BLG_UPPER_DST_PERCENT] > self.blgDistPercent:
                            if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] < 0:
                                res = True,2
            # elif results[Constants.WEEK_DIR_BOT_DST] > 50 and results[Constants.WEEK_DIR_BOT_DST] < 90:
            #     if results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_UP:
            #         if results[Constants.IND_BLG_UPPER_DST_PERCENT] > self.blgDistPercent:
            #             if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] < 0:
            #                 res = True,3
        return res

    def evalNXT_UP_04(self, results, activeParam, difference_optimized):
        res = False,1
        blgDistPercent = activeParam.blgDistPercent
        if (results[Constants.ACUMULADO_ABS] >= (difference_optimized) or
                results[Constants.ACTION_MIN_DIST] >= (
                        difference_optimized)):
            results[Constants.CLOSE_NXT_UP] = 0
            if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
                # if "UP" in results[Constants.ANGLE_FLOW]:
                # if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] > blgDistPercent:
                    res = True,1
        return res

    def evalNXT_UP_05(self, results, activeParam, difference_optimized):
        res = False,1
        blgDistPercent = activeParam.blgDistPercent
        results[Constants.CLOSE_NXT_UP] = 0
        multiplicadorUP = 2

        if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
            # if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
            if results[Constants.IND_BLG_UPPER_DST_PERCENT] > blgDistPercent:
                if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or
                        results[Constants.ACTION_MIN_DIST] >= (
                                difference_optimized * multiplicadorUP)):
                    res = True,1
        return res

    def evalNXT_DOWN_01(self, results, activeParam, difference_optimized):
        res = False
        if (results[Constants.ACUMULADO_ABS] >= (difference_optimized) or
                results[Constants.ACTION_MAX_DIST] >= (
                        difference_optimized)):
            results[Constants.CLOSE_NXT_DOWN] = 0
            if results[Constants.WEEK_DIR_BOT_DST] > 50:
                # if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
                    if results[Constants.IND_BLG_LOWER_DST_PERCENT] > self.blgDistPercent:
                        if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] > 0:
                            res = True
            elif results[Constants.WEEK_DIR_BOT_DST] < 50 and results[Constants.WEEK_DIR_BOT_DST] > 10:
                if results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_DOWN:
                    if results[Constants.IND_BLG_LOWER_DST_PERCENT] > self.blgDistPercent:
                        if results[Constants.IND_BLG_MIDDLE_DST_PERCENT] > 0:
                            res = True
        return res