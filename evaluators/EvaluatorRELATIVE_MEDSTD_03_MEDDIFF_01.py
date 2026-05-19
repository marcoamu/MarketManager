from evaluators.CierreBase import CierreBase
from evaluators.EvaluatorBase import EvaluatorBase
from evaluators.AperturaBase import AperturaBase
from service.Constants import Constants


class EvaluatorRELATIVE_MEDSTD_03_MEDDIFF_01(EvaluatorBase,AperturaBase,CierreBase):

    def __init__(self):
        self.name = "EvaluatorRELATIVE_MEDSTD_03_MEDDIFF_01"
        # self.name = "EvaluatorRELATIVE_MEDSTD_03"


    def evaluate(self, results, activeParam):
        results[Constants.EVAl_NAME] = self.name

        # MULTIPLICADORES
        #para cerrar cuanto antes se usa para cuando el valor es negativo mas pequeño cierra mas rapido
        # self.multiplicatorClose = activeParam.difference-(activeParam.difference/3)
        self.multiplicatorClose = activeParam.difference*1.2
        #control para ver si abre cuando ya hay una cantidad X usada
        self.enableControlOpen = False
        self.multiplicadorOpen = 2.2
        #usado para abrir en tendencia inversa
        self.multiplicadorUP= 1.2
        #valor para determinar si week es fuerte si esta bajo este valor es debil
        self.WEEK_FLOW_MINVAL =activeParam.weekDistanceSTDDistance

        #valuador para estado change por market tendence = True  o por indicator = False
        self.evaluateChangeMarketTendence = True
        self.medstdminDiff = activeParam.medstdminDiff


        self.closeAcumValue = activeParam.closeAcumvalue
        if self.closeAcumValue > activeParam.accumulate:
            self.closeAcumValue = activeParam.difference + (activeParam.difference * 0.20)
            # self.closeAcumValue = activeParam.difference

        self.flujo_Count = 2#camtidad de acciones desde la compra o venta

        #print(f'EVALUATOR  {self.name}   ACTIVO: {activeParam.name}')
        if results[Constants.CURRENT_ACTION] == Constants.ACTION_WAIT or results[
            Constants.CURRENT_ACTION] == Constants.ACTION_CLOSE:
            self.evaluarApertura(results, activeParam)
        elif results[Constants.CURRENT_ACTION] == Constants.ACTION_BUY:
            self.evaluarFlujoBUY(results, activeParam)
        elif results[Constants.CURRENT_ACTION] == Constants.ACTION_SELL:
            self.evaluarFlujoSELL(results, activeParam)

    def evaluarApertura(self, results, activeParam):
        #
        # valores
        flujo_count = results[Constants.FLUJO_COUNT]

        if results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_UP or results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_DOWN_CHANGE:
            self.evaluarAperturaUP(results, activeParam, flujo_count)
        elif results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_DOWN or results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_UP_CHANGE:
            self.evaluarAperturaDOWN(results, activeParam, flujo_count)
        elif results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_WAIT:
            nada = ""
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

        if results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_DOWN and results[Constants.WEEK_FLOW_ABSVAL]>=self.WEEK_FLOW_MINVAL :
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP):
                    if results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_DOWN or \
                            results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_DOWN_CHANGE:
                        # if results[Constants.ACUMULADO_ABS] <= (difference_optimized * multiplicador):
                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                        print(" INICIO MERCADO SELLWAIT01")
        elif results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_UP and results[Constants.WEEK_FLOW_ABSVAL]>=self.WEEK_FLOW_MINVAL:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP):
                    if results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_UP or \
                            results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_UP_CHANGE:
                        # if results[Constants.ACUMULADO_ABS] <= (difference_optimized * multiplicador):
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        print(" INICIO MERCADO BUYWAIT01")
        else:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP):
                    if self.enableControlOpen:
                        if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
                            if results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_DOWN or \
                            results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_DOWN_CHANGE:
                                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                print(" INICIO MERCADO SELLXUNDEF02")
                    else:
                        if results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_DOWN or \
                            results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_DOWN_CHANGE:
                            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                            print(" INICIO MERCADO SELLUNDEF02")
            elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP):
                    if self.enableControlOpen:
                        if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
                            if results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_UP or \
                            results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_UP_CHANGE:
                                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                print(" INICIO MERCADO BUYUNDEF01")
                    else:
                        if results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_UP or \
                            results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_UP_CHANGE:
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            print(" INICIO MERCADO BUYUNDEF01")

        # if self.evaluateChangeMarketTendence:
        #     if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_DOWN:
        #         if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
        #             if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[
        #                 Constants.ACTION_MAX_DIST] >= difference_optimized:
        #                 # if results[Constants.ACUMULADO_ABS] <= (difference_optimized * multiplicador):
        #                     results[Constants.NEW_ACTION] = Constants.ACTION_SELL
        #                     print(" INICIO MERCADO SELLX5")
        #     elif results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UP:
        #         if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
        #             if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[
        #                 Constants.ACTION_MAX_DIST] >= difference_optimized:
        #                 # if results[Constants.ACUMULADO_ABS] <= (difference_optimized * multiplicador):
        #                     results[Constants.NEW_ACTION] = Constants.ACTION_BUY
        #                     print(" INICIO MERCADO BUY4")
        #     elif results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UNDEF:
        #         if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
        #             if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[
        #                 Constants.ACTION_MAX_DIST] >= difference_optimized:
        #                 if self.enableControlOpen:
        #                     if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
        #                         results[Constants.NEW_ACTION] = Constants.ACTION_SELL
        #                         print(" INICIO MERCADO SELLXUNDEF02")
        #                 else:
        #                     results[Constants.NEW_ACTION] = Constants.ACTION_SELL
        #                     print(" INICIO MERCADO SELLUNDEF02")
        #         elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
        #             if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[
        #                 Constants.ACTION_MIN_DIST] >= difference_optimized:
        #                 if self.enableControlOpen:
        #                     if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
        #                         results[Constants.NEW_ACTION] = Constants.ACTION_BUY
        #                         print(" INICIO MERCADO BUYUNDEF01")
        #                 else:
        #                     results[Constants.NEW_ACTION] = Constants.ACTION_BUY
        #                     print(" INICIO MERCADO BUYUNDEF01")
        # else:
        #     if results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_DOWN:
        #         if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
        #             if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[
        #                 Constants.ACTION_MAX_DIST] >= difference_optimized:
        #
        #                 if self.enableControlOpen:
        #                     if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
        #                         results[Constants.NEW_ACTION] = Constants.ACTION_SELL
        #                         print(" INICIO MERCADO SELLX5")
        #                 else:
        #                     results[Constants.NEW_ACTION] = Constants.ACTION_SELL
        #                     print(" INICIO MERCADO SELLX5")
        #     elif results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_UP:
        #         if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
        #             if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[
        #                 Constants.ACTION_MAX_DIST] >= difference_optimized:
        #                 if self.enableControlOpen:
        #                     if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
        #                         results[Constants.NEW_ACTION] = Constants.ACTION_BUY
        #                         print(" INICIO MERCADO BUY4")
        #                 else:
        #                     results[Constants.NEW_ACTION] = Constants.ACTION_BUY
        #                     print(" INICIO MERCADO BUY4")
        #     elif results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_WAIT:
        #         if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
        #             if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[
        #                 Constants.ACTION_MAX_DIST] >= difference_optimized:
        #
        #                 if self.enableControlOpen:
        #                     if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
        #                         results[Constants.NEW_ACTION] = Constants.ACTION_SELL
        #                         print(" INICIO MERCADO SELLXUNDEF02")
        #                 else:
        #                     results[Constants.NEW_ACTION] = Constants.ACTION_SELL
        #                     print(" INICIO MERCADO SELLUNDEF02")
        #         elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
        #             if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[
        #                 Constants.ACTION_MAX_DIST] >= difference_optimized:
        #                 if self.enableControlOpen:
        #                     if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
        #                         results[Constants.NEW_ACTION] = Constants.ACTION_BUY
        #                         print(" INICIO MERCADO BUYUNDEF02")
        #                 else:
        #                     results[Constants.NEW_ACTION] = Constants.ACTION_BUY
        #                     print(" INICIO MERCADO BUYUNDEF02")

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



        if results[Constants.INDICATOR_MED_STD] == Constants.INDICATOR_M_STD_DOWN:
                    if self.enableControlOpen:
                        if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
                                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                print(" INICIO MERCADO SELLX1")
                    else:
                        difOpenHours = self.getDifTimeFromOpen(results)
                        print(f"difOpenHours {difOpenHours}")
                        if difOpenHours <= 60:
                            if abs(results[Constants.MEDSTDDIFF]) > self.medstdminDiff:
                                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                print(" INICIO MERCADO SELLX1")
                        else:
                            #no abrir si la diferencia anterior es superior a difference
                            # if abs(results[Constants.PREVIOUS_DIST]) <= activeParam.difference:
                            if abs(results[Constants.MEDSTDDIFF]) > self.medstdminDiff:
                                    results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                    print(" INICIO MERCADO SELLX1")
        elif results[Constants.INDICATOR_MED_STD] == Constants.INDICATOR_M_STD_UP:
            nada =""
            # if results[Constants.FLUJO_COUNT]>1:
            #     if results[Constants.ACUMULADO_ABS]>= (difference_optimized * self.multiplicadorUP):
            #         if results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_DOWN or \
            #             results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_DOWN_CHANGE:
            #             results[Constants.NEW_ACTION] = Constants.ACTION_SELL
            #             print(" INICIO MERCADO SELL WEEKUP 1")

        elif results[Constants.INDICATOR_MED_STD] == Constants.INDICATOR_M_STD_WAIT:

            if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UP:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP):
                    if abs(results[Constants.MEDSTDDIFF]) > self.medstdminDiff:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        print(" INICIO MERCADO BUY WAIT01")
            elif results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_DOWN:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP):
                    if abs(results[Constants.MEDSTDDIFF]) > self.medstdminDiff:
                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                        print(" INICIO MERCADO SELL WAIT01")

        # inversa COMPRA
        elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
            nada = ""

                # if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
                #     Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP):
                #     if results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_UP or \
                #             results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_UP_CHANGE:
                #         difOpenHours = self.getDifTimeFromOpen(results)
                #         print(f"difOpenHours {difOpenHours}")
                #         if difOpenHours <= 60:
                #             results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                #             print(" INICIO MERCADO BUY INVERSA02")
                #         else:
                #             if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorUP*2):
                #                 results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                #                 print(" INICIO MERCADO BUY INVERSA03")


    def evaluarAperturaPREDOWN(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0

        difference_optimized, unit_diff = self.evaluarAperturaPREDOWNDifference(results, activeParam, flujo_count)

        print(
            f"DIFFERENCE_OPTIMIZED evaluarAperturaPREDOWN {difference_optimized} original {activeParam.difference} unit_diffb {unit_diff}")

        # INDICADORES
        if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
            if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_DOWN:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP):
                    if self.enableControlOpen:
                        if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
                            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                            print(" INICIO MERCADO SELL PREDOWN01")
                    else:
                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                        print(" INICIO MERCADO SELL PREDOWN01")
            elif results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UP:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP):
                    results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                    print(" INICIO MERCADO SELL PREDOWN02")
            elif results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UNDEF:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP):
                    results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                    print(" INICIO MERCADO SELL undefined02")

        # inversa COMPRA
        elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
            nada =""
            # if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UP:
            #     if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
            #         Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP):
            #         results[Constants.NEW_ACTION] = Constants.ACTION_BUY
            #         print(" INICIO MERCADO BUY INVERSA01")



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
        unit_diff = 0
        multiplicador = 2


        difference_optimized, unit_diff = self.evaluarDifferencePREUP(results, activeParam, flujo_count)
        print(
            f"DIFFERENCE_OPTIMIZED evaluarAperturaPREUP {difference_optimized} original {activeParam.difference} unit_diffb {unit_diff}")

        # EVALUADORES
        if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
            if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UP:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP):

                    if self.enableControlOpen:
                        if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            print(" INICIO MERCADO BUYPREBUY01")
                    else:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        print(" INICIO MERCADO BUYPREBUY01")
            elif results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_DOWN:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP):
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                    print(" INICIO MERCADO PREBUY02")
            elif results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UNDEF:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized* self.multiplicadorUP):
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                    print(" INICIO MERCADO BUY UNDEFINED02")

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
            #                         print(" INICIO MERCADO SELL INVERSE1")
            #                 else:
            #                     results[Constants.NEW_ACTION] = Constants.ACTION_SELL
            #                     print(" INICIO MERCADO SELL INVERSE1")


    def evaluarAperturaUP(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0

        difference_optimized, unit_diff = self.evaluarDifferenceUP(results, activeParam, flujo_count)

        print(
            f"DIFFERENCE_OPTIMIZED evaluarAperturaUP {difference_optimized} original {activeParam.difference} unit_diffb {unit_diff}")

        if results[Constants.INDICATOR_MED_STD] == Constants.INDICATOR_M_STD_UP :
                if self.enableControlOpen:
                    if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            print(" INICIO MERCADO BUY1")
                else:
                    #para abrir sin restricciones ya que es inicio mercado
                    difOpenHours = self.getDifTimeFromOpen(results)
                    if difOpenHours <=10:
                        if abs(results[Constants.MEDSTDDIFF]) > self.medstdminDiff:
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            print(" INICIO MERCADO BUYOPEN1")
                    else:
                        if abs(results[Constants.MEDSTDDIFF]) > self.medstdminDiff:
                        # if abs(results[Constants.PREVIOUS_DIST]) <= activeParam.difference:
                                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                print(" INICIO MERCADO BUYprevious01")
        elif results[Constants.INDICATOR_MED_STD] == Constants.WEEK_FLOW_DOWN:
            nada = ""
            # difOpenHours = self.getDifTimeFromOpen(results)
            # print(f"difOpenHours {difOpenHours}")
            # if results[Constants.FLUJO_COUNT] > 1 or difOpenHours<= 60:
            #     if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorOpen):
            #         if results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_UP or \
            #             results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_UP_CHANGE:
            #             results[Constants.NEW_ACTION] = Constants.ACTION_BUY
            #             print(" INICIO MERCADO BUYWEEKINV01")

        elif results[Constants.INDICATOR_MED_STD] == Constants.INDICATOR_M_STD_WAIT:
            if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UP:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP):
                    if abs(results[Constants.MEDSTDDIFF]) > self.medstdminDiff:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        print(" INICIO MERCADO BUY WAIT01")
            elif results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_DOWN:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP):
                    if abs(results[Constants.MEDSTDDIFF]) > self.medstdminDiff:
                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                        print(" INICIO MERCADO SELL WAIT01")



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

        # cerramos si llega al minimo admisible de perdida
        if results[Constants.ACTION_ACUM] < 0:
            # es negativo
            # vericicar si bajo mas de lo esperado
            if abs(results[Constants.ACTION_ACUM]) >= self.closeAcumValue:
                print(
                    f"CERRAMOS MERCADO BUY_CLOSE_ACUM profit:{results[Constants.ACTION_ACUM]} ")
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

        # #CERRAMOS SI BAJO mucho
        if results[Constants.ACUMULADO] <= 0:
            if results[Constants.ACUMULADO_ABS] >= (self.closeAcumValue):
                print(
                    f"CERRAMOS MERCADO BUY_ACTION_DIST01 {results[Constants.ACUMULADO]} profit:{self.closeAcumValue}")
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

        # cerramos si tenemos ganancias y baja closeAcumValue/2
        if results[Constants.ACTION_ACUM] > 0:
            if results[Constants.ACTION_ACUM] >= self.closeAcumValue * 2:
                if results[Constants.ACUMULADO] <= 0:
                    if results[Constants.ACUMULADO_ABS] >= (self.closeAcumValue / 2):
                        print(
                            f"CERRAMOS MERCADO BUY_ACTION_PROFIT_DIST01 {results[Constants.ACTION_ACUM]} profit:{self.closeAcumValue}")
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return


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

    def evaluarFlujoSELL(self, results, activeParam):
        difference_optimized = activeParam.difference
        unit_diff = 0
        # valores
        flujo_count = results[Constants.FLUJO_COUNT]

        difference_optimized, unit_diff = self.evaluarDifferenceSELL(results, activeParam, flujo_count)

        print(
            f"DIFFERENCE_OPTIMIZED  evaluarFlujoSELL {difference_optimized} original {activeParam.difference} unit_diffb {unit_diff}")

        # cerramos si llega al minimo admisible de perdida
        if results[Constants.ACTION_ACUM] > 0:
            # es negativo
            # vericicar si bajo mas de lo esperado
            if abs(results[Constants.ACTION_ACUM]) >= self.closeAcumValue:
                print(
                    f"CERRAMOS MERCADO BUY_CLOSE_ACUM profit:{results[Constants.ACTION_ACUM]} ")
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

        # #CERRAMOS SI BAJO mucho
        if results[Constants.ACUMULADO] > 0:
            if results[Constants.ACUMULADO_ABS] >= (self.closeAcumValue):
                print(
                    f"CERRAMOS MERCADO BUY_ACTION_DIST01 {results[Constants.ACUMULADO]} profit:{self.closeAcumValue}")
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

        # cerramos si tenemos ganancias y baja closeAcumValue/2
        if results[Constants.ACTION_ACUM] < 0:
            if abs(results[Constants.ACTION_ACUM]) >= self.closeAcumValue * 2:
                if results[Constants.ACUMULADO] > 0:
                    if results[Constants.ACUMULADO_ABS] >= (self.closeAcumValue / 2):
                        print(
                            f"CERRAMOS MERCADO BUY_ACTION_PROFIT_DIST01 {results[Constants.ACTION_ACUM]} profit:{self.closeAcumValue}")
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return