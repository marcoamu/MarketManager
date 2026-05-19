from evaluators.CierreBase import CierreBase
from evaluators.EvaluatorBase import EvaluatorBase
from evaluators.AperturaBase import AperturaBase
from service.Constants import Constants


class EvaluatorBOLLINGER_ONLY_UP_03_01(EvaluatorBase,AperturaBase,CierreBase):
    #se añaden los porcentages uppper y lower de blg

    #nuevos controles de aperturamrapida


    #basado en 06 intenta mejorar
    #las subidas cuando la tendencia es up que ignore el close nxt

    # añade
    # bollingerDst
    # reduce las reglas de apertura

    # mejora las reglas close_NXT

    # añade
    # blgLowerDist

    # refina CLOSE_NXT_UP
    # cambia INDICATOR_MED_MOMENT por MED

    # 5
    # refina mas las reglas de apertura
    # refina las reglas de close nxt

    def __init__(self):
        self.name = "EvaluatorBOLLINGER_ONLY_UP_03_01"
        # self.name = "EvaluatorBOLLINGER_ONLY_UP_03"
        # self.name = "EvaluatorBOLLINGER_ONLY_UP_02"
        # self.name = "EvaluatorBOLLINGER_ONLY_UP_01"
        # self.name = "EvaluatorBOLLINGER_07"
        # self.name = "EvaluatorBOLLINGER_05"
        # self.name = "EvaluatorBOLLINGER_04"
        # self.name = "EvaluatorBOLLINGER_03"
        # self.name = "EvaluatorBOLLINGER_02"
        # self.name = "EvaluatorBOLLINGER_01"
        # self.name = "EvaluatorEMA_01"
        # self.name = "EvaluatorPROBMEDSTD_CLEAN_Opt03_MEDDIFF_01"
        # self.name = "EvaluatorPROBMEDSTD_CLEAN_Opt03"


    def evaluate(self, results, activeParam):
        results[Constants.EVAl_NAME] = self.name
        self.updateTimeZoneValues(results)
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
        self.multiplicatorNXT= 1
        self.closeAcumValue = activeParam.closeProfit
        self.accumulate = activeParam.accumulate
        #valor para determinar si week es fuerte si esta bajo este valor es debil
        self.WEEK_FLOW_MINVAL =activeParam.weekDistanceSTDDistance

        self.medstdminDiff = activeParam.medstdminDiff
        self.medstdmaxDiff = activeParam.medstdmaxDiff

        #valuador para estado change por market tendence = True  o por indicator = False
        self.evaluateChangeMarketTendence = True

        self.BLGDist = activeParam.bollingerDst
        self.blgLowerDist =1.5
        self.blgDistPercent = activeParam.blgDistPercent

        self.closeBollingerValue = activeParam.bollingerClose
        self.closeProfit = activeParam.closeProfit
        self.closeDifference = activeParam.difference + (activeParam.difference * 0.20)

        # if self.closeBollingerValue > activeParam.accumulate:
        #     self.closeBollingerValue = activeParam.difference + (activeParam.difference * 0.20)

        self.flujo_Count = 2#camtidad de acciones desde la compra o venta
        # SOLO EN LOS INTERVALOS definidos
        currentTime = self.gettime(results)
        intime = False

        #print(f'EVALUATOR  {self.name}   ACTIVO: {activeParam.name}')
        if currentTime >= int(self.iniStart) and currentTime < int(self.iniEnd):
            intime = True
        if currentTime >= int(self.closeStart) and currentTime < int(self.closeEnd):
            intime = True

        if Constants.ONLY_START_END in results:
            if results[Constants.ONLY_START_END] == False:
                intime = True

        if results[Constants.CURRENT_ACTION] == Constants.ACTION_WAIT or results[
            Constants.CURRENT_ACTION] == Constants.ACTION_CLOSE:
            # self.evaluarApertura(results, activeParam)

            if intime:
            # self.evaluarApertura(results, activeParam)
                self.evaluarAperturaEMA(results, activeParam)
            else:
                print(f"FUERA DE HORARIO")
        elif results[Constants.CURRENT_ACTION] == Constants.ACTION_BUY:
            self.evaluarFlujoBUY(results, activeParam)
        elif results[Constants.CURRENT_ACTION] == Constants.ACTION_SELL:
            nada=""
            # self.evaluarFlujoSELL(results, activeParam)


    def evaluarAperturaEMA(self, results, activeParam):
        #
        # valores
        flujo_count = results[Constants.FLUJO_COUNT]

        if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_BUY:
            self.evaluarAperturaUP(results, activeParam, flujo_count)
        elif results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
            self.evaluarAperturaDOWN(results, activeParam, flujo_count)
        elif results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_WAIT:
            print("EMA WAIT")
            self.evaluarAperturaCHANGE(results, activeParam, flujo_count)
        else:
            print(f"ESTAMOS A LA ESPERA DE INDICADORES BUENOS")



    def evaluarAperturaCHANGE(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0
        multiplicador = 2
        # difference_optimized, unit_diff = self.evaluarAperturaCHANGEDifference(results, activeParam, flujo_count)

        self.printDifference("evaluarAperturaDOWN", difference_optimized, self.closeAcumValue, self.closeDifference)

        if results[Constants.CLOSE_NXT_DOWN]==1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
                results[Constants.CLOSE_NXT_UP] = 0
                return






    def evaluarAperturaDOWN(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0

        # difference_optimized, unit_diff = self.evaluarAperturaDOWNDifference(results, activeParam, flujo_count)

        self.printDifference("evaluarAperturaDOWN", difference_optimized, self.closeAcumValue, self.closeDifference)

        if results[Constants.CLOSE_NXT_DOWN]==1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] =0

                return
        if results[Constants.CLOSE_NXT_UP]==1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
                    # if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
                        if results[Constants.IND_BLG_LOWER_DST]<self.blgLowerDist:
                            # results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                            # print(
                            #     f" INICIO MERCADO {results[Constants.DATE].values[0]} DOWN_BLG_NXTUP_SELL02 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} IND_BLG_UPPER_DST_PERCENT: {results[Constants.IND_BLG_UPPER_DST_PERCENT]} angle: {results[Constants.ANGLE]} direction {results[Constants.DIRECTION]} INDICATOR_MED_MOMENT {results[Constants.INDICATOR_MED_MOMENT]} ")
                            # results[Constants.CLOSE_NXT_DOWN] = 0
                            results[Constants.CLOSE_NXT_UP] = 0
                            return


                elif results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_UP:
                    if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
                        if results[Constants.DIRECTION] == Constants.DIR_UP or results[
                            Constants.DIRECTION] == Constants.DIR_PRE_UP or results[
                                            Constants.DIRECTION] == Constants.DIR_CHANGE:
                            if results[Constants.IND_BLG_UPPER_DST_PERCENT] > self.blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] <0:

                                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                self.printInicioLog("DOWN_NXT_DOWN_02", results, activeParam)

                        results[Constants.CLOSE_NXT_DOWN] = 0
                        # results[Constants.CLOSE_NXT_UP] = 0
                        return

        res, action, num = self.evaluateDownOpen_EMA_OUP_03(results, activeParam)
        if res:
            if "BUY" in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                self.printInicioLog(f"BUY_DOWN_BUY_{num}", results, activeParam)
                return
            # elif "SELL" in action:
            #     results[Constants.NEW_ACTION] = Constants.ACTION_SELL
            #     self.printInicioLog(f"SELL_DOWN_SELL_{num}", results, activeParam)
            #     return






    def evaluarAperturaUP(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0

        self.printDifference("evaluarAperturaUP", difference_optimized, self.closeAcumValue, self.closeDifference)

        if results[Constants.CLOSE_NXT_UP]==1:
            print(f"ENTRO CLOSE_NXT_UP")
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
                    if results[Constants.INDICATOR_EMA]==Constants.INDICATOR_EMA_BUY:
                        nada =""
                        # results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                        # print(
                        #     f" INICIO MERCADO {results[Constants.DATE].values[0]} UP_BLG_NXTUP_SELL01 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} IND_BLG_UPPER_DST_PERCENT: {results[Constants.IND_BLG_UPPER_DST_PERCENT]} angle: {results[Constants.ANGLE]} direction {results[Constants.DIRECTION]} INDICATOR_MED_MOMENT {results[Constants.INDICATOR_MED_MOMENT]} ")

                    # results[Constants.CLOSE_NXT_DOWN] =0
                    results[Constants.CLOSE_NXT_UP] =0
                    return
                elif results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_UP:
                    if results[Constants.INDICATOR_EMA]==Constants.INDICATOR_EMA_SELL:
                        if results[Constants.IND_BLG_UPPER_DST_PERCENT] > self.blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] <0:
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            self.printInicioLog("UP_NXT_UP_02", results, activeParam)


                # results[Constants.CLOSE_NXT_DOWN] =0
                results[Constants.CLOSE_NXT_UP] =0

        if results[Constants.CLOSE_NXT_DOWN]==1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
                results[Constants.CLOSE_NXT_UP] = 0
                if results[Constants.INDICATOR_MED_MOMENT] == Constants.INDICATOR_TM_UP:
                    multiplicator = self.multiplicadorUP * self.multiplicatorNXT
                    print(f"multiplicator {self.multiplicatorNXT}")
                else:
                    multiplicator = self.multiplicadorUP
                    print(f"multiplicator 1")

                print(f"new difference {difference_optimized * multiplicator}")

                if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicator) or
                        results[Constants.ACTION_MAX_DIST] >= (
                                difference_optimized * multiplicator)):
                    if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
                        # results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                        results[Constants.CLOSE_NXT_DOWN] =0
                        # print(
                        #     f" INICIO MERCADO {results[Constants.DATE].values[0]} UP_BLG_SELL acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} IND_BLG_UPPER_DST_PERCENT: {results[Constants.IND_BLG_UPPER_DST_PERCENT]} angle: {results[Constants.ANGLE]} direction {results[Constants.DIRECTION]} INDICATOR_MED_MOMENT {results[Constants.INDICATOR_MED_MOMENT]} ")
                        # return
                    elif results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_UP:
                        nada = ""
                        #esta en racha dejamos un poco mas
                        # if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or
                        #         results[Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP)):
                        if results[Constants.IND_BLG_UPPER_DST_PERCENT] > self.blgDistPercent or results[Constants.IND_BLG_UPPER_DST_PERCENT] <0:
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            self.printInicioLog("UP_NXT_DOWN_01", results, activeParam)

                            # results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            results[Constants.CLOSE_NXT_DOWN] = 0
                            # print(
                            #     f" INICIO MERCADO {results[Constants.DATE].values[0]} UP_BLG_BUY2 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} IND_BLG_UPPER_DST_PERCENT: {results[Constants.IND_BLG_UPPER_DST_PERCENT]} angle: {results[Constants.ANGLE]} direction {results[Constants.DIRECTION]} INDICATOR_MED_MOMENT {results[Constants.INDICATOR_MED_MOMENT]} ")
                        # return

        res, action, num = self.evaluateUpOpen_EMA_OUP_04(results, activeParam)
        if res:
            if "BUY" in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                self.printInicioLog(f"BUY_UP_BUY_{num}", results, activeParam)
                return
            elif "SELL" in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                self.printInicioLog(f"SELL_UP_SELL_{num}", results, activeParam)
                return




    def evaluarFlujoBUY(self, results, activeParam):
        # CONTROL LIMITES MAXIMOS
        difference_optimized = activeParam.difference
        unit_diff = 0
        flujo_count = results[Constants.FLUJO_COUNT]

        self.printDifference("evaluarFlujoBUY", difference_optimized, self.closeAcumValue, self.closeDifference,
                             self.accumulate)
        self.control_BUY_EMA_OUP_04(results, activeParam, self.closeAcumValue, self.closeDifference)






