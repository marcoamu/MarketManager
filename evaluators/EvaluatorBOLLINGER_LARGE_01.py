from evaluators.CierreBase import CierreBase
from evaluators.EvaluatorBase import EvaluatorBase
from evaluators.AperturaBase import AperturaBase
from service.Constants import Constants


class EvaluatorBOLLINGER_LARGE_01(EvaluatorBase,AperturaBase,CierreBase):

    # añade
    # bollingerDst
    # reduce las reglas de apertura

    # mejora las reglas close_NXT

    #añade
    #blgLowerDist

    # refina CLOSE_NXT_UP
    # cambia INDICATOR_MED_MOMENT por MED



    def __init__(self):
        self.name = "EvaluatorBOLLINGER_LARGE_01"
        # self.name = "EvaluatorBOLLINGER_04"
        # self.name = "EvaluatorBOLLINGER_03"
        # self.name = "EvaluatorBOLLINGER_02"
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

        self.BLGDist = activeParam.bollingerDst
        self.blgLowerDist =1.5
        self.bollingerClose =activeParam.bollingerClose

        self.closeAcumValue = activeParam.closeProfit
        # if self.closeAcumValue > activeParam.accumulate:
        #     self.closeAcumValue = activeParam.difference + (activeParam.difference * 0.20)

        self.flujo_Count = 2#camtidad de acciones desde la compra o venta

        print(f'EVALUATOR  {self.name}   ACTIVO: {activeParam.name}')
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
            print("EMA WAIT")
            # self.evaluarAperturaCHANGE(results, activeParam, flujo_count)
        else:
            print(f"ESTAMOS A LA ESPERA DE INDICADORES BUENOS")
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
            # self.evaluarAperturaCHANGE(results, activeParam, flujo_count)
        else:
            print(f"ESTAMOS A LA ESPERA DE INDICADORES BUENOS")

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

    def evaluarAperturaCHANGE(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0
        multiplicador = 2
        difference_optimized, unit_diff = self.evaluarAperturaCHANGEDifference(results, activeParam, flujo_count)

        print(
            f"DIFFERENCE_OPTIMIZED evaluarAperturaCHANGE {difference_optimized} original {activeParam.difference} unit_diffb {unit_diff}")


        if self.evaluateChangeMarketTendence:
            if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_DOWN:
                if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[
                        Constants.ACTION_MAX_DIST] >= difference_optimized:
                        if results[Constants.PREVIOUS_DIST] <= (self.multiplicatorPREVIUS):
                            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                            print(" INICIO MERCADO {results[Constants.DATE].values[0]} CHANGE_DOWN_SELL01")
            elif results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UP:
                if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[
                        Constants.ACTION_MIN_DIST] >= difference_optimized:
                        if results[Constants.PREVIOUS_DIST] <= (self.multiplicatorPREVIUS):
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            print(" INICIO MERCADO {results[Constants.DATE].values[0]} CHANGE_UP_BUY01")
            elif results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UNDEF:
                if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[
                        Constants.ACTION_MAX_DIST] >= difference_optimized:
                        if self.enableControlOpen:
                            if results[Constants.ACUMULADO_ABS] <= (self.multiplicatorClose):
                                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                print(" INICIO MERCADO {results[Constants.DATE].values[0]} CHANGE_UNDEF_DOWN_SELL01")
                        else:
                            if results[Constants.PREVIOUS_DIST] <= (self.multiplicatorPREVIUS):
                                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                print(" INICIO MERCADO {results[Constants.DATE].values[0]} CHANGE_UNDEF_DOWN_SELL01")
                elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[
                        Constants.ACTION_MIN_DIST] >= difference_optimized:
                        if self.enableControlOpen:
                            if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
                                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                print(" INICIO MERCADO {results[Constants.DATE].values[0]} CHANGE_UNDEF_UP_BUY01")
                        else:
                            if results[Constants.PREVIOUS_DIST] <= (self.multiplicatorPREVIUS):
                                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                print(" INICIO MERCADO {results[Constants.DATE].values[0]} CHANGE_UNDEF_UP_BUY01")
        else:
            if results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_DOWN:
                if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[
                        Constants.ACTION_MAX_DIST] >= difference_optimized:

                        if self.enableControlOpen:
                            if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
                                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                print(" INICIO MERCADO {results[Constants.DATE].values[0]} SELLX5")
                        else:
                            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                            print(" INICIO MERCADO {results[Constants.DATE].values[0]} SELLX5")
            elif results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_UP:
                if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[
                        Constants.ACTION_MAX_DIST] >= difference_optimized:
                        if self.enableControlOpen:
                            if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
                                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                print(" INICIO MERCADO {results[Constants.DATE].values[0]} BUY4")
                        else:
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            print(" INICIO MERCADO {results[Constants.DATE].values[0]} BUY4")
            elif results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_WAIT:
                if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[
                        Constants.ACTION_MAX_DIST] >= difference_optimized:

                        if self.enableControlOpen:
                            if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
                                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                print(" INICIO MERCADO {results[Constants.DATE].values[0]} SELLXUNDEF02")
                        else:
                            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                            print(" INICIO MERCADO {results[Constants.DATE].values[0]} SELLUNDEF02")
                elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[
                        Constants.ACTION_MAX_DIST] >= difference_optimized:
                        if self.enableControlOpen:
                            if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
                                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                print(" INICIO MERCADO {results[Constants.DATE].values[0]} BUYUNDEF02")
                        else:
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            print(" INICIO MERCADO {results[Constants.DATE].values[0]} BUYUNDEF02")

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

        print(
            f"DIFFERENCE_OPTIMIZED evaluarAperturaDOWN {difference_optimized} original {activeParam.difference} unit_diffb {unit_diff}")
        if results[Constants.CLOSE_NXT_DOWN]==1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                results[Constants.CLOSE_NXT_DOWN] =0
                results[Constants.CLOSE_NXT_UP] =0
                print(
                    f" INICIO MERCADO {results[Constants.DATE].values[0]} DOWN_BLG_SELL acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")
                return
        if results[Constants.CLOSE_NXT_UP]==1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
                    if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
                        if results[Constants.IND_BLG_LOWER_DST]<self.blgLowerDist:
                            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                            print(
                                f" INICIO MERCADO {results[Constants.DATE].values[0]} DOWN_BLG_NXTUP_SELL02 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")
                        else:
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            print(
                                f" INICIO MERCADO {results[Constants.DATE].values[0]} DOWN_BLG_NXTUP_BUY_02 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")


                elif results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_UP:
                    if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        print(
                            f" INICIO MERCADO {results[Constants.DATE].values[0]} DOWN_BLG_NXTUP_BUY_01 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")

        if (abs(results[Constants.MEDSTDDIFF]) > self.medstdminDiff or abs(results[Constants.MEDSTDDIFF]) ==0) and abs(results[Constants.MEDSTDDIFF]) < self.medstdmaxDiff:
            if results[Constants.INDICATOR_MED]==Constants.INDICATOR_TM_DOWN:
                if results[Constants.IND_BLG] == Constants.IND_BLG_MED_BUY:
                    ##ESTAMOS SOBRE LA MEDIA
                    if results[Constants.ACUMULADO] < 0:
                        if results[Constants.MEDSTDDIFF] < 0:
                            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                            print(
                                f" INICIO MERCADO {results[Constants.DATE].values[0]} DOWN_DOWN_SELL01 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")

                else:
                    ##ESTAMOS BAJO LA MEDIA
                    if results[Constants.IND_BLG_LOWER_DST] < self.blgLowerDist:
                        if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or
                                results[Constants.ACTION_MAX_DIST] >= (
                                        difference_optimized * self.multiplicadorUP)):
                            if results[Constants.ACUMULADO] < 0:
                                if results[Constants.MEDSTDDIFF] < 0:
                                    results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                    print(f" INICIO MERCADO {results[Constants.DATE].values[0]} DOWN_DOWN_SELL02 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")
                            else:
                                if results[Constants.MEDSTDDIFF] >0:
                                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                    print(
                                        f" INICIO MERCADO {results[Constants.DATE].values[0]} DOWN_DOWN_SELLBUY03 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")
            # elif results[Constants.INDICATOR_MED]==Constants.INDICATOR_TM_UP:
            #     if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
            #         #estamos bajo la media
            #         if results[Constants.ACUMULADO] > 0:
            #             if results[Constants.MEDSTDDIFF] > 0:
            #                 results[Constants.NEW_ACTION] = Constants.ACTION_BUY
            #                 print(
            #                     f" INICIO MERCADO {results[Constants.DATE].values[0]} DOWN_DOWN_BUY_01 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")

    def evaluarAperturaPREDOWN(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0

        difference_optimized, unit_diff = self.evaluarAperturaPREDOWNDifference(results, activeParam, flujo_count)

        print(
            f"DIFFERENCE_OPTIMIZED evaluarAperturaPREDOWN {difference_optimized} original {activeParam.difference} unit_diffb {unit_diff}")

        # INDICADORES
        if results[Constants.FLUJO] == Constants.FLUJO_BAJA:

            if self.enableControlOpen:
                if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
                    results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                    print(f" INICIO MERCADO {results[Constants.DATE].values[0]} PREDOWN_DOWN_SELL01 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")
            else:
                if (abs(results[Constants.MEDSTDDIFF]) > self.medstdminDiff or abs(results[Constants.MEDSTDDIFF]) ==0) and abs(results[Constants.MEDSTDDIFF]) < self.medstdmaxDiff:
                    results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                    print(f" INICIO MERCADO {results[Constants.DATE].values[0]} SELL PREDOWN_DOWN_SELL02 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")

        # inversa COMPRA
        elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
            nada =""
            # if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UP:
            #     if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
            #         Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP):
            #         results[Constants.NEW_ACTION] = Constants.ACTION_BUY
            #         print(" INICIO MERCADO {results[Constants.DATE].values[0]} BUY INVERSA01")



    def evaluarDifferencePREUP(self, results, activeParam, flujo_count):
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

        difference_optimized = difference_optimized + unit_diff
        return difference_optimized, unit_diff

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

    def evaluarAperturaPREUP(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference



        difference_optimized, unit_diff = self.evaluarDifferencePREUP(results, activeParam, flujo_count)
        print(
            f"DIFFERENCE_OPTIMIZED evaluarAperturaPREUP {difference_optimized} original {activeParam.difference} unit_diffb {unit_diff}")

        # EVALUADORES
        if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
            if self.enableControlOpen:
                if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                    print(f" INICIO MERCADO {results[Constants.DATE].values[0]} PREUP_UP_BUY01 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")
            else:
                if (abs(results[Constants.MEDSTDDIFF]) > self.medstdminDiff or abs(results[Constants.MEDSTDDIFF]) ==0) and abs(results[Constants.MEDSTDDIFF]) < self.medstdmaxDiff:
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                    print(f" INICIO MERCADO {results[Constants.DATE].values[0]} PREUP_UP_BUY02 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")

        # EVALUADORES A LA INVERSA VENTA
        elif results[Constants.FLUJO] == Constants.FLUJO_BAJA:
            nada = ""
            # if results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_DOWN:
            #     if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_DOWN:
            #         if results[Constants.FLUJO_COUNT] > 1:
            #             if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
            #                 Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP):
            #                 if self.enableControlOpen:
            #                     if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
            #                         results[Constants.NEW_ACTION] = Constants.ACTION_SELL
            #                         print(" INICIO MERCADO {results[Constants.DATE].values[0]} SELL INVERSE1")
            #                 else:
            #                     results[Constants.NEW_ACTION] = Constants.ACTION_SELL
            #                     print(" INICIO MERCADO {results[Constants.DATE].values[0]} SELL INVERSE1")


    def evaluarAperturaUP(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0

        difference_optimized, unit_diff = self.evaluarDifferenceUP(results, activeParam, flujo_count)

        print(
            f"DIFFERENCE_OPTIMIZED evaluarAperturaUP {difference_optimized} original {activeParam.difference} unit_diffb {unit_diff}")

        if results[Constants.CLOSE_NXT_UP]==1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
                    if results[Constants.INDICATOR_EMA]==Constants.INDICATOR_EMA_BUY:
                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                        print(
                            f" INICIO MERCADO {results[Constants.DATE].values[0]} UP_BLG_NXTUP_SELL01 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")

                    results[Constants.CLOSE_NXT_DOWN] =0
                    results[Constants.CLOSE_NXT_UP] =0
                    return
                elif results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_UP:
                    if results[Constants.INDICATOR_EMA]==Constants.INDICATOR_EMA_SELL:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        print(
                            f" INICIO MERCADO {results[Constants.DATE].values[0]} UP_BLG_NXTUP_BUY_01 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")

            results[Constants.CLOSE_NXT_DOWN] =0
            results[Constants.CLOSE_NXT_UP] =0

        if results[Constants.CLOSE_NXT_DOWN]==1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
                    results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                    results[Constants.CLOSE_NXT_DOWN] =0
                    print(
                        f" INICIO MERCADO {results[Constants.DATE].values[0]} UP_BLG_SELL acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")
                    return
                elif results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_UP:
                    #esta en racha dejamos un poco mas
                    # if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or
                    #         results[Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP)):
                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                        results[Constants.CLOSE_NXT_DOWN] = 0
                        print(
                            f" INICIO MERCADO {results[Constants.DATE].values[0]} UP_BLG_SELL2 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")
                        return


        if (abs(results[Constants.MEDSTDDIFF]) > self.medstdminDiff or abs(results[Constants.MEDSTDDIFF]) ==0) and abs(results[Constants.MEDSTDDIFF]) < self.medstdmaxDiff:
            if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_UP:
                if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
                # if results[Constants.IND_BLG_UPPER_DST] >= self.BLGDist:
                #     if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or
                #             results[Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP)):
                       if results[Constants.ACUMULADO] > 0:
                           if results[Constants.MEDSTDDIFF] > 0:
                                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                print(f" INICIO MERCADO {results[Constants.DATE].values[0]} UP_UP_BUY01 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")
                       else:
                           nada = ""
                           # if results[Constants.MEDSTDDIFF] < 0:
                           #     results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                           #     print(
                           #         f" INICIO MERCADO {results[Constants.DATE].values[0]} UP_UP_SELL01 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")
                else:
                    ##ESTAMOS SOBRE LA MEDIA
                    if results[Constants.IND_BLG_UPPER_DST] < self.blgLowerDist:
                        if (results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or
                                results[Constants.ACTION_MIN_DIST] >= (
                                        difference_optimized * self.multiplicadorUP)):
                            if results[Constants.ACUMULADO] > 0:
                                if results[Constants.MEDSTDDIFF] > 0:
                                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                    print(
                                        f" INICIO MERCADO {results[Constants.DATE].values[0]} UP_UP_BUY02 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")
                            else:
                                if results[Constants.MEDSTDDIFF] < 0:
                                    results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                    print(
                                        f" INICIO MERCADO {results[Constants.DATE].values[0]} UP_UP_SELL01 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")

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

    def evaluarFlujoBUY(self, results, activeParam):
        # CONTROL LIMITES MAXIMOS
        difference_optimized = activeParam.difference
        unit_diff = 0
        flujo_count = results[Constants.FLUJO_COUNT]

        difference_optimized, unit_diff = self.evaluarDifferenceBUY(results, activeParam, flujo_count)

        print(
            f"DIFFERENCE_OPTIMIZED  evaluarFlujoBUY {difference_optimized} original {activeParam.difference} unit_diffb {unit_diff}")
        if results[Constants.CLOSE_NXT_DOWN]==1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                # results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                results[Constants.CLOSE_NXT_DOWN] =0
                results[Constants.CLOSE_NXT_UP] =0
                # print(
                #     f" CERRAMOS MERCADO {results[Constants.DATE].values[0]} {results[Constants.DATE].values[0]} BUY_DOWN_BLG_01 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")
                # return

        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
            if results[Constants.ACUMULADO] < 0 or results[Constants.ACUMULADO] <= 0:
                if abs(results[Constants.ACUMULADO]) >= self.closeAcumValue:

                    print(
                        f"CERRAMOS MERCADO {results[Constants.DATE].values[0]} {results[Constants.DATE].values[0]} BUY_CLOSE_ISSELL profit:{results[Constants.ACTION_ACUM]} ")
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        # cerramos si llega al minimo admisible de perdida
        if results[Constants.ACTION_ACUM] < 0:
            # es negativo
            # vericicar si bajo mas de lo esperado
            if abs(results[Constants.ACTION_ACUM]) >= self.bollingerClose:
                print(
                    f"CERRAMOS MERCADO {results[Constants.DATE].values[0]} {results[Constants.DATE].values[0]} BUY_CLOSE_ACUM profit:{results[Constants.ACTION_ACUM]} ")
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

        if results[Constants.ACTION_ACUM] < 0:
            # es negativo
            # vericicar si bajo mas de lo esperado
            if abs(results[Constants.ACTION_ACUM]) >= self.closeAcumValue:
                print(
                    f"CERRAMOS MERCADO {results[Constants.DATE].values[0]} {results[Constants.DATE].values[0]} BUY_CLOSE_ACUM profit:{results[Constants.ACTION_ACUM]} ")
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

        # # #CERRAMOS SI BAJO mucho
        if results[Constants.ACUMULADO] <= 0:
            if results[Constants.ACTION_MAX_DIST] >= (self.bollingerClose):
                print(
                    f"CERRAMOS MERCADO {results[Constants.DATE].values[0]} {results[Constants.DATE].values[0]} BUY_BLG_CLOSE01 {results[Constants.ACUMULADO]} profit:{self.closeAcumValue}")
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

        # # cerramos si tenemos ganancias y baja closeAcumValue/2
        # if results[Constants.ACTION_ACUM] > 0:
        #     if results[Constants.ACTION_ACUM] >= self.closeAcumValue * 2:
        #         if results[Constants.ACUMULADO] <= 0:
        #             if results[Constants.ACUMULADO_ABS] >= (self.closeAcumValue / 2):
        #                 print(
        #                     f"CERRAMOS MERCADO {results[Constants.DATE].values[0]} {results[Constants.DATE].values[0]} BUY_ACTION_PROFIT_DIST01 {results[Constants.ACTION_ACUM]} profit:{self.closeAcumValue}")
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

        print(
            f"DIFFERENCE_OPTIMIZED  evaluarFlujoSELL {difference_optimized} original {activeParam.difference} unit_diffb {unit_diff}")

        if results[Constants.CLOSE_NXT_UP]==1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                # results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                # print(
                #     f" CERRAMOS MERCADO {results[Constants.DATE].values[0]} {results[Constants.DATE].values[0]} SELL_UP_BLG_01 acum: {results[Constants.ACUMULADO_ABS]} medddiff {results[Constants.MEDSTDDIFF]} percentSTD: {results[Constants.IND_REL_PERCENT_STD]}")

                results[Constants.CLOSE_NXT_DOWN] =0
                results[Constants.CLOSE_NXT_UP] =0
                # return

        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_BUY:
            if results[Constants.ACUMULADO] > 0:
                if abs(results[Constants.ACUMULADO]) >= self.closeAcumValue:
                    print(
                        f"CERRAMOS MERCADO {results[Constants.DATE].values[0]} {results[Constants.DATE].values[0]} SELL_CLOSE_ISBUY profit:{results[Constants.ACTION_ACUM]} ")
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

        # cerramos si llega al minimo admisible de perdida
        if results[Constants.ACTION_ACUM] > 0:
            # es negativo
            # vericicar si bajo mas de lo esperado
            if abs(results[Constants.ACTION_ACUM]) >= self.bollingerClose:
                print(
                    f"CERRAMOS MERCADO {results[Constants.DATE].values[0]} {results[Constants.DATE].values[0]} SELL_CLOSE_ACUM profit:{results[Constants.ACTION_ACUM]} ")
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

        # # #CERRAMOS SI SUBIO mucho
        if results[Constants.ACUMULADO] > 0:
            if results[Constants.ACTION_MIN_DIST] >= (self.bollingerClose):
                print(
                    f"CERRAMOS MERCADO {results[Constants.DATE].values[0]} {results[Constants.DATE].values[0]} SELL_BLG_CLOSE01 {results[Constants.ACUMULADO]} profit:{self.closeAcumValue}")
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

        # # cerramos si tenemos ganancias y baja closeAcumValue/2
        # if results[Constants.ACTION_ACUM] < 0:
        #     if abs(results[Constants.ACTION_ACUM]) >= self.closeAcumValue * 2:
        #         if results[Constants.ACUMULADO] > 0:
        #             if results[Constants.ACUMULADO_ABS] >= (self.closeAcumValue / 2):
        #                 print(
        #                     f"CERRAMOS MERCADO {results[Constants.DATE].values[0]} {results[Constants.DATE].values[0]} SELL_ACTION_PROFIT_DIST01 {results[Constants.ACTION_ACUM]} profit:{self.closeAcumValue}")
        #                 results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
        #                 return