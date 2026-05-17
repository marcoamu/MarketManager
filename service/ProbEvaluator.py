from service.Constants import Constants


class ProbEvaluator:

    def __init__(self):
        name = "ProbEvaluator"

    @classmethod
    def getProMEDSTD_END_BLG_05(self, results, active):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            week = results[Constants.WEEK_FLOW]
            weekPrev = results[Constants.WEEK_FLOW_PREV]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            week_med_abs = abs(results[Constants.WEEK_FLOW_MED])
            flowdiff = results[Constants.FLOW_DIFF]
            week_std = results[Constants.WEEK_FLOW_STD]
            weekdiff = results[Constants.WEEK_FLOW_DIFF]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            medDay = results[Constants.INDICATOR_MED_DAY]
            absMedDay = abs(medDay)
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            # BLG
            IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]
            IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
            blgDistPercent = active.parameters.blgDistPercent

            # valores del dia
            numUP = results[Constants.IND_NUM_UP]
            numDOWN = results[Constants.IND_NUM_DOWN]

            sumUP = results[Constants.IND_SUM_UP]
            sumDOWN = results[Constants.IND_SUM_DOWN]

            sumDay = int(sumUP) - int(sumDOWN)

            weekdiffTendenceValue = 1
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]

            if prevPercent is not None:
                prevPercent = float(prevPercent)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]
            # if med == 0:
            #     if direction == Constants.DIR_UP:
            #         med = 1
            #     elif direction == Constants.DIR_DOWN:
            #         med = -1
            # percentFlow = Constants.DIR_WAIT
            # if percent > prevPercent:
            #     percentFlow = Constants.DIR_UP
            # else:
            #     # baja
            #     percentFlow = Constants.DIR_DOWN
            # CALCULOS final del
            week_prev_res = None
            if week_prev_med < week_med:
                week_prev_res = Constants.DIR_UP
                # if flowdiff > 0:
                #     week_prev_res = Constants.DIR_UP
                # else:
                #     week_prev_res = Constants.DIR_DOWN
                #     ndad =""
                #     # ver que hacer cuando no coinciden
                #     print(f" getProMEDSTD_END_BLG_05 NO COINCIDE")
            elif week_prev_med > week_med:
                week_prev_res = Constants.DIR_DOWN
                # if flowdiff < 0:
                #     week_prev_res = Constants.DIR_DOWN
                # else:
                #     week_prev_res = Constants.DIR_UP
                #     ndad =""
                #     # ver que hacer cuando no coinciden
                #     print(f" getProMEDSTD_END_BLG_05 NO COINCIDE")
            if week == Constants.WEEK_FLOW_UP:
                # SUBE
                res = Constants.DIR_UP
                if active.parameters.weekMindiff != 0.7:
                    # ha cambiado el weekdiff
                    if abs(weekdiff) < active.parameters.weekMindiff:
                        print(f"prob is using week_prev_differential")
                        res = week_prev_res
            else:
                # BAJA
                res = Constants.DIR_DOWN
                if active.parameters.weekMindiff != 0.7:
                    # ha cambiado el weekdiff
                    if abs(weekdiff) < active.parameters.weekMindiff:
                        print(f"prob is using week_prev_differential")
                        res = week_prev_res
        except Exception as error:
            print("Error getProMEDSTD_END BLG05", error)
        return res

    @classmethod
    def getProMEDSTD_END_BLG_06(self, results, active):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            weekFlow = results[Constants.WEEK_FLOW]
            weekPrev = results[Constants.WEEK_FLOW_PREV]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            week_med_abs = abs(results[Constants.WEEK_FLOW_MED])

            flowdiff = results[Constants.FLOW_DIFF]
            week_std = results[Constants.WEEK_FLOW_STD]
            weekdiff = results[Constants.WEEK_FLOW_DIFF]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            medDay = results[Constants.INDICATOR_MED_DAY]
            absMedDay = abs(medDay)
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            # BLG
            blgDistPercent = active.parameters.blgDistPercent
            weekdirBotPercentPrev = results[Constants.WEEK_DIR_BOT_DST_PREV]
            weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
            # valores del dia
            numUP = results[Constants.IND_NUM_UP]
            numDOWN = results[Constants.IND_NUM_DOWN]

            sumUP = results[Constants.IND_SUM_UP]
            sumDOWN = results[Constants.IND_SUM_DOWN]
            angle = results[Constants.ANGLE]
            angleCounter = int(results[Constants.ANGLE_COUNTER])
            angleM1 = results[Constants.ANGLEm1]
            angleM2 = results[Constants.ANGLEm21]
            angleUp = float(active.parameters.angleUp)
            angleDown = float(active.parameters.angleDown)
            close_NXT_UP = results[Constants.CLOSE_NXT_UP]
            close_NXT_DOWN = results[Constants.CLOSE_NXT_DOWN]
            # BLG
            IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]
            IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]

            sumDay = int(sumUP) - int(sumDOWN)

            weekdiffTendenceValue = 1
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]


            if prevPercent is not None:
                prevPercent = float(prevPercent)
            if weekdirBotPercent is not None:
                weekdirBotPercent = float(weekdirBotPercent)
            if weekdirBotPercentPrev is not None:
                weekdirBotPercentPrev = float(weekdirBotPercentPrev)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]
            # if med == 0:
            #     if direction == Constants.DIR_UP:
            #         med = 1
            #     elif direction == Constants.DIR_DOWN:
            #         med = -1
            # percentFlow = Constants.DIR_WAIT
            # if percent > prevPercent:
            #     percentFlow = Constants.DIR_UP
            # else:
            #     # baja
            #     percentFlow = Constants.DIR_DOWN
            # CALCULOS final del
            week_prev_res = None
            if week_prev_med < week_med:
                week_prev_res = Constants.DIR_UP
                # if flowdiff > 0:
                #     week_prev_res = Constants.DIR_UP
                # else:
                #     week_prev_res = Constants.DIR_DOWN
                #     ndad =""
                #     # ver que hacer cuando no coinciden
                #     print(f" getProMEDSTD_END_BLG_05 NO COINCIDE")
            elif week_prev_med > week_med:
                week_prev_res = Constants.DIR_DOWN
                # if flowdiff < 0:
                #     week_prev_res = Constants.DIR_DOWN
                # else:
                #     week_prev_res = Constants.DIR_UP
                #     ndad =""
                #     # ver que hacer cuando no coinciden
                #     print(f" getProMEDSTD_END_BLG_05 NO COINCIDE")
            if weekFlow == Constants.WEEK_FLOW_UP:
                # SUBE
                res = Constants.DIR_UP
                if active.parameters.weekMindiff != 0.7:
                    # ha cambiado el weekdiff
                    if abs(weekdiff) < active.parameters.weekMindiff:
                        print(f"prob is using week_prev_differential")
                        res = week_prev_res
                # if abs(week_med) < 1:
                res = self.verifyExtremeValuesUP(res, weekdirBotPercent, active, angle, angleCounter, weekFlow, IND_BLG_LOWER_DST_PERCENT, week_prev_res)

            else:
                # BAJA
                res = Constants.DIR_DOWN
                if active.parameters.weekMindiff != 0.7:
                    # ha cambiado el weekdiff
                    if abs(weekdiff) < active.parameters.weekMindiff:
                        print(f"prob is using week_prev_differential")
                        res = week_prev_res
                res = self.verifyExtremeValuesDOWN(res, weekdirBotPercent, active, angle, angleCounter, weekFlow,
                                                 IND_BLG_LOWER_DST_PERCENT,week_prev_res)
        except Exception as error:
            print("Error getProMEDSTD_END BLG05", error)
        return res

    @classmethod
    def getProMEDSTD_END_BLG_07(self, results, active):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            weekFlow = results[Constants.WEEK_FLOW]
            weekPrev = results[Constants.WEEK_FLOW_PREV]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            week_med_abs = abs(results[Constants.WEEK_FLOW_MED])

            flowdiff = results[Constants.FLOW_DIFF]
            week_std = results[Constants.WEEK_FLOW_STD]
            weekdiff = results[Constants.WEEK_FLOW_DIFF]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            medDay = results[Constants.INDICATOR_MED_DAY]
            absMedDay = abs(medDay)
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            # BLG
            blgDistPercent = active.parameters.blgDistPercent
            weekdirBotPercentPrev = results[Constants.WEEK_DIR_BOT_DST_PREV]
            weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
            # valores del dia
            numUP = results[Constants.IND_NUM_UP]
            numDOWN = results[Constants.IND_NUM_DOWN]

            sumUP = results[Constants.IND_SUM_UP]
            sumDOWN = results[Constants.IND_SUM_DOWN]
            angle = results[Constants.ANGLE]
            angleCounter = int(results[Constants.ANGLE_COUNTER])
            angleM1 = results[Constants.ANGLEm1]
            angleM2 = results[Constants.ANGLEm21]
            angleUp = float(active.parameters.angleUp)
            angleDown = float(active.parameters.angleDown)
            close_NXT_UP = results[Constants.CLOSE_NXT_UP]
            close_NXT_DOWN = results[Constants.CLOSE_NXT_DOWN]
            # BLG
            IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]
            IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]

            sumDay = int(sumUP) - int(sumDOWN)

            weekdiffTendenceValue = 1
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]

            if prevPercent is not None:
                prevPercent = float(prevPercent)
            if weekdirBotPercent is not None:
                weekdirBotPercent = float(weekdirBotPercent)
            if weekdirBotPercentPrev is not None:
                weekdirBotPercentPrev = float(weekdirBotPercentPrev)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]
            # if med == 0:
            #     if direction == Constants.DIR_UP:
            #         med = 1
            #     elif direction == Constants.DIR_DOWN:
            #         med = -1
            # percentFlow = Constants.DIR_WAIT
            # if percent > prevPercent:
            #     percentFlow = Constants.DIR_UP
            # else:
            #     # baja
            #     percentFlow = Constants.DIR_DOWN
            # CALCULOS final del
            week_prev_res = None
            if week_prev_med < week_med:
                week_prev_res = Constants.DIR_UP
                # if flowdiff > 0:
                #     week_prev_res = Constants.DIR_UP
                # else:
                #     week_prev_res = Constants.DIR_DOWN
                #     ndad =""
                #     # ver que hacer cuando no coinciden
                #     print(f" getProMEDSTD_END_BLG_05 NO COINCIDE")
            elif week_prev_med > week_med:
                week_prev_res = Constants.DIR_DOWN
                # if flowdiff < 0:
                #     week_prev_res = Constants.DIR_DOWN
                # else:
                #     week_prev_res = Constants.DIR_UP
                #     ndad =""
                #     # ver que hacer cuando no coinciden
                #     print(f" getProMEDSTD_END_BLG_05 NO COINCIDE")
            if weekFlow == Constants.WEEK_FLOW_UP:
                # SUBE
                res = Constants.DIR_UP
                if active.parameters.weekMindiff != 0.7:
                    # ha cambiado el weekdiff
                    if abs(weekdiff) < active.parameters.weekMindiff:
                        print(f"prob is using week_prev_differential")
                        res = week_prev_res
                # if abs(week_med) < 1:
                res = self.verifyExtremeValuesUP_01(res, weekdirBotPercent, active, angle, angleCounter, weekFlow,
                                                 IND_BLG_LOWER_DST_PERCENT, week_prev_res)

            else:
                # BAJA
                res = Constants.DIR_DOWN
                if active.parameters.weekMindiff != 0.7:
                    # ha cambiado el weekdiff
                    if abs(weekdiff) < active.parameters.weekMindiff:
                        print(f"prob is using week_prev_differential")
                        res = week_prev_res
                res = self.verifyExtremeValuesDOWN_01(res, weekdirBotPercent, active, angle, angleCounter, weekFlow,
                                                   IND_BLG_LOWER_DST_PERCENT, week_prev_res)
        except Exception as error:
            print("Error getProMEDSTD_END BLG05", error)
        return res

    @classmethod
    def getProMEDSTD_END_BLG_08(self, results, active):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            weekFlow = results[Constants.WEEK_FLOW]
            weekPrev = results[Constants.WEEK_FLOW_PREV]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            week_med_abs = abs(results[Constants.WEEK_FLOW_MED])

            flowdiff = results[Constants.FLOW_DIFF]
            week_std = results[Constants.WEEK_FLOW_STD]
            weekdiff = results[Constants.WEEK_FLOW_DIFF]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            medDay = results[Constants.INDICATOR_MED_DAY]
            absMedDay = abs(medDay)
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            # BLG
            blgDistPercent = active.parameters.blgDistPercent
            weekdirBotPercentPrev = results[Constants.WEEK_DIR_BOT_DST_PREV]
            weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
            # valores del dia
            numUP = results[Constants.IND_NUM_UP]
            numDOWN = results[Constants.IND_NUM_DOWN]

            sumUP = results[Constants.IND_SUM_UP]
            sumDOWN = results[Constants.IND_SUM_DOWN]
            angle = results[Constants.ANGLE]
            angleCounter = int(results[Constants.ANGLE_COUNTER])
            angleM1 = results[Constants.ANGLEm1]
            angleM2 = results[Constants.ANGLEm21]
            angleUp = float(active.parameters.angleUp)
            angleDown = float(active.parameters.angleDown)
            close_NXT_UP = results[Constants.CLOSE_NXT_UP]
            close_NXT_DOWN = results[Constants.CLOSE_NXT_DOWN]
            # BLG
            IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]
            IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]

            sumDay = int(sumUP) - int(sumDOWN)

            weekdiffTendenceValue = 1
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]

            if prevPercent is not None:
                prevPercent = float(prevPercent)
            if weekdirBotPercent is not None:
                weekdirBotPercent = float(weekdirBotPercent)
            if weekdirBotPercentPrev is not None:
                weekdirBotPercentPrev = float(weekdirBotPercentPrev)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]
            # if med == 0:
            #     if direction == Constants.DIR_UP:
            #         med = 1
            #     elif direction == Constants.DIR_DOWN:
            #         med = -1
            # percentFlow = Constants.DIR_WAIT
            # if percent > prevPercent:
            #     percentFlow = Constants.DIR_UP
            # else:
            #     # baja
            #     percentFlow = Constants.DIR_DOWN
            # CALCULOS final del
            week_prev_res = None
            if week_prev_med < week_med:
                week_prev_res = Constants.DIR_UP
            elif week_prev_med > week_med:
                week_prev_res = Constants.DIR_DOWN

            if weekFlow == Constants.WEEK_FLOW_UP:
                # SUBE
                res = Constants.DIR_UP
                res = self.verifyExtremeValuesUP_03(res, week_prev_res,results, active)

            else:
                # BAJA
                res = Constants.DIR_DOWN
                res = self.verifyExtremeValuesDOWN_03(res, week_prev_res, results, active)
        except Exception as error:
            print("Error getProMEDSTD_END_BLG_08", error)
        return res

    @classmethod
    def getProb_HOURLY_ANGLE_01(self, results, active):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            weekFlow = results[Constants.WEEK_FLOW]
            weekPrev = results[Constants.WEEK_FLOW_PREV]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            week_med_abs = abs(results[Constants.WEEK_FLOW_MED])

            flowdiff = results[Constants.FLOW_DIFF]
            week_std = results[Constants.WEEK_FLOW_STD]
            weekdiff = results[Constants.WEEK_FLOW_DIFF]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            medDay = results[Constants.INDICATOR_MED_DAY]
            absMedDay = abs(medDay)
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            # BLG
            blgDistPercent = active.parameters.blgDistPercent
            weekdirBotPercentPrev = results[Constants.WEEK_DIR_BOT_DST_PREV]
            weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
            # valores del dia
            numUP = results[Constants.IND_NUM_UP]
            numDOWN = results[Constants.IND_NUM_DOWN]

            sumUP = results[Constants.IND_SUM_UP]
            sumDOWN = results[Constants.IND_SUM_DOWN]
            angle = results[Constants.ANGLE]
            angleCounter = int(results[Constants.ANGLE_COUNTER])
            angleM1 = results[Constants.ANGLEm1]
            angleM2 = results[Constants.ANGLEm21]
            angleUp = float(active.parameters.angleUp)
            angleDown = float(active.parameters.angleDown)
            close_NXT_UP = results[Constants.CLOSE_NXT_UP]
            close_NXT_DOWN = results[Constants.CLOSE_NXT_DOWN]
            # BLG
            IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]
            IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]

            sumDay = int(sumUP) - int(sumDOWN)

            weekdiffTendenceValue = 1
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]

            if prevPercent is not None:
                prevPercent = float(prevPercent)
            if weekdirBotPercent is not None:
                weekdirBotPercent = float(weekdirBotPercent)
            if weekdirBotPercentPrev is not None:
                weekdirBotPercentPrev = float(weekdirBotPercentPrev)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]
            # if med == 0:
            #     if direction == Constants.DIR_UP:
            #         med = 1
            #     elif direction == Constants.DIR_DOWN:
            #         med = -1
            # percentFlow = Constants.DIR_WAIT
            # if percent > prevPercent:
            #     percentFlow = Constants.DIR_UP
            # else:
            #     # baja
            #     percentFlow = Constants.DIR_DOWN
            # CALCULOS final del
            week_prev_res = None
            if week_prev_med < week_med:
                week_prev_res = Constants.DIR_UP
            elif week_prev_med > week_med:
                week_prev_res = Constants.DIR_DOWN

            rising, angleDiff = self.isRisingAngleHourly(results, active)
            if rising:
                # SUBE
                res = Constants.DIR_UP
                res = self.verifyExtremeValuesUP_03(res, week_prev_res, results, active)

            else:
                # BAJA
                res = Constants.DIR_DOWN
                res = self.verifyExtremeValuesDOWN_03(res, week_prev_res, results, active)
        except Exception as error:
            print("Error getProb_HOURLY_ANGLE_01", error)
        return res

    @classmethod
    def getProb_END_HOURLY_ANGLE_02(self, results, active):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            weekFlow = results[Constants.WEEK_FLOW]
            weekPrev = results[Constants.WEEK_FLOW_PREV]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            week_med_abs = abs(results[Constants.WEEK_FLOW_MED])

            flowdiff = results[Constants.FLOW_DIFF]
            week_std = results[Constants.WEEK_FLOW_STD]
            weekdiff = results[Constants.WEEK_FLOW_DIFF]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            medDay = results[Constants.INDICATOR_MED_DAY]
            absMedDay = abs(medDay)
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            # BLG
            blgDistPercent = active.parameters.blgDistPercent
            weekdirBotPercentPrev = results[Constants.WEEK_DIR_BOT_DST_PREV]
            weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
            # valores del dia
            numUP = results[Constants.IND_NUM_UP]
            numDOWN = results[Constants.IND_NUM_DOWN]

            sumUP = results[Constants.IND_SUM_UP]
            sumDOWN = results[Constants.IND_SUM_DOWN]
            angle = results[Constants.ANGLE]
            angleCounter = int(results[Constants.ANGLE_COUNTER])
            angleM1 = results[Constants.ANGLEm1]
            angleM2 = results[Constants.ANGLEm21]
            angleUp = float(active.parameters.angleUp)
            angleDown = float(active.parameters.angleDown)
            close_NXT_UP = results[Constants.CLOSE_NXT_UP]
            close_NXT_DOWN = results[Constants.CLOSE_NXT_DOWN]
            # BLG
            IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]
            IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]

            sumDay = int(sumUP) - int(sumDOWN)

            weekdiffTendenceValue = 1
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]

            if prevPercent is not None:
                prevPercent = float(prevPercent)
            if weekdirBotPercent is not None:
                weekdirBotPercent = float(weekdirBotPercent)
            if weekdirBotPercentPrev is not None:
                weekdirBotPercentPrev = float(weekdirBotPercentPrev)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]
            # if med == 0:
            #     if direction == Constants.DIR_UP:
            #         med = 1
            #     elif direction == Constants.DIR_DOWN:
            #         med = -1
            # percentFlow = Constants.DIR_WAIT
            # if percent > prevPercent:
            #     percentFlow = Constants.DIR_UP
            # else:
            #     # baja
            #     percentFlow = Constants.DIR_DOWN
            # CALCULOS final del
            week_prev_res = None
            if week_prev_med < week_med:
                week_prev_res = Constants.DIR_UP
            elif week_prev_med > week_med:
                week_prev_res = Constants.DIR_DOWN

            # rising, angleDiff = self.isRisingAngle(results)
            risinghourly, angleHourlyDiff = self.isRisingAngle(results)
            if risinghourly:
                # SUBE
                res = Constants.DIR_UP
                res = self.verifyExtremeValuesUP_03(res, week_prev_res, results, active)

            else:
                # BAJA
                res = Constants.DIR_DOWN
                res = self.verifyExtremeValuesDOWN_06(res, week_prev_res, results, active)
        except Exception as error:
            print("Error getProb_END_HOURLY_ANGLE_02", error)
        return res

    @classmethod
    def getProb_END_WEEK_MONTH_01(self, results, active):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            weekFlow = results[Constants.WEEK_FLOW]
            weekPrev = results[Constants.WEEK_FLOW_PREV]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            closeWeekDiffNew = active.parameters.closeWeekDiffNew
            # BLG
            IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]
            IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]


            week_prev_res = None
            isRisingMonth, angleDiffMonth = self.isRisingFromMONTH(results)
            if isRisingMonth:
                week_prev_res = Constants.DIR_UP
            else:
                week_prev_res = Constants.DIR_DOWN


            isRising, angleDiff = self.isRisingFromWEEKNEW(results)
            if isRising:
                if angleDiff > 0 and (angleDiff > closeWeekDiffNew):
                    res = Constants.DIR_UP
                else:
                    # SUBE
                    res = Constants.DIR_UP
                    res = self.verifyExtremeValuesUP_03(res, week_prev_res, results, active)

            else:
                if angleDiff < 0 and (abs(angleDiff) > closeWeekDiffNew):
                    res = Constants.DIR_DOWN
                else:
                    # BAJA
                    res = Constants.DIR_DOWN
                    res = self.verifyExtremeValuesDOWN_06(res, week_prev_res, results, active)
        except Exception as error:
            print("Error getProb_END_WEEK_MONTH_01", error)
        return res

    @classmethod
    def getProb_END_HOURLY_ANGLE_03(self, results, active):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            weekFlow = results[Constants.WEEK_FLOW]
            weekPrev = results[Constants.WEEK_FLOW_PREV]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            week_med_abs = abs(results[Constants.WEEK_FLOW_MED])

            flowdiff = results[Constants.FLOW_DIFF]
            week_std = results[Constants.WEEK_FLOW_STD]
            weekdiff = results[Constants.WEEK_FLOW_DIFF]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            medDay = results[Constants.INDICATOR_MED_DAY]
            absMedDay = abs(medDay)
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            # BLG
            blgDistPercent = active.parameters.blgDistPercent
            weekdirBotPercentPrev = results[Constants.WEEK_DIR_BOT_DST_PREV]
            weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
            # valores del dia
            numUP = results[Constants.IND_NUM_UP]
            numDOWN = results[Constants.IND_NUM_DOWN]

            sumUP = results[Constants.IND_SUM_UP]
            sumDOWN = results[Constants.IND_SUM_DOWN]
            angle = results[Constants.ANGLE]
            angleCounter = int(results[Constants.ANGLE_COUNTER])
            angleM1 = results[Constants.ANGLEm1]
            angleM2 = results[Constants.ANGLEm21]
            angleUp = float(active.parameters.angleUp)
            angleDown = float(active.parameters.angleDown)
            close_NXT_UP = results[Constants.CLOSE_NXT_UP]
            close_NXT_DOWN = results[Constants.CLOSE_NXT_DOWN]
            # BLG
            IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]
            IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]

            sumDay = int(sumUP) - int(sumDOWN)

            weekdiffTendenceValue = 1
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]

            if prevPercent is not None:
                prevPercent = float(prevPercent)
            if weekdirBotPercent is not None:
                weekdirBotPercent = float(weekdirBotPercent)
            if weekdirBotPercentPrev is not None:
                weekdirBotPercentPrev = float(weekdirBotPercentPrev)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]
            # if med == 0:
            #     if direction == Constants.DIR_UP:
            #         med = 1
            #     elif direction == Constants.DIR_DOWN:
            #         med = -1
            # percentFlow = Constants.DIR_WAIT
            # if percent > prevPercent:
            #     percentFlow = Constants.DIR_UP
            # else:
            #     # baja
            #     percentFlow = Constants.DIR_DOWN
            # CALCULOS final del
            week_prev_res = None
            if week_prev_med < week_med:
                week_prev_res = Constants.DIR_UP
            elif week_prev_med > week_med:
                week_prev_res = Constants.DIR_DOWN

            # rising, angleDiff = self.isRisingAngleHourly(results, active)
            rising, angleDiff = self.isRisingAngleIma1(results)
            if rising:
                # SUBE
                res = Constants.DIR_UP
                res = self.verifyExtremeValuesUP_03(res, week_prev_res, results, active)

            else:
                # BAJA
                res = Constants.DIR_DOWN
                res = self.verifyExtremeValuesDOWN_05(res, week_prev_res, results, active)
        except Exception as error:
            print("Error getProb_END_HOURLY_ANGLE_03", error)
        return res

    @classmethod
    def getProb_END_HOURLY_ANGLE_04(self, results, active):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            weekFlow = results[Constants.WEEK_FLOW]
            weekPrev = results[Constants.WEEK_FLOW_PREV]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            week_med_abs = abs(results[Constants.WEEK_FLOW_MED])

            flowdiff = results[Constants.FLOW_DIFF]
            week_std = results[Constants.WEEK_FLOW_STD]
            weekdiff = results[Constants.WEEK_FLOW_DIFF]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            medDay = results[Constants.INDICATOR_MED_DAY]
            absMedDay = abs(medDay)
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            # BLG
            blgDistPercent = active.parameters.blgDistPercent
            weekdirBotPercentPrev = results[Constants.WEEK_DIR_BOT_DST_PREV]
            weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
            # valores del dia
            numUP = results[Constants.IND_NUM_UP]
            numDOWN = results[Constants.IND_NUM_DOWN]

            sumUP = results[Constants.IND_SUM_UP]
            sumDOWN = results[Constants.IND_SUM_DOWN]
            angle = results[Constants.ANGLE]
            angleCounter = int(results[Constants.ANGLE_COUNTER])
            angleM1 = results[Constants.ANGLEm1]
            angleM2 = results[Constants.ANGLEm21]
            angleUp = float(active.parameters.angleUp)
            angleDown = float(active.parameters.angleDown)
            close_NXT_UP = results[Constants.CLOSE_NXT_UP]
            close_NXT_DOWN = results[Constants.CLOSE_NXT_DOWN]
            hourlyAngleMed = results[Constants.HOURLY_ANGLE_MED]
            hourlyAngleMedAbs = abs(results[Constants.HOURLY_ANGLE_MED])
            # BLG
            IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]
            IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]

            sumDay = int(sumUP) - int(sumDOWN)

            weekdiffTendenceValue = 1
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]

            if prevPercent is not None:
                prevPercent = float(prevPercent)
            if weekdirBotPercent is not None:
                weekdirBotPercent = float(weekdirBotPercent)
            if weekdirBotPercentPrev is not None:
                weekdirBotPercentPrev = float(weekdirBotPercentPrev)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]
            # if med == 0:
            #     if direction == Constants.DIR_UP:
            #         med = 1
            #     elif direction == Constants.DIR_DOWN:
            #         med = -1
            # percentFlow = Constants.DIR_WAIT
            # if percent > prevPercent:
            #     percentFlow = Constants.DIR_UP
            # else:
            #     # baja
            #     percentFlow = Constants.DIR_DOWN
            # CALCULOS final del
            week_prev_res = None
            if week_prev_med < week_med:
                week_prev_res = Constants.DIR_UP
            elif week_prev_med > week_med:
                week_prev_res = Constants.DIR_DOWN

            # rising, angleDiff = self.isRisingAngle(results)
            risinghourly, angleHourlyDiff = self.isRisingAngle(results)

            # if hourlyAngleMed < 0:
            #         risinghourly = False
            # else:
            #         risinghourly = True

            if risinghourly:
                # SUBE
                res = Constants.DIR_UP
                res = self.verifyExtremeValuesUP_03(res, week_prev_res, results, active)

            else:
                # BAJA
                res = Constants.DIR_DOWN
                res = self.verifyExtremeValuesDOWN_06(res, week_prev_res, results, active)
        except Exception as error:
            print("Error getProb_END_HOURLY_ANGLE_04", error)
        return res

    @classmethod
    def getProb_END_HOURLY_ANGLE_05(self, results, active):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            weekFlow = results[Constants.WEEK_FLOW]
            weekPrev = results[Constants.WEEK_FLOW_PREV]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            week_med_abs = abs(results[Constants.WEEK_FLOW_MED])

            flowdiff = results[Constants.FLOW_DIFF]
            week_std = results[Constants.WEEK_FLOW_STD]
            weekdiff = results[Constants.WEEK_FLOW_DIFF]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            medDay = results[Constants.INDICATOR_MED_DAY]
            absMedDay = abs(medDay)
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            # BLG
            blgDistPercent = active.parameters.blgDistPercent
            weekdirBotPercentPrev = results[Constants.WEEK_DIR_BOT_DST_PREV]
            weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
            # valores del dia
            numUP = results[Constants.IND_NUM_UP]
            numDOWN = results[Constants.IND_NUM_DOWN]

            sumUP = results[Constants.IND_SUM_UP]
            sumDOWN = results[Constants.IND_SUM_DOWN]
            angle = results[Constants.ANGLE]
            angleCounter = int(results[Constants.ANGLE_COUNTER])
            angleM1 = results[Constants.ANGLEm1]
            angleM2 = results[Constants.ANGLEm21]
            angleUp = float(active.parameters.angleUp)
            angleDown = float(active.parameters.angleDown)
            close_NXT_UP = results[Constants.CLOSE_NXT_UP]
            close_NXT_DOWN = results[Constants.CLOSE_NXT_DOWN]
            # BLG
            IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]
            IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]

            sumDay = int(sumUP) - int(sumDOWN)

            weekdiffTendenceValue = 1
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]

            if prevPercent is not None:
                prevPercent = float(prevPercent)
            if weekdirBotPercent is not None:
                weekdirBotPercent = float(weekdirBotPercent)
            if weekdirBotPercentPrev is not None:
                weekdirBotPercentPrev = float(weekdirBotPercentPrev)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]
            # if med == 0:
            #     if direction == Constants.DIR_UP:
            #         med = 1
            #     elif direction == Constants.DIR_DOWN:
            #         med = -1
            # percentFlow = Constants.DIR_WAIT
            # if percent > prevPercent:
            #     percentFlow = Constants.DIR_UP
            # else:
            #     # baja
            #     percentFlow = Constants.DIR_DOWN
            # CALCULOS final del
            week_prev_res = None
            if week_prev_med < week_med:
                week_prev_res = Constants.DIR_UP
            elif week_prev_med > week_med:
                week_prev_res = Constants.DIR_DOWN

            # rising, angleDiff = self.isRisingAngleHourly(results, active)
            rising, angleDiff = self.isRisingAngleIma1(results)
            if rising:
                # SUBE
                res = Constants.DIR_UP
                res = self.verifyExtremeValuesUP_04(res, week_prev_res, results, active)

            else:
                # BAJA
                res = Constants.DIR_DOWN
                res = self.verifyExtremeValuesDOWN_05(res, week_prev_res, results, active)
        except Exception as error:
            print("Error getProb_END_HOURLY_ANGLE_05", error)
        return res

    @classmethod
    def getProb_END_RSI_01(self, results, active):
        res = Constants.DIR_WAIT
        try:
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]



            week_prev_res = None
            if week_prev_med < week_med:
                week_prev_res = Constants.DIR_UP
            elif week_prev_med > week_med:
                week_prev_res = Constants.DIR_DOWN

            # rising, angleDiff = self.isRisingAngleHourly(results, active)
            rising, angleDiff = self.isRisingRSI(results)
            if rising:
                # SUBE
                res = Constants.DIR_UP
                res = self.verifyExtremeValuesUP_05(res, week_prev_res, results, active)

            else:
                # BAJA
                res = Constants.DIR_DOWN
                res = self.verifyExtremeValuesDOWN_05(res, week_prev_res, results, active)
        except Exception as error:
            print("Error getProb_END_RSI_01", error)
        return res

    @classmethod
    def getProb_END_EMA_RSI_01(self, results, active):
        res = Constants.DIR_WAIT
        try:
            # Indicadores base
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]

            # RSI (Numeric), EMA (Literal), EMA50 (Literal)
            rsi = results[Constants.RSI]
            ema = results[Constants.INDICATOR_EMA]
            ema50 = results[Constants.INDICATOR_EMA50]

            # Determinamos week_prev_res
            week_prev_res = None
            if week_prev_med < week_med:
                week_prev_res = Constants.DIR_UP
            elif week_prev_med > week_med:
                week_prev_res = Constants.DIR_DOWN

            # Lógica de Confluencia: RSI + EMA + EMA50
            if ema == Constants.INDICATOR_EMA_BUY and ema50 == Constants.INDICATOR_EMA_BUY:
                if rsi < 75:  # Zona alcista saludable
                    res = Constants.DIR_UP
                    res = self.verifyExtremeValuesUP_06(res, week_prev_res, results, active)
                else:
                    res = Constants.DIR_WAIT

            elif ema == Constants.INDICATOR_EMA_SELL and ema50 == Constants.INDICATOR_EMA_SELL:
                if rsi > 25:  # Zona bajista saludable
                    res = Constants.DIR_DOWN
                    res = self.verifyExtremeValuesDOWN_05(res, week_prev_res, results, active)
                else:
                    res = Constants.DIR_WAIT

            else:
                # Fallback: Sin confluencia clara de EMAs, usamos HOURLY_ANGLE (v05)
                rising, angleDiff = self.isRisingAngleIma1(results)
                if rising:
                    res = Constants.DIR_UP
                    res = self.verifyExtremeValuesUP_04(res, week_prev_res, results, active)
                else:
                    res = Constants.DIR_DOWN
                    res = self.verifyExtremeValuesDOWN_05(res, week_prev_res, results, active)

        except Exception as error:
            print("Error getProb_END_EMA_RSI_01", error)
        return res

    @classmethod
    def getANGLE_END_BLG_01(self, results, active):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            weekFlow = results[Constants.WEEK_FLOW]
            weekPrev = results[Constants.WEEK_FLOW_PREV]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            week_med_abs = abs(results[Constants.WEEK_FLOW_MED])

            flowdiff = results[Constants.FLOW_DIFF]
            week_std = results[Constants.WEEK_FLOW_STD]
            weekdiff = results[Constants.WEEK_FLOW_DIFF]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            medDay = results[Constants.INDICATOR_MED_DAY]
            absMedDay = abs(medDay)
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            # BLG
            blgDistPercent = active.parameters.blgDistPercent
            weekdirBotPercentPrev = results[Constants.WEEK_DIR_BOT_DST_PREV]
            weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
            # valores del dia
            numUP = results[Constants.IND_NUM_UP]
            numDOWN = results[Constants.IND_NUM_DOWN]

            sumUP = results[Constants.IND_SUM_UP]
            sumDOWN = results[Constants.IND_SUM_DOWN]
            angle = results[Constants.ANGLE]
            angleCounter = int(results[Constants.ANGLE_COUNTER])
            angleM1 = results[Constants.ANGLEm1]
            angleM2 = results[Constants.ANGLEm21]
            angleUp = float(active.parameters.angleUp)
            angleDown = float(active.parameters.angleDown)
            close_NXT_UP = results[Constants.CLOSE_NXT_UP]
            close_NXT_DOWN = results[Constants.CLOSE_NXT_DOWN]
            # BLG
            IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]
            IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]

            sumDay = int(sumUP) - int(sumDOWN)

            weekdiffTendenceValue = 1
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]

            if prevPercent is not None:
                prevPercent = float(prevPercent)
            if weekdirBotPercent is not None:
                weekdirBotPercent = float(weekdirBotPercent)
            if weekdirBotPercentPrev is not None:
                weekdirBotPercentPrev = float(weekdirBotPercentPrev)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]
            # if med == 0:
            #     if direction == Constants.DIR_UP:
            #         med = 1
            #     elif direction == Constants.DIR_DOWN:
            #         med = -1
            # percentFlow = Constants.DIR_WAIT
            # if percent > prevPercent:
            #     percentFlow = Constants.DIR_UP
            # else:
            #     # baja
            #     percentFlow = Constants.DIR_DOWN
            # CALCULOS final del
            week_prev_res = None
            if week_prev_med < week_med:
                week_prev_res = Constants.DIR_UP
                # if flowdiff > 0:
                #     week_prev_res = Constants.DIR_UP
                # else:
                #     week_prev_res = Constants.DIR_DOWN
                #     ndad =""
                #     # ver que hacer cuando no coinciden
                #     print(f" getProMEDSTD_END_BLG_05 NO COINCIDE")
            elif week_prev_med > week_med:
                week_prev_res = Constants.DIR_DOWN
                # if flowdiff < 0:
                #     week_prev_res = Constants.DIR_DOWN
                # else:
                #     week_prev_res = Constants.DIR_UP
                #     ndad =""
                #     # ver que hacer cuando no coinciden
                #     print(f" getProMEDSTD_END_BLG_05 NO COINCIDE")
            if weekFlow == Constants.WEEK_FLOW_UP:
                # SUBE
                res = Constants.DIR_UP

                # if abs(week_med) < 1:
                res = self.verifyExtremeValuesUP_02(res, week_prev_res, results, active)

            else:
                # BAJA
                res = Constants.DIR_DOWN

                res = self.verifyExtremeValuesDOWN_01(res, weekdirBotPercent, active, angle, angleCounter, weekFlow,
                                                      IND_BLG_LOWER_DST_PERCENT, week_prev_res)
        except Exception as error:
            print("Error getProMEDSTD_END BLG05", error)
        return res

    @classmethod
    def getANGLE_END_WEEK_NEW_01(self, results, active):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            weekFlow = results[Constants.WEEK_FLOW]
            weekPrev = results[Constants.WEEK_FLOW_PREV]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            closeWeekDiffNew = active.parameters.closeWeekDiffNew
            # BLG
            IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]
            IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]

            week_prev_res = None
            isRisingMonth, angleDiffMonth = self.isRisingFromMONTH(results)
            if isRisingMonth:
                week_prev_res = Constants.DIR_UP
            else:
                week_prev_res = Constants.DIR_DOWN

            isRising, angleDiff = self.isRisingFromWEEKNEW(results)
            if isRising:

                res = Constants.DIR_UP
                res = self.verifyExtVal_UP_Week_01(res, week_prev_res, results, active)

            else:

                # BAJA
                res = Constants.DIR_DOWN
                res = self.verifyExtVal_DOWN_WEEK_01(res, week_prev_res, results, active)
        except Exception as error:
            print("Error getANGLE_END_WEEK_NEW_01", error)
        return res

    @classmethod
    def getANGLE_END_WEEK_NEW_02(self, results, active):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            weekFlow = results[Constants.WEEK_FLOW]
            weekPrev = results[Constants.WEEK_FLOW_PREV]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            closeWeekDiffNew = active.parameters.closeWeekDiffNew
            # BLG
            IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]
            IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]

            week_prev_res = None
            isRisingMonth, angleDiffMonth = self.isRisingFromMONTH(results)
            if isRisingMonth:
                week_prev_res = Constants.DIR_UP
            else:
                week_prev_res = Constants.DIR_DOWN

            isRising, angleDiff = self.isRisingFromWEEKNEW(results)
            if isRising:

                res = Constants.DIR_UP
                res = self.verifyExtVal_UP_Week_02(res, week_prev_res, results, active)

            else:

                # BAJA
                res = Constants.DIR_DOWN
                res = self.verifyExtVal_DOWN_WEEK_02(res, week_prev_res, results, active)
        except Exception as error:
            print("Error getANGLE_END_WEEK_NEW_01", error)
        return res

    @classmethod
    def convertir_a_float(self, valor):
        try:
            if valor is None or valor == "":
                return 0.0
            return float(valor)
        except ValueError:
            return 0.0

    @classmethod
    def getANGLE_START_WEEK_NEW_01(self, results, active):
        res = Constants.DIR_WAIT
        try:

            indicator_ema = results[Constants.INDICATOR_EMA]
            # blgma_min_diff = float(active.parameters.blgma_min_diff)
            blgma_min_diff = float(getattr(active.parameters, 'blgma_min_diff', 0.0) or 0.0)
            # blgna_mean = float(results[Constants.BLG_MA_MEAN])
            raw_value = results.get(Constants.BLG_MA_MEAN)  # Devuelve None si no existe

            blgna_mean = self.convertir_a_float(raw_value)
            closeWeekDiffNew = active.parameters.closeWeekDiffNew
            # BLG
            week_prev_res = None
            isRisingMonth, angleDiffMonth = self.isRisingFromMONTH(results)
            if isRisingMonth:
                week_prev_res = Constants.DIR_UP
            else:
                week_prev_res = Constants.DIR_DOWN

            isRisingima1, angleDiffima1 = self.isRisingAngleIma1(results)

            isRising, angleDiff = self.isRisingFromWEEKNEW(results)
            if indicator_ema==Constants.INDICATOR_EMA_BUY:
                res = Constants.DIR_UP
                if blgna_mean < 0:
                    if abs(blgna_mean) > blgma_min_diff:
                        res = Constants.DIR_DOWN
                    else:
                        nada = ""
                        if not isRisingMonth:
                            res = Constants.DIR_DOWN
                    # res = self.verifyExtremeValuesUP_03(res, week_prev_res, results, active)

            else:

                # BAJA
                res = Constants.DIR_DOWN
                if blgna_mean > 0:
                    if abs(blgna_mean) > blgma_min_diff:
                        res = Constants.DIR_UP
                    else:
                        nada = ""
                        if isRisingMonth:
                            res = Constants.DIR_UP
                # res = self.verifyExtremeValuesDOWN_06(res, week_prev_res, results, active)
        except Exception as error:
            print("Error getANGLE_START_WEEK_NEW_01", error)
        return res



    @classmethod
    def getANGLE_START_BLG_01(self, results, active):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            week = results[Constants.WEEK_FLOW]
            weekPrev = results[Constants.WEEK_FLOW_PREV]
            weekDir = results[Constants.WEEK_DIR]
            weekminDir = results[Constants.WEEK_MIN_DIR]
            weekmaxDir = results[Constants.WEEK_MAX_DIR]
            weekTopDst = results[Constants.WEEK_DIR_TOP_DST]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            week_med_abs = abs(results[Constants.WEEK_FLOW_MED])
            flowdiff = results[Constants.FLOW_DIFF]
            week_std = results[Constants.WEEK_FLOW_STD]
            weekdiff = results[Constants.WEEK_FLOW_DIFF]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            medDay = results[Constants.INDICATOR_MED_DAY]
            absMedDay = abs(medDay)
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            # BLG
            IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]
            IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
            blgDistPercent = active.parameters.blgDistPercent

            # valores del dia
            numUP = results[Constants.IND_NUM_UP]
            numDOWN = results[Constants.IND_NUM_DOWN]

            sumUP = results[Constants.IND_SUM_UP]
            sumDOWN = results[Constants.IND_SUM_DOWN]

            sumDay = int(sumUP) - int(sumDOWN)

            res = Constants.DIR_WAIT
            weekdiffTendenceValue = 1
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]

            if prevPercent is not None:
                prevPercent = float(prevPercent)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]
            # if med == 0:
            #     if direction == Constants.DIR_UP:
            #         med = 1
            #     elif direction == Constants.DIR_DOWN:
            #         med = -1
            # percentFlow = Constants.DIR_WAIT
            # if percent > prevPercent:
            #     percentFlow = Constants.DIR_UP
            # else:
            #     # baja
            #     percentFlow = Constants.DIR_DOWN
            # CALCULOS final del
            week_prev_res = None
            if week_prev_med < week_med:
                week_prev_res = Constants.DIR_UP
                # if flowdiff > 0:
                #     week_prev_res = Constants.DIR_UP
                # else:
                #     week_prev_res = Constants.DIR_DOWN
                #     ndad =""
                #     # ver que hacer cuando no coinciden
                #     print(f" getProMEDSTD_END_BLG_05 NO COINCIDE")
            elif week_prev_med > week_med:
                week_prev_res = Constants.DIR_DOWN
                # if flowdiff < 0:
                #     week_prev_res = Constants.DIR_DOWN
                # else:
                #     week_prev_res = Constants.DIR_UP
                #     ndad =""
                #     # ver que hacer cuando no coinciden
                #     print(f" getProMEDSTD_END_BLG_05 NO COINCIDE")
            secondCriteria = False
            if weekTopDst >= 75:
                secondCriteria = True
            elif weekTopDst <= 25:
                secondCriteria = True
            if "UP" in weekDir:
                # SUBE
                res = Constants.DIR_UP

                # if abs(week_med) < 1:
                res = self.verifyExtremeValuesUP_02(res, week_prev_res, results, active)

            elif "DOWN" in weekDir:
                # BAJA
                res = Constants.DIR_DOWN

                res = self.verifyExtremeValuesDOWN_02(res, week_prev_res,results, active)

        except Exception as error:
            print("Error getProb_WEEK_DIRECTION_02 ", error)
        return res

    @classmethod
    def getANGLE_START_BLG_02(self, results, active):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            week = results[Constants.WEEK_FLOW]
            weekPrev = results[Constants.WEEK_FLOW_PREV]
            weekDir = results[Constants.WEEK_DIR]
            weekminDir = results[Constants.WEEK_MIN_DIR]
            weekmaxDir = results[Constants.WEEK_MAX_DIR]
            weekTopDst = results[Constants.WEEK_DIR_TOP_DST]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            week_med_abs = abs(results[Constants.WEEK_FLOW_MED])
            flowdiff = results[Constants.FLOW_DIFF]
            week_std = results[Constants.WEEK_FLOW_STD]
            weekdiff = results[Constants.WEEK_FLOW_DIFF]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            medDay = results[Constants.INDICATOR_MED_DAY]
            absMedDay = abs(medDay)
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            # BLG
            IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]
            IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
            blgDistPercent = active.parameters.blgDistPercent

            # valores del dia
            numUP = results[Constants.IND_NUM_UP]
            numDOWN = results[Constants.IND_NUM_DOWN]

            sumUP = results[Constants.IND_SUM_UP]
            sumDOWN = results[Constants.IND_SUM_DOWN]

            sumDay = int(sumUP) - int(sumDOWN)

            res = Constants.DIR_WAIT
            weekdiffTendenceValue = 1
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]

            if prevPercent is not None:
                prevPercent = float(prevPercent)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]

            # CALCULOS final del
            week_prev_res = None
            if week_prev_med < week_med:
                week_prev_res = Constants.DIR_UP

            elif week_prev_med > week_med:
                week_prev_res = Constants.DIR_DOWN

            secondCriteria = False
            if weekTopDst >= 75:
                secondCriteria = True
            elif weekTopDst <= 25:
                secondCriteria = True
            if "UP" in weekDir:
                # SUBE
                res = Constants.DIR_UP

                # if abs(week_med) < 1:
                res = self.verifyExtremeValuesUP_02(res, week_prev_res, results, active)

            elif "DOWN" in weekDir:
                # BAJA
                res = Constants.DIR_DOWN

                res = self.verifyExtremeValuesDOWN_02(res, week_prev_res, results, active)

        except Exception as error:
            print("Error getProb_WEEK_DIRECTION_02 ", error)
        return res

    @classmethod
    def getANGLE_START_BLG_05(self, results, active):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            week = results[Constants.WEEK_FLOW]
            weekPrev = results[Constants.WEEK_FLOW_PREV]
            weekDir = results[Constants.WEEK_DIR]
            weekminDir = results[Constants.WEEK_MIN_DIR]
            weekmaxDir = results[Constants.WEEK_MAX_DIR]
            weekTopDst = results[Constants.WEEK_DIR_TOP_DST]
            C = results[Constants.WEEK_DIR_BOT_DST]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            week_med_abs = abs(results[Constants.WEEK_FLOW_MED])
            flowdiff = results[Constants.FLOW_DIFF]
            week_std = results[Constants.WEEK_FLOW_STD]
            weekdiff = results[Constants.WEEK_FLOW_DIFF]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            medDay = results[Constants.INDICATOR_MED_DAY]
            absMedDay = abs(medDay)
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            # BLG
            IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]
            IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
            blgDistPercent = active.parameters.blgDistPercent

            # valores del dia
            numUP = results[Constants.IND_NUM_UP]
            numDOWN = results[Constants.IND_NUM_DOWN]

            sumUP = results[Constants.IND_SUM_UP]
            sumDOWN = results[Constants.IND_SUM_DOWN]

            sumDay = int(sumUP) - int(sumDOWN)

            res = Constants.DIR_WAIT
            weekdiffTendenceValue = 1
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]

            if prevPercent is not None:
                prevPercent = float(prevPercent)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]

            # CALCULOS final del
            week_prev_res = None
            if week_prev_med < week_med:
                week_prev_res = Constants.DIR_UP

            elif week_prev_med > week_med:
                week_prev_res = Constants.DIR_DOWN

            secondCriteria = False
            if weekTopDst >= 75:
                secondCriteria = True
            elif weekTopDst <= 25:
                secondCriteria = True

            risingH, angleHdiff = self.isRisingAngleHourly(results, active)
            rising, anglediff = self.isRisingAngle(results)
            risingIma1, anglediff = self.isRisingAngleIma1(results)

            if risingIma1:
                # SUBE
                res = Constants.DIR_UP

                # if abs(week_med) < 1:
                res = self.verifyExtremeValuesUP_05(res, week_prev_res, results, active)

            else:
                # BAJA
                res = Constants.DIR_DOWN

                res = self.verifyExtremeValuesDOWN_02(res, week_prev_res, results, active)

        except Exception as error:
            print("Error getANGLE_START_BLG_03 ", error)
        return res

    @classmethod
    def getSTART_NONE(self, results, active):
        res = Constants.DIR_WAIT
        return res


    @classmethod
    def getANGLE_START_BLG_03(self, results, active):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            week = results[Constants.WEEK_FLOW]
            weekPrev = results[Constants.WEEK_FLOW_PREV]
            weekDir = results[Constants.WEEK_DIR]
            weekminDir = results[Constants.WEEK_MIN_DIR]
            weekmaxDir = results[Constants.WEEK_MAX_DIR]
            weekTopDst = results[Constants.WEEK_DIR_TOP_DST]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            week_med_abs = abs(results[Constants.WEEK_FLOW_MED])
            flowdiff = results[Constants.FLOW_DIFF]
            week_std = results[Constants.WEEK_FLOW_STD]
            weekdiff = results[Constants.WEEK_FLOW_DIFF]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            medDay = results[Constants.INDICATOR_MED_DAY]
            absMedDay = abs(medDay)
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            # BLG
            IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]
            IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
            blgDistPercent = active.parameters.blgDistPercent

            # valores del dia
            numUP = results[Constants.IND_NUM_UP]
            numDOWN = results[Constants.IND_NUM_DOWN]

            sumUP = results[Constants.IND_SUM_UP]
            sumDOWN = results[Constants.IND_SUM_DOWN]

            sumDay = int(sumUP) - int(sumDOWN)

            res = Constants.DIR_WAIT
            weekdiffTendenceValue = 1
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]

            if prevPercent is not None:
                prevPercent = float(prevPercent)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]

            # CALCULOS final del
            week_prev_res = None
            if week_prev_med < week_med:
                week_prev_res = Constants.DIR_UP

            elif week_prev_med > week_med:
                week_prev_res = Constants.DIR_DOWN

            secondCriteria = False
            if weekTopDst >= 75:
                secondCriteria = True
            elif weekTopDst <= 25:
                secondCriteria = True

            risingH, angleHdiff = self.isRisingAngleHourly(results, active)
            rising, anglediff = self.isRisingAngle(results)
            risingIma1, anglediff = self.isRisingAngleIma1(results)

            if risingIma1:
                # SUBE
                res = Constants.DIR_UP

                # if abs(week_med) < 1:
                res = self.verifyExtremeValuesUP_02(res, week_prev_res, results, active)

            else:
                # BAJA
                res = Constants.DIR_DOWN

                res = self.verifyExtremeValuesDOWN_02(res, week_prev_res, results, active)

        except Exception as error:
            print("Error getANGLE_START_BLG_03 ", error)
        return res

    @classmethod
    def getANGLE_START_BLG_04(self, results, active):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            week = results[Constants.WEEK_FLOW]
            weekPrev = results[Constants.WEEK_FLOW_PREV]
            weekDir = results[Constants.WEEK_DIR]
            weekminDir = results[Constants.WEEK_MIN_DIR]
            weekmaxDir = results[Constants.WEEK_MAX_DIR]
            weekTopDst = results[Constants.WEEK_DIR_TOP_DST]
            C = results[Constants.WEEK_DIR_BOT_DST]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            week_med_abs = abs(results[Constants.WEEK_FLOW_MED])
            flowdiff = results[Constants.FLOW_DIFF]
            week_std = results[Constants.WEEK_FLOW_STD]
            weekdiff = results[Constants.WEEK_FLOW_DIFF]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            medDay = results[Constants.INDICATOR_MED_DAY]
            absMedDay = abs(medDay)
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            # BLG
            IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]
            IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
            blgDistPercent = active.parameters.blgDistPercent

            # valores del dia
            numUP = results[Constants.IND_NUM_UP]
            numDOWN = results[Constants.IND_NUM_DOWN]

            sumUP = results[Constants.IND_SUM_UP]
            sumDOWN = results[Constants.IND_SUM_DOWN]

            sumDay = int(sumUP) - int(sumDOWN)

            res = Constants.DIR_WAIT
            weekdiffTendenceValue = 1
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]

            if prevPercent is not None:
                prevPercent = float(prevPercent)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]

            # CALCULOS final del
            week_prev_res = None
            if week_prev_med < week_med:
                week_prev_res = Constants.DIR_UP

            elif week_prev_med > week_med:
                week_prev_res = Constants.DIR_DOWN

            secondCriteria = False
            if weekTopDst >= 75:
                secondCriteria = True
            elif weekTopDst <= 25:
                secondCriteria = True

            risingH, angleHdiff = self.isRisingAngleHourly(results, active)
            rising, anglediff = self.isRisingAngle(results)
            risingIma1, anglediff = self.isRisingAngleIma1(results)

            if risingIma1:
                # SUBE
                res = Constants.DIR_UP

                # if abs(week_med) < 1:
                res = self.verifyExtremeValuesUP_02(res, week_prev_res, results, active)

            else:
                # BAJA
                res = Constants.DIR_DOWN

                res = self.verifyExtremeValuesDOWN_02(res, week_prev_res, results, active)

        except Exception as error:
            print("Error getANGLE_START_BLG_03 ", error)
        return res

    @classmethod
    def getANGLE_START_EMA_RSI_01(self, results, active):
        res = Constants.DIR_WAIT
        try:

            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]

            # RSI (Numeric), EMA (Literal), EMA50 (Literal)
            rsi = results[Constants.RSI]
            ema = results[Constants.INDICATOR_EMA]
            ema50 = results[Constants.INDICATOR_EMA50]
            ema10Angle = results[Constants.EMA10_ANGLE]



            res = Constants.DIR_WAIT



            # CALCULOS final del
            week_prev_res = None
            if week_prev_med < week_med:
                week_prev_res = Constants.DIR_UP

            elif week_prev_med > week_med:
                week_prev_res = Constants.DIR_DOWN


            risingH, angleHdiff = self.isRisingAngleHourly(results, active)
            rising, anglediff = self.isRisingAngle(results)
            risingIma1, anglediff = self.isRisingAngleIma1(results)

            if ema == Constants.INDICATOR_EMA_BUY and ema50 == Constants.INDICATOR_EMA_BUY:
                if rsi < 75:  # Zona alcista saludable
                    # SUBE
                    res = Constants.DIR_UP

                    # if abs(week_med) < 1:
                res = self.verifyExtremeValuesUP_06(res, week_prev_res, results, active)


            elif ema == Constants.INDICATOR_EMA_SELL and ema50 == Constants.INDICATOR_EMA_SELL:

                if rsi > 25:  # Zona bajista saludable
                    # BAJA
                    res = Constants.DIR_DOWN

                res = self.verifyExtremeValuesDOWN_05(res, week_prev_res, results, active)

        except Exception as error:
            print("Error getANGLE_START_EMA_RSI_01 ", error)
        return res
    @classmethod
    def verifyExtremeValuesUP(self, res, weekdirBotPercent,active, angle, angleCounter, weekFlow, IND_BLG_LOWER_DST_PERCENT, week_prev_res):
        res = res
        angleUp = float(active.parameters.angleUp)
        angleDown = float(active.parameters.angleDown)
        weekMedMinLevel = float(active.parameters.weekMEDMinLevel)
        if weekdirBotPercent > 95:
            if abs(angle) < angleDown:
                # determinar un flujo grande de bajada
                if angleCounter !=0 and angleCounter < 3:
                    res = Constants.DIR_DOWN
                else:
                    if "DOWN" in weekFlow:
                        res = Constants.DIR_DOWN

        elif weekdirBotPercent > 80 and weekdirBotPercent < 95:
            if IND_BLG_LOWER_DST_PERCENT > 90:
                if "DOWN" in weekFlow:
                    res = Constants.DIR_DOWN
            else:
                ##esta en medio de todo
                if angle < 0:
                    if abs(angle) > angleDown:
                        if angleCounter >= 3:
                            res = Constants.DIR_DOWN

        else:
            if angle <0:
                if abs(angle) > angleDown:
                    if angleCounter !=0 and angleCounter >= 3:
                        if IND_BLG_LOWER_DST_PERCENT > 10:
                            ##puede bajar
                            # if "DOWN" in weekFlow:
                            res = Constants.DIR_DOWN
        return res

    @classmethod
    def verifyExtremeValuesUP_01(self, res, weekdirBotPercent, active, angle, angleCounter, weekFlow,
                              IND_BLG_LOWER_DST_PERCENT, week_prev_res):
        res = res
        angleUp = float(active.parameters.angleUp)
        angleDown = float(active.parameters.angleDown)
        weekMedMinLevel = float(active.parameters.weekMEDMinLevel)
        if weekdirBotPercent > 95:
            if abs(angle) < angleDown:
                # determinar un flujo grande de bajada
                if angleCounter != 0 and angleCounter < 3:
                    res = Constants.DIR_DOWN
                else:
                    if "DOWN" in week_prev_res:
                        res = Constants.DIR_DOWN

        elif weekdirBotPercent > 80 and weekdirBotPercent < 95:
            if IND_BLG_LOWER_DST_PERCENT > 90:
                if "DOWN" in weekFlow:
                    res = Constants.DIR_DOWN
            else:
                ##esta en medio de todo
                # res = week_prev_res
                if IND_BLG_LOWER_DST_PERCENT >85:
                    res = Constants.DIR_DOWN
                else:
                    res = week_prev_res

        else:
            if angle < 0:
                if abs(angle) > angleDown:
                    if angleCounter != 0 and angleCounter >= 3:
                        if IND_BLG_LOWER_DST_PERCENT > 10:
                            ##puede bajar
                            # if "DOWN" in weekFlow:
                            res = Constants.DIR_DOWN

        return res

    @classmethod
    def verifyExtremeValuesUP_02(self, res, week_prev_res, results, active):
        res = res

        weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
        angle = results[Constants.ANGLE]
        angleCounter = results[Constants.ANGLE_COUNTER]
        angleIma1 = results[Constants.ANGLE_IMA1]
        angleIma1Counter = results[Constants.ANGLE_IMA1_COUNTER]
        ima1EmaMinValue = active.parameters.ima1EmaMinValue
        IND_BLG_LOWER_DST_PERCENT= results[Constants.IND_BLG_LOWER_DST_PERCENT]
        weekFlow = results[Constants.WEEK_FLOW]
        ##se anaden controles BLF_LOWERDIST
        angleUp = float(active.parameters.angleUp)
        angleDown = float(active.parameters.angleDown)
        weekMedMinLevel = float(active.parameters.weekMEDMinLevel)
        if weekdirBotPercent > 95:
            if abs(angle) < angleDown:
                # determinar un flujo grande de bajada
                if angleCounter != 0 and angleCounter < 3:
                    res = Constants.DIR_DOWN
                else:
                    if "DOWN" in week_prev_res:
                        res = Constants.DIR_DOWN

        elif weekdirBotPercent > 80 and weekdirBotPercent < 95:
            if IND_BLG_LOWER_DST_PERCENT > 90:
                if "DOWN" in weekFlow:
                    res = Constants.DIR_DOWN
                else:
                    if results[Constants.IMA1EMADIFF]<0:
                        if abs(results[Constants.IMA1EMADIFF]) >=0.4:
                            res = Constants.DIR_DOWN
            else:
                ##esta en medio de todo
                # res = week_prev_res
                if IND_BLG_LOWER_DST_PERCENT > 85:
                    res = Constants.DIR_DOWN
                else:
                    nada =""
                    # res = week_prev_res

        else:
            if IND_BLG_LOWER_DST_PERCENT > 90:
                if results[Constants.IMA1EMADIFF]< 0:
                    res = Constants.DIR_DOWN
                else:
                    if results[Constants.IMA1EMADIFF] < ima1EmaMinValue:
                        res = Constants.DIR_DOWN

            else:
                if angle < 0:
                    if abs(angle) > angleDown:
                        if angleCounter != 0 and angleCounter >= 3:
                            if IND_BLG_LOWER_DST_PERCENT > 10:
                                ##puede bajar
                                # if "DOWN" in weekFlow:
                                res = Constants.DIR_DOWN
                else:
                    #26-05 controles para down
                    if IND_BLG_LOWER_DST_PERCENT > 70:
                        #podria estar bajando
                        if abs(angleIma1) >= 60:
                            if angleIma1Counter >=2:
                                res = Constants.DIR_DOWN


        return res

    @classmethod
    def verifyExtremeValuesUP_05(self, res, week_prev_res, results, active):
        res = res

        weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
        angle = results[Constants.ANGLE]
        angleCounter = results[Constants.ANGLE_COUNTER]
        angleIma1 = results[Constants.ANGLE_IMA1]
        angleIma1Counter = results[Constants.ANGLE_IMA1_COUNTER]
        ima1EmaMinValue = active.parameters.ima1EmaMinValue
        IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
        weekFlow = results[Constants.WEEK_FLOW]
        ##se anaden controles BLF_LOWERDIST
        angleUp = float(active.parameters.angleUp)
        angleDown = float(active.parameters.angleDown)
        weekMedMinLevel = float(active.parameters.weekMEDMinLevel)
        if weekdirBotPercent > 95:
            # if abs(angle) < angleDown:
            #     # determinar un flujo grande de bajada
            #     if angleCounter != 0 and angleCounter < 3:
            #         res = Constants.DIR_DOWN
            #     else:
            #         if "DOWN" in week_prev_res:
            res = Constants.DIR_DOWN

        elif weekdirBotPercent > 80 and weekdirBotPercent < 95:
            if IND_BLG_LOWER_DST_PERCENT > 90:
                if "DOWN" in weekFlow:
                    res = Constants.DIR_DOWN
                else:
                    if results[Constants.IMA1EMADIFF] < 0:
                        if abs(results[Constants.IMA1EMADIFF]) >= 0.4:
                            res = Constants.DIR_DOWN
            else:
                ##esta en medio de todo
                # res = week_prev_res
                if IND_BLG_LOWER_DST_PERCENT > 85:
                    res = Constants.DIR_DOWN
                else:
                    nada = ""
                    # res = week_prev_res

        else:
            if IND_BLG_LOWER_DST_PERCENT > 90:
                if results[Constants.IMA1EMADIFF] < 0:
                    res = Constants.DIR_DOWN
                else:
                    if results[Constants.IMA1EMADIFF] < ima1EmaMinValue:
                        res = Constants.DIR_DOWN

            else:
               anda = ""


        return res

    @classmethod
    def verifyExtremeValuesUP_03(self, res, week_prev_res, results, active):
        res = res

        weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
        angle = results[Constants.ANGLE]
        angleCounter = results[Constants.ANGLE_COUNTER]
        angleIma1 = results[Constants.ANGLE_IMA1]
        angleIma1Counter = results[Constants.ANGLE_IMA1_COUNTER]

        IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
        weekFlow = results[Constants.WEEK_FLOW]
        ##se anaden controles BLF_LOWERDIST
        angleUp = float(active.parameters.angleUp)
        angleDown = float(active.parameters.angleDown)
        weekMedMinLevel = float(active.parameters.weekMEDMinLevel)
        hourlyAngleDiff = active.parameters.hourlyAngleDiff
        rising, anglediff = self.isRisingFromWEEKNEW(results)
        if weekdirBotPercent > 90:
            if rising==False:
                # determinar un flujo grande de bajada
                if angleCounter != 0 and angleCounter < 3:
                    res = Constants.DIR_DOWN
                else:
                    if "DOWN" in week_prev_res:
                        res = Constants.DIR_DOWN

        elif weekdirBotPercent > 80 and weekdirBotPercent < 90:
            if IND_BLG_LOWER_DST_PERCENT > 90:
                if "DOWN" in weekFlow:
                    res = Constants.DIR_DOWN
                else:
                    if results[Constants.IMA1EMADIFF] < 0:
                        if abs(results[Constants.IMA1EMADIFF]) >= 0.4:
                            res = Constants.DIR_DOWN
            else:
                ##esta en medio de todo
                # res = week_prev_res
                if IND_BLG_LOWER_DST_PERCENT > 85:
                    res = Constants.DIR_DOWN
                else:
                    nada = ""
                    # res = week_prev_res

        else:
            if IND_BLG_LOWER_DST_PERCENT > 80:
                re = res = Constants.DIR_DOWN
            elif IND_BLG_LOWER_DST_PERCENT < 20:
                re = res = Constants.DIR_UP
            else:

                if abs(results[Constants.HOURLY_ANGLE_MED]) > hourlyAngleDiff:
                    if results[Constants.HOURLY_ANGLE_MED] < 0:
                        #bajara porque el angulo es fuerte
                        res = Constants.DIR_DOWN


            

        return res

    @classmethod
    def verifyExtremeValuesUP_04(self, res, week_prev_res, results, active):
        res = res

        weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
        angle = results[Constants.ANGLE]
        angleCounter = results[Constants.ANGLE_COUNTER]
        angleIma1 = results[Constants.ANGLE_IMA1]
        angleIma1Counter = results[Constants.ANGLE_IMA1_COUNTER]

        IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
        weekFlow = results[Constants.WEEK_FLOW]
        ##se anaden controles BLF_LOWERDIST
        angleUp = float(active.parameters.angleUp)
        angleDown = float(active.parameters.angleDown)
        weekMedMinLevel = float(active.parameters.weekMEDMinLevel)
        hourlyAngleDiff = active.parameters.hourlyAngleDiff
        rising, anglediff = self.isRisingFromWEEKNEW(results)
        if weekdirBotPercent > 95:
            if rising == False:
                # determinar un flujo grande de bajada
                if angleCounter != 0 and angleCounter < 3:
                    res = Constants.DIR_DOWN
                else:
                    if "DOWN" in week_prev_res:
                        res = Constants.DIR_DOWN
            else:
                if angleCounter >10:
                    res = Constants.DIR_DOWN

        elif weekdirBotPercent > 80 and weekdirBotPercent < 90:
            if IND_BLG_LOWER_DST_PERCENT > 90:
                if "DOWN" in weekFlow:
                    res = Constants.DIR_DOWN
                else:
                    if results[Constants.IMA1EMADIFF] < 0:
                        if abs(results[Constants.IMA1EMADIFF]) >= 0.4:
                            res = Constants.DIR_DOWN
            else:
                ##esta en medio de todo
                # res = week_prev_res
                if IND_BLG_LOWER_DST_PERCENT > 85:
                    res = Constants.DIR_DOWN
                else:
                    nada = ""
                    # res = week_prev_res

        else:
            if IND_BLG_LOWER_DST_PERCENT > 80:
                re = res = Constants.DIR_DOWN
            elif IND_BLG_LOWER_DST_PERCENT < 20:
                re = res = Constants.DIR_UP
            else:

                if abs(results[Constants.HOURLY_ANGLE_MED]) > hourlyAngleDiff:
                    if results[Constants.HOURLY_ANGLE_MED] < 0:
                        # bajara porque el angulo es fuerte
                        res = Constants.DIR_DOWN

        return res

    @classmethod
    def verifyExtremeValuesUP_06(self, res, week_prev_res, results, active):
        res = res

        weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
        angle = results[Constants.ANGLE]
        angleCounter = results[Constants.ANGLE_COUNTER]
        angleIma1 = results[Constants.ANGLE_IMA1]
        angleIma1Counter = results[Constants.ANGLE_IMA1_COUNTER]

        IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
        weekFlow = results[Constants.WEEK_FLOW]
        ##se anaden controles BLF_LOWERDIST
        angleUp = float(active.parameters.angleUp)
        angleDown = float(active.parameters.angleDown)
        weekMedMinLevel = float(active.parameters.weekMEDMinLevel)
        hourlyAngleDiff = active.parameters.hourlyAngleDiff
        rising, anglediff = self.isRisingFromWEEKNEW(results)
        if weekdirBotPercent > 95:
            if rising == False:
                # determinar un flujo grande de bajada
                if angleCounter != 0 and angleCounter < 3:
                    res = Constants.DIR_DOWN
                else:
                    if "DOWN" in week_prev_res:
                        res = Constants.DIR_DOWN
            else:
                if angleCounter > 10:
                    res = Constants.DIR_DOWN

        elif weekdirBotPercent > 80 and weekdirBotPercent < 90:
            if IND_BLG_LOWER_DST_PERCENT > 90:

                if results[Constants.IMA1EMADIFF] < 0:
                    if abs(results[Constants.IMA1EMADIFF]) >= 0.4:
                        res = Constants.DIR_DOWN
            else:
                ##esta en medio de todo
                # res = week_prev_res
                if IND_BLG_LOWER_DST_PERCENT > 85:
                    res = Constants.DIR_DOWN
                else:
                    nada = ""
                    # res = week_prev_res

        else:
            if IND_BLG_LOWER_DST_PERCENT > 80:
                re = res = Constants.DIR_DOWN
            elif IND_BLG_LOWER_DST_PERCENT < 20:
                re = res = Constants.DIR_UP
            else:

                if abs(results[Constants.HOURLY_ANGLE_MED]) > hourlyAngleDiff:
                    if results[Constants.HOURLY_ANGLE_MED] < 0:
                        # bajara porque el angulo es fuerte
                        res = Constants.DIR_DOWN

        return res
    @classmethod
    def verifyExtVal_UP_Week_01(self, res, week_prev_res, results, active):
        res = res

        weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
        angleCounter = results[Constants.ANGLE_COUNTER]
        closeWeekDiffNew = active.parameters.closeWeekDiffNew

        IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
        weekFlow = results[Constants.WEEK_FLOW]
        ##se anaden controles BLF_LOWERDIST
        hourlyAngleDiff = active.parameters.hourlyAngleDiff

        rising, angleDiff = self.isRisingFromWEEKNEW(results)
        if weekdirBotPercent > 90:
            if angleDiff > 0 and (angleDiff > closeWeekDiffNew):
                res = Constants.DIR_UP
            else:
                # determinar un flujo grande de bajada
                # if angleCounter != 0 and angleCounter < 3:
                #     res = Constants.DIR_DOWN
                # else:
                res = Constants.DIR_DOWN

        elif weekdirBotPercent > 80 and weekdirBotPercent < 90:
            if IND_BLG_LOWER_DST_PERCENT > 90:
                if "DOWN" in weekFlow:
                    res = Constants.DIR_DOWN
                else:
                    if results[Constants.IMA1EMADIFF] < 0:
                        if abs(results[Constants.IMA1EMADIFF]) >= 0.4:
                            res = Constants.DIR_DOWN
            else:
                ##esta en medio de todo
                # res = week_prev_res
                if IND_BLG_LOWER_DST_PERCENT > 85:
                    res = Constants.DIR_DOWN
                else:
                    nada = ""
                    # res = week_prev_res

        else:
            if IND_BLG_LOWER_DST_PERCENT > 80:
                re = res = Constants.DIR_DOWN
            elif IND_BLG_LOWER_DST_PERCENT < 20:
                re = res = Constants.DIR_UP
            else:

                if abs(results[Constants.HOURLY_ANGLE_MED]) > hourlyAngleDiff:
                    if results[Constants.HOURLY_ANGLE_MED] < 0:
                        # bajara porque el angulo es fuerte
                        res = Constants.DIR_DOWN

        return res

    @classmethod
    def verifyExtVal_UP_Week_02(self, res, week_prev_res, results, active):
        res = res

        weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
        angleCounter = results[Constants.ANGLE_COUNTER]
        closeWeekDiffNew = active.parameters.closeWeekDiffNew

        IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
        weekFlow = results[Constants.WEEK_FLOW]
        ##se anaden controles BLF_LOWERDIST
        hourlyAngleDiff = active.parameters.hourlyAngleDiff
        blgma_min_diff = active.parameters.blgma_min_diff
        blgMaMean = results[Constants.BLG_MA_MEAN]

        rising, angleDiff = self.isRisingFromWEEKNEW(results)
        if weekdirBotPercent > 90:
            if blgMaMean < 0 and (abs(blgMaMean) > blgma_min_diff):

                res = Constants.DIR_DOWN

        elif weekdirBotPercent > 80 and weekdirBotPercent < 90:
            if blgMaMean < 0 and (abs(blgMaMean) > blgma_min_diff):
                res = Constants.DIR_DOWN

        else:
            if IND_BLG_LOWER_DST_PERCENT > 80:
                re = res = Constants.DIR_DOWN
            elif IND_BLG_LOWER_DST_PERCENT < 20:
                re = res = Constants.DIR_UP
            else:

                if blgMaMean < 0 and (abs(blgMaMean) > blgma_min_diff):
                    res = Constants.DIR_DOWN

        return res

    @classmethod
    def verifyExtremeValues_START_UP_01(self, res, week_prev_res, results, active):
        res = res

        weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
        angle = results[Constants.ANGLE]
        angleCounter = results[Constants.ANGLE_COUNTER]
        angleIma1 = results[Constants.ANGLE_IMA1]
        angleIma1Counter = results[Constants.ANGLE_IMA1_COUNTER]

        IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
        weekFlow = results[Constants.WEEK_FLOW]
        ##se anaden controles BLF_LOWERDIST
        angleUp = float(active.parameters.angleUp)
        angleDown = float(active.parameters.angleDown)
        weekMedMinLevel = float(active.parameters.weekMEDMinLevel)
        hourlyAngleDiff = active.parameters.hourlyAngleDiff
        rising, anglediff = self.isRisingAngle(results)
        if weekdirBotPercent > 90:
            if weekdirBotPercent > 105:
                res = Constants.DIR_DOWN
            else:
                if rising == False:
                    # determinar un flujo grande de bajada
                    if abs(anglediff) > angleDown:
                        res = Constants.DIR_DOWN


        elif weekdirBotPercent > 80 and weekdirBotPercent < 90:
            if IND_BLG_LOWER_DST_PERCENT > 90:
                if "DOWN" in weekFlow:
                    res = Constants.DIR_DOWN
                else:
                    if results[Constants.IMA1EMADIFF] < 0:
                        if abs(results[Constants.IMA1EMADIFF]) >= 0.4:
                            res = Constants.DIR_DOWN
            else:
                ##esta en medio de todo
                # res = week_prev_res
                if IND_BLG_LOWER_DST_PERCENT > 85:
                    res = Constants.DIR_DOWN
                else:
                    nada = ""
                    # res = week_prev_res

        else:
            if abs(results[Constants.HOURLY_ANGLE_MED]) > hourlyAngleDiff:
                if results[Constants.HOURLY_ANGLE_MED] < 0:
                    # bajara porque el angulo es fuerte
                    res = Constants.DIR_DOWN

        return res

    @classmethod
    def verifyExtremeValuesDOWN(self, res, weekdirBotPercent, active, angle, angleCounter, weekFlow, IND_BLG_LOWER_DST_PERCENT,week_prev_res):
        res = res
        angleUp = float(active.parameters.angleUp)
        angleDown = float(active.parameters.angleDown)
        weekMedMinLevel = float(active.parameters.weekMEDMinLevel)
        if weekdirBotPercent < 5:
            if abs(angle) < angleDown:
                # determinar un flujo grande de bajada
                if angleCounter !=0 and angleCounter < 3:
                    res = Constants.DIR_UP
                else:
                    if "UP" in weekFlow:
                        res = Constants.DIR_UP
        elif weekdirBotPercent > 5 and weekdirBotPercent < 30:
            if IND_BLG_LOWER_DST_PERCENT < 10:
                if "UP" in weekFlow:
                    res = Constants.DIR_UP
            else:
                ##esta en medio de todo
                if angle > 0:
                    if abs(angle) > angleDown:
                        if angleCounter >= 3:
                            res = Constants.DIR_UP
        else:
            if angle > 0:
                if angle > angleUp:
                    if angleCounter !=0 and angleCounter >= 3:
                        if IND_BLG_LOWER_DST_PERCENT < 90:
                            # if "UP" in weekFlow:
                            res = Constants.DIR_UP
        return res

    @classmethod
    def verifyExtremeValuesDOWN_01(self, res, weekdirBotPercent, active, angle, angleCounter, weekFlow,
                                IND_BLG_LOWER_DST_PERCENT, week_prev_res):
        res = res

        angleUp = float(active.parameters.angleUp)
        angleDown = float(active.parameters.angleDown)
        weekMedMinLevel = float(active.parameters.weekMEDMinLevel)
        if weekdirBotPercent < 5:
            if abs(angle) < angleDown:
                # determinar un flujo grande de bajada
                if angleCounter != 0 and angleCounter < 3:
                    res = Constants.DIR_UP
                else:
                    if "UP" in week_prev_res:
                        res = Constants.DIR_UP
        elif weekdirBotPercent > 5 and weekdirBotPercent < 30:
            if IND_BLG_LOWER_DST_PERCENT < 10:
                if "UP" in weekFlow:
                    res = Constants.DIR_UP
            else:
                ##esta en medio de todo
                if IND_BLG_LOWER_DST_PERCENT < 15:
                    res = Constants.DIR_UP
                else:
                    res = week_prev_res
        else:
            if angle > 0:
                if angle > angleUp:
                    if angleCounter != 0 and angleCounter >= 3:
                        if IND_BLG_LOWER_DST_PERCENT < 90:
                            # if "UP" in weekFlow:
                            res = Constants.DIR_UP
        return res


    @classmethod
    def verifyExtremeValuesDOWN_02(self, res, week_prev_res, results, active ):
        res = res
        weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
        angle = results[Constants.ANGLE]
        angleCounter = results[Constants.ANGLE_COUNTER]
        angleIma1 = results[Constants.ANGLE_IMA1]
        angleIma1Counter = results[Constants.ANGLE_IMA1_COUNTER]

        IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
        weekFlow = results[Constants.WEEK_FLOW]
        angleUp = float(active.parameters.angleUp)
        angleDown = float(active.parameters.angleDown)
        weekMedMinLevel = float(active.parameters.weekMEDMinLevel)
        if weekdirBotPercent < 5:
            if abs(angle) > angleDown:
                # determinar un flujo grande de bajada
                if angleCounter != 0 and angleCounter >= 3:
                    res = Constants.DIR_UP
                else:
                    if "UP" in week_prev_res:
                        res = Constants.DIR_UP
        elif weekdirBotPercent > 5 and weekdirBotPercent < 30:
            if IND_BLG_LOWER_DST_PERCENT < 10:
                if "UP" in weekFlow:
                    res = Constants.DIR_UP
            else:
                ##esta en medio de todo
                if IND_BLG_LOWER_DST_PERCENT < 15:
                    res = Constants.DIR_UP
                else:
                    res = week_prev_res
        else:
            if angle > 0:
                if angle > angleUp:
                    if angleCounter != 0 and angleCounter >= 3:
                        if IND_BLG_LOWER_DST_PERCENT < 90:
                            # if "UP" in weekFlow:
                            res = Constants.DIR_UP
        return res


    @classmethod
    def verifyExtremeValuesDOWN_03(self, res, week_prev_res, results, active):
        res = res
        weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
        angle = results[Constants.ANGLE]
        angleCounter = results[Constants.ANGLE_COUNTER]
        angleIma1 = results[Constants.ANGLE_IMA1]
        angleIma1Counter = results[Constants.ANGLE_IMA1_COUNTER]

        IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
        weekFlow = results[Constants.WEEK_FLOW]
        angleUp = float(active.parameters.angleUp)
        angleDown = float(active.parameters.angleDown)
        weekMedMinLevel = float(active.parameters.weekMEDMinLevel)
        risingH, angleHdiff = self.isRisingAngleHourly(results,active)
        rising, anglediff = self.isRisingAngle(results)
        if weekdirBotPercent < 10:
            if results[Constants.HOURLY_ANGLE_MED] > 0:
                res = Constants.DIR_UP
            else:
                if results[Constants.IND_BLG_LOWER_DST_PERCENT] < 15:
                    res = Constants.DIR_UP
        elif weekdirBotPercent > 10 and weekdirBotPercent < 30:
            if risingH:
                # determinar un flujo grande de bajada
                    if "UP" in results[Constants.ANGLE_FLOW]:
                        res = Constants.DIR_UP

            # if IND_BLG_LOWER_DST_PERCENT < 15:
            #     if "UP" in weekFlow:
            #         res = Constants.DIR_UP
            # else:
            #     ##esta en medio de todo
            #     if IND_BLG_LOWER_DST_PERCENT < 15:
            #         res = Constants.DIR_UP
            #     else:
            #         res = week_prev_res
        else:
            nada = ""
            if angleHdiff > 0:
                if "UP" in results[Constants.ANGLE_FLOW]:
                    if angle > angleUp:
                        if rising:
                            # if angleCounter != 0 and angleCounter >= 3:
                                if IND_BLG_LOWER_DST_PERCENT < 90:
                                    # if "UP" in weekFlow:
                                    res = Constants.DIR_UP
        return res

    @classmethod
    def verifyExtremeValuesDOWN_04(self, res, week_prev_res, results, active):
        res = res
        weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
        angle = results[Constants.ANGLE]
        angleCounter = results[Constants.ANGLE_COUNTER]
        angleIma1 = results[Constants.ANGLE_IMA1]
        angleIma1Counter = results[Constants.ANGLE_IMA1_COUNTER]
        ima1Emadiff = results[Constants.IMA1EMADIFF]

        IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
        weekFlow = results[Constants.WEEK_FLOW]
        angleUp = float(active.parameters.angleUp)
        angleDown = float(active.parameters.angleDown)
        weekMedMinLevel = float(active.parameters.weekMEDMinLevel)
        risingH, angleHdiff = self.isRisingAngleHourly(results, active)
        rising, anglediff = self.isRisingAngle(results)
        if weekdirBotPercent < 10:
            if ima1Emadiff >0:
                res = Constants.DIR_UP
            else:
                if results[Constants.HOURLY_ANGLE_MED] > 0:
                    res = Constants.DIR_UP
                else:
                    if results[Constants.IND_BLG_LOWER_DST_PERCENT] < 15:
                        res = Constants.DIR_UP
        elif weekdirBotPercent > 10 and weekdirBotPercent < 30:
            if risingH:
                # determinar un flujo grande de bajada
                if "UP" in results[Constants.ANGLE_FLOW]:
                    res = Constants.DIR_UP

            # if IND_BLG_LOWER_DST_PERCENT < 15:
            #     if "UP" in weekFlow:
            #         res = Constants.DIR_UP
            # else:
            #     ##esta en medio de todo
            #     if IND_BLG_LOWER_DST_PERCENT < 15:
            #         res = Constants.DIR_UP
            #     else:
            #         res = week_prev_res
        else:
            nada = ""
            if angleHdiff > 0:
                if "UP" in results[Constants.ANGLE_FLOW]:
                    if angle > angleUp:
                        if rising:
                            # if angleCounter != 0 and angleCounter >= 3:
                            if IND_BLG_LOWER_DST_PERCENT < 90:
                                # if "UP" in weekFlow:
                                res = Constants.DIR_UP
        return res

    @classmethod
    def verifyExtremeValuesDOWN_05(self, res, week_prev_res, results, active):
        res = res
        weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
        angle = results[Constants.ANGLE]
        angleCounter = results[Constants.ANGLE_COUNTER]
        angleIma1 = results[Constants.ANGLE_IMA1]
        angleIma1Counter = results[Constants.ANGLE_IMA1_COUNTER]
        ima1Emadiff = results[Constants.IMA1EMADIFF]

        IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
        weekFlow = results[Constants.WEEK_FLOW]
        angleUp = float(active.parameters.angleUp)
        angleDown = float(active.parameters.angleDown)
        weekMedMinLevel = float(active.parameters.weekMEDMinLevel)
        risingH, angleHdiff = self.isRisingAngleHourly(results, active)
        rising, anglediff = self.isRisingAngle(results)
        if weekdirBotPercent < 10:
            if ima1Emadiff > 0:
                res = Constants.DIR_UP
            else:
                if results[Constants.HOURLY_ANGLE_MED] > 0:
                    res = Constants.DIR_UP
                else:
                    if results[Constants.IND_BLG_LOWER_DST_PERCENT] < 15:
                        res = Constants.DIR_UP
        elif weekdirBotPercent > 10 and weekdirBotPercent < 30:
            if risingH:
                # determinar un flujo grande de bajada
                if "UP" in results[Constants.ANGLE_FLOW]:
                    res = Constants.DIR_UP

            # if IND_BLG_LOWER_DST_PERCENT < 15:
            #     if "UP" in weekFlow:
            #         res = Constants.DIR_UP
            # else:
            #     ##esta en medio de todo
            #     if IND_BLG_LOWER_DST_PERCENT < 15:
            #         res = Constants.DIR_UP
            #     else:
            #         res = week_prev_res
        else:
            nada = ""
            if rising:
                if results[Constants.ACUMULADO]>0:
                    if results[Constants.FLUJO_COUNT]>=2:
                        # if angleCounter != 0 and angleCounter >= 3:
                        if IND_BLG_LOWER_DST_PERCENT < 90:
                            # if "UP" in weekFlow:
                            res = Constants.DIR_UP
        return res

    @classmethod
    def verifyExtremeValuesDOWN_06(self, res, week_prev_res, results, active):
        res = res
        weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
        angle = results[Constants.ANGLE]
        angleCounter = results[Constants.ANGLE_COUNTER]
        angleIma1 = results[Constants.ANGLE_IMA1]
        angleIma1Counter = results[Constants.ANGLE_IMA1_COUNTER]

        IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
        weekFlow = results[Constants.WEEK_FLOW]
        angleUp = float(active.parameters.angleUp)
        angleDown = float(active.parameters.angleDown)
        weekMedMinLevel = float(active.parameters.weekMEDMinLevel)
        risingH, angleHdiff = self.isRisingAngleHourly(results, active)
        rising, anglediff = self.isRisingAngle(results)
        if weekdirBotPercent < 10:
            if results[Constants.HOURLY_ANGLE_MED] > 0:
                res = Constants.DIR_UP
            else:
                if results[Constants.IND_BLG_LOWER_DST_PERCENT] < 35:
                    res = Constants.DIR_UP
        elif weekdirBotPercent > 10 and weekdirBotPercent < 30:
            if risingH:
                # determinar un flujo grande de bajada
                if "UP" in results[Constants.ANGLE_FLOW]:
                    res = Constants.DIR_UP

            # if IND_BLG_LOWER_DST_PERCENT < 15:
            #     if "UP" in weekFlow:
            #         res = Constants.DIR_UP
            # else:
            #     ##esta en medio de todo
            #     if IND_BLG_LOWER_DST_PERCENT < 15:
            #         res = Constants.DIR_UP
            #     else:
            #         res = week_prev_res
        else:
            nada = ""
            if rising:
                # if angleCounter != 0 and angleCounter >= 3:
                if IND_BLG_LOWER_DST_PERCENT < 90:
                    # if "UP" in weekFlow:
                    res = Constants.DIR_UP
        return res

    @classmethod
    def verifyExtVal_DOWN_WEEK_01(self, res, week_prev_res, results, active):
        res = res
        weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
        angle = results[Constants.ANGLE]
        angleCounter = results[Constants.ANGLE_COUNTER]
        angleIma1 = results[Constants.ANGLE_IMA1]
        angleIma1Counter = results[Constants.ANGLE_IMA1_COUNTER]
        closeWeekDiffNew = active.parameters.closeWeekDiffNew

        IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
        weekFlow = results[Constants.WEEK_FLOW]
        angleUp = float(active.parameters.angleUp)
        angleDown = float(active.parameters.angleDown)
        weekMedMinLevel = float(active.parameters.weekMEDMinLevel)
        risingH, angleHdiff = self.isRisingFromMONTH(results)
        rising, angleDiff = self.isRisingFromWEEKNEW(results)
        if weekdirBotPercent < 10:
            if angleDiff < 0 and (abs(angleDiff) > closeWeekDiffNew):
                res = Constants.DIR_DOWN
            else:
                res = Constants.DIR_UP

        elif weekdirBotPercent > 10 and weekdirBotPercent < 30:
            if angleDiff > 0 and (angleDiff > closeWeekDiffNew):
                # determinar un flujo grande de bajada

                    res = Constants.DIR_UP


        else:
            nada = ""
            if rising:
                if angleDiff > 0 and (angleDiff > closeWeekDiffNew):
                    if IND_BLG_LOWER_DST_PERCENT < 90:
                        # if "UP" in weekFlow:
                        res = Constants.DIR_UP
        return res

    @classmethod
    def verifyExtVal_DOWN_WEEK_02(self, res, week_prev_res, results, active):
        res = res
        weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
        angle = results[Constants.ANGLE]
        angleCounter = results[Constants.ANGLE_COUNTER]
        angleIma1 = results[Constants.ANGLE_IMA1]
        angleIma1Counter = results[Constants.ANGLE_IMA1_COUNTER]
        closeWeekDiffNew = active.parameters.closeWeekDiffNew
        blgma_min_diff = active.parameters.blgma_min_diff
        blgMaMean = results[Constants.BLG_MA_MEAN]
        IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]

        weekFlow = results[Constants.WEEK_FLOW]
        angleUp = float(active.parameters.angleUp)
        angleDown = float(active.parameters.angleDown)
        weekMedMinLevel = float(active.parameters.weekMEDMinLevel)
        risingH, angleHdiff = self.isRisingFromMONTH(results)
        rising, angleDiff = self.isRisingFromWEEKNEW(results)
        if weekdirBotPercent < 10:
            if blgMaMean >0:
                res = Constants.DIR_UP

        elif weekdirBotPercent > 10 and weekdirBotPercent < 30:
            if blgMaMean >0 and blgMaMean > blgma_min_diff:
                # determinar un flujo grande de bajada

                res = Constants.DIR_UP


        else:
            if blgMaMean >0 and blgMaMean > blgma_min_diff:
                        # if "UP" in weekFlow:
                        res = Constants.DIR_UP
        return res
    @classmethod
    def verifyExtremeValues_START_DOWN_01(self, res, week_prev_res, results, active):
        res = res
        weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
        angle = results[Constants.ANGLE]
        angleCounter = results[Constants.ANGLE_COUNTER]
        angleIma1 = results[Constants.ANGLE_IMA1]
        angleIma1Counter = results[Constants.ANGLE_IMA1_COUNTER]

        IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
        weekFlow = results[Constants.WEEK_FLOW]
        angleUp = float(active.parameters.angleUp)
        angleDown = float(active.parameters.angleDown)
        weekMedMinLevel = float(active.parameters.weekMEDMinLevel)
        risingH, angleHdiff = self.isRisingAngleHourly(results, active)
        rising, anglediff = self.isRisingAngle(results)
        if weekdirBotPercent < 10:
            if results[Constants.HOURLY_ANGLE_MED] > 0:
                res = Constants.DIR_UP
            else:
                if results[Constants.IND_BLG_LOWER_DST_PERCENT] < 15:
                    res = Constants.DIR_UP
        elif weekdirBotPercent > 10 and weekdirBotPercent < 30:
            if risingH:
                # determinar un flujo grande de bajada
                if "UP" in results[Constants.ANGLE_FLOW]:
                    res = Constants.DIR_UP

            # if IND_BLG_LOWER_DST_PERCENT < 15:
            #     if "UP" in weekFlow:
            #         res = Constants.DIR_UP
            # else:
            #     ##esta en medio de todo
            #     if IND_BLG_LOWER_DST_PERCENT < 15:
            #         res = Constants.DIR_UP
            #     else:
            #         res = week_prev_res
        else:
            nada = ""
            if angleHdiff > 0:
                if "UP" in results[Constants.ANGLE_FLOW]:
                    if angle > angleUp:
                        if rising:
                            # if angleCounter != 0 and angleCounter >= 3:
                            if IND_BLG_LOWER_DST_PERCENT < 90:
                                # if "UP" in weekFlow:
                                res = Constants.DIR_UP
        return res

    @classmethod
    def verifyExtremeValues_START_DOWN_02(self, res, week_prev_res, results, active):
        res = res
        weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
        angle = results[Constants.ANGLE]
        angleCounter = results[Constants.ANGLE_COUNTER]
        angleIma1 = results[Constants.ANGLE_IMA1]
        angleIma1Counter = results[Constants.ANGLE_IMA1_COUNTER]

        IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
        weekFlow = results[Constants.WEEK_FLOW]
        angleUp = float(active.parameters.angleUp)
        angleDown = float(active.parameters.angleDown)
        weekMedMinLevel = float(active.parameters.weekMEDMinLevel)
        risingH, angleHdiff = self.isRisingAngleHourly(results, active)
        rising, anglediff = self.isRisingAngle(results)
        if weekdirBotPercent < 10:
            if results[Constants.HOURLY_ANGLE_MED] > 0:
                res = Constants.DIR_UP
            else:
                if results[Constants.IND_BLG_LOWER_DST_PERCENT] < 15:
                    res = Constants.DIR_UP
        elif weekdirBotPercent > 10 and weekdirBotPercent < 30:
            if risingH:
                # determinar un flujo grande de bajada
                if "UP" in results[Constants.ANGLE_FLOW]:
                    res = Constants.DIR_UP

            # if IND_BLG_LOWER_DST_PERCENT < 15:
            #     if "UP" in weekFlow:
            #         res = Constants.DIR_UP
            # else:
            #     ##esta en medio de todo
            #     if IND_BLG_LOWER_DST_PERCENT < 15:
            #         res = Constants.DIR_UP
            #     else:
            #         res = week_prev_res
        else:
            nada = ""
            if IND_BLG_LOWER_DST_PERCENT < 5:
                if results[Constants.ANGLE] <0:
                    if abs(results[Constants.ANGLE]) < angleDown:
                        res = Constants.DIR_UP
            else:
                if angleHdiff > 0:
                    if "UP" in results[Constants.ANGLE_FLOW]:
                        if angle > angleUp:
                            if rising:
                                # if angleCounter != 0 and angleCounter >= 3:
                                if IND_BLG_LOWER_DST_PERCENT < 90:
                                    # if "UP" in weekFlow:
                                    res = Constants.DIR_UP
        return res

    @classmethod
    def isRisingAngle(self, results):
        res = False, 0
        angleDIff = float(results[Constants.ANGLE]) -float(results[Constants.ANGLE_PREV])
        if angleDIff > 0:
            res = True, angleDIff
        else:
            res = False, angleDIff
        return res

    @classmethod
    def isRisingFromWEEK(self, results):
        res = False, 0
        angleDIff = float(results[Constants.WEEK_DIR_BOT_DST]) -float(results[Constants.WEEK_DIR_BOT_DST_MED])
        if angleDIff > 0:
            res = True, angleDIff
        else:
            res = False, angleDIff
        return res

    @classmethod
    def isRisingFromWEEKNEW(self, results):
        res = False, 0
        angleDIff = float(results[Constants.WEEK_DIR_BOT_DST_NEW]) - float(results[Constants.WEEK_DIR_BOT_DST_MED_NEW])
        if angleDIff > 0:
            res = True, angleDIff
        else:
            res = False, angleDIff
        return res

    @classmethod
    def isRisingFromMONTH(self, results):
        res = False, 0
        try:
            angleDIff = float(results[Constants.MONTH_DIR_BOT_DST]) - float(results[Constants.MONTH_DIR_BOT_DST_MED])
            if angleDIff > 0:
                res = True, angleDIff
            else:
                res = False, angleDIff
        except Exception as error:
            print("Error isRisingFromMONTH ", error)
        return res

    @classmethod
    def isRisingAngleIma1(self, results):
        res = False, 0
        angleDIff = float(results[Constants.ANGLE_IMA1]) - float(results[Constants.ANGLE_IMA1_PREV])
        if angleDIff > 0:
            res = True, angleDIff
        else:
            res = False, angleDIff
        return res

    @classmethod
    def isRisingRSI(self, results):
        res = False, 0

        if ((results[Constants.RSI] > 30 and results[Constants.RSI] < 42) or (
                results[Constants.RSI] > 50 and results[Constants.RSI] < 60)) and results[Constants.RSI_DIFF] > 0:
            if results[Constants.RSI_DIFF] > 1:
                res = True, results[Constants.RSI_DIFF]
        elif ((results[Constants.RSI] >40 and results[Constants.RSI] <50) or (results[Constants.RSI] >60 and results[Constants.RSI] <70))  and   results[Constants.RSI_DIFF] < 0:
            if abs(results[Constants.RSI_DIFF]) > 1:
                res =False
        return res

    @classmethod
    def isRisingAngleHourly(self, results, active):
        res = False, 0
        angleDIff = float(results[Constants.HOURLY_ANGLE_MED]) - float(results[Constants.HOURLY_ANGLE_MED_PREV])
        angleMed = float(results[Constants.HOURLY_ANGLE_MED])
        angleH = float(results[Constants.HOURLY_ANGLE])
        hourlyAngleDiff = active.parameters.hourlyAngleDiff
        if angleMed == 0:
            if "UP" in results[Constants.WEEK_FLOW]:
                res = True, angleDIff
            else:
                res = False, angleDIff
        elif angleMed > 0:
            res = True, angleDIff
            if angleH <0:
                if angleDIff < 0:
                    res = False, angleDIff
                else:
                    if abs(angleMed) < hourlyAngleDiff:
                        if angleDIff > 0:
                            res = True, angleDIff
                        else:
                            res = False, angleDIff

        else:
            res = False, angleDIff
            if angleH > 0:
                if angleDIff > 0:
                    res = True, angleDIff
                else:
                    if abs(angleMed) < hourlyAngleDiff:
                        if angleDIff > 0:
                            res = True, angleDIff
                        else:
                            res = False, angleDIff

        return res

    @classmethod
    def getProb_WEEK_DIRECTION_01(self, results, active):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            week = results[Constants.WEEK_FLOW]
            weekPrev = results[Constants.WEEK_FLOW_PREV]
            weekDir = results[Constants.WEEK_DIR]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            week_med_abs = abs(results[Constants.WEEK_FLOW_MED])
            flowdiff = results[Constants.FLOW_DIFF]
            week_std = results[Constants.WEEK_FLOW_STD]
            weekdiff = results[Constants.WEEK_FLOW_DIFF]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            medDay = results[Constants.INDICATOR_MED_DAY]
            absMedDay = abs(medDay)
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            # BLG
            IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]
            IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
            blgDistPercent = active.parameters.blgDistPercent

            # valores del dia
            numUP = results[Constants.IND_NUM_UP]
            numDOWN = results[Constants.IND_NUM_DOWN]

            sumUP = results[Constants.IND_SUM_UP]
            sumDOWN = results[Constants.IND_SUM_DOWN]

            sumDay = int(sumUP) - int(sumDOWN)

            res = Constants.DIR_WAIT
            weekdiffTendenceValue = 1
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]

            if prevPercent is not None:
                prevPercent = float(prevPercent)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]
            # if med == 0:
            #     if direction == Constants.DIR_UP:
            #         med = 1
            #     elif direction == Constants.DIR_DOWN:
            #         med = -1
            # percentFlow = Constants.DIR_WAIT
            # if percent > prevPercent:
            #     percentFlow = Constants.DIR_UP
            # else:
            #     # baja
            #     percentFlow = Constants.DIR_DOWN
            # CALCULOS final del
            week_prev_res = None
            if week_prev_med < week_med:
                week_prev_res = Constants.DIR_UP
                # if flowdiff > 0:
                #     week_prev_res = Constants.DIR_UP
                # else:
                #     week_prev_res = Constants.DIR_DOWN
                #     ndad =""
                #     # ver que hacer cuando no coinciden
                #     print(f" getProMEDSTD_END_BLG_05 NO COINCIDE")
            elif week_prev_med > week_med:
                week_prev_res = Constants.DIR_DOWN
                # if flowdiff < 0:
                #     week_prev_res = Constants.DIR_DOWN
                # else:
                #     week_prev_res = Constants.DIR_UP
                #     ndad =""
                #     # ver que hacer cuando no coinciden
                #     print(f" getProMEDSTD_END_BLG_05 NO COINCIDE")
            if "UP" in weekDir:
                # SUBE
                res = Constants.DIR_UP
                if active.parameters.weekMindiff != 0.7:
                    # ha cambiado el weekdiff
                    if abs(weekdiff) < active.parameters.weekMindiff:
                        print(f"prob is using week_prev_differential")
                        res = week_prev_res
            elif "DOWN" in weekDir:
                # BAJA
                res = Constants.DIR_DOWN
                if active.parameters.weekMindiff != 0.7:
                    # ha cambiado el weekdiff
                    if abs(weekdiff) < active.parameters.weekMindiff:
                        print(f"prob is using week_prev_differential")
                        res = week_prev_res
        except Exception as error:
            print("Error getProb_WEEK_DIRECTION_01 ", error)
        return res

    @classmethod
    def evaluate_WEEK_DIR_FLOW_01(self, results, active):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            week = results[Constants.WEEK_FLOW]
            weekPrev = results[Constants.WEEK_FLOW_PREV]
            weekDir = results[Constants.WEEK_DIR]
            weekDirFlow = results[Constants.WEEK_DIR_FLOW]
            weekDirFlowDiff = results[Constants.WEEK_DIR_FLOW_DIFF]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            week_med_abs = abs(results[Constants.WEEK_FLOW_MED])
            flowdiff = results[Constants.FLOW_DIFF]
            week_std = results[Constants.WEEK_FLOW_STD]
            weekdiff = results[Constants.WEEK_FLOW_DIFF]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            medDay = results[Constants.INDICATOR_MED_DAY]
            absMedDay = abs(medDay)
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            # BLG
            IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]
            IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
            blgDistPercent = active.parameters.blgDistPercent

            # valores del dia
            numUP = results[Constants.IND_NUM_UP]
            numDOWN = results[Constants.IND_NUM_DOWN]

            sumUP = results[Constants.IND_SUM_UP]
            sumDOWN = results[Constants.IND_SUM_DOWN]

            sumDay = int(sumUP) - int(sumDOWN)

            res = Constants.DIR_WAIT
            weekdiffTendenceValue = 1
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]

            if prevPercent is not None:
                prevPercent = float(prevPercent)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]
            # if med == 0:
            #     if direction == Constants.DIR_UP:
            #         med = 1
            #     elif direction == Constants.DIR_DOWN:
            #         med = -1
            # percentFlow = Constants.DIR_WAIT
            # if percent > prevPercent:
            #     percentFlow = Constants.DIR_UP
            # else:
            #     # baja
            #     percentFlow = Constants.DIR_DOWN
            # CALCULOS final del
            week_prev_res = "WAIT"
            if week_prev_med < week_med:
                week_prev_res = Constants.DIR_UP
                # if flowdiff > 0:
                #     week_prev_res = Constants.DIR_UP
                # else:
                #     week_prev_res = Constants.DIR_DOWN
                #     ndad =""
                #     # ver que hacer cuando no coinciden
                #     print(f" getProMEDSTD_END_BLG_05 NO COINCIDE")
            elif week_prev_med > week_med:
                week_prev_res = Constants.DIR_DOWN
                # if flowdiff < 0:
                #     week_prev_res = Constants.DIR_DOWN
                # else:
                #     week_prev_res = Constants.DIR_UP
                #     ndad =""
                #     # ver que hacer cuando no coinciden
                #     print(f" getProMEDSTD_END_BLG_05 NO COINCIDE")
            if "UP" in weekDirFlow:
                # SUBE
                res = Constants.DIR_UP
                if active.parameters.weekMindiff != 0.7:
                    # ha cambiado el weekdiff
                    if abs(weekdiff) < active.parameters.weekMindiff:
                        print(f"prob is using week_prev_differential")
                        res = week_prev_res
            elif "DOWN" in weekDirFlow:
                # BAJA
                res = Constants.DIR_DOWN
                if active.parameters.weekMindiff != 0.7:
                    # ha cambiado el weekdiff
                    if abs(weekdiff) < active.parameters.weekMindiff:
                        print(f"prob is using week_prev_differential")
                        res = week_prev_res
        except Exception as error:
            print("Error evaluate_WEEK_DIR_FLOW_01 ", error)
        return res

    ##SIRVE PARA INICIO
    @classmethod
    def evaluate_WEEK_ANGLE_FLOW_START_01(self, results, active):
        res = Constants.DIR_WAIT
        try:
            week = results[Constants.WEEK_FLOW]
            weekPrev = results[Constants.WEEK_FLOW_PREV]
            weekDir = results[Constants.WEEK_DIR]
            weekDirFlow = results[Constants.WEEK_DIR_FLOW]
            weekDirFlowDiff = results[Constants.WEEK_DIR_FLOW_DIFF]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            weekdirBotPercentPrev = results[Constants.WEEK_DIR_BOT_DST_PREV]
            weekdirBotPercent= results[Constants.WEEK_DIR_BOT_DST]
            week_med_abs = abs(results[Constants.WEEK_FLOW_MED])
            flowdiff = results[Constants.FLOW_DIFF]
            week_std = results[Constants.WEEK_FLOW_STD]
            weekdiff = results[Constants.WEEK_FLOW_DIFF]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            medDay = results[Constants.INDICATOR_MED_DAY]
            absMedDay = abs(medDay)
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            angleIma1= results[Constants.ANGLE_IMA1]
            angle= results[Constants.ANGLE]
            angleUp = active.parameters.angleUp
            angleDown = active.parameters.angleDown
            # BLG
            IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]
            IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
            blgDistPercent = active.parameters.blgDistPercent

            # valores del dia
            numUP = results[Constants.IND_NUM_UP]
            numDOWN = results[Constants.IND_NUM_DOWN]

            sumUP = results[Constants.IND_SUM_UP]
            sumDOWN = results[Constants.IND_SUM_DOWN]

            sumDay = int(sumUP) - int(sumDOWN)

            res = Constants.DIR_WAIT
            weekdiffTendenceValue = 1
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]

            if prevPercent is not None:
                prevPercent = float(prevPercent)
            if weekdirBotPercent is not None:
                weekdirBotPercent = float(weekdirBotPercent)
            if weekdirBotPercentPrev is not None:
                weekdirBotPercentPrev = float(weekdirBotPercentPrev)


            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]

            week_prev_res = "WAIT"
            if weekdirBotPercentPrev < weekdirBotPercent:
                week_prev_res = Constants.DIR_UP
                

            elif weekdirBotPercentPrev > weekdirBotPercent:
                week_prev_res = Constants.DIR_DOWN

            if "UP" in week_prev_res:
                # SUBE
                res = Constants.DIR_UP
                #verificamos que no este en lso extemos
                if weekdirBotPercent > 95:
                    res = Constants.DIR_DOWN
            elif "DOWN" in week_prev_res:
                # BAJA
                res = Constants.DIR_DOWN
                # verificamos que no este en lso extemos
                if weekdirBotPercent < 5:
                    res = Constants.DIR_UP
        except Exception as error:
            print("Error evaluate_WEEK_ANGLE_FLOW_01 ", error)
        return res

    @classmethod
    def evaluate_WEEK_ANGLE_FLOW_START_02(self, results, active):
        res = Constants.DIR_WAIT
        try:
            week = results[Constants.WEEK_FLOW]
            weekPrev = results[Constants.WEEK_FLOW_PREV]
            weekDir = results[Constants.WEEK_DIR]
            weekDirFlow = results[Constants.WEEK_DIR_FLOW]
            weekDirFlowDiff = results[Constants.WEEK_DIR_FLOW_DIFF]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            weekdirBotPercentPrev = results[Constants.WEEK_DIR_BOT_DST_PREV]
            weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
            week_med_abs = abs(results[Constants.WEEK_FLOW_MED])
            flowdiff = results[Constants.FLOW_DIFF]
            week_std = results[Constants.WEEK_FLOW_STD]
            weekdiff = results[Constants.WEEK_FLOW_DIFF]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            medDay = results[Constants.INDICATOR_MED_DAY]
            absMedDay = abs(medDay)
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            angleIma1 = results[Constants.ANGLE_IMA1]
            angleIma1Counter = results[Constants.ANGLE_IMA1_COUNTER]
            angle = results[Constants.ANGLE]
            angleCounter = results[Constants.ANGLE_COUNTER]
            angleUp = active.parameters.angleUp
            angleDown = active.parameters.angleDown
            # BLG
            IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]
            IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
            blgDistPercent = active.parameters.blgDistPercent

            # valores del dia
            numUP = results[Constants.IND_NUM_UP]
            numDOWN = results[Constants.IND_NUM_DOWN]

            sumUP = results[Constants.IND_SUM_UP]
            sumDOWN = results[Constants.IND_SUM_DOWN]

            sumDay = int(sumUP) - int(sumDOWN)

            res = Constants.DIR_WAIT
            weekdiffTendenceValue = 1
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]

            if prevPercent is not None:
                prevPercent = float(prevPercent)
            if weekdirBotPercent is not None:
                weekdirBotPercent = float(weekdirBotPercent)
            if weekdirBotPercentPrev is not None:
                weekdirBotPercentPrev = float(weekdirBotPercentPrev)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]

            week_prev_res = "WAIT"
            if angle > 0:
                week_prev_res = Constants.DIR_UP
            elif angle < 0:
                week_prev_res = Constants.DIR_DOWN

            if angle ==0:
                if angleIma1 >0:
                    week_prev_res = Constants.DIR_UP
                else:
                    week_prev_res = Constants.DIR_DOWN
            if "UP" in week_prev_res:
                # SUBE
                res = Constants.DIR_UP
                # verificamos que no este en lso extemos
                if weekdirBotPercent > 95:
                    if angleCounter < 3:
                        if angleIma1Counter < 4:
                            res = Constants.DIR_DOWN
                else:
                    if weekdirBotPercent >= 90:
                        res = Constants.DIR_DOWN
                    else:
                        if angleCounter <= 3:
                            #duda
                            if angleIma1 < 0:
                                res = Constants.DIR_DOWN
            elif "DOWN" in week_prev_res:
                # BAJA
                res = Constants.DIR_DOWN
                # verificamos que no este en lso extemos
                if weekdirBotPercent < 5:
                    if angleCounter < 3:
                        if angleIma1Counter < 4:
                            res = Constants.DIR_UP
                else:
                    if weekdirBotPercent <= 10:
                        res = Constants.DIR_UP
                    else:
                        if angleCounter <= 3:
                            # duda
                            if angleIma1 > 0:
                                res = Constants.DIR_UP
        except Exception as error:
            print("Error evaluate_WEEK_ANGLE_FLOW_01 ", error)
        return res

    @classmethod
    def evaluate_WEEK_ANGLE_FLOW_START_03(self, results, active):
        res = Constants.DIR_WAIT
        try:
            weekFlow = results[Constants.WEEK_FLOW]
            weekPrev = results[Constants.WEEK_FLOW_PREV]
            weekDir = results[Constants.WEEK_DIR]
            weekDirFlow = results[Constants.WEEK_DIR_FLOW]
            weekDirFlowDiff = results[Constants.WEEK_DIR_FLOW_DIFF]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            weekdirBotPercentPrev = results[Constants.WEEK_DIR_BOT_DST_PREV]
            weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
            week_med_abs = abs(results[Constants.WEEK_FLOW_MED])
            flowdiff = results[Constants.FLOW_DIFF]
            week_std = results[Constants.WEEK_FLOW_STD]
            weekdiff = results[Constants.WEEK_FLOW_DIFF]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            medDay = results[Constants.INDICATOR_MED_DAY]
            absMedDay = abs(medDay)
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            angleIma1 = results[Constants.ANGLE_IMA1]
            angleIma1Counter = results[Constants.ANGLE_IMA1_COUNTER]
            angle = results[Constants.ANGLE]
            angleCounter = results[Constants.ANGLE_COUNTER]
            angleUp = active.parameters.angleUp
            angleDown = active.parameters.angleDown
            # BLG
            IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]
            IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
            blgDistPercent = active.parameters.blgDistPercent

            # valores del dia
            numUP = results[Constants.IND_NUM_UP]
            numDOWN = results[Constants.IND_NUM_DOWN]

            sumUP = results[Constants.IND_SUM_UP]
            sumDOWN = results[Constants.IND_SUM_DOWN]

            sumDay = int(sumUP) - int(sumDOWN)

            res = Constants.DIR_WAIT
            weekdiffTendenceValue = 1
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]

            if prevPercent is not None:
                prevPercent = float(prevPercent)
            if weekdirBotPercent is not None:
                weekdirBotPercent = float(weekdirBotPercent)
            if weekdirBotPercentPrev is not None:
                weekdirBotPercentPrev = float(weekdirBotPercentPrev)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]

            week_prev_res = "WAIT"
            if angle > 0:
                week_prev_res = Constants.DIR_UP
            elif angle < 0:
                week_prev_res = Constants.DIR_DOWN

            if angle == 0:
                if angleIma1 > 0:
                    week_prev_res = Constants.DIR_UP
                else:
                    week_prev_res = Constants.DIR_DOWN
            if "UP" in week_prev_res:
                # SUBE
                res = Constants.DIR_UP
                # verificamos que no este en lso extemos
                if weekdirBotPercent > 95:
                    if abs(angle) < angleDown:
                        # determinar un flujo grande de bajada
                        if angleCounter < 3:
                            res = Constants.DIR_DOWN
                        else:
                            if "DOWN" in weekFlow:
                                res = Constants.DIR_DOWN

                elif weekdirBotPercent > 80 and weekdirBotPercent < 95:
                    if IND_BLG_LOWER_DST_PERCENT > 90:
                        if "DOWN" in weekFlow:
                            res = Constants.DIR_DOWN
                else:
                    if abs(angle) < angleDown:
                        if IND_BLG_LOWER_DST_PERCENT > 90:
                            ##puede bajar
                            if "DOWN" in weekFlow:
                                res = Constants.DIR_DOWN

            elif "DOWN" in week_prev_res:
                # BAJA
                res = Constants.DIR_DOWN
                # verificamos que no este en lso extemos
                if weekdirBotPercent < 5:
                    if abs(angle) < angleDown:
                        # determinar un flujo grande de bajada
                        if angleCounter < 3:
                            res = Constants.DIR_UP
                        else:
                            if "UP" in weekFlow:
                                res = Constants.DIR_UP
                elif weekdirBotPercent > 5 and weekdirBotPercent < 30:
                    if IND_BLG_LOWER_DST_PERCENT < 10:
                        if "UP" in weekFlow:
                            res = Constants.DIR_UP
                else:
                    if abs(angle) < angleDown:
                        if IND_BLG_LOWER_DST_PERCENT < 10:
                            if "UP" in weekFlow:
                                res = Constants.DIR_UP
        except Exception as error:
            print("Error evaluate_WEEK_ANGLE_FLOW_01 ", error)
        return res

    @classmethod
    def evaluate_NORMAL_ANGLE_FLOW_01(self, results, active):
        res = Constants.DIR_WAIT
        try:
            weekFlow = results[Constants.WEEK_FLOW]
            # weekPrev = results[Constants.WEEK_FLOW_PREV]
            # weekDir = results[Constants.WEEK_DIR]
            # weekDirFlow = results[Constants.WEEK_DIR_FLOW]
            # weekDirFlowDiff = results[Constants.WEEK_DIR_FLOW_DIFF]
            # week_med = results[Constants.WEEK_FLOW_MED]
            # week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            weekdirBotPercentPrev = results[Constants.WEEK_DIR_BOT_DST_PREV]
            weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
            # angleIma1 = results[Constants.ANGLE_IMA1]
            # angle = results[Constants.ANGLE]
            # minAngleIma1 = active.parameters.minAngleIma1
            # week_med_abs = abs(results[Constants.WEEK_FLOW_MED])
            # flowdiff = results[Constants.FLOW_DIFF]
            # week_std = results[Constants.WEEK_FLOW_STD]
            # weekdiff = results[Constants.WEEK_FLOW_DIFF]
            # direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            medDay = results[Constants.INDICATOR_MED_DAY]
            # absMedDay = abs(medDay)
            # stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            angleIma1 = results[Constants.ANGLE_IMA1]
            # angle = results[Constants.ANGLE]
            # angleUp = active.parameters.angleUp
            # angleDown = active.parameters.angleDown
            # # BLG
            # IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]
            # IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
            # blgDistPercent = active.parameters.blgDistPercent

            # valores del dia
            # numUP = results[Constants.IND_NUM_UP]
            # numDOWN = results[Constants.IND_NUM_DOWN]
            #
            # sumUP = results[Constants.IND_SUM_UP]
            # sumDOWN = results[Constants.IND_SUM_DOWN]



            res = Constants.DIR_WAIT
            weekdiffTendenceValue = 1
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]

            if prevPercent is not None:
                prevPercent = float(prevPercent)
            if weekdirBotPercent is not None:
                weekdirBotPercent = float(weekdirBotPercent)
            if weekdirBotPercentPrev is not None:
                weekdirBotPercentPrev = float(weekdirBotPercentPrev)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]

            week_res = "WAIT"
            if "UP" in weekFlow:
                week_res = Constants.DIR_UP
            elif "DOWN" in weekFlow:
                week_res = Constants.DIR_DOWN

            prev_res = "WAIT"
            if angleIma1 > 0:
                prev_res = Constants.DIR_UP
            elif angleIma1 < 0:
                prev_res = Constants.DIR_DOWN

            if "UP" in prev_res:
                # SUBE
                res = Constants.DIR_UP
                # verificamos que no este en lso extemos
                if weekdirBotPercent > 95:
                    if results[Constants.ANGLE_IMA1_COUNTER]<=2:
                        res =week_res
            elif "DOWN" in prev_res:
                # BAJA
                res = Constants.DIR_DOWN
                # verificamos que no este en lso extemos
                if weekdirBotPercent < 5:
                    if results[Constants.ANGLE_IMA1_COUNTER] <= 2:
                        res = week_res
        except Exception as error:
            print("Error evaluate_NORMAL_ANGLE_FLOW_01 ", error)
        return res

    ##SIRVE PARA FIN
    @classmethod
    def evaluate_WEEK_ANGLE_FLOW_END_01(self, results, active):
        res = Constants.DIR_WAIT
        try:
            weekFlow = results[Constants.WEEK_FLOW]
            weekPrev = results[Constants.WEEK_FLOW_PREV]
            weekDir = results[Constants.WEEK_DIR]
            weekDirFlow = results[Constants.WEEK_DIR_FLOW]
            weekDirFlowDiff = results[Constants.WEEK_DIR_FLOW_DIFF]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            weekdirBotPercentPrev = results[Constants.WEEK_DIR_BOT_DST_PREV]
            weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
            week_med_abs = abs(results[Constants.WEEK_FLOW_MED])
            flowdiff = results[Constants.FLOW_DIFF]
            week_std = results[Constants.WEEK_FLOW_STD]
            weekdiff = results[Constants.WEEK_FLOW_DIFF]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            medDay = results[Constants.INDICATOR_MED_DAY]
            absMedDay = abs(medDay)
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            angleIma1 = results[Constants.ANGLE_IMA1]
            angle = results[Constants.ANGLE]
            angleM1 = results[Constants.ANGLEm1]
            angleM2 = results[Constants.ANGLEm21]
            angleUp = float(active.parameters.angleUp)
            angleDown = float(active.parameters.angleDown)
            # BLG
            IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]
            IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
            blgDistPercent = active.parameters.blgDistPercent

            # valores del dia
            numUP = results[Constants.IND_NUM_UP]
            numDOWN = results[Constants.IND_NUM_DOWN]

            sumUP = results[Constants.IND_SUM_UP]
            sumDOWN = results[Constants.IND_SUM_DOWN]

            sumDay = int(sumUP) - int(sumDOWN)

            res = Constants.DIR_WAIT
            weekdiffTendenceValue = 1
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]

            if prevPercent is not None:
                prevPercent = float(prevPercent)
            if weekdirBotPercent is not None:
                weekdirBotPercent = float(weekdirBotPercent)
            if weekdirBotPercentPrev is not None:
                weekdirBotPercentPrev = float(weekdirBotPercentPrev)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]

            week_prev_res = "WAIT"

            if angle >0:
                week_prev_res = Constants.DIR_UP
                if angle < angleUp:
                    #verificar
                    if angleM1 < 0:
                        if angleM2 > 0:
                            week_prev_res = Constants.DIR_UP
                        else:
                            week_prev_res = weekFlow

                    if abs(angleM2) < 1:
                        #es dudoso se lo dejamos a week
                        week_prev_res = weekFlow

            elif angle < 0:
                week_prev_res = Constants.DIR_DOWN
                if abs(angle) < angleDown:
                    # verificar
                    if angleM1 > 0:
                        if angleM2 < 0:
                            week_prev_res = Constants.DIR_DOWN
                        else:
                            week_prev_res = weekFlow

                    if abs(angleM2) < 1:
                        #es dudoso se lo dejamos a week
                        week_prev_res = weekFlow

            if "UP" in week_prev_res:
                # SUBE
                res = Constants.DIR_UP
                # verificamos que no este en lso extemos
                if weekdirBotPercent > 95:
                    res = Constants.DIR_DOWN
            elif "DOWN" in week_prev_res:
                # BAJA
                res = Constants.DIR_DOWN
                # verificamos que no este en lso extemos
                if weekdirBotPercent < 5:
                    if abs(angle) < angleDown:
                        res = Constants.DIR_UP
        except Exception as error:
            print("Error evaluate_WEEK_ANGLE_FLOW_01 ", error)
        return res

    ##SIRVE PARA FIN
    @classmethod
    def evaluate_WEEK_ANGLE_FLOW_END_02(self, results, active):
        res = Constants.DIR_WAIT
        try:
            weekFlow = results[Constants.WEEK_FLOW]
            weekPrev = results[Constants.WEEK_FLOW_PREV]
            weekDir = results[Constants.WEEK_DIR]
            weekDirFlow = results[Constants.WEEK_DIR_FLOW]
            weekDirFlowDiff = results[Constants.WEEK_DIR_FLOW_DIFF]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            weekdirBotPercentPrev = results[Constants.WEEK_DIR_BOT_DST_PREV]
            weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
            week_med_abs = abs(results[Constants.WEEK_FLOW_MED])
            flowdiff = results[Constants.FLOW_DIFF]
            week_std = results[Constants.WEEK_FLOW_STD]
            weekdiff = results[Constants.WEEK_FLOW_DIFF]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            medDay = results[Constants.INDICATOR_MED_DAY]
            absMedDay = abs(medDay)
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            angleIma1 = results[Constants.ANGLE_IMA1]
            angle = results[Constants.ANGLE]
            angleM1 = results[Constants.ANGLEm1]
            angleM2 = results[Constants.ANGLEm21]
            angleUp = float(active.parameters.angleUp)
            angleDown = float(active.parameters.angleDown)
            # BLG
            IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]
            IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
            blgDistPercent = active.parameters.blgDistPercent

            # valores del dia
            numUP = results[Constants.IND_NUM_UP]
            numDOWN = results[Constants.IND_NUM_DOWN]

            sumUP = results[Constants.IND_SUM_UP]
            sumDOWN = results[Constants.IND_SUM_DOWN]

            sumDay = int(sumUP) - int(sumDOWN)

            res = Constants.DIR_WAIT
            weekdiffTendenceValue = 1
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]

            if prevPercent is not None:
                prevPercent = float(prevPercent)
            if weekdirBotPercent is not None:
                weekdirBotPercent = float(weekdirBotPercent)
            if weekdirBotPercentPrev is not None:
                weekdirBotPercentPrev = float(weekdirBotPercentPrev)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]

            week_prev_res = "WAIT"

            if angle > 0:
                week_prev_res = Constants.DIR_UP
                if angle < angleUp:
                    # verificar
                    if angleM1 < 0:
                        if angleM2 > 0:
                            week_prev_res = Constants.DIR_UP
                        else:
                            week_prev_res = weekFlow

                    if abs(angleM2) < 1:
                        # es dudoso se lo dejamos a week
                        week_prev_res = weekFlow

            elif angle < 0:
                week_prev_res = Constants.DIR_DOWN
                if abs(angle) < angleDown:
                    # verificar
                    if angleM1 > 0:
                        if angleM2 < 0:
                            week_prev_res = Constants.DIR_DOWN
                        else:
                            week_prev_res = weekFlow

                    if abs(angleM2) < 1:
                        # es dudoso se lo dejamos a week
                        week_prev_res = weekFlow

            if "UP" in week_prev_res:
                # SUBE
                res = Constants.DIR_UP
                # verificamos que no este en lso extemos
                if weekdirBotPercent > 95:
                    if abs(angle) < angleDown:
                        res = Constants.DIR_DOWN
            elif "DOWN" in week_prev_res:
                # BAJA
                res = Constants.DIR_DOWN
                # verificamos que no este en lso extemos
                if weekdirBotPercent < 5:
                    if abs(angle) < angleDown:
                        res = Constants.DIR_UP
        except Exception as error:
            print("Error evaluate_WEEK_ANGLE_FLOW_01 ", error)
        return res

    @classmethod
    def evaluate_WEEK_ANGLE_FLOW_END_03(self, results, active):
        res = Constants.DIR_WAIT
        try:
            weekFlow = results[Constants.WEEK_FLOW]
            weekPrev = results[Constants.WEEK_FLOW_PREV]
            weekDir = results[Constants.WEEK_DIR]
            weekDirFlow = results[Constants.WEEK_DIR_FLOW]
            weekDirFlowDiff = results[Constants.WEEK_DIR_FLOW_DIFF]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            weekdirBotPercentPrev = results[Constants.WEEK_DIR_BOT_DST_PREV]
            weekdirBotPercent = results[Constants.WEEK_DIR_BOT_DST]
            week_med_abs = abs(results[Constants.WEEK_FLOW_MED])
            flowdiff = results[Constants.FLOW_DIFF]
            week_std = results[Constants.WEEK_FLOW_STD]
            weekdiff = results[Constants.WEEK_FLOW_DIFF]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            medDay = results[Constants.INDICATOR_MED_DAY]
            absMedDay = abs(medDay)
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            angleIma1 = results[Constants.ANGLE_IMA1]
            angle = results[Constants.ANGLE]
            angleCounter = int(results[Constants.ANGLE_COUNTER])
            angleM1 = results[Constants.ANGLEm1]
            angleM2 = results[Constants.ANGLEm21]
            angleUp = float(active.parameters.angleUp)
            angleDown = float(active.parameters.angleDown)
            close_NXT_UP = results[Constants.CLOSE_NXT_UP]
            close_NXT_DOWN = results[Constants.CLOSE_NXT_DOWN]
            # BLG
            IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]
            IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
            blgDistPercent = active.parameters.blgDistPercent

            # valores del dia
            numUP = results[Constants.IND_NUM_UP]
            numDOWN = results[Constants.IND_NUM_DOWN]

            sumUP = results[Constants.IND_SUM_UP]
            sumDOWN = results[Constants.IND_SUM_DOWN]

            sumDay = int(sumUP) - int(sumDOWN)

            res = Constants.DIR_WAIT
            weekdiffTendenceValue = 1
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]

            if prevPercent is not None:
                prevPercent = float(prevPercent)
            if weekdirBotPercent is not None:
                weekdirBotPercent = float(weekdirBotPercent)
            if weekdirBotPercentPrev is not None:
                weekdirBotPercentPrev = float(weekdirBotPercentPrev)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]


            week_prev_res = "WAIT"

            if angle > 0:
                week_prev_res = Constants.DIR_UP
                if angle < angleUp:
                    # verificar
                    if angleIma1 < 0:
                        if abs(angleIma1) > angleUp:
                            week_prev_res = Constants.DIR_DOWN
                        else:
                            week_prev_res = weekFlow

            elif angle < 0:
                week_prev_res = Constants.DIR_DOWN
                if abs(angle) < angleDown:
                    # verificar
                    if angleIma1 > 0:
                        if abs(angleIma1) > angleUp:
                            week_prev_res = Constants.DIR_UP
                        else:
                            week_prev_res = weekFlow


            res_week = "WAIT"
            if "UP" in weekFlow:
                res_week = Constants.DIR_UP
            elif "DOWN" in weekFlow:
                res_week = Constants.DIR_DOWN

            if "UP" in week_prev_res:
                # SUBE
                res = Constants.DIR_UP
                # verificamos que no este en lso extemos
                if  weekdirBotPercent > 95:
                    if abs(angle) < angleDown:
                        # determinar un flujo grande de bajada
                        if angleCounter < 3:
                            res = Constants.DIR_DOWN
                        else:
                            if "DOWN" in weekFlow:
                                res = Constants.DIR_DOWN

                elif weekdirBotPercent > 80 and weekdirBotPercent < 95:
                    if IND_BLG_LOWER_DST_PERCENT > 90:
                        if "DOWN" in weekFlow:
                            res = Constants.DIR_DOWN
                else:
                    if abs(angle) < angleDown:
                        if IND_BLG_LOWER_DST_PERCENT >90:
                            ##puede bajar
                            if "DOWN" in weekFlow:
                                res = Constants.DIR_DOWN

            elif "DOWN" in week_prev_res:
                # BAJA
                res = Constants.DIR_DOWN
                # verificamos que no este en lso extemos
                if weekdirBotPercent < 5:
                    if abs(angle) < angleDown:
                        #determinar un flujo grande de bajada
                        if angleCounter < 3:
                            res = Constants.DIR_UP
                        else:
                            if "UP" in weekFlow:
                                res = Constants.DIR_UP
                elif weekdirBotPercent > 5 and weekdirBotPercent < 30:
                    if IND_BLG_LOWER_DST_PERCENT < 10:
                        if "UP" in weekFlow:
                            res = Constants.DIR_UP
                else:
                    if abs(angle) < angleDown:
                        if IND_BLG_LOWER_DST_PERCENT < 10:
                            if "UP" in weekFlow:
                                res = Constants.DIR_UP
        except Exception as error:
            print("Error evaluate_WEEK_ANGLE_FLOW_01 ", error)
        return res


    @classmethod
    def evaluate_WEEK_DIR_FLOW_02(self, results, active):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            week = results[Constants.WEEK_FLOW]
            weekPrev = results[Constants.WEEK_FLOW_PREV]
            weekDir = results[Constants.WEEK_DIR]
            weekDirFlow = results[Constants.WEEK_DIR_FLOW]
            weekDirFlowDiff = float(results[Constants.WEEK_DIR_FLOW_DIFF])
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            weekDirFlowPrev = float(results[Constants.WEEK_DIR_FLOW_PREV])
            week_med_abs = abs(results[Constants.WEEK_FLOW_MED])
            flowdiff = results[Constants.FLOW_DIFF]
            week_std = results[Constants.WEEK_FLOW_STD]
            weekdiff = results[Constants.WEEK_FLOW_DIFF]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            medDay = results[Constants.INDICATOR_MED_DAY]
            absMedDay = abs(medDay)
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            # BLG
            IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]
            IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
            blgDistPercent = active.parameters.blgDistPercent

            # valores del dia
            numUP = results[Constants.IND_NUM_UP]
            numDOWN = results[Constants.IND_NUM_DOWN]

            sumUP = results[Constants.IND_SUM_UP]
            sumDOWN = results[Constants.IND_SUM_DOWN]

            sumDay = int(sumUP) - int(sumDOWN)

            res = Constants.DIR_WAIT
            weekdiffTendenceValue = 1
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]

            if prevPercent is not None:
                prevPercent = float(prevPercent)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]
            # if med == 0:
            #     if direction == Constants.DIR_UP:
            #         med = 1
            #     elif direction == Constants.DIR_DOWN:
            #         med = -1
            # percentFlow = Constants.DIR_WAIT
            # if percent > prevPercent:
            #     percentFlow = Constants.DIR_UP
            # else:
            #     # baja
            #     percentFlow = Constants.DIR_DOWN
            # CALCULOS final del
            week_prev_res = None
            if weekDirFlowPrev < weekDirFlowDiff:
                week_prev_res = Constants.DIR_UP
                # if flowdiff > 0:
                #     week_prev_res = Constants.DIR_UP
                # else:
                #     week_prev_res = Constants.DIR_DOWN
                #     ndad =""
                #     # ver que hacer cuando no coinciden
                #     print(f" getProMEDSTD_END_BLG_05 NO COINCIDE")
            elif weekDirFlowPrev > weekDirFlowDiff:
                week_prev_res = Constants.DIR_DOWN
                # if flowdiff < 0:
                #     week_prev_res = Constants.DIR_DOWN
                # else:
                #     week_prev_res = Constants.DIR_UP
                #     ndad =""
                #     # ver que hacer cuando no coinciden
                #     print(f" getProMEDSTD_END_BLG_05 NO COINCIDE")
            if "UP" in weekDirFlow:
                # SUBE
                res = Constants.DIR_UP
                if IND_BLG_LOWER_DST_PERCENT > 0 and IND_BLG_LOWER_DST_PERCENT >90:
                    res = Constants.DIR_DOWN
                else:

                    if active.parameters.weekMindiff != 0.7:
                        # ha cambiado el weekdiff
                        if abs(weekdiff) < active.parameters.weekMindiff:
                            print(f"prob is using week_prev_differential")
                            res = week_prev_res
            elif "DOWN" in weekDirFlow:
                # BAJA
                res = Constants.DIR_DOWN
                if IND_BLG_UPPER_DST_PERCENT > 0 and IND_BLG_UPPER_DST_PERCENT >90:
                    res = Constants.DIR_UP
                if active.parameters.weekMindiff != 0.7:
                    # ha cambiado el weekdiff
                    if abs(weekdiff) < active.parameters.weekMindiff:
                        print(f"prob is using week_prev_differential")
                        res = week_prev_res
        except Exception as error:
            print("Error evaluate_WEEK_DIR_FLOW_02 ", error)
        return res

    @classmethod
    def getProb_WEEK_DIRECTION_02(self, results, active):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            week = results[Constants.WEEK_FLOW]
            weekPrev = results[Constants.WEEK_FLOW_PREV]
            weekDir = results[Constants.WEEK_DIR]
            weekminDir = results[Constants.WEEK_MIN_DIR]
            weekmaxDir = results[Constants.WEEK_MAX_DIR]
            weekTopDst = results[Constants.WEEK_DIR_TOP_DST]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            week_med_abs = abs(results[Constants.WEEK_FLOW_MED])
            flowdiff = results[Constants.FLOW_DIFF]
            week_std = results[Constants.WEEK_FLOW_STD]
            weekdiff = results[Constants.WEEK_FLOW_DIFF]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            medDay = results[Constants.INDICATOR_MED_DAY]
            absMedDay = abs(medDay)
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            # BLG
            IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]
            IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
            blgDistPercent = active.parameters.blgDistPercent

            # valores del dia
            numUP = results[Constants.IND_NUM_UP]
            numDOWN = results[Constants.IND_NUM_DOWN]

            sumUP = results[Constants.IND_SUM_UP]
            sumDOWN = results[Constants.IND_SUM_DOWN]

            sumDay = int(sumUP) - int(sumDOWN)

            res = Constants.DIR_WAIT
            weekdiffTendenceValue = 1
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]

            if prevPercent is not None:
                prevPercent = float(prevPercent)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]
            # if med == 0:
            #     if direction == Constants.DIR_UP:
            #         med = 1
            #     elif direction == Constants.DIR_DOWN:
            #         med = -1
            # percentFlow = Constants.DIR_WAIT
            # if percent > prevPercent:
            #     percentFlow = Constants.DIR_UP
            # else:
            #     # baja
            #     percentFlow = Constants.DIR_DOWN
            # CALCULOS final del
            week_prev_res = None
            if week_prev_med < week_med:
                week_prev_res = Constants.DIR_UP
                # if flowdiff > 0:
                #     week_prev_res = Constants.DIR_UP
                # else:
                #     week_prev_res = Constants.DIR_DOWN
                #     ndad =""
                #     # ver que hacer cuando no coinciden
                #     print(f" getProMEDSTD_END_BLG_05 NO COINCIDE")
            elif week_prev_med > week_med:
                week_prev_res = Constants.DIR_DOWN
                # if flowdiff < 0:
                #     week_prev_res = Constants.DIR_DOWN
                # else:
                #     week_prev_res = Constants.DIR_UP
                #     ndad =""
                #     # ver que hacer cuando no coinciden
                #     print(f" getProMEDSTD_END_BLG_05 NO COINCIDE")
            secondCriteria = False
            if weekTopDst >= 75:
                secondCriteria = True
            elif weekTopDst <= 25:
                secondCriteria = True
            if "UP" in weekDir:
                # SUBE
                res = Constants.DIR_UP

                if active.parameters.weekMindiff != 0.7 or secondCriteria==True:
                    # ha cambiado el weekdiff
                    if abs(weekdiff) < active.parameters.weekMindiff:
                        print(f"prob is using week_prev_differential")
                        res = self.getBlgUpperDirection(results, res)
            elif "DOWN" in weekDir:
                # BAJA
                res = Constants.DIR_DOWN
                if active.parameters.weekMindiff != 0.7 or secondCriteria==True:
                    # ha cambiado el weekdiff
                    if abs(weekdiff) < active.parameters.weekMindiff:
                        print(f"prob is using week_prev_differential")
                        res = self.getBlgUpperDirection(results,res)
        except Exception as error:
            print("Error getProb_WEEK_DIRECTION_02 ", error)
        return res


    @classmethod
    def getProb_START_ANGLE_H_01(self, results, active):
        res = Constants.DIR_WAIT
        try:
            weekDir = results[Constants.WEEK_DIR]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            medDay = results[Constants.INDICATOR_MED_DAY]

            week_prev_res = None
            if week_prev_med < week_med:
                week_prev_res = Constants.DIR_UP

            elif week_prev_med > week_med:
                week_prev_res = Constants.DIR_DOWN

            raisingH, angleHDiff = self.isRisingAngleHourly(results,active)
            if raisingH:
                # SUBE
                res = Constants.DIR_UP
                res = self.verifyExtremeValues_START_UP_01(res, week_prev_res, results, active)

            else:
                # BAJA
                res = Constants.DIR_DOWN
                res = self.verifyExtremeValues_START_DOWN_02(res, week_prev_res, results, active)

        except Exception as error:
            print("Error getProb_START_ANGLE_H_01 ", error)
        return res

    @classmethod
    def getProb_START_ANGLE_H_02(self, results, active):
        res = Constants.DIR_WAIT
        try:
            weekDir = results[Constants.WEEK_DIR]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            medDay = results[Constants.INDICATOR_MED_DAY]

            week_prev_res = None
            if week_prev_med < week_med:
                week_prev_res = Constants.DIR_UP

            elif week_prev_med > week_med:
                week_prev_res = Constants.DIR_DOWN

            raisingH, angleHDiff = self.isRisingAngleHourly(results, active)
            raisingH, angleHDiff = self.isRisingAngle(results)
            if raisingH:
                # SUBE
                res = Constants.DIR_UP
                res = self.verifyExtremeValues_START_UP_01(res, week_prev_res, results, active)

            else:
                # BAJA
                res = Constants.DIR_DOWN
                res = self.verifyExtremeValues_START_DOWN_02(res, week_prev_res, results, active)

        except Exception as error:
            print("Error getProb_START_ANGLE_H_02 ", error)
        return res

    @classmethod
    def getProb_WEEK_DIRECTION_03(self, results, active):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            week = results[Constants.WEEK_FLOW]
            weekPrev = results[Constants.WEEK_FLOW_PREV]
            weekDir = results[Constants.WEEK_DIR]
            weekminDir = results[Constants.WEEK_MIN_DIR]
            weekmaxDir = results[Constants.WEEK_MAX_DIR]
            weekTopDst = results[Constants.WEEK_DIR_TOP_DST]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            week_med_abs = abs(results[Constants.WEEK_FLOW_MED])
            flowdiff = results[Constants.FLOW_DIFF]
            week_std = results[Constants.WEEK_FLOW_STD]
            weekdiff = results[Constants.WEEK_FLOW_DIFF]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            medDay = results[Constants.INDICATOR_MED_DAY]
            absMedDay = abs(medDay)
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            # BLG
            IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]
            IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
            blgDistPercent = active.parameters.blgDistPercent

            # valores del dia
            numUP = results[Constants.IND_NUM_UP]
            numDOWN = results[Constants.IND_NUM_DOWN]

            sumUP = results[Constants.IND_SUM_UP]
            sumDOWN = results[Constants.IND_SUM_DOWN]

            sumDay = int(sumUP) - int(sumDOWN)

            res = Constants.DIR_WAIT
            weekdiffTendenceValue = 1
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]

            if prevPercent is not None:
                prevPercent = float(prevPercent)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]

            if week_prev_med < week_med:
                week_prev_res = Constants.DIR_UP
            elif week_prev_med > week_med:
                week_prev_res = Constants.DIR_DOWN


            if "UP" in weekDir:
                # SUBE
                res = Constants.DIR_UP
                res = self.verifyExtremeValuesUP_03(res, week_prev_res, results, active)


            elif "DOWN" in weekDir:
                # BAJA
                res = Constants.DIR_DOWN
                res = self.verifyExtremeValuesDOWN_03(res, week_prev_res, results, active)


        except Exception as error:
            print("Error getProb_WEEK_DIRECTION_03 ", error)
        return res
    @classmethod
    def getBlgUpperDirection(self, results, direction):
        res = Constants.DIR_WAIT
        week_med = results[Constants.WEEK_FLOW_MED]
        week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
        medDay = results[Constants.INDICATOR_MED_DAY]
        weekTopDst = results[Constants.WEEK_DIR_TOP_DST]
        IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]

        if direction ==Constants.DIR_UP:
            res = Constants.DIR_UP
            #caso en el que no
            if IND_BLG_UPPER_DST_PERCENT <= 40 or weekTopDst < 25:
                    res = Constants.DIR_DOWN
                    # # puede que haya estado subiendo
                    # if week_prev_med < week_med:
                    #     res = Constants.DIR_UP

            elif IND_BLG_UPPER_DST_PERCENT > 40 and IND_BLG_UPPER_DST_PERCENT <= 60:
                # aca no sabemos
                if results[Constants.DIRECTION] == Constants.DIR_UP:
                    res = Constants.DIR_UP
                elif results[Constants.DIRECTION] == Constants.DIR_DOWN:
                    res = Constants.DIR_DOWN
                # if fcst == Constants.IND_REL_FCST_PRE_UP or fcst == Constants.IND_REL_FCST_UP \
                #         or fcst == Constants.IND_REL_FCST_DOWN_INV_REL:
                #     res = Constants.DIR_UP
                # else:
                #     res = Constants.DIR_DOWN
        elif direction ==Constants.DIR_DOWN:
            res = Constants.DIR_DOWN
            #caso en el que no
            if IND_BLG_UPPER_DST_PERCENT >= 60 or weekTopDst > 75:
                    res = Constants.DIR_UP
                    # # puede que haya estado subiendo
                    # if week_prev_med < week_med:
                    #     res = Constants.DIR_UP

            elif IND_BLG_UPPER_DST_PERCENT > 40 and IND_BLG_UPPER_DST_PERCENT <= 60:
                # aca no sabemos
                if results[Constants.DIRECTION] == Constants.DIR_UP:
                    res = Constants.DIR_UP
                elif results[Constants.DIRECTION] == Constants.DIR_DOWN:
                    res = Constants.DIR_DOWN
                # if fcst == Constants.IND_REL_FCST_PRE_UP or fcst == Constants.IND_REL_FCST_UP \
                #         or fcst == Constants.IND_REL_FCST_DOWN_INV_REL:
                #     res = Constants.DIR_UP
                # else:
                #     res = Constants.DIR_DOWN

        return res

    def getProMEDSTD_END_BLG_071(self, results, active):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            week = results[Constants.WEEK_FLOW]
            weekPrev = results[Constants.WEEK_FLOW_PREV]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            week_med_abs = abs(results[Constants.WEEK_FLOW_MED])
            flowdiff = results[Constants.FLOW_DIFF]
            week_std = results[Constants.WEEK_FLOW_STD]
            weekdiff = results[Constants.WEEK_FLOW_DIFF]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            medDay = results[Constants.INDICATOR_MED_DAY]
            absMedDay = abs(medDay)
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            # BLG
            IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]
            IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
            blgDistPercent = active.parameters.blgDistPercent

            # valores del dia
            numUP = results[Constants.IND_NUM_UP]
            numDOWN = results[Constants.IND_NUM_DOWN]

            sumUP = results[Constants.IND_SUM_UP]
            sumDOWN = results[Constants.IND_SUM_DOWN]

            sumDay = int(sumUP) - int(sumDOWN)

            weekdiffTendenceValue = 1
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]

            if prevPercent is not None:
                prevPercent = float(prevPercent)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]
            # if med == 0:
            #     if direction == Constants.DIR_UP:
            #         med = 1
            #     elif direction == Constants.DIR_DOWN:
            #         med = -1
            # percentFlow = Constants.DIR_WAIT
            # if percent > prevPercent:
            #     percentFlow = Constants.DIR_UP
            # else:
            #     # baja
            #     percentFlow = Constants.DIR_DOWN
            # CALCULOS final del
            week_prev_res = None
            if week_prev_med < week_med:
                week_prev_res = Constants.DIR_UP
                if flowdiff > 0:
                    week_prev_res = Constants.DIR_UP
                else:
                    week_prev_res = Constants.DIR_DOWN
                    ndad =""
                    # ver que hacer cuando no coinciden
                    print(f" getProMEDSTD_END_BLG_05 NO COINCIDE")
            elif week_prev_med > week_med:
                week_prev_res = Constants.DIR_DOWN
                if flowdiff < 0:
                    week_prev_res = Constants.DIR_DOWN
                else:
                    week_prev_res = Constants.DIR_UP
                    ndad =""
                    # ver que hacer cuando no coinciden
                    print(f" getProMEDSTD_END_BLG_05 NO COINCIDE")
            if week == Constants.WEEK_FLOW_UP:
                #SUBE
                res = Constants.DIR_UP
                if active.parameters.weekMindiff != 0.7:
                    #ha cambiado el weekdiff
                    if abs(weekdiff) < active.parameters.weekMindiff:
                        print(f"prob is using week_prev_differential")
                        res = week_prev_res
            else:
                # BAJA
                res = Constants.DIR_DOWN
                if active.parameters.weekMindiff != 0.7:
                    # ha cambiado el weekdiff
                    if abs(weekdiff) < active.parameters.weekMindiff:
                        print(f"prob is using week_prev_differential")
                        res = week_prev_res
        except Exception as error:
            print("Error getProMEDSTD_END BLG05", error)
        return res

    def getProMEDSTD_END_BLG_03(self, results, active):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            week = results[Constants.WEEK_FLOW]
            weekPrev = results[Constants.WEEK_FLOW_PREV]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            week_med_abs = abs(results[Constants.WEEK_FLOW_MED])
            week_prev_med_abs = abs(results[Constants.WEEK_FLOW_PREV_MED])
            week_std = results[Constants.WEEK_FLOW_STD]
            weekdiff = results[Constants.WEEK_FLOW_DIFF]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            medDay = results[Constants.INDICATOR_MED_DAY]
            absMedDay = abs(medDay)
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            # BLG
            IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]
            IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
            blgDistPercent = active.parameters.blgDistPercent

            # valores del dia
            numUP = results[Constants.IND_NUM_UP]
            numDOWN = results[Constants.IND_NUM_DOWN]

            sumUP = results[Constants.IND_SUM_UP]
            sumDOWN = results[Constants.IND_SUM_DOWN]

            sumDay = int(sumUP) - int(sumDOWN)

            weekdiffTendenceValue = 1
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]

            if prevPercent is not None:
                prevPercent = float(prevPercent)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]
            # if med == 0:
            #     if direction == Constants.DIR_UP:
            #         med = 1
            #     elif direction == Constants.DIR_DOWN:
            #         med = -1
            percentFlow = Constants.DIR_WAIT
            if percent > prevPercent:
                percentFlow = Constants.DIR_UP
            else:
                # baja
                percentFlow = Constants.DIR_DOWN
            # CALCULOS final del dia
            if week == Constants.WEEK_FLOW_UP:
                #SUBE
                res = Constants.DIR_UP
                if active.parameters.weekMindiff != 0.7:
                    #ha cambiado el weekdiff
                    if abs(weekdiff) < active.parameters.weekMindiff:

                        #esta cambiando no esta claro
                        if IND_BLG_UPPER_DST_PERCENT <= 40:
                            res = Constants.DIR_DOWN
                            #puede que haya estado subiendo
                            if week_prev_med < week_med:
                                res = Constants.DIR_UP

                        elif IND_BLG_UPPER_DST_PERCENT > 40 and IND_BLG_UPPER_DST_PERCENT <= 60:
                            # aca no sabemos
                            if results[Constants.DIRECTION] == Constants.DIR_UP:
                                res = Constants.DIR_UP
                            elif results[Constants.DIRECTION] == Constants.DIR_DOWN:
                                res = Constants.DIR_DOWN
                            # if fcst == Constants.IND_REL_FCST_PRE_UP or fcst == Constants.IND_REL_FCST_UP \
                            #         or fcst == Constants.IND_REL_FCST_DOWN_INV_REL:
                            #     res = Constants.DIR_UP
                            # else:
                            #     res = Constants.DIR_DOWN
                        elif IND_BLG_UPPER_DST_PERCENT > 60:
                            res = Constants.DIR_UP
                else:
                    nada = ""
                    # if week_med_abs < 1 or weekdiff <0 :
                    #     print(f"prob is using DIRECTION")
                    #     if results[Constants.DIRECTION]== Constants.DIR_UP:
                    #         res = Constants.DIR_UP
                    #     elif results[Constants.DIRECTION]== Constants.DIR_DOWN:
                    #         res = Constants.DIR_DOWN
                    #     else:
                    #         if weekPrev ==Constants.WEEK_FLOW_UP:
                    #             res = Constants.DIR_DOWN
                    #         else:
                    #             res = Constants.DIR_UP
            else:
                #BAJA
                res = Constants.DIR_DOWN
                if active.parameters.weekMindiff != 0.7:
                    #ha cambiado el weekdiff
                    if abs(weekdiff) < active.parameters.weekMindiff:
                        print(f"prob is using DIRECTION")

                        #esta cambiando no esta claro
                        if IND_BLG_UPPER_DST_PERCENT <= 40:
                            res = Constants.DIR_DOWN
                            # puede que haya estado subiendo
                            if week_prev_med < week_med:
                                res = Constants.DIR_UP

                        elif IND_BLG_UPPER_DST_PERCENT > 40 and IND_BLG_UPPER_DST_PERCENT <= 60:
                            # aca no sabemos
                            if results[Constants.DIRECTION] == Constants.DIR_UP:
                                res = Constants.DIR_UP
                            elif results[Constants.DIRECTION] == Constants.DIR_DOWN:
                                res = Constants.DIR_DOWN
                            # if fcst == Constants.IND_REL_FCST_PRE_UP or fcst == Constants.IND_REL_FCST_UP \
                            #         or fcst == Constants.IND_REL_FCST_DOWN_INV_REL:
                            #     res = Constants.DIR_UP
                            # else:
                            #     res = Constants.DIR_DOWN
                        elif IND_BLG_UPPER_DST_PERCENT > 60:
                            res = Constants.DIR_UP
                else:
                    nada = ""
                    # if week_med_abs < 1 or weekdiff <0 :
                    #     print(f"prob is using DIRECTION")
                    #     if results[Constants.DIRECTION]== Constants.DIR_UP:
                    #         res = Constants.DIR_UP
                    #     elif results[Constants.DIRECTION]== Constants.DIR_DOWN:
                    #         res = Constants.DIR_DOWN
                    #     else:
                    #         if weekPrev ==Constants.WEEK_FLOW_UP:
                    #             res = Constants.DIR_DOWN
                    #         else:
                    #             res = Constants.DIR_UP


        except Exception as error:
            print("Error getProMEDSTD_END BLG03", error)
        return res

    def getProMEDSTD_END_05(self, results):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            week = results[Constants.WEEK_FLOW]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_med_abs = results[Constants.WEEK_FLOW_MED]
            week_std = results[Constants.WEEK_FLOW_STD]
            weekdiff = abs(week_med_abs - week_std)
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            medDay = results[Constants.INDICATOR_MED_DAY]
            absMedDay = abs(medDay)
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]

            # valores del dia
            numUP = results[Constants.IND_NUM_UP]
            numDOWN = results[Constants.IND_NUM_DOWN]

            sumUP = results[Constants.IND_SUM_UP]
            sumDOWN = results[Constants.IND_SUM_DOWN]

            sumDay = int(sumUP) - int(sumDOWN)
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]

            if prevPercent is not None:
                prevPercent = float(prevPercent)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]
            # if med == 0:
            #     if direction == Constants.DIR_UP:
            #         med = 1
            #     elif direction == Constants.DIR_DOWN:
            #         med = -1
            percentFlow = Constants.DIR_WAIT
            if percent > prevPercent:
                percentFlow = Constants.DIR_UP
            else:
                # baja
                percentFlow = Constants.DIR_DOWN
            # CALCULOS final del dia

            # CALCULOS final del dia
            if fcst == Constants.IND_REL_FCST_PRE_UP or fcst == Constants.IND_REL_FCST_UP \
                    or fcst == Constants.IND_REL_FCST_DOWN_INV_REL:
                if percent >= 0 and percent < 80:
                    if sumDay > 0:
                        # ha subido entonces bajara
                        if percent > 10:
                            res = res = Constants.DIR_DOWN
                        else:
                            if absMedDay > stdDay:
                                if medDay > 0:
                                    res = Constants.DIR_UP
                                else:
                                    res = Constants.DIR_DOWN
                            else:
                                if med > medDay:
                                    # sube
                                    res = Constants.DIR_UP
                                else:
                                    res = Constants.DIR_DOWN
                    else:
                        # bajo mucho subira
                        if percent <= 90:
                            res = res = Constants.DIR_UP
                        else:
                            if absMedDay > stdDay:
                                if medDay > 0:
                                    res = Constants.DIR_UP
                                else:
                                    res = Constants.DIR_DOWN
                            else:
                                if med > medDay:
                                    # sube
                                    res = Constants.DIR_UP
                                else:
                                    res = Constants.DIR_DOWN
                elif percent >= 80 and percent < 90:
                    # revisar si esta en tendencia de subida.
                    isTendence = False
                    if week_med_abs > week_std:
                        if weekdiff > 1.5:
                            isTendence = True

                    if isTendence:
                        res = Constants.DIR_UP
                    else:
                        if sumDay > 0:
                            # ha subido entonces bajara
                            if percent > 10:
                                res = res = Constants.DIR_DOWN
                            else:
                                if absMedDay > stdDay:
                                    if medDay > 0:
                                        res = Constants.DIR_UP
                                    else:
                                        res = Constants.DIR_DOWN
                                else:
                                    if med > medDay:
                                        # sube
                                        res = Constants.DIR_UP
                                    else:
                                        res = Constants.DIR_DOWN
                        else:
                            # bajo mucho subira
                            if percent <= 90:
                                res = res = Constants.DIR_UP
                            else:
                                if absMedDay > stdDay:
                                    if medDay > 0:
                                        res = Constants.DIR_UP
                                    else:
                                        res = Constants.DIR_DOWN
                                else:
                                    if med > medDay:
                                        # sube
                                        res = Constants.DIR_UP
                                    else:
                                        res = Constants.DIR_DOWN

                elif percent >= 90 and percent <= 100:
                    # revisar si esta en tendencia de subida.
                    isTendence = False
                    if week_med_abs > week_std:
                        if weekdiff > 1.5:
                            isTendence = True

                    if isTendence:
                        res = Constants.DIR_UP
                    else:
                        if sumDay > 0:
                            # ha subido entonces bajara
                            if percent > 10:
                                res = res = Constants.DIR_DOWN
                            else:
                                if absMedDay > stdDay:
                                    if medDay > 0:
                                        res = Constants.DIR_UP
                                    else:
                                        res = Constants.DIR_DOWN
                                else:
                                    if med > medDay:
                                        # sube
                                        res = Constants.DIR_UP
                                    else:
                                        res = Constants.DIR_DOWN
                        else:
                            # bajo mucho subira
                            if percent <= 90:
                                res = res = Constants.DIR_UP
                            else:
                                if absMedDay > stdDay:
                                    if medDay > 0:
                                        res = Constants.DIR_UP
                                    else:
                                        res = Constants.DIR_DOWN
                                else:
                                    if med > medDay:
                                        # sube
                                        res = Constants.DIR_UP
                                    else:
                                        res = Constants.DIR_DOWN

            if fcst == Constants.IND_REL_FCST_PRE_DOWN or fcst == Constants.IND_REL_FCST_DOWN \
                    or fcst == Constants.IND_REL_FCST_UP_INV_REL:
                if percent > 20 and percent <= 100:
                    # if abs(medFcst) > stdFcst:
                    #     res = Constants.DIR_DOWN
                    # else:
                    #     if med > 0:
                    #         if absmed > std:
                    #             res = Constants.DIR_UP
                    #         else:
                    #             res = Constants.DIR_PRE_UP
                    #     elif med < 0:
                    #         if absmed > std:
                    #             res = Constants.DIR_DOWN
                    #         else:
                    #             res = Constants.DIR_PRE_DOWN
                    if sumDay > 0:
                        # ha subido entonces bajara
                        if percent > 10:
                            res = res = Constants.DIR_DOWN
                        else:
                            # no estamos seguros evaluamos otro factor
                            if absMedDay > stdDay:
                                if medDay > 0:
                                    res = Constants.DIR_UP
                                else:
                                    res = Constants.DIR_DOWN
                            else:
                                if med > medDay:
                                    # sube
                                    res = Constants.DIR_UP
                                else:
                                    res = Constants.DIR_DOWN
                    else:
                        # bajo mucho subira
                        # ha subido entonces bajara
                        if percent <= 90:
                            res = res = Constants.DIR_UP
                        else:
                            # no estamos seguros evaluamos otro factor
                            if absMedDay > stdDay:
                                if medDay > 0:
                                    res = Constants.DIR_UP
                                else:
                                    res = Constants.DIR_DOWN
                            else:
                                if med > medDay:
                                    # sube
                                    res = Constants.DIR_UP
                                else:
                                    res = Constants.DIR_DOWN

                elif percent > 10 and percent <= 20:
                    isTendence = False
                    if week_med_abs > week_std:
                        if weekdiff > 1.5:
                            isTendence = True

                    if isTendence:
                        res = Constants.DIR_DOWN
                    else:

                        if sumDay > 0:
                            # ha subido entonces bajara
                            if percent > 10:
                                res = res = Constants.DIR_DOWN
                            else:
                                if absMedDay > stdDay:
                                    if medDay > 0:
                                        res = Constants.DIR_UP
                                    else:
                                        res = Constants.DIR_DOWN
                                else:
                                    if absMedDay > 1:
                                        if medMoment >= 0:
                                            if absMedMoment > stdMoment:
                                                # sube
                                                res = Constants.DIR_UP
                                            else:
                                                res = Constants.DIR_PRE_UP
                                        elif medMoment < 0:
                                            if absMedMoment > stdMoment:
                                                res = Constants.DIR_DOWN
                                            else:
                                                res = Constants.DIR_PRE_DOWN
                                    else:
                                        if med > medDay:
                                            # sube
                                            res = Constants.DIR_UP
                                        else:
                                            res = Constants.DIR_DOWN
                        else:
                            # bajo mucho subira
                            # ha subido entonces bajara
                            if percent <= 90:
                                res = res = Constants.DIR_UP
                            else:
                                if absMedDay > stdDay:
                                    if medDay > 0:
                                        res = Constants.DIR_UP
                                    else:
                                        res = Constants.DIR_DOWN
                                else:
                                    if absMedDay > 1:
                                        if medMoment >= 0:
                                            if absMedMoment > stdMoment:
                                                # sube
                                                res = Constants.DIR_UP
                                            else:
                                                res = Constants.DIR_PRE_UP
                                        elif medMoment < 0:
                                            if absMedMoment > stdMoment:
                                                res = Constants.DIR_DOWN
                                            else:
                                                res = Constants.DIR_PRE_DOWN
                                    else:
                                        if med > medDay:
                                            # sube
                                            res = Constants.DIR_UP
                                        else:
                                            res = Constants.DIR_DOWN

                elif percent >= 0 and percent <= 10:
                    isTendence = False
                    if week_med_abs > week_std:
                        if weekdiff > 1.5:
                            isTendence = True

                    if isTendence:
                        res = Constants.DIR_DOWN
                    else:

                        if sumDay > 0:
                            # ha subido entonces bajara
                            if percent > 10:
                                res = res = Constants.DIR_DOWN
                            else:
                                if absMedDay > stdDay:
                                    if medDay > 0:
                                        res = Constants.DIR_UP
                                    else:
                                        res = Constants.DIR_DOWN
                                else:
                                    if absMedDay > 1:
                                        if medMoment >= 0:
                                            if absMedMoment > stdMoment:
                                                # sube
                                                res = Constants.DIR_UP
                                            else:
                                                res = Constants.DIR_PRE_UP
                                        elif medMoment < 0:
                                            if absMedMoment > stdMoment:
                                                res = Constants.DIR_DOWN
                                            else:
                                                res = Constants.DIR_PRE_DOWN
                                    else:
                                        if med > medDay:
                                            # sube
                                            res = Constants.DIR_UP
                                        else:
                                            res = Constants.DIR_DOWN
                        else:
                            # bajo mucho subira
                            # ha subido entonces bajara
                            if percent <= 90:
                                res = res = Constants.DIR_UP
                            else:
                                if absMedDay > stdDay:
                                    if medDay > 0:
                                        res = Constants.DIR_UP
                                    else:
                                        res = Constants.DIR_DOWN
                                else:
                                    if absMedDay > 1:
                                        if medMoment >= 0:
                                            if absMedMoment > stdMoment:
                                                # sube
                                                res = Constants.DIR_UP
                                            else:
                                                res = Constants.DIR_PRE_UP
                                        elif medMoment < 0:
                                            if absMedMoment > stdMoment:
                                                res = Constants.DIR_DOWN
                                            else:
                                                res = Constants.DIR_PRE_DOWN
                                    else:
                                        if med > medDay:
                                            # sube
                                            res = Constants.DIR_UP
                                        else:
                                            res = Constants.DIR_DOWN


        except Exception as error:
            print("Error getProMEDSTD_END_05 ", error)
        return res

    def getProMEDSTD_INI(self, results):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            week = results[Constants.WEEK_FLOW]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_med_abs = results[Constants.WEEK_FLOW_MED]
            week_std = results[Constants.WEEK_FLOW_STD]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            if prevPercent is not None:
                prevPercent = float(prevPercent)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]
            flujo = results[Constants.FLUJO]
            if med == 0:
                if direction == Constants.DIR_UP:
                    med = 1
                elif direction == Constants.DIR_DOWN:
                    med = -1
            percentFlow = Constants.DIR_WAIT
            if percent > prevPercent:
                percentFlow = Constants.DIR_UP
            else:
                # baja
                percentFlow = Constants.DIR_DOWN
            # CALCULOS RAPIDOS AL MOMENTO
            if fcst == Constants.IND_REL_FCST_PRE_UP or fcst == Constants.IND_REL_FCST_UP:
                if percent >= 0 and percent < 95:
                    if med > 0:
                        if absmed > std:
                            res = Constants.DIR_UP
                        else:
                            # res = Constants.DIR_PRE_UP
                            res = self.determine_Direction_percent_Flow(direction, percentFlow)
                    else:
                        if absmed >= std:
                            # verificacion
                            if percentFlow == Constants.DIR_DOWN:
                                res = Constants.DIR_DOWN
                            elif percentFlow == Constants.DIR_UP:
                                res = Constants.DIR_PRE_UP
                            else:
                                res = Constants.DIR_DOWN
                        else:

                            # if percentFlow == Constants.DIR_UP:
                            #     if absMedMoment >= stdMoment:
                            #         res = Constants.DIR_UP
                            #     else:
                            #         res = Constants.DIR_PRE_UP
                            # elif percentFlow == Constants.DIR_DOWN:
                            #     # baja
                            #     res = Constants.DIR_PRE_DOWN
                            # else:
                            #     if absMedMoment >= stdMoment:
                            #         res = Constants.DIR_DOWN
                            #     else:
                            #         res = Constants.DIR_PRE_DOWN
                            if medMoment > 0:
                                # baja
                                if absMedMoment > stdMoment:
                                    res = Constants.DIR_UP
                                else:
                                    res = Constants.DIR_PRE_UP
                            else:
                                # sube
                                # res = Constants.DIR_PRE_UP
                                if percentFlow == Constants.DIR_DOWN:
                                    res = Constants.DIR_PRE_DOWN
                elif percent >= 95:
                    if med < 0:
                        if absmed > std:
                            res = Constants.DIR_DOWN
                        else:
                            # res = Constants.DIR_PRE_DOWN
                            res = self.determine_Direction_percent_Flow(direction, percentFlow)
                    if med >= 0:
                        if absmed > std:
                            res = Constants.DIR_UP
                        else:
                            # fix se anade direction
                            if direction == Constants.DIR_UP or direction == Constants.DIR_PRE_UP:
                                res = Constants.DIR_UP
                            else:
                                if percentFlow == Constants.DIR_UP:
                                    res = Constants.DIR_PRE_UP
                                else:
                                    res = Constants.DIR_PRE_DOWN

            if fcst == Constants.IND_REL_FCST_DOWN_INV_REL:
                if percent > 10 and percent <= 100:
                    if med > 0:
                        if absmed > std:
                            res = Constants.DIR_UP
                        else:
                            # res = Constants.DIR_PRE_UP
                            res = self.determine_Direction_percent_Flow(direction, percentFlow)
                    else:
                        if absmed > std:
                            res = Constants.DIR_DOWN
                        else:
                            # res = Constants.DIR_PRE_DOWN
                            res = self.determine_Direction_percent_Flow(direction, percentFlow)
                elif percent <= 10:
                    if med >= 0:
                        if absmed > std:
                            res = Constants.DIR_UP
                        else:
                            # res = Constants.DIR_PRE_UP
                            res = self.determineMedMomentFlow(medMoment, absMedMoment, stdMoment, direction)
                    if med < 0:
                        if absmed > std:
                            res = Constants.DIR_DOWN
                        else:
                            if direction == Constants.DIR_DOWN or direction == Constants.DIR_PRE_DOWN:
                                res = Constants.DIR_DOWN
                            else:
                                if percentFlow == Constants.DIR_UP:
                                    res = Constants.DIR_PRE_UP
                                else:
                                    res = Constants.DIR_PRE_DOWN

            if fcst == Constants.IND_REL_FCST_PRE_DOWN or fcst == Constants.IND_REL_FCST_DOWN:
                if percent >= 15 and percent <= 100:
                    if med < 0:
                        if absmed > std:
                            res = Constants.DIR_DOWN
                        else:
                            # res = Constants.DIR_PRE_DOWN
                            res = self.determine_Direction_percent_Flow(direction, percentFlow)
                    elif med > 0:
                        if absmed >= std:
                            # verificacion
                            if flujo == Constants.FLUJO_SUBE:
                                res = Constants.DIR_UP
                            else:
                                res = Constants.DIR_PRE_DOWN
                        else:
                            # res = Constants.DIR_PRE_UP
                            # contradiccion revisar week
                            if medMoment < 0:
                                # baja
                                if absMedMoment > stdMoment:
                                    res = Constants.DIR_DOWN
                                else:
                                    res = Constants.DIR_PRE_DOWN
                            else:
                                # sube
                                # res = Constants.DIR_PRE_UP
                                if percentFlow == Constants.DIR_UP:
                                    res = Constants.DIR_PRE_UP

                elif percent <= 15:
                    if med >= 0:
                        if absmed > std:
                            res = Constants.DIR_UP
                        else:
                            # res = Constants.DIR_PRE_UP
                            # res = self.determine_Direction_percent_Flow(direction, percentFlow)
                            res = self.determineMedMomentFlow(medMoment, absMedMoment, stdMoment, direction)
                    if med < 0:
                        if absmed > std:
                            res = Constants.DIR_DOWN
                        else:
                            # res = Constants.DIR_PRE_DOWN
                            if direction == Constants.DIR_DOWN or direction == Constants.DIR_PRE_DOWN:
                                res = Constants.DIR_DOWN
                            else:
                                if percentFlow == Constants.DIR_UP:
                                    res = Constants.DIR_PRE_UP
                                else:
                                    res = Constants.DIR_PRE_DOWN

            if fcst == Constants.IND_REL_FCST_UP_INV_REL:
                if percent >= 0 and percent < 95:
                    if med > 0:
                        if absmed > std:
                            res = Constants.DIR_UP
                        else:
                            # res = Constants.DIR_PRE_UP
                            # res = self.determine_Direction_percent_Flow(direction, percentFlow)
                            res = self.determineMedMomentFlow(medMoment, absMedMoment, stdMoment, direction)
                    elif med < 0:
                        if absmed > std:
                            res = Constants.DIR_DOWN
                        else:
                            # res = Constants.DIR_PRE_DOWN
                            # res = self.determine_Direction_percent_Flow(direction, percentFlow)
                            res = self.determineMedMomentFlow(medMoment, absMedMoment, stdMoment, direction)
                elif percent >= 95:
                    res = Constants.DIR_DOWN
                    # if med < 0:
                    #     if absmed > std:
                    #         res = Constants.DIR_DOWN
                    #     else:
                    #         # res = Constants.DIR_PRE_DOWN
                    #         # res = self.determine_Direction_percent_Flow(direction, percentFlow)
                    #         res = self.determineMedMomentFlow(medMoment, absMedMoment, stdMoment, direction)
                    # if med > 0:
                    #     if absmed > std:
                    #         res = Constants.DIR_UP
                    #     else:
                    #         # fix se anade direction
                    #         if direction == Constants.DIR_UP or direction == Constants.DIR_PRE_UP:
                    #             res = Constants.DIR_UP
                    #         else:
                    #             if percentFlow == Constants.DIR_UP:
                    #                 res = Constants.DIR_PRE_UP
                    #             else:
                    #                 res = Constants.DIR_PRE_DOWN

        except Exception as error:
            print("Error getProMEDSTD_INI ", error)
        return res

    def getProMEDSTD_INI_02(self, results):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            week = results[Constants.WEEK_FLOW]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_med_abs = results[Constants.WEEK_FLOW_MED]
            week_std = results[Constants.WEEK_FLOW_STD]
            direction = results[Constants.DIRECTION]

            medDay = results[Constants.INDICATOR_MED_DAY]
            absMedDay = abs(medDay)
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]

            # valores del dia
            sumUP = results[Constants.IND_SUM_UP]
            sumDOWN = results[Constants.IND_SUM_DOWN]

            # valores de varios dias
            sumUPDAYS = results[Constants.IND_SUM_UP_DAYS]
            sumDOWNDAYS = results[Constants.IND_SUM_DOWN_DAYS]

            sumDay = int(sumUP) - int(sumDOWN)
            sumDAYS = int(sumUPDAYS) - int(sumDOWNDAYS)

            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            if prevPercent is not None:
                prevPercent = float(prevPercent)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]
            flujo = results[Constants.FLUJO]
            diffPercent = abs(prevPercent - percent)
            if med == 0:
                if direction == Constants.DIR_UP:
                    med = 1
                elif direction == Constants.DIR_DOWN:
                    med = -1
            percentFlow = Constants.DIR_WAIT
            if percent > prevPercent:
                percentFlow = Constants.DIR_UP
            else:
                # baja
                percentFlow = Constants.DIR_DOWN
            # CALCULOS RAPIDOS AL MOMENTO

            # if percentFlow == Constants.DIR_UP:
            #     res = Constants.DIR_DOWN
            # else:
            #     res = Constants.DIR_UP
            if sumDAYS > 0:
                # ha subido entonces bajara
                if percent > 10:
                    res = res = Constants.DIR_DOWN
                else:
                    # inverso del valor le toca subir
                    res = Constants.DIR_UP

            else:
                # bajo mucho subira
                if percent <= 90:
                    res = res = Constants.DIR_UP
                else:
                    # inversa del valor le toca bajar
                    res = Constants.DIR_DOWN

        except Exception as error:
            print("Error getProMEDSTD_INI ", error)
        return res

    def getProMEDSTD_INI_03(self, results):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            week = results[Constants.WEEK_FLOW]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_med_abs = results[Constants.WEEK_FLOW_MED]
            week_std = results[Constants.WEEK_FLOW_STD]
            direction = results[Constants.DIRECTION]

            medDay = results[Constants.INDICATOR_MED_DAY]
            absMedDay = abs(medDay)
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]

            # valores del dia
            sumUP = results[Constants.IND_SUM_UP]
            sumDOWN = results[Constants.IND_SUM_DOWN]

            # valores de varios dias
            sumUPDAYS = results[Constants.IND_SUM_UP_DAYS]
            sumDOWNDAYS = results[Constants.IND_SUM_DOWN_DAYS]

            sumDay = int(sumUP) - int(sumDOWN)
            sumDAYS = int(sumUPDAYS) - int(sumDOWNDAYS)

            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            if prevPercent is not None:
                prevPercent = float(prevPercent)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]
            flujo = results[Constants.FLUJO]
            diffPercent = abs(prevPercent - percent)
            if med == 0:
                if direction == Constants.DIR_UP:
                    med = 1
                elif direction == Constants.DIR_DOWN:
                    med = -1
            percentFlow = Constants.DIR_WAIT
            if percent > prevPercent:
                percentFlow = Constants.DIR_UP
            else:
                # baja
                percentFlow = Constants.DIR_DOWN
            # CALCULOS RAPIDOS AL MOMENTO

            # if percentFlow == Constants.DIR_UP:
            #     res = Constants.DIR_DOWN
            # else:
            #     res = Constants.DIR_UP

            # INVERSA
            if percentFlow == Constants.DIR_UP and med > 0:
                print("getProMEDSTD_INI_03 percentFlow UP")
                res = Constants.DIR_DOWN
            elif percentFlow == Constants.DIR_DOWN and med < 0:
                print("getProMEDSTD_INI_03 percentFlow DOWN")
                res = Constants.DIR_UP
            else:
                print("getProMEDSTD_INI_03 percentFlow SUMDAYS")
                if sumDAYS > 0:
                    # ha subido entonces bajara
                    if percent > 10:
                        res = res = Constants.DIR_DOWN
                    else:
                        # inverso del valor le toca subir
                        res = Constants.DIR_UP

                else:
                    # bajo mucho subira
                    if percent <= 90:
                        res = res = Constants.DIR_UP
                    else:
                        # inversa del valor le toca bajar
                        res = Constants.DIR_DOWN

        except Exception as error:
            print("Error getProMEDSTD_INI ", error)
        return res

    def getProMEDSTD_INI_01(self, results):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            week = results[Constants.WEEK_FLOW]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_med_abs = results[Constants.WEEK_FLOW_MED]
            week_std = results[Constants.WEEK_FLOW_STD]
            direction = results[Constants.DIRECTION]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            if prevPercent is not None:
                prevPercent = float(prevPercent)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]
            flujo = results[Constants.FLUJO]
            diffPercent = abs(prevPercent - percent)
            if med == 0:
                if direction == Constants.DIR_UP:
                    med = 1
                elif direction == Constants.DIR_DOWN:
                    med = -1
            percentFlow = Constants.DIR_WAIT
            if percent > prevPercent:
                percentFlow = Constants.DIR_UP
            else:
                # baja
                percentFlow = Constants.DIR_DOWN
            # CALCULOS RAPIDOS AL MOMENTO

            # if percentFlow == Constants.DIR_UP:
            #     res = Constants.DIR_DOWN
            # else:
            #     res = Constants.DIR_UP

            if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UP:
                if diffPercent <= 20:
                    res = Constants.DIR_UP
                else:
                    if percentFlow == Constants.DIR_UP:
                        res = Constants.DIR_DOWN
                    else:
                        res = Constants.DIR_UP
            elif results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_DOWN:
                if diffPercent <= 20:
                    res = Constants.DIR_DOWN
                else:
                    if percentFlow == Constants.DIR_UP:
                        res = Constants.DIR_DOWN
                    else:
                        res = Constants.DIR_UP

            # if fcst == Constants.IND_REL_FCST_PRE_UP or fcst == Constants.IND_REL_FCST_UP:
            #     if percent >= 0 and percent < 95:
            #         if med > 0:
            #             if absmed > std:
            #                 res = Constants.DIR_UP
            #             else:
            #                 # res = Constants.DIR_PRE_UP
            #                 res = self.determine_Direction_percent_Flow(direction, percentFlow)
            #         else:
            #             if absmed >= std:
            #                 # verificacion
            #                 if percentFlow == Constants.DIR_DOWN:
            #                     res = Constants.DIR_DOWN
            #                 elif percentFlow == Constants.DIR_UP:
            #                     res = Constants.DIR_PRE_UP
            #                 else:
            #                     res = Constants.DIR_DOWN
            #             else:
            #
            #                 # if percentFlow == Constants.DIR_UP:
            #                 #     if absMedMoment >= stdMoment:
            #                 #         res = Constants.DIR_UP
            #                 #     else:
            #                 #         res = Constants.DIR_PRE_UP
            #                 # elif percentFlow == Constants.DIR_DOWN:
            #                 #     # baja
            #                 #     res = Constants.DIR_PRE_DOWN
            #                 # else:
            #                 #     if absMedMoment >= stdMoment:
            #                 #         res = Constants.DIR_DOWN
            #                 #     else:
            #                 #         res = Constants.DIR_PRE_DOWN
            #                 if medMoment > 0:
            #                     # baja
            #                     if absMedMoment > stdMoment:
            #                         res = Constants.DIR_UP
            #                     else:
            #                         res = Constants.DIR_PRE_UP
            #                 else:
            #                     # sube
            #                     # res = Constants.DIR_PRE_UP
            #                     if percentFlow==Constants.DIR_DOWN:
            #                             res = Constants.DIR_PRE_DOWN
            #     elif percent >= 95:
            #         if med < 0:
            #             if absmed > std:
            #                 res = Constants.DIR_DOWN
            #             else:
            #                 # res = Constants.DIR_PRE_DOWN
            #                 res = self.determine_Direction_percent_Flow(direction, percentFlow)
            #         if med >= 0:
            #             if absmed > std:
            #                 res = Constants.DIR_UP
            #             else:
            #                 # fix se anade direction
            #                 if direction == Constants.DIR_UP or direction == Constants.DIR_PRE_UP:
            #                     res = Constants.DIR_UP
            #                 else:
            #                     if percentFlow == Constants.DIR_UP:
            #                         res = Constants.DIR_PRE_UP
            #                     else:
            #                         res = Constants.DIR_PRE_DOWN
            #
            # if fcst == Constants.IND_REL_FCST_DOWN_INV_REL:
            #     if percent > 10 and percent <= 100:
            #         if med > 0:
            #             if absmed > std:
            #                 res = Constants.DIR_UP
            #             else:
            #                 # res = Constants.DIR_PRE_UP
            #                 res = self.determine_Direction_percent_Flow(direction, percentFlow)
            #         else:
            #             if absmed > std:
            #                 res = Constants.DIR_DOWN
            #             else:
            #                 # res = Constants.DIR_PRE_DOWN
            #                 res = self.determine_Direction_percent_Flow(direction, percentFlow)
            #     elif percent <= 10:
            #         if med >= 0:
            #             if absmed > std:
            #                 res = Constants.DIR_UP
            #             else:
            #                 # res = Constants.DIR_PRE_UP
            #                 res = self.determineMedMomentFlow(medMoment, absMedMoment, stdMoment, direction)
            #         if med < 0:
            #             if absmed > std:
            #                 res = Constants.DIR_DOWN
            #             else:
            #                 if direction == Constants.DIR_DOWN or direction == Constants.DIR_PRE_DOWN:
            #                     res = Constants.DIR_DOWN
            #                 else:
            #                     if percentFlow == Constants.DIR_UP:
            #                         res = Constants.DIR_PRE_UP
            #                     else:
            #                         res = Constants.DIR_PRE_DOWN
            #
            # if fcst == Constants.IND_REL_FCST_PRE_DOWN or fcst == Constants.IND_REL_FCST_DOWN:
            #     if percent >= 15 and percent <= 100:
            #         if med < 0:
            #             if absmed > std:
            #                 res = Constants.DIR_DOWN
            #             else:
            #                 # res = Constants.DIR_PRE_DOWN
            #                 res = self.determine_Direction_percent_Flow(direction, percentFlow)
            #         elif med > 0:
            #             if absmed >= std:
            #                 # verificacion
            #                if flujo == Constants.FLUJO_SUBE:
            #                    res = Constants.DIR_UP
            #                else:
            #                    res = Constants.DIR_PRE_DOWN
            #             else:
            #                 # res = Constants.DIR_PRE_UP
            #                 # contradiccion revisar week
            #                 if medMoment < 0:
            #                     # baja
            #                     if absMedMoment > stdMoment:
            #                         res = Constants.DIR_DOWN
            #                     else:
            #                         res = Constants.DIR_PRE_DOWN
            #                 else:
            #                     # sube
            #                     # res = Constants.DIR_PRE_UP
            #                     if percentFlow==Constants.DIR_UP:
            #                             res = Constants.DIR_PRE_UP
            #
            #     elif percent <= 15:
            #         if med >= 0:
            #             if absmed > std:
            #                 res = Constants.DIR_UP
            #             else:
            #                 # res = Constants.DIR_PRE_UP
            #                 # res = self.determine_Direction_percent_Flow(direction, percentFlow)
            #                 res = self.determineMedMomentFlow(medMoment, absMedMoment, stdMoment, direction)
            #         if med < 0:
            #             if absmed > std:
            #                 res = Constants.DIR_DOWN
            #             else:
            #                 # res = Constants.DIR_PRE_DOWN
            #                 if direction == Constants.DIR_DOWN or direction == Constants.DIR_PRE_DOWN:
            #                     res = Constants.DIR_DOWN
            #                 else:
            #                     if percentFlow == Constants.DIR_UP:
            #                         res = Constants.DIR_PRE_UP
            #                     else:
            #                         res = Constants.DIR_PRE_DOWN
            #
            # if fcst == Constants.IND_REL_FCST_UP_INV_REL:
            #     if percent >= 0 and percent < 95:
            #         if med > 0:
            #             if absmed > std:
            #                 res = Constants.DIR_UP
            #             else:
            #                 # res = Constants.DIR_PRE_UP
            #                 # res = self.determine_Direction_percent_Flow(direction, percentFlow)
            #                 res = self.determineMedMomentFlow(medMoment, absMedMoment, stdMoment, direction)
            #         elif med < 0:
            #             if absmed > std:
            #                 res = Constants.DIR_DOWN
            #             else:
            #                 # res = Constants.DIR_PRE_DOWN
            #                 # res = self.determine_Direction_percent_Flow(direction, percentFlow)
            #                 res = self.determineMedMomentFlow(medMoment, absMedMoment, stdMoment, direction)
            #     elif percent >= 90:
            #         if med < 0:
            #             if absmed > std:
            #                 res = Constants.DIR_DOWN
            #             else:
            #                 # res = Constants.DIR_PRE_DOWN
            #                 # res = self.determine_Direction_percent_Flow(direction, percentFlow)
            #                 res = self.determineMedMomentFlow(medMoment, absMedMoment, stdMoment, direction)
            #         if med > 0:
            #             if absmed > std:
            #                 res = Constants.DIR_UP
            #             else:
            #                 # fix se anade direction
            #                 if direction == Constants.DIR_UP or direction == Constants.DIR_PRE_UP:
            #                     res = Constants.DIR_UP
            #                 else:
            #                     if percentFlow == Constants.DIR_UP:
            #                         res = Constants.DIR_PRE_UP
            #                     else:
            #                         res = Constants.DIR_PRE_DOWN

        except Exception as error:
            print("Error getProMEDSTD_INI ", error)
        return res

    def getPROBMEDSTD_OKFlow(self, results, active):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            week = results[Constants.WEEK_FLOW]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_med_abs = results[Constants.WEEK_FLOW_MED]
            week_std = results[Constants.WEEK_FLOW_STD]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            if prevPercent is not None:
                prevPercent = float(prevPercent)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]

            if med == 0:
                if direction == Constants.DIR_UP:
                    med = 1
                elif direction == Constants.DIR_DOWN:
                    med = -1
            percentFlow = Constants.DIR_WAIT
            if percent > prevPercent:
                percentFlow = Constants.DIR_UP
            else:
                # baja
                percentFlow = Constants.DIR_DOWN
            diftimeOpen = self.getDifTimeFromOpen(results)
            if int(diftimeOpen) <= 10:
                if fcst == Constants.IND_REL_FCST_PRE_UP or fcst == Constants.IND_REL_FCST_UP:
                    if percent >= 0 and percent < 95:
                        if medMoment > 0:
                            if absMedMoment > stdMoment:
                                res = Constants.DIR_UP
                            else:
                                res = Constants.DIR_PRE_UP
                        else:
                            if absMedMoment > stdMoment:
                                # verificacion
                                if percentFlow == Constants.DIR_DOWN:
                                    res = Constants.DIR_DOWN
                                elif percentFlow == Constants.DIR_UP:
                                    res = Constants.DIR_PRE_UP
                                else:
                                    res = Constants.DIR_DOWN

                            else:
                                # contradiccion revisar week
                                if week_med > 0:
                                    # sube
                                    if week_med_abs > week_std:
                                        res = Constants.DIR_UP
                                    else:
                                        res = Constants.DIR_PRE_UP
                                else:
                                    # baja
                                    res = Constants.DIR_PRE_DOWN
                    elif percent >= 95:
                        if medMoment < 0:
                            if absMedMoment > stdMoment:
                                res = Constants.DIR_DOWN
                            else:
                                res = Constants.DIR_PRE_DOWN
                        if medMoment >= 0:
                            if absMedMoment > stdMoment:
                                res = Constants.DIR_UP
                            else:
                                # fix se anade direction
                                if direction == Constants.DIR_UP or direction == Constants.DIR_PRE_UP:
                                    res = Constants.DIR_UP
                                else:
                                    if percentFlow == Constants.DIR_UP:
                                        res = Constants.DIR_PRE_UP
                                    else:
                                        res = Constants.DIR_PRE_DOWN

                if fcst == Constants.IND_REL_FCST_DOWN_INV_REL:
                    if percent > 10 and percent <= 100:
                        if medMoment > 0:
                            if absMedMoment > stdMoment:
                                res = Constants.DIR_UP
                            else:
                                res = Constants.DIR_PRE_UP
                        else:
                            if absMedMoment > stdMoment:
                                res = Constants.DIR_DOWN
                            else:
                                res = Constants.DIR_PRE_DOWN
                    elif percent <= 10:
                        if medMoment >= 0:
                            if absMedMoment > stdMoment:
                                res = Constants.DIR_UP
                            else:
                                res = Constants.DIR_PRE_UP
                        if medMoment < 0:
                            if absMedMoment > stdMoment:
                                res = Constants.DIR_DOWN
                            else:
                                if direction == Constants.DIR_DOWN or direction == Constants.DIR_PRE_DOWN:
                                    res = Constants.DIR_DOWN
                                else:
                                    if percentFlow == Constants.DIR_UP:
                                        res = Constants.DIR_PRE_UP
                                    else:
                                        res = Constants.DIR_PRE_DOWN

                if fcst == Constants.IND_REL_FCST_PRE_DOWN or fcst == Constants.IND_REL_FCST_DOWN:
                    if percent >= 10 and percent <= 100:
                        if medMoment < 0:
                            if absMedMoment > stdMoment:
                                res = Constants.DIR_DOWN
                            else:
                                res = Constants.DIR_PRE_DOWN
                        elif medMoment > 0:
                            if absMedMoment >= stdMoment:
                                # verificacion
                                if percentFlow == Constants.DIR_UP:
                                    res = Constants.DIR_UP
                                elif percentFlow == Constants.DIR_DOWN:
                                    res = Constants.DIR_PRE_DOWN
                                else:
                                    res = Constants.DIR_UP
                            else:
                                # res = Constants.DIR_PRE_UP
                                # contradiccion revisar week
                                if week_med < 0:
                                    # sube
                                    if week_med_abs > week_std:
                                        res = Constants.DIR_DOWN
                                    else:
                                        res = Constants.DIR_PRE_DOWN
                                else:
                                    # baja
                                    res = Constants.DIR_PRE_UP
                            # if percentFlow==Constants.DIR_UP:
                            #     if absMedMoment >= stdMoment:
                            #         res = Constants.DIR_UP
                            #     else:
                            #         res = Constants.DIR_PRE_UP
                            # elif percentFlow==Constants.DIR_DOWN:
                            #     # baja
                            #     res = Constants.DIR_PRE_DOWN
                            # else:
                            #     if absMedMoment >= stdMoment:
                            #         res = Constants.DIR_UP
                            #     else:
                            #         res = Constants.DIR_PRE_UP
                    elif percent <= 10:
                        if medMoment >= 0:
                            if absMedMoment > stdMoment:
                                res = Constants.DIR_UP
                            else:
                                res = Constants.DIR_PRE_UP
                        if medMoment < 0:
                            if absMedMoment > stdMoment:
                                res = Constants.DIR_DOWN
                            else:
                                # res = Constants.DIR_PRE_DOWN
                                if direction == Constants.DIR_DOWN or direction == Constants.DIR_PRE_DOWN:
                                    res = Constants.DIR_DOWN
                                else:
                                    if percentFlow == Constants.DIR_UP:
                                        res = Constants.DIR_PRE_UP
                                    else:
                                        res = Constants.DIR_PRE_DOWN

                if fcst == Constants.IND_REL_FCST_UP_INV_REL:
                    if percent >= 0 and percent < 95:
                        if medMoment > 0:
                            if absMedMoment > stdMoment:
                                res = Constants.DIR_UP
                            else:
                                res = Constants.DIR_PRE_UP
                        elif medMoment < 0:
                            if absMedMoment > stdMoment:
                                res = Constants.DIR_DOWN
                            else:
                                res = Constants.DIR_PRE_DOWN
                    elif percent >= 90:
                        if medMoment < 0:
                            if absMedMoment > stdMoment:
                                res = Constants.DIR_DOWN
                            else:
                                res = Constants.DIR_PRE_DOWN
                        if medMoment > 0:
                            if absMedMoment > stdMoment:
                                res = Constants.DIR_UP
                            else:
                                # fix se anade direction
                                if direction == Constants.DIR_UP or direction == Constants.DIR_PRE_UP:
                                    res = Constants.DIR_UP
                                else:
                                    if percentFlow == Constants.DIR_UP:
                                        res = Constants.DIR_PRE_UP
                                    else:
                                        res = Constants.DIR_PRE_DOWN
            else:
                if fcst == Constants.IND_REL_FCST_PRE_UP or fcst == Constants.IND_REL_FCST_UP:
                    if percent >= 0 and percent < 95:
                        if med > 0:
                            if absmed > std:
                                res = Constants.DIR_UP
                            else:
                                res = Constants.DIR_PRE_UP
                        else:
                            if absmed > std:
                                res = Constants.DIR_DOWN
                            else:
                                # contradiccion revisar week
                                if week_med > 0:
                                    # sube
                                    if week_med_abs > week_std:
                                        res = Constants.DIR_UP
                                    else:
                                        res = Constants.DIR_PRE_UP
                                else:
                                    # baja
                                    res = Constants.DIR_PRE_DOWN

                    elif percent >= 95:
                        if med < 0:
                            if absmed > std:
                                res = Constants.DIR_DOWN
                            else:
                                res = Constants.DIR_PRE_DOWN
                        if med >= 0:
                            if absmed > std:
                                res = Constants.DIR_UP
                            else:
                                # fix se ande direction
                                if direction == Constants.DIR_UP or direction == Constants.DIR_PRE_UP:
                                    res = Constants.DIR_UP
                                else:
                                    if percentFlow == Constants.DIR_UP:
                                        res = Constants.DIR_PRE_UP
                                    else:
                                        res = Constants.DIR_PRE_DOWN

                if fcst == Constants.IND_REL_FCST_DOWN_INV_REL:
                    if percent > 10 and percent <= 100:
                        if med > 0:
                            if absmed > std:
                                res = Constants.DIR_UP
                            else:
                                res = Constants.DIR_PRE_UP
                        else:
                            if absmed > std:
                                res = Constants.DIR_DOWN
                            else:
                                res = Constants.DIR_PRE_DOWN
                    elif percent <= 10:
                        if med >= 0:
                            if absmed > std:
                                res = Constants.DIR_UP
                            else:
                                res = Constants.DIR_PRE_UP
                        if med < 0:
                            if absmed > std:
                                res = Constants.DIR_DOWN
                            else:
                                # res = Constants.DIR_PRE_UP
                                # fix se anade direction
                                if direction == Constants.DIR_DOWN or direction == Constants.DIR_PRE_DOWN:
                                    res = Constants.DIR_DOWN
                                else:
                                    if percentFlow == Constants.DIR_UP:
                                        res = Constants.DIR_PRE_UP
                                    else:
                                        res = Constants.DIR_PRE_DOWN

                if fcst == Constants.IND_REL_FCST_PRE_DOWN or fcst == Constants.IND_REL_FCST_DOWN:
                    if percent > 10 and percent <= 100:
                        if med < 0:
                            if absmed > std:
                                res = Constants.DIR_DOWN
                            else:
                                res = Constants.DIR_PRE_DOWN
                        elif med > 0:
                            if absmed >= std:
                                res = Constants.DIR_UP
                            else:
                                # contradiccion revisar week
                                if week_med < 0:
                                    # baja
                                    if week_med_abs > week_std:
                                        res = Constants.DIR_DOWN
                                    else:
                                        res = Constants.DIR_PRE_DOWN
                                else:
                                    # sube
                                    res = Constants.DIR_PRE_UP

                    elif percent > 0 and percent <= 10:
                        if med > 0:
                            if absmed > std:
                                res = Constants.DIR_UP
                            else:
                                res = Constants.DIR_PRE_UP
                        elif med < 0:
                            if absmed > std:
                                res = Constants.DIR_DOWN
                            else:
                                if direction == Constants.DIR_DOWN or direction == Constants.DIR_PRE_DOWN:
                                    res = Constants.DIR_DOWN
                                else:
                                    if percentFlow == Constants.DIR_UP:
                                        res = Constants.DIR_PRE_UP
                                    else:
                                        res = Constants.DIR_PRE_DOWN
                    elif percent == 0:
                        if medMoment >= 0:
                            if absMedMoment > stdMoment:
                                res = Constants.DIR_UP
                            else:
                                res = Constants.DIR_PRE_UP
                        if medMoment < 0:
                            if absMedMoment > stdMoment:
                                res = Constants.DIR_DOWN
                            else:
                                # res = Constants.DIR_PRE_DOWN
                                if direction == Constants.DIR_DOWN or direction == Constants.DIR_PRE_DOWN:
                                    res = Constants.DIR_DOWN
                                else:
                                    if percentFlow == Constants.DIR_UP:
                                        res = Constants.DIR_PRE_UP
                                    else:
                                        res = Constants.DIR_PRE_DOWN

                if fcst == Constants.IND_REL_FCST_UP_INV_REL:
                    if percent >= 0 and percent < 95:
                        if med > 0:
                            if absmed > std:
                                res = Constants.DIR_UP
                            else:
                                res = Constants.DIR_PRE_UP
                        elif med < 0:
                            if absmed > std:
                                res = Constants.DIR_DOWN
                            else:
                                res = Constants.DIR_PRE_DOWN
                    elif percent >= 95:
                        if med < 0:
                            if absmed > std:
                                res = Constants.DIR_DOWN
                            else:
                                res = Constants.DIR_PRE_DOWN
                        if med > 0:
                            if absmed > std:
                                res = Constants.DIR_UP
                            else:

                                # fix se anade direction
                                if direction == Constants.DIR_UP or direction == Constants.DIR_PRE_UP:
                                    res = Constants.DIR_UP
                                else:
                                    if percentFlow == Constants.DIR_UP:
                                        res = Constants.DIR_PRE_UP
                                    else:
                                        res = Constants.DIR_PRE_DOWN
        except Exception as error:
            print("Error getPROBMEDSTD_OKFlow ", error)
        return res

    def getProMEDSTD_END(self, results):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            week = results[Constants.WEEK_FLOW]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_med_abs = results[Constants.WEEK_FLOW_MED]
            week_std = results[Constants.WEEK_FLOW_STD]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            if prevPercent is not None:
                prevPercent = float(prevPercent)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]
            # if med == 0:
            #     if direction == Constants.DIR_UP:
            #         med = 1
            #     elif direction == Constants.DIR_DOWN:
            #         med = -1
            percentFlow = Constants.DIR_WAIT
            if percent > prevPercent:
                percentFlow = Constants.DIR_UP
            else:
                # baja
                percentFlow = Constants.DIR_DOWN
            # CALCULOS final del dia
            if fcst == Constants.IND_REL_FCST_PRE_UP or fcst == Constants.IND_REL_FCST_UP:
                if percent >= 0 and percent < 95:
                    if medMoment > 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_UP
                        else:
                            res = Constants.DIR_PRE_UP
                    elif medMoment <= 0:
                        if absMedMoment > stdMoment and absMedMoment > 1:
                            res = Constants.DIR_DOWN
                        else:
                            # contradiccion revisar week
                            if week_med > 0:
                                # sube
                                if week_med_abs > week_std:
                                    res = Constants.DIR_UP
                                else:
                                    res = Constants.DIR_PRE_UP
                            else:
                                # baja
                                res = Constants.DIR_PRE_DOWN

                elif percent >= 95:
                    if medMoment < 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_DOWN
                        else:
                            res = Constants.DIR_PRE_DOWN
                    if medMoment >= 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_UP
                        else:
                            res = Constants.DIR_PRE_DOWN

            if fcst == Constants.IND_REL_FCST_DOWN_INV_REL:
                if percent > 10 and percent <= 100:
                    if medMoment > 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_UP
                        else:
                            res = Constants.DIR_PRE_UP
                    else:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_DOWN
                        else:
                            res = Constants.DIR_PRE_DOWN
                elif percent <= 10:
                    if medMoment >= 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_UP
                        else:
                            res = Constants.DIR_PRE_UP
                    if medMoment < 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_DOWN
                        else:
                            res = Constants.DIR_PRE_UP

            if fcst == Constants.IND_REL_FCST_PRE_DOWN or fcst == Constants.IND_REL_FCST_DOWN:
                if percent > 20 and percent <= 100:
                    if medMoment < 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_DOWN
                        else:
                            res = Constants.DIR_PRE_DOWN
                    elif medMoment > 0:
                        if absMedMoment >= stdMoment and absMedMoment > 1:
                            res = Constants.DIR_UP
                        else:
                            # contradiccion revisar week
                            if week_med < 0:
                                # baja
                                if week_med_abs > week_std:
                                    res = Constants.DIR_DOWN
                                else:
                                    res = Constants.DIR_PRE_DOWN
                            else:
                                # sube
                                res = Constants.DIR_PRE_UP

                elif percent > 0 and percent <= 20:
                    if medMoment > 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_UP
                        else:
                            res = Constants.DIR_PRE_UP
                    elif medMoment < 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_DOWN
                        else:
                            res = Constants.DIR_PRE_UP

                elif percent == 0:
                    if medMoment >= 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_UP
                        else:
                            res = Constants.DIR_PRE_UP
                    if medMoment < 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_DOWN
                        else:
                            res = Constants.DIR_PRE_UP

            if fcst == Constants.IND_REL_FCST_UP_INV_REL:
                if percent >= 0 and percent < 95:
                    if medMoment > 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_UP
                        else:
                            res = Constants.DIR_PRE_UP
                    elif medMoment < 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_DOWN
                        else:
                            res = Constants.DIR_PRE_DOWN
                elif percent >= 95:
                    if medMoment < 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_DOWN
                        else:
                            res = Constants.DIR_PRE_DOWN
                    if medMoment > 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_UP
                        else:

                            res = Constants.DIR_PRE_DOWN
        except Exception as error:
            print("Error getProMEDSTD_END ", error)
        return res

    def getProMEDSTD_END_01(self, results):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            week = results[Constants.WEEK_FLOW]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_med_abs = results[Constants.WEEK_FLOW_MED]
            week_std = results[Constants.WEEK_FLOW_STD]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            if prevPercent is not None:
                prevPercent = float(prevPercent)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]
            # if med == 0:
            #     if direction == Constants.DIR_UP:
            #         med = 1
            #     elif direction == Constants.DIR_DOWN:
            #         med = -1
            percentFlow = Constants.DIR_WAIT
            if percent > prevPercent:
                percentFlow = Constants.DIR_UP
            else:
                # baja
                percentFlow = Constants.DIR_DOWN
            # CALCULOS final del dia
            if fcst == Constants.IND_REL_FCST_PRE_UP or fcst == Constants.IND_REL_FCST_UP:
                if percent >= 0 and percent < 95:
                    if medMoment > 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_UP
                        else:
                            res = Constants.DIR_PRE_UP
                    elif medMoment <= 0:
                        if absMedMoment > stdMoment:  # and absMedMoment >1:
                            res = Constants.DIR_DOWN
                        else:
                            # contradiccion revisar week
                            if week_med > 0:
                                # sube
                                if week_med_abs > week_std:
                                    res = Constants.DIR_UP
                                else:
                                    res = Constants.DIR_PRE_UP
                            else:
                                # baja
                                res = Constants.DIR_PRE_DOWN

                elif percent >= 95:
                    if medMoment < 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_DOWN
                        else:
                            res = Constants.DIR_PRE_DOWN
                    if medMoment >= 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_UP
                        else:
                            res = Constants.DIR_PRE_DOWN

            if fcst == Constants.IND_REL_FCST_DOWN_INV_REL:
                if percent > 10 and percent <= 100:
                    if medMoment > 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_UP
                        else:
                            res = Constants.DIR_PRE_UP
                    else:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_DOWN
                        else:
                            res = Constants.DIR_PRE_DOWN
                elif percent <= 10:
                    if medMoment >= 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_UP
                        else:
                            res = Constants.DIR_PRE_UP
                    if medMoment < 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_DOWN
                        else:
                            res = Constants.DIR_PRE_UP

            if fcst == Constants.IND_REL_FCST_PRE_DOWN or fcst == Constants.IND_REL_FCST_DOWN:
                if percent > 20 and percent <= 100:
                    if medMoment < 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_DOWN
                        else:
                            res = Constants.DIR_PRE_DOWN
                    elif medMoment > 0:
                        if absMedMoment >= stdMoment:  # and absMedMoment >1:
                            res = Constants.DIR_UP
                        else:
                            # contradiccion revisar week
                            if week_med < 0:
                                # baja
                                if week_med_abs > week_std:
                                    res = Constants.DIR_DOWN
                                else:
                                    res = Constants.DIR_PRE_DOWN
                            else:
                                # sube
                                res = Constants.DIR_PRE_UP

                elif percent > 0 and percent <= 20:
                    if medMoment > 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_UP
                        else:
                            res = Constants.DIR_PRE_UP
                    elif medMoment < 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_DOWN
                        else:
                            res = Constants.DIR_PRE_UP

                elif percent == 0:
                    if medMoment >= 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_UP
                        else:
                            res = Constants.DIR_PRE_UP
                    if medMoment < 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_DOWN
                        else:
                            res = Constants.DIR_PRE_UP

            if fcst == Constants.IND_REL_FCST_UP_INV_REL:
                if percent >= 0 and percent < 95:
                    if medMoment > 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_UP
                        else:
                            res = Constants.DIR_PRE_UP
                    elif medMoment < 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_DOWN
                        else:
                            res = Constants.DIR_PRE_DOWN
                elif percent >= 95:
                    if medMoment < 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_DOWN
                        else:
                            res = Constants.DIR_PRE_DOWN
                    if medMoment > 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_UP
                        else:

                            res = Constants.DIR_PRE_DOWN
        except Exception as error:
            print("Error getProMEDSTD_END 01", error)
        return res

    def getProMEDSTD_END_02(self, results):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            week = results[Constants.WEEK_FLOW]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_med_abs = results[Constants.WEEK_FLOW_MED]
            week_std = results[Constants.WEEK_FLOW_STD]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]

            if prevPercent is not None:
                prevPercent = float(prevPercent)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]
            # if med == 0:
            #     if direction == Constants.DIR_UP:
            #         med = 1
            #     elif direction == Constants.DIR_DOWN:
            #         med = -1
            percentFlow = Constants.DIR_WAIT
            if percent > prevPercent:
                percentFlow = Constants.DIR_UP
            else:
                # baja
                percentFlow = Constants.DIR_DOWN
            # CALCULOS final del dia
            if fcst == Constants.IND_REL_FCST_PRE_UP or fcst == Constants.IND_REL_FCST_UP:
                if percent >= 0 and percent < 95:
                    # res = Constants.DIR_UP
                    if abs(medFcst) > stdFcst:
                        res = Constants.DIR_UP
                    else:
                        if med > 0:
                            if absmed > std:
                                res = Constants.DIR_UP
                            else:
                                res = Constants.DIR_PRE_UP
                        elif med < 0:
                            if absmed > std:
                                res = Constants.DIR_DOWN
                            else:
                                res = Constants.DIR_PRE_DOWN
                elif percent >= 95:
                    if week_med < 0:
                        if week_med_abs > week_std:
                            res = Constants.DIR_DOWN
                        else:
                            res = Constants.DIR_PRE_DOWN
                    if week_med >= 0:
                        if week_med_abs > week_std:
                            res = Constants.DIR_UP
                        else:
                            res = Constants.DIR_PRE_UP

            if fcst == Constants.IND_REL_FCST_DOWN_INV_REL:
                if percent > 10 and percent <= 100:
                    res = Constants.DIR_DOWN
                elif percent <= 10:
                    if medMoment >= 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_UP
                        else:
                            res = Constants.DIR_PRE_UP
                    if medMoment < 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_DOWN
                        else:
                            res = Constants.DIR_PRE_DOWN

            if fcst == Constants.IND_REL_FCST_PRE_DOWN or fcst == Constants.IND_REL_FCST_DOWN:
                if percent > 20 and percent <= 100:
                    if abs(medFcst) > stdFcst:
                        res = Constants.DIR_DOWN
                    else:
                        if med > 0:
                            if absmed > std:
                                res = Constants.DIR_UP
                            else:
                                res = Constants.DIR_PRE_UP
                        elif med < 0:
                            if absmed > std:
                                res = Constants.DIR_DOWN
                            else:
                                res = Constants.DIR_PRE_DOWN

                elif percent > 0 and percent <= 20:
                    if week_med > 0:
                        if week_med_abs > week_std:
                            res = Constants.DIR_UP
                        else:
                            res = Constants.DIR_PRE_UP
                    elif week_med < 0:
                        if week_med_abs > week_std:
                            res = Constants.DIR_DOWN
                        else:
                            res = Constants.DIR_PRE_DOWN

                elif percent == 0:
                    if medMoment >= 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_UP
                        else:
                            res = Constants.DIR_PRE_UP
                    if medMoment < 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_DOWN
                        else:
                            res = Constants.DIR_PRE_DOWN

            if fcst == Constants.IND_REL_FCST_UP_INV_REL:
                if percent >= 0 and percent < 95:
                    res = Constants.DIR_UP
                elif percent >= 95:
                    if medMoment < 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_DOWN
                        else:
                            res = Constants.DIR_PRE_DOWN
                    if medMoment > 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_UP
                        else:

                            res = Constants.DIR_PRE_UP
        except Exception as error:
            print("Error getProMEDSTD_END 02", error)
        return res

    def getProMEDSTD_END_03(self, results):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            week = results[Constants.WEEK_FLOW]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_med_abs = results[Constants.WEEK_FLOW_MED]
            week_std = results[Constants.WEEK_FLOW_STD]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            medDay = results[Constants.INDICATOR_MED_DAY]
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]

            if prevPercent is not None:
                prevPercent = float(prevPercent)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]
            # if med == 0:
            #     if direction == Constants.DIR_UP:
            #         med = 1
            #     elif direction == Constants.DIR_DOWN:
            #         med = -1
            percentFlow = Constants.DIR_WAIT
            if percent > prevPercent:
                percentFlow = Constants.DIR_UP
            else:
                # baja
                percentFlow = Constants.DIR_DOWN
            # CALCULOS final del dia
            if fcst == Constants.IND_REL_FCST_PRE_UP or fcst == Constants.IND_REL_FCST_UP:
                if percent >= 0 and percent < 80:
                    # res = Constants.DIR_UP
                    if abs(medFcst) > stdFcst:
                        res = Constants.DIR_UP
                    else:
                        if med > 0:
                            if absmed > std:
                                res = Constants.DIR_UP
                            else:
                                res = Constants.DIR_PRE_UP
                        elif med < 0:
                            if absmed > std:
                                res = Constants.DIR_DOWN
                            else:
                                res = Constants.DIR_PRE_DOWN
                elif percent >= 80 and percent < 100:
                    # if week_med < 0:
                    #     if week_med_abs > week_std:
                    #         res = Constants.DIR_DOWN
                    #     else:
                    #         res = Constants.DIR_PRE_DOWN
                    # if week_med >= 0:
                    #     if week_med_abs > week_std:
                    #         res = Constants.DIR_UP
                    #     else:
                    #         res = Constants.DIR_PRE_UP
                    if med > medDay:
                        # sube
                        res = Constants.DIR_UP
                    else:
                        res = Constants.DIR_DOWN


                elif percent == 100:
                    if medMoment >= 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_UP
                        else:
                            res = Constants.DIR_PRE_UP
                    if medMoment < 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_DOWN
                        else:
                            res = Constants.DIR_PRE_DOWN

            if fcst == Constants.IND_REL_FCST_DOWN_INV_REL:
                if percent > 10 and percent <= 100:
                    res = Constants.DIR_DOWN
                elif percent <= 10:
                    if medMoment >= 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_UP
                        else:
                            res = Constants.DIR_PRE_UP
                    if medMoment < 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_DOWN
                        else:
                            res = Constants.DIR_PRE_DOWN

            if fcst == Constants.IND_REL_FCST_PRE_DOWN or fcst == Constants.IND_REL_FCST_DOWN:
                if percent > 20 and percent <= 100:
                    if abs(medFcst) > stdFcst:
                        res = Constants.DIR_DOWN
                    else:
                        if med > 0:
                            if absmed > std:
                                res = Constants.DIR_UP
                            else:
                                res = Constants.DIR_PRE_UP
                        elif med < 0:
                            if absmed > std:
                                res = Constants.DIR_DOWN
                            else:
                                res = Constants.DIR_PRE_DOWN

                elif percent > 0 and percent <= 20:
                    # if week_med > 0:
                    #     if week_med_abs > week_std:
                    #         res = Constants.DIR_UP
                    #     else:
                    #         res = Constants.DIR_PRE_UP
                    # elif week_med < 0:
                    #     if week_med_abs > week_std:
                    #         res = Constants.DIR_DOWN
                    #     else:
                    #         res = Constants.DIR_PRE_DOWN
                    if med > medDay:
                        # sube
                        res = Constants.DIR_UP
                    else:
                        res = Constants.DIR_DOWN

                elif percent == 0:
                    if medMoment >= 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_UP
                        else:
                            res = Constants.DIR_PRE_UP
                    if medMoment < 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_DOWN
                        else:
                            res = Constants.DIR_PRE_DOWN

            if fcst == Constants.IND_REL_FCST_UP_INV_REL:
                if percent >= 0 and percent < 95:
                    res = Constants.DIR_UP
                elif percent >= 95:
                    if medMoment < 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_DOWN
                        else:
                            res = Constants.DIR_PRE_DOWN
                    if medMoment > 0:
                        if absMedMoment > stdMoment:
                            res = Constants.DIR_UP
                        else:

                            res = Constants.DIR_PRE_UP
        except Exception as error:
            print("Error getProMEDSTD_END 03", error)
        return res

    def getProMEDSTD_END_04(self, results):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            week = results[Constants.WEEK_FLOW]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_med_abs = results[Constants.WEEK_FLOW_MED]
            week_std = results[Constants.WEEK_FLOW_STD]
            weekdiff = abs(week_med_abs - week_std)
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            medDay = results[Constants.INDICATOR_MED_DAY]
            absMedDay = abs(medDay)
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]

            # valores del dia
            numUP = results[Constants.IND_NUM_UP]
            numDOWN = results[Constants.IND_NUM_DOWN]

            sumUP = results[Constants.IND_SUM_UP]
            sumDOWN = results[Constants.IND_SUM_DOWN]

            sumDay = int(sumUP) - int(sumDOWN)

            weekdiffTendenceValue = 1
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]

            if prevPercent is not None:
                prevPercent = float(prevPercent)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]
            # if med == 0:
            #     if direction == Constants.DIR_UP:
            #         med = 1
            #     elif direction == Constants.DIR_DOWN:
            #         med = -1
            percentFlow = Constants.DIR_WAIT
            if percent > prevPercent:
                percentFlow = Constants.DIR_UP
            else:
                # baja
                percentFlow = Constants.DIR_DOWN
            # CALCULOS final del dia

            # CALCULOS final del dia
            if fcst == Constants.IND_REL_FCST_PRE_UP or fcst == Constants.IND_REL_FCST_UP \
                    or fcst == Constants.IND_REL_FCST_DOWN_INV_REL:
                if percent >= 0 and percent < 80:
                    if sumDay > 0:
                        # ha subido entonces bajara
                        if percent > 10:
                            # verificar si es una tendencia week
                            if weekdiff > 0 and weekdiff > weekdiffTendenceValue:
                                # seguira subiendo
                                res = Constants.DIR_UP
                            else:
                                # res = res = Constants.DIR_DOWN
                                if absMedDay > stdDay:
                                    if medDay > 0:
                                        res = Constants.DIR_UP
                                    else:
                                        res = Constants.DIR_DOWN
                                else:
                                    if medDay > 0:
                                        # sube
                                        res = Constants.DIR_UP
                                    else:
                                        res = Constants.DIR_DOWN
                        else:

                            if absMedDay > stdDay:
                                if medDay > 0:
                                    res = Constants.DIR_UP
                                else:
                                    res = Constants.DIR_DOWN
                            else:
                                if medDay > 0:
                                    # sube
                                    res = Constants.DIR_UP
                                else:
                                    res = Constants.DIR_DOWN
                    else:
                        # bajo mucho subira
                        if percent <= 90:
                            res = res = Constants.DIR_UP
                        else:
                            if absMedDay > stdDay:
                                if medDay > 0:
                                    res = Constants.DIR_UP
                                else:
                                    res = Constants.DIR_DOWN
                            else:
                                if med > medDay:
                                    # sube
                                    res = Constants.DIR_UP
                                else:
                                    res = Constants.DIR_DOWN
                elif percent >= 80 and percent < 90:
                    # revisar si esta en tendencia de subida.
                    isTendence = False
                    if week_med_abs > week_std:
                        if weekdiff > 1.2:
                            isTendence = True

                    if isTendence:
                        res = Constants.DIR_UP
                    else:
                        if sumDay > 0:
                            # ha subido entonces bajara
                            if percent > 10:
                                res = res = Constants.DIR_DOWN
                            else:
                                if absMedDay > stdDay:
                                    if medDay > 0:
                                        res = Constants.DIR_UP
                                    else:
                                        res = Constants.DIR_DOWN
                                else:
                                    if med > medDay:
                                        # sube
                                        res = Constants.DIR_UP
                                    else:
                                        res = Constants.DIR_DOWN
                        else:
                            # bajo mucho subira
                            if percent <= 90:
                                res = res = Constants.DIR_UP
                            else:
                                if absMedDay > stdDay:
                                    if medDay > 0:
                                        res = Constants.DIR_UP
                                    else:
                                        res = Constants.DIR_DOWN
                                else:
                                    if med > medDay:
                                        # sube
                                        res = Constants.DIR_UP
                                    else:
                                        res = Constants.DIR_DOWN

                elif percent >= 90 and percent <= 100:
                    # revisar si esta en tendencia de subida.
                    isTendence = False
                    if week_med_abs > week_std:
                        if weekdiff > 1.2:
                            isTendence = True

                    if isTendence:
                        res = Constants.DIR_UP
                    else:
                        if medMoment >= 0:
                            if absMedMoment > stdMoment:
                                res = Constants.DIR_UP
                            else:
                                res = Constants.DIR_PRE_UP
                        if medMoment < 0:
                            if absMedMoment > stdMoment:
                                res = Constants.DIR_DOWN
                            else:
                                res = Constants.DIR_PRE_DOWN

            # if fcst == Constants.IND_REL_FCST_DOWN_INV_REL:
            #     if percent > 10 and percent <= 100:
            #         res = Constants.DIR_DOWN
            #     elif percent <= 10:
            #         if medMoment >= 0:
            #             if absMedMoment > stdMoment:
            #                 res = Constants.DIR_UP
            #             else:
            #                 res = Constants.DIR_PRE_UP
            #         if medMoment < 0:
            #             if absMedMoment > stdMoment:
            #                 res = Constants.DIR_DOWN
            #             else:
            #                 res = Constants.DIR_PRE_DOWN

            if fcst == Constants.IND_REL_FCST_PRE_DOWN or fcst == Constants.IND_REL_FCST_DOWN \
                    or fcst == Constants.IND_REL_FCST_UP_INV_REL:
                if percent > 20 and percent <= 100:
                    # if abs(medFcst) > stdFcst:
                    #     res = Constants.DIR_DOWN
                    # else:
                    #     if med > 0:
                    #         if absmed > std:
                    #             res = Constants.DIR_UP
                    #         else:
                    #             res = Constants.DIR_PRE_UP
                    #     elif med < 0:
                    #         if absmed > std:
                    #             res = Constants.DIR_DOWN
                    #         else:
                    #             res = Constants.DIR_PRE_DOWN
                    if sumDay > 0:
                        # ha subido entonces bajara
                        if percent > 10:
                            res = res = Constants.DIR_DOWN
                        else:
                            # no estamos seguros evaluamos otro factor
                            if absMedDay > stdDay:
                                if medDay > 0:
                                    res = Constants.DIR_UP
                                else:
                                    res = Constants.DIR_DOWN
                            else:
                                if med > medDay:
                                    # sube
                                    res = Constants.DIR_UP
                                else:
                                    res = Constants.DIR_DOWN
                    else:
                        # bajo mucho subira
                        # ha subido entonces bajara
                        if percent <= 90:
                            res = res = Constants.DIR_UP
                        else:
                            # no estamos seguros evaluamos otro factor
                            if absMedDay > stdDay:
                                if medDay > 0:
                                    res = Constants.DIR_UP
                                else:
                                    res = Constants.DIR_DOWN
                            else:
                                if med > medDay:
                                    # sube
                                    res = Constants.DIR_UP
                                else:
                                    res = Constants.DIR_DOWN

                elif percent > 10 and percent <= 20:
                    isTendence = False
                    if week_med_abs > week_std:
                        if weekdiff > 0 and weekdiff > weekdiffTendenceValue:
                            isTendence = True

                    if isTendence:
                        res = Constants.DIR_DOWN
                    else:

                        if sumDay > 0:
                            # ha subido entonces bajara
                            if percent > 10:
                                res = res = Constants.DIR_DOWN
                            else:
                                if absMedDay > stdDay:
                                    if medDay > 0:
                                        res = Constants.DIR_UP
                                    else:
                                        res = Constants.DIR_DOWN
                                else:
                                    if absMedDay > 1:
                                        if medMoment >= 0:
                                            if absMedMoment > stdMoment:
                                                # sube
                                                res = Constants.DIR_UP
                                            else:
                                                res = Constants.DIR_PRE_UP
                                        elif medMoment < 0:
                                            if absMedMoment > stdMoment:
                                                res = Constants.DIR_DOWN
                                            else:
                                                res = Constants.DIR_PRE_DOWN
                                    else:
                                        if med > medDay:
                                            # sube
                                            res = Constants.DIR_UP
                                        else:
                                            res = Constants.DIR_DOWN
                        else:
                            # bajo mucho subira
                            # ha subido entonces bajara
                            if percent <= 90:
                                res = res = Constants.DIR_UP
                            else:
                                if absMedDay > stdDay:
                                    if medDay > 0:
                                        res = Constants.DIR_UP
                                    else:
                                        res = Constants.DIR_DOWN
                                else:
                                    if absMedDay > 1:
                                        if medMoment >= 0:
                                            if absMedMoment > stdMoment:
                                                # sube
                                                res = Constants.DIR_UP
                                            else:
                                                res = Constants.DIR_PRE_UP
                                        elif medMoment < 0:
                                            if absMedMoment > stdMoment:
                                                res = Constants.DIR_DOWN
                                            else:
                                                res = Constants.DIR_PRE_DOWN
                                    else:
                                        if med > medDay:
                                            # sube
                                            res = Constants.DIR_UP
                                        else:
                                            res = Constants.DIR_DOWN

                elif percent >= 0 and percent <= 10:
                    isTendence = False
                    if week_med_abs > week_std:
                        if weekdiff > 1.2:
                            isTendence = True

                    if isTendence:
                        res = Constants.DIR_DOWN
                    else:
                        if medMoment >= 0:
                            if absMedMoment > stdMoment:
                                res = Constants.DIR_UP
                            else:
                                res = Constants.DIR_PRE_UP
                        if medMoment < 0:
                            if absMedMoment > stdMoment:
                                res = Constants.DIR_DOWN
                            else:
                                res = Constants.DIR_PRE_DOWN

            # if fcst == Constants.IND_REL_FCST_UP_INV_REL:
            #     if percent >= 0 and percent < 95:
            #         res = Constants.DIR_UP
            #     elif percent >= 95:
            #         if medMoment < 0:
            #             if absMedMoment > stdMoment:
            #                 res = Constants.DIR_DOWN
            #             else:
            #                 res = Constants.DIR_PRE_DOWN
            #         if medMoment > 0:
            #             if absMedMoment > stdMoment:
            #                 res = Constants.DIR_UP
            #             else:
            #
            #                 res = Constants.DIR_PRE_UP
        except Exception as error:
            print("Error getProMEDSTD_END 04", error)
        return res

    def getProMEDSTD_END_BLG_01(self, results, active):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            week = results[Constants.WEEK_FLOW]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_med_abs = results[Constants.WEEK_FLOW_MED]
            week_std = results[Constants.WEEK_FLOW_STD]
            weekdiff = abs(week_med_abs - week_std)
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            medDay = results[Constants.INDICATOR_MED_DAY]
            absMedDay = abs(medDay)
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            # BLG
            IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]
            IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
            blgDistPercent = active.parameters.blgDistPercent

            # valores del dia
            numUP = results[Constants.IND_NUM_UP]
            numDOWN = results[Constants.IND_NUM_DOWN]

            sumUP = results[Constants.IND_SUM_UP]
            sumDOWN = results[Constants.IND_SUM_DOWN]

            sumDay = int(sumUP) - int(sumDOWN)

            weekdiffTendenceValue = 1
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]

            if prevPercent is not None:
                prevPercent = float(prevPercent)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]
            # if med == 0:
            #     if direction == Constants.DIR_UP:
            #         med = 1
            #     elif direction == Constants.DIR_DOWN:
            #         med = -1
            percentFlow = Constants.DIR_WAIT
            if percent > prevPercent:
                percentFlow = Constants.DIR_UP
            else:
                # baja
                percentFlow = Constants.DIR_DOWN
            # CALCULOS final del dia
            # if week == Constants.WEEK_FLOW_UP:
            #
            if IND_BLG_UPPER_DST_PERCENT <= 40:
                res = Constants.DIR_DOWN
            elif IND_BLG_UPPER_DST_PERCENT > 40 and IND_BLG_UPPER_DST_PERCENT <= 60:
                # aca no sabemos
                if fcst == Constants.IND_REL_FCST_PRE_UP or fcst == Constants.IND_REL_FCST_UP \
                        or fcst == Constants.IND_REL_FCST_DOWN_INV_REL:
                    res = Constants.DIR_UP
                else:
                    res = Constants.DIR_DOWN
            elif IND_BLG_UPPER_DST_PERCENT > 60:
                res = Constants.DIR_UP


        except Exception as error:
            print("Error getProMEDSTD_END BLG1", error)
        return res

    def getProMEDSTD_END_BLG_02(self, results, active):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            week = results[Constants.WEEK_FLOW]
            weekPrev = results[Constants.WEEK_FLOW_PREV]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            week_med_abs = abs(results[Constants.WEEK_FLOW_MED])

            week_std = results[Constants.WEEK_FLOW_STD]
            weekdiff = results[Constants.WEEK_FLOW_DIFF]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            medDay = results[Constants.INDICATOR_MED_DAY]
            absMedDay = abs(medDay)
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            # BLG
            IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]
            IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
            blgDistPercent = active.parameters.blgDistPercent

            # valores del dia
            numUP = results[Constants.IND_NUM_UP]
            numDOWN = results[Constants.IND_NUM_DOWN]

            sumUP = results[Constants.IND_SUM_UP]
            sumDOWN = results[Constants.IND_SUM_DOWN]

            sumDay = int(sumUP) - int(sumDOWN)

            weekdiffTendenceValue = 1
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]

            if prevPercent is not None:
                prevPercent = float(prevPercent)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]
            # if med == 0:
            #     if direction == Constants.DIR_UP:
            #         med = 1
            #     elif direction == Constants.DIR_DOWN:
            #         med = -1
            percentFlow = Constants.DIR_WAIT
            if percent > prevPercent:
                percentFlow = Constants.DIR_UP
            else:
                # baja
                percentFlow = Constants.DIR_DOWN
            # CALCULOS final del dia
            if week == Constants.WEEK_FLOW_UP:
                # SUBE
                res = Constants.DIR_UP
                if active.parameters.weekMindiff != 0.7:
                    # ha cambiado el weekdiff
                    if abs(weekdiff) < active.parameters.weekMindiff:
                        print(f"prob is using DIRECTION")
                        if results[Constants.DIRECTION] == Constants.DIR_UP:
                            res = Constants.DIR_UP
                        elif results[Constants.DIRECTION] == Constants.DIR_DOWN:
                            res = Constants.DIR_DOWN
                        else:
                            # esta cambiando no esta claro
                            if IND_BLG_UPPER_DST_PERCENT <= 40:
                                res = Constants.DIR_DOWN
                                # puede que haya estado subiendo
                                if week_prev_med < week_med:
                                    res = Constants.DIR_UP

                            elif IND_BLG_UPPER_DST_PERCENT > 40 and IND_BLG_UPPER_DST_PERCENT <= 60:
                                # aca no sabemos
                                if fcst == Constants.IND_REL_FCST_PRE_UP or fcst == Constants.IND_REL_FCST_UP \
                                        or fcst == Constants.IND_REL_FCST_DOWN_INV_REL:
                                    res = Constants.DIR_UP
                                else:
                                    res = Constants.DIR_DOWN
                            elif IND_BLG_UPPER_DST_PERCENT > 60:
                                res = Constants.DIR_UP
                else:
                    nada = ""
                    # if week_med_abs < 1 or weekdiff <0 :
                    #     print(f"prob is using DIRECTION")
                    #     if results[Constants.DIRECTION]== Constants.DIR_UP:
                    #         res = Constants.DIR_UP
                    #     elif results[Constants.DIRECTION]== Constants.DIR_DOWN:
                    #         res = Constants.DIR_DOWN
                    #     else:
                    #         if weekPrev ==Constants.WEEK_FLOW_UP:
                    #             res = Constants.DIR_DOWN
                    #         else:
                    #             res = Constants.DIR_UP
            else:
                # BAJA
                res = Constants.DIR_DOWN
                if active.parameters.weekMindiff != 0.7:
                    # ha cambiado el weekdiff
                    if abs(weekdiff) < active.parameters.weekMindiff:
                        print(f"prob is using DIRECTION")
                        if results[Constants.DIRECTION] == Constants.DIR_UP:
                            res = Constants.DIR_UP
                        elif results[Constants.DIRECTION] == Constants.DIR_DOWN:
                            res = Constants.DIR_DOWN
                        else:
                            # esta cambiando no esta claro
                            if IND_BLG_UPPER_DST_PERCENT <= 40:
                                res = Constants.DIR_DOWN
                                if week_prev_med < week_med:
                                    res = Constants.DIR_UP
                            elif IND_BLG_UPPER_DST_PERCENT > 40 and IND_BLG_UPPER_DST_PERCENT <= 60:
                                # aca no sabemos
                                if fcst == Constants.IND_REL_FCST_PRE_UP or fcst == Constants.IND_REL_FCST_UP \
                                        or fcst == Constants.IND_REL_FCST_DOWN_INV_REL:
                                    res = Constants.DIR_UP
                                else:
                                    res = Constants.DIR_DOWN
                            elif IND_BLG_UPPER_DST_PERCENT > 60:
                                res = Constants.DIR_UP
                else:
                    nada = ""
                    # if week_med_abs < 1 or weekdiff <0 :
                    #     print(f"prob is using DIRECTION")
                    #     if results[Constants.DIRECTION]== Constants.DIR_UP:
                    #         res = Constants.DIR_UP
                    #     elif results[Constants.DIRECTION]== Constants.DIR_DOWN:
                    #         res = Constants.DIR_DOWN
                    #     else:
                    #         if weekPrev ==Constants.WEEK_FLOW_UP:
                    #             res = Constants.DIR_DOWN
                    #         else:
                    #             res = Constants.DIR_UP


        except Exception as error:
            print("Error getProMEDSTD_END BLG02", error)
        return

    def getProMEDSTD_END_BLG_04(self, results, active):
        res = Constants.DIR_WAIT
        try:
            percent = float(results[Constants.IND_REL_FCST_PERCENT])
            fcst = results[Constants.IND_REL_FCST]
            week = results[Constants.WEEK_FLOW]
            weekPrev = results[Constants.WEEK_FLOW_PREV]
            week_med = results[Constants.WEEK_FLOW_MED]
            week_prev_med = results[Constants.WEEK_FLOW_PREV_MED]
            week_med_abs = abs(results[Constants.WEEK_FLOW_MED])

            week_std = results[Constants.WEEK_FLOW_STD]
            weekdiff = results[Constants.WEEK_FLOW_DIFF]
            direction = results[Constants.DIRECTION]
            # percent = results[Constants.IND_REL_FCST_PERCENT]
            medDay = results[Constants.INDICATOR_MED_DAY]
            absMedDay = abs(medDay)
            stdDay = results[Constants.INDICATOR_STD_DAY]
            prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
            # BLG
            IND_BLG_UPPER_DST_PERCENT = results[Constants.IND_BLG_UPPER_DST_PERCENT]
            IND_BLG_LOWER_DST_PERCENT = results[Constants.IND_BLG_LOWER_DST_PERCENT]
            blgDistPercent = active.parameters.blgDistPercent

            # valores del dia
            numUP = results[Constants.IND_NUM_UP]
            numDOWN = results[Constants.IND_NUM_DOWN]

            sumUP = results[Constants.IND_SUM_UP]
            sumDOWN = results[Constants.IND_SUM_DOWN]

            sumDay = int(sumUP) - int(sumDOWN)

            weekdiffTendenceValue = 1
            medFcst = 0
            if Constants.IND_REL_FCST_MED in results:
                medFcst = results[Constants.IND_REL_FCST_MED]

            stdFcst = 0
            if Constants.IND_REL_FCST_STD in results:
                stdFcst = results[Constants.IND_REL_FCST_STD]

            if prevPercent is not None:
                prevPercent = float(prevPercent)

            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
            absMedMoment = abs(medMoment)
            stdMoment = results[Constants.STD_MOMENT]
            # if med == 0:
            #     if direction == Constants.DIR_UP:
            #         med = 1
            #     elif direction == Constants.DIR_DOWN:
            #         med = -1
            percentFlow = Constants.DIR_WAIT
            if percent > prevPercent:
                percentFlow = Constants.DIR_UP
            else:
                # baja
                percentFlow = Constants.DIR_DOWN
            # CALCULOS final del dia
            if week == Constants.WEEK_FLOW_UP:
                # SUBE
                res = Constants.DIR_UP
                if active.parameters.weekMindiff != 0.7:
                    # ha cambiado el weekdiff
                    if abs(weekdiff) < active.parameters.weekMindiff:
                        print(f"prob is using DIRECTION")
                        if results[Constants.DIRECTION] == Constants.DIR_UP or results[
                            Constants.DIRECTION] == Constants.DIR_PRE_UP:
                            res = Constants.DIR_UP
                        elif results[Constants.DIRECTION] == Constants.DIR_DOWN or results[
                            Constants.DIRECTION] == Constants.DIR_PRE_DOWN:
                            res = Constants.DIR_DOWN
                        else:
                            # esta cambiando no esta claro
                            if IND_BLG_UPPER_DST_PERCENT <= 40:
                                res = Constants.DIR_DOWN
                                # puede que haya estado subiendo
                                if week_prev_med < week_med:
                                    res = Constants.DIR_UP

                            elif IND_BLG_UPPER_DST_PERCENT > 40 and IND_BLG_UPPER_DST_PERCENT <= 60:
                                # aca no sabemos
                                if fcst == Constants.IND_REL_FCST_PRE_UP or fcst == Constants.IND_REL_FCST_UP \
                                        or fcst == Constants.IND_REL_FCST_DOWN_INV_REL:
                                    res = Constants.DIR_UP
                                else:
                                    res = Constants.DIR_DOWN
                            elif IND_BLG_UPPER_DST_PERCENT > 60:
                                res = Constants.DIR_UP
                                if week_prev_med > week_med:
                                    res = Constants.DIR_DOWN
                else:
                    nada = ""
                    # if week_med_abs < 1 or weekdiff <0 :
                    #     print(f"prob is using DIRECTION")
                    #     if results[Constants.DIRECTION]== Constants.DIR_UP:
                    #         res = Constants.DIR_UP
                    #     elif results[Constants.DIRECTION]== Constants.DIR_DOWN:
                    #         res = Constants.DIR_DOWN
                    #     else:
                    #         if weekPrev ==Constants.WEEK_FLOW_UP:
                    #             res = Constants.DIR_DOWN
                    #         else:
                    #             res = Constants.DIR_UP
            else:
                # BAJA
                res = Constants.DIR_DOWN
                if active.parameters.weekMindiff != 0.7:
                    # ha cambiado el weekdiff
                    if abs(weekdiff) < active.parameters.weekMindiff:
                        print(f"prob is using DIRECTION")
                        if results[Constants.DIRECTION] == Constants.DIR_UP or results[
                            Constants.DIRECTION] == Constants.DIR_PRE_UP:
                            res = Constants.DIR_UP
                        elif results[Constants.DIRECTION] == Constants.DIR_DOWN or results[
                            Constants.DIRECTION] == Constants.DIR_PRE_DOWN:
                            res = Constants.DIR_DOWN
                        else:
                            # esta cambiando no esta claro
                            if IND_BLG_LOWER_DST_PERCENT <= 40:
                                res = Constants.DIR_UP
                                if week_prev_med > week_med:
                                    res = Constants.DIR_DOWN
                            elif IND_BLG_LOWER_DST_PERCENT > 40 and IND_BLG_LOWER_DST_PERCENT <= 60:
                                # aca no sabemos
                                if fcst == Constants.IND_REL_FCST_PRE_UP or fcst == Constants.IND_REL_FCST_UP \
                                        or fcst == Constants.IND_REL_FCST_DOWN_INV_REL:
                                    res = Constants.DIR_UP
                                else:
                                    res = Constants.DIR_DOWN
                            elif IND_BLG_LOWER_DST_PERCENT > 60:
                                res = Constants.DIR_DOWN
                                if week_prev_med < week_med:
                                    res = Constants.DIR_UP
                else:
                    nada = ""
                    # if week_med_abs < 1 or weekdiff <0 :
                    #     print(f"prob is using DIRECTION")
                    #     if results[Constants.DIRECTION]== Constants.DIR_UP:
                    #         res = Constants.DIR_UP
                    #     elif results[Constants.DIRECTION]== Constants.DIR_DOWN:
                    #         res = Constants.DIR_DOWN
                    #     else:
                    #         if weekPrev ==Constants.WEEK_FLOW_UP:
                    #             res = Constants.DIR_DOWN
                    #         else:
                    #             res = Constants.DIR_UP


        except Exception as error:
            print("Error getProMEDSTD_END BLG04", error)
        return res


