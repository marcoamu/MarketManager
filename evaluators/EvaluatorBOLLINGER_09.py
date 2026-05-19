from evaluators.CierreBase import CierreBase
from evaluators.EvaluatorBase import EvaluatorBase
from evaluators.AperturaBase import AperturaBase
from service.Constants import Constants


class EvaluatorBOLLINGER_09(EvaluatorBase,AperturaBase,CierreBase):

    def __init__(self):
        self.name = "EvaluatorBOLLINGER_09"
        # self.name = "EvaluatorBOLLINGER_01"
        # self.name = "EvaluatorEMA_01"
        # self.name = "EvaluatorPROBMEDSTD_CLEAN_Opt03_MEDDIFF_01"
        # self.name = "EvaluatorPROBMEDSTD_CLEAN_Opt03"


    def evaluate(self, results, activeParam):
        results[Constants.EVAl_NAME] = self.name

        # MULTIPLICADORES
        #para cerrar cuanto antes se usa para cuando el valor es negativo mas pequeño cierra mas rapido
        # self.multiplicatorClose = activeParam.difference-(activeParam.difference/3)
        self.multiplicatorClose = activeParam.difference*1.2
        self.multiplicatorPREVIUS = activeParam.difference * 1.2
        #control para ver si abre cuando ya hay una cantidad X usada
        self.enableControlOpen = False
        self.multiplicadorOpen = 1
        #usado para abrir en tendencia inversa
        self.multiplicadorUP= 1
        #valor para determinar si week es fuerte si esta bajo este valor es debil
        self.WEEK_FLOW_MINVAL =activeParam.weekDistanceSTDDistance

        self.medstdminDiff = activeParam.medstdminDiff
        self.medstdmaxDiff = activeParam.medstdmaxDiff

        #valuador para estado change por market tendence = True  o por indicator = False
        self.evaluateChangeMarketTendence = True

        self.closeAcumValue = activeParam.closeProfit
        # if self.closeAcumValue > activeParam.accumulate:
        #     self.closeAcumValue = activeParam.difference + (activeParam.difference * 0.20)

        self.flujo_Count = 2#camtidad de acciones desde la compra o venta

        #print(f'EVALUATOR  {self.name}   ACTIVO: {activeParam.name}')
        if results[Constants.CURRENT_ACTION] == Constants.ACTION_WAIT or results[
            Constants.CURRENT_ACTION] == Constants.ACTION_CLOSE:
            # self.evaluarApertura(results, activeParam)
            self.evaluarAperturaEMA(results, activeParam)
        elif results[Constants.CURRENT_ACTION] == Constants.ACTION_BUY:
            self.evaluarFlujoBUY(results, activeParam)
        elif results[Constants.CURRENT_ACTION] == Constants.ACTION_SELL:
            self.evaluarFlujoSELL(results, activeParam)

    def evaluarApertura(self, results, activeParam):
        #
        # valores
        flujo_count = results[Constants.FLUJO_COUNT]

        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_BUY:
            self.evaluarAperturaUP(results, activeParam, flujo_count)
        # if results[Constants.INDICATOR_EMA] == Constants.DIR_PRE_UP:
        #     nada = ""
        #     # print(f"DIFFERENCE_OPTIMIZED evaluarAperturaPREUP  NADA")
        #     # self.evaluarAperturaPREUP(results, activeParam, flujo_count)
        elif results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
            self.evaluarAperturaDOWN(results, activeParam, flujo_count)
        # elif results[Constants.IND_PROB_FLOW] == Constants.DIR_PRE_DOWN:
        #     nada = ""
        #     # print(f"DIFFERENCE_OPTIMIZED evaluarAperturaPREDOWN  NADA")
        #     self.evaluarAperturaPREDOWN(results, activeParam, flujo_count)
        elif results[Constants.IND_BLG] == Constants.IND_BLG_MED_WAIT:
#             print("EMA WAIT")
            # self.evaluarAperturaCHANGE(results, activeParam, flujo_count)
        else:
#             print(f"ESTAMOS A LA ESPERA DE INDICADORES BUENOS")
    def evaluarAperturaEMA(self, results, activeParam):
        #
        # valores
        flujo_count = results[Constants.FLUJO_COUNT]

        if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_BUY:
            self.evaluarAperturaUP(results, activeParam, flujo_count)
        elif results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
            self.evaluarAperturaDOWN(results, activeParam, flujo_count)
        elif results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_WAIT:
#             print("EMA WAIT")
            # self.evaluarAperturaCHANGE(results, activeParam, flujo_count)
        else:
#             print(f"ESTAMOS A LA ESPERA DE INDICADORES BUENOS")

    def evaluarAperturaCHANGEDifference(self, results, activeParam, flujo_count):
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
        elif results[Constants.MARKET_TENDENCE] == Constants.INDICATOR_SELLX:
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



    def evaluarAperturaDOWNDifference(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0
        if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
            if flujo_count >= 1:
                unit_diff = activeParam.unit * (flujo_count)
                unit_diff = unit_diff * -1
            # else:
            #     difference_optimized = activeParam.difference / 2



        difference_optimized = difference_optimized + unit_diff
        return difference_optimized, unit_diff

    def evaluarAperturaPREDOWNDifference(self, results, activeParam, flujo_count):
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
        if results[Constants.CLOSE_NXT_DOWN]==1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                results[Constants.CLOSE_NXT_DOWN] =0
                results[Constants.CLOSE_NXT_UP] =0
#                 print(
                    f" INICIO MERCADO DOWN_BLG_SELL acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")
                return
        if results[Constants.CLOSE_NXT_UP]==1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:

                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                results[Constants.CLOSE_NXT_UP] = 0
#                 print(
                    f" INICIO MERCADO DOWN_BLG_BUY acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")
                return
        # if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
        if self.enableControlOpen:
            if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
                    results[Constants.NEW_ACTION] = Constants.ACTION_SELL
#                     print(f" INICIO MERCADO DOWN_DOWN_SELL01 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")
        else:
            difOpenHours = self.getDifTimeFromOpen(results)
#             print(f"difOpenHours {difOpenHours}")
            if difOpenHours <= 60:
                if results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_DOWN:
                    if self.getProbFlow(results,activeParam)==Constants.DIR_DOWN:
                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
#                         print(f" INICIO MERCADO DOWN_PROB_SELL02 acum: ")
            else:
                if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or
                        results[Constants.ACTION_MAX_DIST] >= (
                                difference_optimized * self.multiplicadorUP)):
                    if results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_DOWN:
                        if (abs(results[Constants.MEDSTDDIFF]) > self.medstdminDiff or abs(results[Constants.MEDSTDDIFF]) ==0) and abs(results[Constants.MEDSTDDIFF]) < self.medstdmaxDiff:
                            if results[Constants.INDICATOR_MED_MOMENT]==Constants.INDICATOR_TM_DOWN:
                                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
#                                 print(f" INICIO MERCADO DOWN_DOWN_SELL03 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")






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

        if results[Constants.CLOSE_NXT_UP]==1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                results[Constants.CLOSE_NXT_DOWN] =0
                results[Constants.CLOSE_NXT_UP] =0
#                 print(
                    f" INICIO MERCADO UP_BLG_UP acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")
                return
        if results[Constants.CLOSE_NXT_DOWN]==1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if results[Constants.INDICATOR_MED_MOMENT] == Constants.INDICATOR_TM_DOWN:
                    results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                    results[Constants.CLOSE_NXT_DOWN] =0
#                     print(
                        f" INICIO MERCADO UP_BLG_SELL acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")
                    return
                elif results[Constants.INDICATOR_MED_MOMENT] == Constants.INDICATOR_TM_UP:
                    #esta en racha dejamos un poco mas
                    if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or
                            results[Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP)):
                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                        results[Constants.CLOSE_NXT_DOWN] = 0
#                         print(
                            f" INICIO MERCADO UP_BLG_SELL2 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")
                        return
        # if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
        if self.enableControlOpen:
            # if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
#             print(f" INICIO MERCADO UP_UP_BUY01 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")
        else:
            #para abrir sin restricciones ya que es inicio mercado
            difOpenHours = self.getDifTimeFromOpen(results)
            if difOpenHours <=20:
                if results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_UP:
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
#                     print(f" INICIO MERCADO UP_UP_BUY02 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")
            else:
                # if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or
                #     results[Constants.ACTION_MIN_DIST] >= (difference_optimized * self.multiplicadorUP)):
                    # if abs(results[Constants.PREVIOUS_DIST]) <= (
                    #         difference_optimized * self.multiplicadorUP):
                        if (abs(results[Constants.MEDSTDDIFF]) > self.medstdminDiff or abs(results[Constants.MEDSTDDIFF]) ==0) and abs(results[Constants.MEDSTDDIFF]) < self.medstdmaxDiff:
                        # if results[Constants.RELATIVE]== Constants.INDICATOR_RELATIVE_UP or results[Constants.RELATIVE]== Constants.INDICATOR_RELATIVE_DOWN_CHANGE:
                            if results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_UP:
                                if results[Constants.INDICATOR_MED_MOMENT] == Constants.INDICATOR_TM_UP:
                                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
#                                     print(f" INICIO MERCADO UP_UP_BUY03 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")


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

    def evaluarFlujoBUY(self, results, activeParam):
        # CONTROL LIMITES MAXIMOS
        difference_optimized = activeParam.difference
        unit_diff = 0
        flujo_count = results[Constants.FLUJO_COUNT]

        difference_optimized, unit_diff = self.evaluarDifferenceBUY(results, activeParam, flujo_count)

#         print(
            f"DIFFERENCE_OPTIMIZED  evaluarFlujoBUY {difference_optimized} original {activeParam.difference} unit_diffb {unit_diff}")
        if results[Constants.CLOSE_NXT_DOWN]==1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                results[Constants.CLOSE_NXT_DOWN] =0
                results[Constants.CLOSE_NXT_UP] =0
#                 print(
                    f" CERRAMOS MERCADO BUY_DOWN_BLG_01 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")
                return

        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
            if results[Constants.ACTION_ACUM] < 0 or results[Constants.ACUMULADO] <= 0:
#                 print(
                    f"CERRAMOS MERCADO BUY_CLOSE_ISSELL profit:{results[Constants.ACTION_ACUM]} ")
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return
        # cerramos si llega al minimo admisible de perdida
        if results[Constants.ACTION_ACUM] < 0:
            # es negativo
            # vericicar si bajo mas de lo esperado
            if abs(results[Constants.ACTION_ACUM]) >= self.closeAcumValue:
#                 print(
                    f"CERRAMOS MERCADO BUY_CLOSE_ACUM profit:{results[Constants.ACTION_ACUM]} ")
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

        if results[Constants.ACTION_ACUM] < 0:
            # es negativo
            # vericicar si bajo mas de lo esperado
            if abs(results[Constants.ACTION_ACUM]) >= self.closeAcumValue:
#                 print(
                    f"CERRAMOS MERCADO BUY_CLOSE_ACUM profit:{results[Constants.ACTION_ACUM]} ")
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

        # #CERRAMOS SI BAJO mucho
        if results[Constants.ACUMULADO] <= 0:
            if results[Constants.ACUMULADO_ABS] >= (self.closeAcumValue):
#                 print(
                    f"CERRAMOS MERCADO BUY_ACTION_DIST01 {results[Constants.ACUMULADO]} profit:{self.closeAcumValue}")
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

        # # cerramos si tenemos ganancias y baja closeAcumValue/2
        # if results[Constants.ACTION_ACUM] > 0:
        #     if results[Constants.ACTION_ACUM] >= self.closeAcumValue * 2:
        #         if results[Constants.ACUMULADO] <= 0:
        #             if results[Constants.ACUMULADO_ABS] >= (self.closeAcumValue / 2):
        #                 print(
        #                     f"CERRAMOS MERCADO BUY_ACTION_PROFIT_DIST01 {results[Constants.ACTION_ACUM]} profit:{self.closeAcumValue}")
        #                 results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
        #                 return

    def evaluarDifferenceSELL(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0

        if results[Constants.INDICATOR_TENDENCE] != Constants.INDICATOR_T_WAIT:
            if results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_UP:
                difference_optimized = activeParam.difference - (activeParam.difference / 3)
            elif results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_DOWN:
                difference_optimized = activeParam.difference + (activeParam.difference / 4)
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
                        unit_diff = activeParam.unit * (flujo_count) * 1.3
                        unit_diff = unit_diff * -1
            else:
                # wait
                if flujo_count > 2:
                    unit_diff = activeParam.unit * (flujo_count) * 1.3
                    unit_diff = unit_diff * -1

        difference_optimized = difference_optimized + unit_diff
        return difference_optimized, unit_diff

    def evaluarFlujoSELL(self, results, activeParam):
        difference_optimized = activeParam.difference
        unit_diff = 0
        # valores
        flujo_count = results[Constants.FLUJO_COUNT]

        difference_optimized, unit_diff = self.evaluarDifferenceSELL(results, activeParam, flujo_count)

#         print(
            f"DIFFERENCE_OPTIMIZED  evaluarFlujoSELL {difference_optimized} original {activeParam.difference} unit_diffb {unit_diff}")

        if results[Constants.CLOSE_NXT_UP]==1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                results[Constants.CLOSE_NXT_DOWN] =0
                results[Constants.CLOSE_NXT_UP] =0
#                 print(
                    f" CERRAMOS MERCADO SELL_UP_BLG_01 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")
                return

        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_BUY:
            if results[Constants.ACTION_ACUM] > 0 or results[Constants.ACUMULADO] > 0:
#                 print(
                    f"CERRAMOS MERCADO SELL_CLOSE_ISBUY profit:{results[Constants.ACTION_ACUM]} ")
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

        # cerramos si llega al minimo admisible de perdida
        if results[Constants.ACTION_ACUM] > 0:
            # es negativo
            # vericicar si bajo mas de lo esperado
            if abs(results[Constants.ACTION_ACUM]) >= self.closeAcumValue:
#                 print(
                    f"CERRAMOS MERCADO SELL_CLOSE_ACUM profit:{results[Constants.ACTION_ACUM]} ")
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

        # #CERRAMOS SI BAJO mucho
        if results[Constants.ACUMULADO] > 0:
            if results[Constants.ACUMULADO_ABS] >= (self.closeAcumValue):
#                 print(
                    f"CERRAMOS MERCADO SELL_ACTION_DIST01 {results[Constants.ACUMULADO]} profit:{self.closeAcumValue}")
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

        # # cerramos si tenemos ganancias y baja closeAcumValue/2
        # if results[Constants.ACTION_ACUM] < 0:
        #     if abs(results[Constants.ACTION_ACUM]) >= self.closeAcumValue * 2:
        #         if results[Constants.ACUMULADO] > 0:
        #             if results[Constants.ACUMULADO_ABS] >= (self.closeAcumValue / 2):
        #                 print(
        #                     f"CERRAMOS MERCADO SELL_ACTION_PROFIT_DIST01 {results[Constants.ACTION_ACUM]} profit:{self.closeAcumValue}")
        #                 results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
        #                 return