from evaluators.CierreBase import CierreBase
from evaluators.EvaluatorBase import EvaluatorBase
from evaluators.AperturaBase import AperturaBase
from service.Constants import Constants


class EvaluatorIBLG_START_CLOSE_03(EvaluatorBase,AperturaBase,CierreBase):

    #tiene EMA MIN DST

    def __init__(self):
        #se añade cierre mas permisivo
        self.name = "EvaluatorIBLG_START_CLOSE_03"
        # self.name = "EvaluatorIBLG_START_CLOSE_02"
        # self.name = "EvaluatorIBLG_START_CLOSE_01"
        # self.name = "EvaluatorIBLG_LONG_04"




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

        self.accumulate = activeParam.accumulate
        self.angleUP = activeParam.angleUp
        self.angleDOWN = activeParam.angleDown


        self.midMinDst = 0.08
        self.emaMinDst = activeParam.emaMinDst

        results[Constants.EVAl_CLOSE_ACUM] = self.closeAcumValue
        results[Constants.EVAl_CLOSE_DIFF] = self.closeDifference
        results[Constants.EVAl_ACUM] = self.accumulate

        #SOLO EN LOS INTERVALOS definidos
        currentTime = self.gettime(results)
        intime = False
        if currentTime >= int(self.iniStart) and currentTime < int(self.iniEnd):
            intime = True
        if currentTime >= int(self.closeStart) and currentTime < int(self.closeEnd):
            intime = True

        if Constants.ONLY_START_END in results:
            if results[Constants.ONLY_START_END] == False:
                intime = True

        # #print(f'EVALUATOR  {self.name}   ACTIVO: {activeParam.name}')
        if results[Constants.CURRENT_ACTION] == Constants.ACTION_WAIT or results[
            Constants.CURRENT_ACTION] == Constants.ACTION_CLOSE:
            if intime:
                self.evaluarApertura(results, activeParam)
            else:
                print(f"FUERA DE HORARIO")
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
            print(f"ESTAMOS A LA ESPERA DE INDICADORES BUENOS")






    def evaluarAperturaDOWN(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0

        self.printDifference("evaluarAperturaDOWN", difference_optimized, self.closeAcumValue, self.closeDifference)

        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if (results[Constants.ACUMULADO_ABS] >= (difference_optimized) or
                        results[Constants.ACTION_MAX_DIST] >= (
                                difference_optimized)):
                    results[Constants.CLOSE_NXT_DOWN] = 0

        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if self.evalNXT_UP_05(results, activeParam, difference_optimized):
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                    name = "DOWN_BLG_NXTUP_BUY01"
                    self.printInicioLog(name, results, activeParam)
                    return

        res, action, num = self.evaluateDownOpen_start_close_02(results, activeParam)
        if res:
            if "SELL" in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                self.printInicioLog(f"SELL_DOWN_{num}", results, activeParam)
                return
            elif "BUY" in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                self.printInicioLog(f"BUY_DOWN_INV_{num}", results, activeParam)
                return



    def evaluarAperturaUP(
            self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0

        self.printDifference("evaluarAperturaUP", difference_optimized, self.closeAcumValue, self.closeDifference)

        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                # results[Constants.CLOSE_NXT_DOWN] = 0
                results[Constants.CLOSE_NXT_UP] = 0


        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
                # results[Constants.CLOSE_NXT_UP] = 0

        res, action, num = self.evaluateUpOpen_start_close_03(results, activeParam)
        if res:
            if "BUY" in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                self.printInicioLog(f"BUY_UP_BUY_{num}", results, activeParam)
                return
            elif "SELL" in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                self.printInicioLog(f"SELL_UP_BUY_{num}", results, activeParam)
                return




    def evaluarFlujoBUY_LONG(self, results, activeParam):
        difference_optimized = activeParam.difference
        unit_diff = 0
        flujo_count = results[Constants.FLUJO_COUNT]
        self.printDifference("evaluarFlujoBUY", difference_optimized, self.closeAcumValue, self.closeDifference,
                             self.accumulate)
        self.control_BUY_START_CLOSE_05(results, activeParam, self.closeAcumValue, self.closeDifference, self.accumulate)




    def evaluarFlujoSELL_LONG(self, results, activeParam):
        difference_optimized = activeParam.difference
        unit_diff = 0
        # valores
        flujo_count = results[Constants.FLUJO_COUNT]

        self.printDifference("evaluarFlujoSELL", difference_optimized, self.closeAcumValue, self.closeDifference,
                             self.accumulate)
        self.control_SELL_START_CLOSE_02(results, activeParam, self.closeAcumValue, self.closeDifference, self.accumulate)



