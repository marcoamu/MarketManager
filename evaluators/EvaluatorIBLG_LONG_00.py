from evaluators.CierreBase import CierreBase
from evaluators.EvaluatorBase import EvaluatorBase
from evaluators.AperturaBase import AperturaBase
from service.Constants import Constants


class EvaluatorIBLG_LONG_00(EvaluatorBase,AperturaBase,CierreBase):

    def __init__(self):
        #se añade cierre mas permisivo
        self.name = "EvaluatorIBLG_LONG_00"
        # self.name = "EvaluatorIBLG_LONG_ONLY_UP_00"
        # self.name = "EvaluatorIMA1_CLEAN_BLG_04_ONLY_UP_01"
        # self.name = "EvaluatorIMA1_CLEAN_BLG_04"
        # self.name = "EvaluatorIMA1_CLEAN_BLG_03"
        # self.name = "EvaluatorIMA1_CLEAN_BLG_02"
        # self.name = "EvaluatorIMA1_CLEAN_BLG_01"
        # self.name = "EvaluatorIMA1_CLEAN_Optimiz01"


    def evaluate(self, results, activeParam):
        results[Constants.EVAl_NAME] = self.name

        # MULTIPLICADORES
        #para cerrar cuanto antes se usa para cuando el valor es negativo mas pequeño cierra mas rapido
        self.multiplicatorClose = activeParam.difference /2
        #control para ver si abre cuando ya hay una cantidad X usada
        self.enableControlOpen = False
        self.multiplicadorOpen = 2.2
        #usado para abrir en tendencia inversa
        self.multiplicadorUP= 2
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
        self.closeDifference = activeParam.difference + (activeParam.difference * 0.20)

        #print(f'EVALUATOR  {self.name}   ACTIVO: {activeParam.name}')
        if results[Constants.CURRENT_ACTION] == Constants.ACTION_WAIT or results[
            Constants.CURRENT_ACTION] == Constants.ACTION_CLOSE:
            self.evaluarApertura(results, activeParam)
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

        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_BUY:
            self.evaluarAperturaUP(results, activeParam, flujo_count)
        elif results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
            self.evaluarAperturaDOWN(results, activeParam, flujo_count)
        elif results[Constants.IND_BLG] == Constants.IND_BLG_MED_WAIT:
            nada=""
            # self.evaluarAperturaCHANGE(results, activeParam, flujo_count)
        else:
#             print(f"ESTAMOS A LA ESPERA DE INDICADORES BUENOS")




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


    def evaluarAperturaDOWN(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0

        difference_optimized, unit_diff = self.evaluarAperturaDOWNDifference(results, activeParam, flujo_count)

#         print(
            f"DIFFERENCE_OPTIMIZED evaluarAperturaDOWN {difference_optimized} original {activeParam.difference} unit_diffb {unit_diff}")

        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_DOWN] = 0
                results[Constants.CLOSE_NXT_UP] = 0
                if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
                    # if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
                    if results[Constants.IND_BLG_UPPER_DST_PERCENT] > self.blgDistPercent:
                        if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or
                                results[Constants.ACTION_MIN_DIST] >= (
                                        difference_optimized * self.multiplicadorUP)):

                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
#                             print(
                                f" INICIO MERCADO DOWN_BLG_NXTUP_BUY01 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")
                        results[Constants.CLOSE_NXT_DOWN] = 0
                        results[Constants.CLOSE_NXT_UP] = 0
                        return
                    else:
                        nada=""
                        # results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        # print(
                        #     f" INICIO MERCADO DOWN_BLG_NXTUP_BUY_02 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")
                        # results[Constants.CLOSE_NXT_DOWN] = 0
                        # results[Constants.CLOSE_NXT_UP] = 0
                        # return

                elif results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_UP:
                    nada=""
                    # if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
                    #     results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                    #     print(
                    #         f" INICIO MERCADO DOWN_BLG_NXTUP_BUY_01 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")
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
                    # print(f" INICIO MERCADO DOWN_DOWN_SELL01 {results[Constants.DATE].values[0]} Acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} angle: {results[Constants.ANGLE]} direction {results[Constants.DIRECTION]} INDICATOR_MED_MOMENT {results[Constants.INDICATOR_MED_MOMENT]}")

                    results[Constants.NEW_ACTION] = Constants.ACTION_SELL
#                     print(f" INICIO MERCADO DOWN_DOWN_SELL01 {results[Constants.DATE].values[0]} Acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} angle: {results[Constants.ANGLE]} direction {results[Constants.DIRECTION]} INDICATOR_MED_MOMENT {results[Constants.INDICATOR_MED_MOMENT]}")


            else:
                if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= self.blgDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT] ==0:
                    if abs(results[Constants.MEDSTDDIFF]) > self.medstdminDiff:
                        # if (results[Constants.ANGLE]<0 and abs(results[Constants.ANGLE])>1) or results[Constants.ANGLE]==0:

                            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
#                             print(f" INICIO MERCADO DOWN_DOWN_SELL02 {results[Constants.DATE].values[0]} Acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} angle: {results[Constants.ANGLE]} direction {results[Constants.DIRECTION]} INDICATOR_MED_MOMENT {results[Constants.INDICATOR_MED_MOMENT]}")
                elif results[Constants.IND_BLG_LOWER_DST_PERCENT] <0:
                    results[Constants.NEW_ACTION] = Constants.ACTION_SELL
#                     print(
                        f" INICIO MERCADO DOWN_DOWN_SELL03 {results[Constants.DATE].values[0]} Acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} angle: {results[Constants.ANGLE]} direction {results[Constants.DIRECTION]} INDICATOR_MED_MOMENT {results[Constants.INDICATOR_MED_MOMENT]}")

                elif results[Constants.IND_BLG_LOWER_DST_PERCENT] < self.blgDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT]==0:
                    nada=""
                    # if (results[Constants.ANGLE] < 0 and abs(results[Constants.ANGLE]) > 1) or results[
                    #     Constants.ANGLE] == 0:
                    #     if results[Constants.INDICATOR_MED_MOMENT_VALUE] < 0:
                    #         results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                    #         print(
                    #             f" INICIO MERCADO DOWN DOWN_SELLDST_01 {results[Constants.DATE].values[0]} Acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} angle: {results[Constants.ANGLE]} direction {results[Constants.DIRECTION]} INDICATOR_MED_MOMENT {results[Constants.INDICATOR_MED_MOMENT]}")

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

        difference_optimized, unit_diff = self.evaluarDifferenceUP(results, activeParam, flujo_count)

#         print(
            f"DIFFERENCE_OPTIMIZED evaluarAperturaUP {difference_optimized} original {activeParam.difference} unit_diffb {unit_diff}")

        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_DOWN] = 0
                results[Constants.CLOSE_NXT_UP] = 0
                if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
                    if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_BUY:
                        nada = ""
                        # results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                        # print(
                        #     f" INICIO MERCADO {results[Constants.DATE].values[0]} UP_BLG_NXTUP_SELL01 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")

                    results[Constants.CLOSE_NXT_DOWN] = 0
                    results[Constants.CLOSE_NXT_UP] = 0
                    return
                elif results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_UP:
                    if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
                        nada = ""
                        # results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        # print(
                        #     f" INICIO MERCADO {results[Constants.DATE].values[0]} UP_BLG_NXTUP_BUY_01 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")

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
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
#                     print(f" INICIO MERCADO UP_UP_BUY01 {results[Constants.DATE].values[0]} Acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} angle: {results[Constants.ANGLE]} direction {results[Constants.DIRECTION]} INDICATOR_MED_MOMENT {results[Constants.INDICATOR_MED_MOMENT]}")

            else:
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] >= self.blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT]==0:
                    if abs(results[Constants.MEDSTDDIFF]) > self.medstdminDiff:
                        # if (results[Constants.ANGLE] > 0 and abs(results[Constants.ANGLE]) > 1) or results[
                        #         Constants.ANGLE] == 0:

                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
#                             print(f" INICIO MERCADO UP_UP_BUY2 {results[Constants.DATE].values[0]} Acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} angle: {results[Constants.ANGLE]} direction {results[Constants.DIRECTION]} INDICATOR_MED_MOMENT {results[Constants.INDICATOR_MED_MOMENT]}")
                elif results[Constants.IND_BLG_UPPER_DST_PERCENT] <0 :
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
#                     print(
                        f" INICIO MERCADO UP_UP_DSTNEG_BUY3 {results[Constants.DATE].values[0]} Acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} angle: {results[Constants.ANGLE]} direction {results[Constants.DIRECTION]} INDICATOR_MED_MOMENT {results[Constants.INDICATOR_MED_MOMENT]}")

                elif results[Constants.IND_BLG_UPPER_DST_PERCENT] < self.blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT]==0:
                    nada=""
                    # if results[Constants.IND_BLG_UPPER_DST_PERCENT] < 0:
                    #     #esta subiendo
                    #     if (results[Constants.ANGLE] > 0 and abs(results[Constants.ANGLE]) > 1) or results[
                    #                 Constants.ANGLE] == 0:
                    #         if results[Constants.INDICATOR_MED_MOMENT_VALUE]>0:
                    #             results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                    #             print(
                    #                         f" INICIO MERCADO UP_UP_BUY_UPPPER_01 {results[Constants.DATE].values[0]} Acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} angle: {results[Constants.ANGLE]} direction {results[Constants.DIRECTION]} INDICATOR_MED_MOMENT {results[Constants.INDICATOR_MED_MOMENT]}")

                                #abrimos una venta

                    # estamos en una subida muy cerca de upper blg
                    # if (results[Constants.ANGLE] > 0 and abs(results[Constants.ANGLE]) > 1) or results[
                    #             Constants.ANGLE] == 0:
                    #     if results[Constants.INDICATOR_MED_MOMENT_VALUE]>0:
                    #         results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                    #         print(
                    #             f" INICIO MERCADO UP_UP_BUY_UPPPER_01 {results[Constants.DATE].values[0]} Acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} angle: {results[Constants.ANGLE]} direction {results[Constants.DIRECTION]} INDICATOR_MED_MOMENT {results[Constants.INDICATOR_MED_MOMENT]}")

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

        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_DOWN] = 0
                results[Constants.CLOSE_NXT_UP] = 0

        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
                results[Constants.CLOSE_NXT_UP] = 0

        if results[Constants.IND_BLG]== Constants.IND_BLG_MED_SELL:
            if results[Constants.ACTION_COUNT]>5:
#                 print(
                    f"CERRAMOS MERCADO BUY action_acum: {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} BUY_CLOSE_ISSELL 01 profit:{results[Constants.ACTION_ACUM]} ")
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return


        # # # #CERRAMOS SI BAJO mucho
        # if results[Constants.ACTION_ACUM] <= 0:
        #     if abs(results[Constants.ACTION_ACUM]) >= (self.closeAcumValue):
        #         print(
        #             f"CERRAMOS MERCADO {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} BUY_ACTION_DIST01 {results[Constants.ACUMULADO]} profit:{self.closeAcumValue}")
        #         results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
        #         return
        #
        # #CERRAMOS SI SALE DEL TOP BLG
        # if results[Constants.IND_BLG_UPPER_DST_PERCENT]<0:
        #     #HA pASADO EL TOP HAY GANANCIAS
        #     if abs(results[Constants.IND_BLG_UPPER_DST_PERCENT])>1:
        #         print(
        #             f"CERRAMOS MERCADO {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} BUY_MAXIMO_01 {results[Constants.ACUMULADO]} profit:{self.closeAcumValue}")
        #         results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
        #         return
    # def evaluarFlujoBUY(self, results, activeParam):
    #     # CONTROL LIMITES MAXIMOS
    #     difference_optimized = activeParam.difference
    #     unit_diff = 0
    #     flujo_count = results[Constants.FLUJO_COUNT]
    #
    #     difference_optimized, unit_diff = self.evaluarDifferenceBUY(results, activeParam, flujo_count)
    #
    #     print(
    #         f"DIFFERENCE_OPTIMIZED  evaluarFlujoBUY {difference_optimized} original {activeParam.difference} close difference {self.closeDifference} unit_diffb {unit_diff}")
    #
    #     if results[Constants.CLOSE_NXT_DOWN] == 1:
    #         if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
    #             if results[Constants.INDICATOR_MED_MOMENT] == Constants.INDICATOR_TM_UP:
    #                 multiplicator = self.multiplicadorUP * self.multiplicatorNXT
    #                 print(f"multiplicator {self.multiplicatorNXT}")
    #             else:
    #                 multiplicator = self.multiplicadorUP
    #                 print(f"multiplicator 1")
    #
    #             print(f"new difference {difference_optimized * multiplicator}")
    #
    #             if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicator) or
    #                     results[Constants.ACTION_MAX_DIST] >= (
    #                             difference_optimized * multiplicator)):
    #                 # results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
    #
    #                 print(
    #                     f" CERRAMOS MERCADO BUY_DOWN_BLG_01 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")
    #                 results[Constants.CLOSE_NXT_DOWN] = 0
    #                 results[Constants.CLOSE_NXT_UP] = 0
    #                 print(f"Close next down executed")
    #             results[Constants.CLOSE_NXT_DOWN] = 0
    #             results[Constants.CLOSE_NXT_UP] = 0
    #             print(f"Close next down executed")
    #             # return
    #
    #     if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
    #         if results[Constants.ACTION_ACUM] < 0:
    #             # perdidas
    #             # if abs(results[Constants.ACUMULADO]) >= self.closeAcumValue:
    #             print(
    #                 f"CERRAMOS MERCADO BUY action_acum: {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} BUY_CLOSE_ISSELL profit:{results[Constants.ACTION_ACUM]} ")
    #             results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
    #             return
    #         else:
    #             # ganancias
    #             if results[Constants.ACUMULADO] <= 0:
    #                 ##esta bajando
    #                 if abs(results[Constants.ACUMULADO]) >= self.closeDifference:
    #                     print(
    #                         f"CERRAMOS MERCADO BUY action_acum: {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} BUY_CLOSE_ISSELL 01 profit:{results[Constants.ACTION_ACUM]} ")
    #                     results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
    #                     return
    #     # cerramos si llega al minimo admisible de perdida
    #     if results[Constants.ACTION_ACUM] < 0:
    #         # es negativo
    #         # vericicar si bajo mas de lo esperado
    #         if results[Constants.ACUMULADO] >= self.closeAcumValue:
    #             print(
    #                 f"CERRAMOS MERCADO BUY action_acum: {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} BUY_CLOSE_ACUM profit:{results[Constants.ACTION_ACUM]} ")
    #             results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
    #             return
    #
    #     if results[Constants.ACTION_ACUM] < 0:
    #         # es negativo
    #         # vericicar si bajo mas de lo esperado
    #         if abs(results[Constants.ACTION_MAX_DIST]) >= self.closeAcumValue:
    #             print(
    #                 f"CERRAMOS MERCADO BUY action_acum: {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} BUY_CLOSE_ACUM profit:{results[Constants.ACTION_ACUM]} ")
    #             results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
    #             return
    #
    #     # # #CERRAMOS SI BAJO mucho
    #     # if results[Constants.ACUMULADO] <= 0:
    #     #     if results[Constants.ACUMULADO_ABS] >= (self.closeAcumValue):
    #     #         print(
    #     #             f"CERRAMOS MERCADO {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} BUY_ACTION_DIST01 {results[Constants.ACUMULADO]} profit:{self.closeAcumValue}")
    #     #         results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
    #     #         return
    #
    #     # cerramos si tenemos ganancias y baja closeAcumValue/2
    #     if results[Constants.ACTION_ACUM] > 0:
    #         if results[Constants.ACTION_ACUM] >= self.closeAcumValue:
    #             if results[Constants.ACUMULADO] <= 0:
    #                 if results[Constants.ACTION_MAX_DIST] >= (difference_optimized):
    #                     print(
    #                         f"CERRAMOS MERCADO BUY action_acum: {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} BUY_ACTION_PROFIT_DIST01 {results[Constants.ACTION_ACUM]} profit:{self.closeAcumValue}")
    #                     results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
    #                     return


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

        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.CLOSE_NXT_DOWN] = 0
                results[Constants.CLOSE_NXT_UP] = 0

        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
                results[Constants.CLOSE_NXT_UP] = 0

        if results[Constants.IND_BLG]== Constants.IND_BLG_MED_BUY:
            if results[Constants.ACTION_COUNT] > 5:
#                 print(
                    f"CERRAMOS MERCADO SELL action_acum: {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} SELL_CLOSE_ISBUY 01 profit:{results[Constants.ACTION_ACUM]} ")
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

        # # # #CERRAMOS SI SUBIO mucho
        # if results[Constants.ACTION_ACUM] > 0:
        #     if abs(results[Constants.ACTION_ACUM]) >= (self.closeAcumValue):
        #         print(
        #             f"CERRAMOS MERCADO {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} BUY_ACTION_DIST01 {results[Constants.ACUMULADO]} profit:{self.closeAcumValue}")
        #         results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
        #         return
        #
        # # CERRAMOS SI SALE DEL LOWER BLG
        # if results[Constants.IND_BLG_LOWER_DST_PERCENT] < 0:
        #     # HA pASADO EL LOWER HAY GANANCIAS
        #     if abs(results[Constants.IND_BLG_LOWER_DST_PERCENT]) > 1:
        #         print(
        #             f"CERRAMOS MERCADO {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} SELL_MAXIMO_01 {results[Constants.ACUMULADO]} profit:{self.closeAcumValue}")
        #         results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
        #         return

    def evaluarFlujoSELL(self, results, activeParam):
        difference_optimized = activeParam.difference
        unit_diff = 0
        # valores
        flujo_count = results[Constants.FLUJO_COUNT]

        difference_optimized, unit_diff = self.evaluarDifferenceSELL(results, activeParam, flujo_count)

#         print(
            f"DIFFERENCE_OPTIMIZED  evaluarFlujoSELL {difference_optimized} original {activeParam.difference} close difference {self.closeDifference} unit_diffb {unit_diff}")
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or
                        results[Constants.ACTION_MIN_DIST] >= (
                                difference_optimized * self.multiplicadorUP)):
                    # results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE

#                     print(
                        f" CERRAMOS MERCADO SELL_UP_BLG_01 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")

#                 print(f"EVALUO CLOSE_NXT_UP")
                results[Constants.CLOSE_NXT_DOWN] = 0
                results[Constants.CLOSE_NXT_UP] = 0
                # return
        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_BUY:
            if results[Constants.ACTION_ACUM] > 0:
                # esta en perdidas
                if results[Constants.ACUMULADO] >= self.closeDifference:
#                     print(
                        f"CERRAMOS MERCADO SELL action_acum: {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} SELL_CLOSE_ISBUY profit:{results[Constants.ACTION_ACUM]} ")
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
            elif results[Constants.ACTION_ACUM] < 0:
                # paso por med esta bajando tiene ganancias pero subio ya mucho
                nada = ""
                if results[Constants.ACTION_MIN_DIST] >= self.closeDifference:
#                     print(
                        f"CERRAMOS MERCADO SELL action_acum: {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} SELL_CLOSE_ISBUY01 profit:{results[Constants.ACTION_ACUM]} ")
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        # cerramos si llega al minimo admisible de perdida
        if results[Constants.ACTION_ACUM] > 0:
            # es negativo
            # vericicar si bajo mas de lo esperado
            if abs(results[Constants.ACTION_ACUM]) >= self.closeAcumValue:
#                 print(
                    f"CERRAMOS MERCADO SELL action_acum: {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} SELL_CLOSE_ACUM profit:{results[Constants.ACTION_ACUM]} ")
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

        # # #CERRAMOS SI BAJO mucho
        if results[Constants.ACUMULADO] > 0:
            if results[Constants.ACTION_MIN_DIST] >= (self.closeAcumValue):
#                 print(
                    f"CERRAMOS MERCADO SELL action_acum: {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} SELL_ACTION_DIST01 {results[Constants.ACUMULADO]} profit:{self.closeAcumValue}")
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

        # # cerramos si tenemos ganancias y baja closeAcumValue/2
        if results[Constants.ACTION_ACUM] < 0:
            if abs(results[Constants.ACTION_ACUM]) >= self.closeAcumValue:
                if results[Constants.ACUMULADO] > 0:
                    if results[Constants.ACTION_MIN_DIST] >= (difference_optimized):
#                         print(
                            f"CERRAMOS MERCADO SELL action_acum: {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} SELL_ACTION_PROFIT_DIST01 {results[Constants.ACTION_ACUM]} profit:{self.closeAcumValue}")
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return