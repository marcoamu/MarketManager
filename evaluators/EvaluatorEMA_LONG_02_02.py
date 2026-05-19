from evaluators.CierreBase import CierreBase
from evaluators.EvaluatorBase import EvaluatorBase
from evaluators.AperturaBase import AperturaBase
from service.Constants import Constants


class EvaluatorEMA_LONG_02_02(EvaluatorBase,AperturaBase,CierreBase):

    # añade
    # bollingerDst
    # reduce las reglas de apertura

    # mejora las reglas close_NXT

    #añade
    #blgLowerDist

    # refina CLOSE_NXT_UP
    # cambia INDICATOR_MED_MOMENT por MED



    def __init__(self):
        self.name = "EvaluatorEMA_LONG_02_02"
        # self.name = "EvaluatorEMA_LONG_01"
        # self.name = "EvaluatorBOLLINGER_LARGE_01"
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
        #valor para determinar si week es fuerte si esta bajo este valor es debil
        self.WEEK_FLOW_MINVAL =activeParam.weekDistanceSTDDistance

        self.medstdminDiff = activeParam.medstdminDiff
        self.medstdmaxDiff = activeParam.medstdmaxDiff

        #valuador para estado change por market tendence = True  o por indicator = False
        self.evaluateChangeMarketTendence = True

        self.BLGDist = activeParam.bollingerDst
        self.blgLowerDist =1.5
        self.blgLowerDistPercemt =10
        self.bollingerClose =activeParam.bollingerClose

        self.closeAcumValue = activeParam.closeProfit
        self.closeDifference = activeParam.difference + (activeParam.difference * 0.10)
        self.accumulate = activeParam.accumulate
        self.angleUP = activeParam.angleUp
        self.angleDOWN = activeParam.angleDown

        results[Constants.EVAl_CLOSE_ACUM] = self.closeAcumValue
        results[Constants.EVAl_CLOSE_DIFF] = self.closeDifference
        results[Constants.EVAl_ACUM] = self.accumulate

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
            if intime:
            # self.evaluarApertura(results, activeParam)
                self.evaluarAperturaEMA(results, activeParam)
            else:
#                 print(f"FUERA DE HORARIO")
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
        elif results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
            self.evaluarAperturaDOWN(results, activeParam, flujo_count)
        elif results[Constants.IND_BLG] == Constants.IND_BLG_MED_WAIT:
#             print("EMA WAIT")
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





    def evaluarAperturaDOWN(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0

        self.printDifference("evaluarAperturaDOWN", difference_optimized, self.closeAcumValue, self.closeDifference)

        if results[Constants.CLOSE_NXT_DOWN]==1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] =0
                # results[Constants.CLOSE_NXT_UP] =0
                # results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                # self.printInicioLog("DOWN_NXT_DOWN_01", results, activeParam)
                # return
        if results[Constants.CLOSE_NXT_UP]==1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
                    if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
                        if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= activeParam.blgDistPercent:
                            nada = ""
                            # results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                            # self.printInicioLog("DOWN_NXT_DOWN_02", results, activeParam)
                            # return
                        else:
                            nada = ""
                            # results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            # self.printInicioLog("DOWN_NXT_UP_02", results, activeParam)
                            # return


                # elif results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_UP:
                #     if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
                #         results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                #         self.printInicioLog("DOWN_NXT_UP_03", results, activeParam)
                #         return

        res, action, num = self.evaluateDownOpen_EMA_04(results, activeParam)
        if res:
            if "BUY" in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                self.printInicioLog(f"BUY_DOWN_BUY_{num}", results, activeParam)
                return
            elif "SELL" in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                self.printInicioLog(f"SELL_DOWN_SELL_{num}", results, activeParam)
                return



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

        if results[Constants.CLOSE_NXT_UP]==1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
                    if results[Constants.INDICATOR_EMA]==Constants.INDICATOR_EMA_BUY:
                        nada = ""
                        # results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                        # self.printInicioLog("UP_NXT_DOWN_01", results, activeParam)
                        # return

                    # results[Constants.CLOSE_NXT_DOWN] =0
                    results[Constants.CLOSE_NXT_UP] =0

                elif results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_UP:
                    if results[Constants.INDICATOR_EMA]==Constants.INDICATOR_EMA_SELL:
                        nada = ""
                        # results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        # self.printInicioLog("UP_NXT_UP_02", results, activeParam)
                        # return

            # results[Constants.CLOSE_NXT_DOWN] =0
            results[Constants.CLOSE_NXT_UP] =0

        if results[Constants.CLOSE_NXT_DOWN]==1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
                    # results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                    results[Constants.CLOSE_NXT_DOWN] =0
                    # self.printInicioLog("UP_NXT_DOWN_02", results, activeParam)
                    # return
                elif results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_UP:
                    # results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                    results[Constants.CLOSE_NXT_DOWN] = 0
                    # self.printInicioLog("UP_NXT_DOWN_03", results, activeParam)
                    # return

        res, action, num = self.evaluateUpOpen_EMA_05(results, activeParam)
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
        self.control_BUY_EMA_02(results, activeParam, self.closeAcumValue, self.closeDifference)






    def evaluarFlujoSELL(self, results, activeParam):
        difference_optimized = activeParam.difference
        unit_diff = 0
        # valores
        flujo_count = results[Constants.FLUJO_COUNT]

        self.printDifference("evaluarFlujoSELL", difference_optimized, self.closeAcumValue, self.closeDifference,
                             self.accumulate)
        self.control_SELL_EMA_01(results, activeParam, self.closeAcumValue, self.closeDifference)

