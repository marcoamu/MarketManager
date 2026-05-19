from evaluators.CierreBase import CierreBase
from evaluators.EvaluatorBase import EvaluatorBase
from evaluators.AperturaBase import AperturaBase
from service.Constants import Constants


class EvaluatorIBLG_ANGLE_ONLY_UP_05_test02(EvaluatorBase,AperturaBase,CierreBase):

    def __init__(self):
        #se añade cierre mas permisivo
        #se añade ontrol de apertura nxt up usando angleFlow
        self.name = "EvaluatorIBLG_ANGLE_ONLY_UP_05_test02"
        # self.name = "EvaluatorIBLG_ANGLE_ONLY_UP_04"
        # self.name = "EvaluatorIBLG_ANGLE_ONLY_UP_03"
        # self.name = "EvaluatorIBLG_ANGLE_ONLY_UP_00"


    def cambios(self):
        nada =""
        # 21-05-2024
            # -aperturaAngle_01


    def evaluate(self, results, activeParam):
        results[Constants.EVAl_NAME] = self.name

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
        self.minAngleIma1 = activeParam.minAngleIma1
        self.closeDifference = activeParam.difference + (activeParam.difference * 0.80)
        self.accumulate = activeParam.accumulate

        results[Constants.EVAl_CLOSE_ACUM] = self.closeAcumValue
        results[Constants.EVAl_CLOSE_DIFF] = self.closeDifference
        results[Constants.EVAl_ACUM] = self.accumulate

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
            print(f"ESTAMOS A LA ESPERA DE INDICADORES BUENOS")




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
        self.printDifference("evaluarAperturaDOWN", difference_optimized, self.closeAcumValue, self.closeDifference)

        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or
                        results[Constants.ACTION_MAX_DIST] >= (
                                difference_optimized * self.multiplicadorUP)):
                    results[Constants.CLOSE_NXT_DOWN] = 0
                    # results[Constants.CLOSE_NXT_UP] = 0

        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                # results[Constants.CLOSE_NXT_UP] = 0
                # results[Constants.CLOSE_NXT_DOWN] = 0
                res, num = self.evalNXT_UP_04(results, activeParam, difference_optimized)
                if res:
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                    name = f"DOWN_BLG_NXTUP_BUY_{num}"
                    self.printInicioLog(name, results, activeParam)
                    return


        if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
            Constants.ACTION_MAX_DIST] >= (difference_optimized):

            if self.enableControlOpen:
                if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
                    nada = ""

            else:
                if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= self.blgDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT] ==0:
                    if abs(results[Constants.MEDSTDDIFF]) > self.medstdminDiff:
                        nada = ""

                elif results[Constants.IND_BLG_LOWER_DST_PERCENT] < self.blgDistPercent or results[Constants.IND_BLG_LOWER_DST_PERCENT]==0:
                    nada=""

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

    def OpenRule_WEEK_ANGLE_01(self,results, activeParam):
        res = True
        if results[Constants.WEEK_DIR_BOT_DST] >= activeParam.maxWeekBootDist:
            if results[Constants.ANGLE_COUNTER] < activeParam.maxOpenCount:
                res = False
        return res

    def evaluarAperturaUP(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0

        difference_optimized, unit_diff = self.evaluarDifferenceUP(results, activeParam, flujo_count)
        self.printDifference("evaluarAperturaUP",difference_optimized,self.closeAcumValue,self.closeDifference)

        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or
                        results[Constants.ACTION_MIN_DIST] >= (
                                difference_optimized * self.multiplicadorUP)):
                    # results[Constants.CLOSE_NXT_DOWN] = 0
                    results[Constants.CLOSE_NXT_UP] = 0

        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or
                        results[Constants.ACTION_MAX_DIST] >= (
                                difference_optimized * self.multiplicadorUP)):
                    results[Constants.CLOSE_NXT_DOWN] = 0
                    # results[Constants.CLOSE_NXT_UP] = 0

        res, option = self.evaluateUpOpen_05(results, activeParam)
        if res:
            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
            self.printInicioLog(f"BUY_UP_BUY0{option}", results, activeParam)
            return


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
                        print(f"CORRECTION BUY DOWN COUNT")
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
        flujo_count = results[Constants.FLUJO_COUNT]
        name ="evaluarFlujoBUY_LONG"
        difference_optimized, unit_diff = self.evaluarDifferenceBUY(results, activeParam, flujo_count)

        self.printDifference("evaluarFlujoBUY_LONG", difference_optimized, self.closeAcumValue, self.closeDifference, self.accumulate)
        self.control_BUY_LONG_ONLYUP_02(results,activeParam,self.closeAcumValue,self.closeDifference,self.accumulate)




        # self.control_BUY_START_CLOSE_03(results, activeParam, self.closeAcumValue, self.closeDifference)

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
            print(f"estamos en WAIT no hay indicadores de diferencia")

        if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
            if results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_UP:
                if flujo_count > 1:
                    unit_diff = activeParam.unit * (flujo_count - 1)
                    unit_diff = unit_diff * -1
            elif results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_DOWN:
                if results[Constants.INDICATOR] == Constants.INDICATOR_SELL:
                    # intentar cerrar si sube y esta en sell ( no sellX)
                    if flujo_count > 2:
                        print(f"CORRECTION SELL UP COUNT")
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
        flujo_count = results[Constants.FLUJO_COUNT]
        difference_optimized, unit_diff = self.evaluarDifferenceBUY(results, activeParam, flujo_count)
        self.printDifference("evaluarFlujoSELL_LONG", difference_optimized, self.closeAcumValue, self.closeDifference)

        self.control_SELL_LONG_ONLYUP_02(results, activeParam, self.closeAcumValue, self.closeDifference,
                                        self.accumulate)

