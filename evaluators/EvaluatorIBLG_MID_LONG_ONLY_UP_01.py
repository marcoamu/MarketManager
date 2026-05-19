from evaluators.CierreBase import CierreBase
from evaluators.EvaluatorBase import EvaluatorBase
from evaluators.AperturaBase import AperturaBase
from service.Constants import Constants


class EvaluatorIBLG_MID_LONG_ONLY_UP_01(EvaluatorBase,AperturaBase,CierreBase):

    #tiene EMA MIN DST

    def __init__(self):
        #se añade blg_mid_distance closenxt_middle
        self.name = "EvaluatorIBLG_MID_LONG_ONLY_UP_01"
        # self.name = "EvaluatorIBLG_MID_LONG_01"
        # self.name = "EvaluatorIBLG_PROB_FLOW_02"


    def evaluate(self, results, activeParam):
        results[Constants.EVAl_NAME] = self.name
        self.updateTimeZoneValues(results)
        # MULTIPLICADORES
        #para cerrar cuanto antes se usa para cuando el valor es negativo mas pequeño cierra mas rapido
        self.multiplicatorClose = activeParam.difference /2
        #control para ver si abre cuando ya hay una cantidad X usada
        self.enableControlOpen = False
        self.multiplicadorOpen = 2.2
        #usado para abrir en tendencia inversa
        self.multiplicadorUP= 1
        self.multiplicatorNXT = 1

        #valuador para estado change por market tendence = True  o por indicator = False
        self.evaluateChangeMarketTendence = True
        self.closeAcumValue = activeParam.closeAcumvalue

        self.ima1minDistance = activeParam.ima1minDistance
        self.medstdminDiff = activeParam.medstdminDiff
        self.medstdmaxDiff = activeParam.medstdmaxDiff
        self.BLGDist = activeParam.bollingerDst
        self.closeAcumValue = activeParam.bollingerClose
        self.closeProfit = activeParam.closeProfit
        self.blgDistPercent = activeParam.blgDistPercent
        self.closeDifference = activeParam.difference + (activeParam.difference * 0.10)
        self.accumulate= activeParam.accumulate
        self.angleUP = activeParam.angleUp
        self.angleDOWN = activeParam.angleDown

        self.weekMEDMinLevel = activeParam.weekMEDMinLevel

        self.midMinDst = 0.08
        self.emaMinDst = activeParam.emaMinDst

        #SOLO EN LOS INTERVALOS definidos
        currentTime = self.gettime(results)
        intime = False
        if currentTime >= int(self.iniStart) and currentTime < int(self.iniEnd):
            intime = True
        if currentTime >= int(self.closeStart) and currentTime < int(self.closeEnd):
            intime = True

        intime = True
        #print(f'EVALUATOR  {self.name}   ACTIVO: {activeParam.name}')
        if results[Constants.CURRENT_ACTION] == Constants.ACTION_WAIT or results[
            Constants.CURRENT_ACTION] == Constants.ACTION_CLOSE:
            if intime:
                self.evaluarApertura(results, activeParam)
            else:
#                 print(f"FUERA DE HORARIO")
        elif results[Constants.CURRENT_ACTION] == Constants.ACTION_BUY:
            # self.evaluarFlujoBUY(results, activeParam)
            self.evaluarFlujoBUY_LONG(results, activeParam)
        elif results[Constants.CURRENT_ACTION] == Constants.ACTION_SELL:
            # self.evaluarFlujoSELL(results, activeParam)
            self.evaluarFlujoSELL_LONG(results, activeParam)

    def evaluarApertura(self, results, activeParam):
        #
        # valores
        flujo_count = results[Constants.FLUJO_COUNT]
        res = self.aperturaAngle(results,activeParam)
        if "UP" in res:
            self.evaluarAperturaUP(results, activeParam, flujo_count)
        elif "DOWN" in res:
            self.evaluarAperturaDOWN(results, activeParam, flujo_count)
        else:
            nada=""
            self.evaluarAperturaCHANGE(results, activeParam, flujo_count)





    def evaluarAperturaDOWNDifference(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0
        if results[Constants.INDICATOR] == Constants.INDICATOR_SELL:
            if results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_WAIT:
                difference_optimized = activeParam.difference
            elif results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_UP:
                if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_DOWN:
                    if flujo_count > 2:
                        unit_diff = activeParam.unit * (flujo_count) * 1.3
                        unit_diff = unit_diff * -1
                    else:
                        difference_optimized = activeParam.difference / 2
                else:
                    difference_optimized = activeParam.difference + (activeParam.difference / 3)
            else:
                if flujo_count > 2:
                    unit_diff = activeParam.unit * (flujo_count) * 1.3
                    unit_diff = unit_diff * -1
                else:
                    difference_optimized = activeParam.difference - (activeParam.difference / 2)
        elif results[Constants.INDICATOR] == Constants.INDICATOR_SELLX:
            if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_DOWN:
                if flujo_count > 2:
                    unit_diff = activeParam.unit * (flujo_count) * 1.3
                    unit_diff = unit_diff * -1
                else:
                    difference_optimized = activeParam.difference / 2
            else:
                if results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_WAIT:
                    difference_optimized = activeParam.difference
                else:
                    difference_optimized = activeParam.difference / 2

        difference_optimized = difference_optimized + unit_diff
        return difference_optimized, unit_diff

    def evaluarAperturaCHANGE(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0
        self.printDifference("evaluarAperturaCHANGE", difference_optimized, self.closeAcumValue, self.closeDifference)

        if results[Constants.ANGLE]>0:
            self.evaluarAperturaUP(results,activeParam,flujo_count)
        else:
            self.evaluarAperturaDOWN(results, activeParam, flujo_count)

    def evaluarAperturaDOWN(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0


        self.printDifference("evaluarAperturaDOWN", difference_optimized, self.closeAcumValue, self.closeDifference)


        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                # results[Constants.CLOSE_NXT_DOWN] = 0
                if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or
                        results[Constants.ACTION_MIN_DIST] >= (
                                difference_optimized * self.multiplicadorUP)):
                    results[Constants.CLOSE_NXT_UP] = 0

                    if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
                        # if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
                        if results[Constants.IND_BLG_UPPER_DST_PERCENT] > self.blgDistPercent:
                            nada=""
                            # results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            # self.printInicioLog("DOWN_BLG_NXTUP_BUY01",results,activeParam)
                            # return
                        else:
                            nada=""
                            # results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            # print(
                            #     f" INICIO MERCADO DOWN_BLG_NXTUP_BUY_02 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} \tEMA_DST {abs(results[Constants.EMA_DST])}  \tWEEK_FLOW_DIFF {results[Constants.WEEK_FLOW_DIFF]}  percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")
                            # results[Constants.CLOSE_NXT_DOWN] = 0
                            # results[Constants.CLOSE_NXT_UP] = 0
                            # return

                    elif results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_UP:
                        nada=""
                        # if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
                        #     results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        #     print(
                        #         f" INICIO MERCADO DOWN_BLG_NXTUP_BUY_01 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} \tEMA_DST {abs(results[Constants.EMA_DST])}  \tWEEK_FLOW_DIFF {results[Constants.WEEK_FLOW_DIFF]}  percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")
                        #     results[Constants.CLOSE_NXT_DOWN] = 0
                        #     results[Constants.CLOSE_NXT_UP] = 0
                        #     return
        # INDICADORES
        # if results[Constants.IMA1_DISTANCE] >= self.ima1minDistance:
            # if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_DOWN:
        if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
            Constants.ACTION_MAX_DIST] >= (difference_optimized):

            if self.enableControlOpen:
                if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
                    nada = ""
                        # results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                        # print(f" INICIO MERCADO DOWN_DOWN_SELL01 {results[Constants.DATE].values[0]} Acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} \tEMA_DST {abs(results[Constants.EMA_DST])}  \tWEEK_FLOW_DIFF {results[Constants.WEEK_FLOW_DIFF]}  angle: {results[Constants.ANGLE]} direction {results[Constants.DIRECTION]} INDICATOR_MED_MOMENT {results[Constants.INDICATOR_MED_MOMENT]}")


            else:
                if results[Constants.FLUJO]==Constants.FLUJO_BAJA:
                    # if abs(results[Constants.EMA_DST]) >= self.emaMinDst:
                        if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= self.blgDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT] ==0:
                                nada = ""
                                # results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                # print(f" INICIO MERCADO DOWN_DOWN_SELL02 {results[Constants.DATE].values[0]} Acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} \tEMA_DST {abs(results[Constants.EMA_DST])}  \tWEEK_FLOW_DIFF {results[Constants.WEEK_FLOW_DIFF]}  angle: {results[Constants.ANGLE]} direction {results[Constants.DIRECTION]} INDICATOR_MED_MOMENT {results[Constants.INDICATOR_MED_MOMENT]}")


                        elif results[Constants.IND_BLG_LOWER_DST_PERCENT] <0:
                            # if abs(results[Constants.EMA_DST]) >= self.emaMinDst:
                            nada = ""
                                # results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                # print(
                                #     f" INICIO MERCADO DOWN_DOWN_SELL03 {results[Constants.DATE].values[0]} Acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} \tEMA_DST {abs(results[Constants.EMA_DST])}  \tWEEK_FLOW_DIFF {results[Constants.WEEK_FLOW_DIFF]}  angle: {results[Constants.ANGLE]} direction {results[Constants.DIRECTION]} INDICATOR_MED_MOMENT {results[Constants.INDICATOR_MED_MOMENT]}")

                        elif results[Constants.IND_BLG_LOWER_DST_PERCENT] < self.blgDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT]==0:
                            nada=""
                            if results[Constants.ANGLE] < 0 or results[
                                Constants.ANGLE] == 0:
                                # if abs(results[Constants.EMA_DST]) >= self.emaMinDst:
                                    # BAJA
                                nada = ""
                                    # if abs(results[Constants.ANGLE]) > self.angleDOWN:
                                    #     results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                    #     print(
                                    #         f" INICIO MERCADO DOWN_ANGLE_01 {results[Constants.DATE].values[0]} Acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} \tEMA_DST {abs(results[Constants.EMA_DST])}  \tWEEK_FLOW_DIFF {results[Constants.WEEK_FLOW_DIFF]}  angle: {results[Constants.ANGLE]} direction {results[Constants.DIRECTION]} INDICATOR_MED_MOMENT {results[Constants.INDICATOR_MED_MOMENT]}")
                                    # else:
                                    #     if results[Constants.ANGLEm1] > 0:
                                    #         # esta bajando o haciendo el cambio
                                    #         results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                    #         print(
                                    #             f" INICIO MERCADO DOWN_ANGLE_02 {results[Constants.DATE].values[0]} Acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} \tEMA_DST {abs(results[Constants.EMA_DST])}  \tWEEK_FLOW_DIFF {results[Constants.WEEK_FLOW_DIFF]}  angle: {results[Constants.ANGLE]} direction {results[Constants.DIRECTION]} INDICATOR_MED_MOMENT {results[Constants.INDICATOR_MED_MOMENT]}")
                else:
                    nada =""


    def evaluarDifferenceUP(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0
        if results[Constants.INDICATOR] == Constants.INDICATOR_BUY:
            if results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_WAIT:
                difference_optimized = activeParam.difference
            elif results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_DOWN:
                difference_optimized = activeParam.difference + (activeParam.difference / 3)
            else:
                difference_optimized = activeParam.difference - (activeParam.difference / 3)
        elif results[Constants.INDICATOR] == Constants.INDICATOR_BUYX:
            if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UP:
                difference_optimized = activeParam.difference / 2

            else:
                if results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_WAIT:
                    difference_optimized = activeParam.difference
                else:
                    difference_optimized = activeParam.difference / 2
        return difference_optimized, unit_diff


    def evaluarAperturaUP(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0

        self.printDifference("evaluarAperturaUP", difference_optimized, self.closeAcumValue, self.closeDifference)


        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_DOWN] = 0
                results[Constants.CLOSE_NXT_UP] = 0
                if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
                    if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_BUY:
                        nada = ""
                        # results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                        # print(
                        #     f" INICIO MERCADO {results[Constants.DATE].values[0]} UP_BLG_NXTUP_SELL01 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} \tEMA_DST {abs(results[Constants.EMA_DST])}  \tWEEK_FLOW_DIFF {results[Constants.WEEK_FLOW_DIFF]}  percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")

                    results[Constants.CLOSE_NXT_DOWN] = 0
                    results[Constants.CLOSE_NXT_UP] = 0
                    return
                elif results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_UP:
                    if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
                        nada = ""
                        # results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        # print(
                        #     f" INICIO MERCADO {results[Constants.DATE].values[0]} UP_BLG_NXTUP_BUY_01 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} \tEMA_DST {abs(results[Constants.EMA_DST])}  \tWEEK_FLOW_DIFF {results[Constants.WEEK_FLOW_DIFF]}  percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")

                results[Constants.CLOSE_NXT_DOWN] = 0
                results[Constants.CLOSE_NXT_UP] = 0

        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
                results[Constants.CLOSE_NXT_UP] = 0

        # if results[Constants.IMA1_DISTANCE] >= self.ima1minDistance:
        if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
            Constants.ACTION_MIN_DIST] >= (difference_optimized * self.multiplicadorUP):
            if self.enableControlOpen:
                if results[Constants.ACUMULADO_ABS] <= (difference_optimized  * self.multiplicadorOpen):
                    # if abs(results[Constants.EMA_DST]) >= self.emaMinDst:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        self.printInicioLog("UP_UP_BUY01", results, activeParam)

            else:
                if results[Constants.FLUJO]==Constants.FLUJO_SUBE:
                    # if abs(results[Constants.EMA_DST]) >= self.emaMinDst:
                        if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= self.blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT]==0:
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            self.printInicioLog("UP_UP_BUY2", results, activeParam)
                        elif results[Constants.IND_BLG_UPPER_DST_PERCENT] <0 :
                            if "DOWN" in results[Constants.WEEK_FLOW]:
                                if abs(results[Constants.WEEK_FLOW_MED]) < self.weekMEDMinLevel:
                                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                    self.printInicioLog("UP_UP_DSTNEG_BUY3", results, activeParam)

                        elif results[Constants.IND_BLG_UPPER_DST_PERCENT] < self.blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT]==0:
                            nada=""
                            if results[Constants.ANGLE] > 0 or results[
                                            Constants.ANGLE] == 0:
                                #SUBE
                                if abs(results[Constants.ANGLE]) > self.angleUP or results[Constants.ANGLE_COUNTER]>=5:
                                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                    self.printInicioLog("UP_UP_BUY_ANGLE_01", results, activeParam)

                                else:
                                    nada = ""
                                    # if results[Constants.ANGLEm1] <0:
                                    #     # esta subiendo o haciendo el cambio
                                    #     results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                    #     self.printInicioLog("UP_UP_BUY_ANGLE_02", results, activeParam)

    def evaluarDifferenceBUY(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0
        if results[Constants.INDICATOR] == Constants.INDICATOR_SELL or results[
            Constants.INDICATOR] == Constants.INDICATOR_SELLX:
            if results[Constants.IMA_NEW] == Constants.IMA_NEW_BUY:
                difference_optimized = activeParam.difference + (activeParam.difference / 4)
            elif results[Constants.IMA_NEW] == Constants.IMA_NEW_SELL:
                if results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_UP:
                    # si el flujo es subida
                    difference_optimized = activeParam.difference - (activeParam.difference / 3)
                elif results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_DOWN:
                    # baja mas para cerrar cuanto antes
                    difference_optimized = activeParam.difference - (activeParam.difference / 3)
                else:
                    # wait
                    difference_optimized = activeParam.difference - (activeParam.difference / 3)
        elif results[Constants.INDICATOR] == Constants.INDICATOR_BUY or results[
            Constants.INDICATOR] == Constants.INDICATOR_BUYX:
            if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UP:
                if results[Constants.IMA_NEW] == Constants.IMA_NEW_BUY:
                    if flujo_count > 2:
                        unit_diff = activeParam.unit * (flujo_count) * 1.3
                    else:
                        difference_optimized = activeParam.difference + (activeParam.difference / 2)
                # elif results[Constants.IMA_NEW] == Constants.IMA_NEW_SELL:
                #     difference_optimized = activeParam.difference
        if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
            # FIX PARA CERRAR CUANTO ANTES SI BAJA Y HAY GANANCIAS
            if results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_UP:
                controlUP = None
                if results[Constants.INDICATOR] == Constants.INDICATOR_BUY:
                    if flujo_count > 2:
#                         print(f"CORRECTION BUY DOWN COUNT")
                        unit_diff = activeParam.unit * (flujo_count)
                        unit_diff = unit_diff * -1
            elif results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_DOWN:
                if flujo_count > 2:
                    unit_diff = activeParam.unit * (flujo_count) * 1.3
                    unit_diff = unit_diff * -1
            else:
                if flujo_count > 2:
                    unit_diff = activeParam.unit * (flujo_count) * 1.3
                    unit_diff = unit_diff * -1

        difference_optimized = difference_optimized + unit_diff

        return difference_optimized, unit_diff

    def evaluarFlujoBUY_LONG(self, results, activeParam):
        difference_optimized = activeParam.difference
        unit_diff = 0
        flujo_count = results[Constants.FLUJO_COUNT]

        self.printDifference("evaluarFlujoBUY_LONG", difference_optimized, self.closeAcumValue, self.closeDifference, self.accumulate)
        self.control_BUY_BLG_MID_02(results, activeParam, self.closeAcumValue, self.closeDifference,self.accumulate)



    def evaluarDifferenceSELL(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0

        if results[Constants.INDICATOR_TENDENCE] != Constants.INDICATOR_T_WAIT:
            if results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_UP:
                difference_optimized = activeParam.difference - (activeParam.difference / 3)
            elif results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_DOWN:
                difference_optimized = activeParam.difference + (activeParam.difference / 5)
        else:
            difference_optimized = activeParam.difference - (activeParam.difference / 4)
#             print(f"estamos en WAIT no hay indicadores de diferencia")

        if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
            if results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_UP:
                if flujo_count > 1:
                    unit_diff = activeParam.unit * (flujo_count - 1)
                    unit_diff = unit_diff * -1
            elif results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_DOWN:
                if results[Constants.INDICATOR] == Constants.INDICATOR_SELL:
                    # intentar cerrar si sube y esta en sell ( no sellX)
                    if flujo_count > 2:
#                         print(f"CORRECTION SELL UP COUNT")
                        unit_diff = activeParam.unit * (flujo_count) * 1.2
                        unit_diff = unit_diff * -1
            else:
                # wait
                if flujo_count > 2:
                    unit_diff = activeParam.unit * (flujo_count) * 1.3
                    unit_diff = unit_diff * -1

        difference_optimized = difference_optimized + unit_diff
        return difference_optimized, unit_diff

    def evaluarFlujoSELL_LONG(self, results, activeParam):
        difference_optimized = activeParam.difference
        unit_diff = 0
        # valores
        flujo_count = results[Constants.FLUJO_COUNT]

        self.printDifference("evaluarFlujoSELL_LONG", difference_optimized, self.closeAcumValue, self.closeDifference, self.accumulate)
        self.control_SELL_BLG_MID_01(results, activeParam, self.closeAcumValue, self.closeDifference, self.accumulate)

