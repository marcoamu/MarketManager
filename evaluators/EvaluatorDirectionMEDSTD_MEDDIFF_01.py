from evaluators.CierreBase import CierreBase
from evaluators.EvaluatorBase import EvaluatorBase
from evaluators.AperturaBase import AperturaBase
from service.Constants import Constants


class EvaluatorDirectionMEDSTD_MEDDIFF_01(EvaluatorBase,AperturaBase,CierreBase):

    def __init__(self):
        self.name = "EvaluatorDirectionMEDSTD_MEDDIFF_01"
        # self.name = "EvaluatorDirectionMEDSTD03"


    def evaluate(self, results, activeParam):
        results[Constants.EVAl_NAME] = self.name

        # MULTIPLICADORES
        #para cerrar cuanto antes se usa para cuando el valor es negativo mas pequeño cierra mas rapido
        self.multiplicatorClose = activeParam.difference*1.2
        #control para ver si abre cuando ya hay una cantidad X usada
        self.enableControlOpen = True
        self.multiplicadorOpen = 2.5
        #usado para abrir en tendencia inversa
        self.multiplicadorUP= 1.2
        # valor para determinar si week es fuerte si esta bajo este valor es debil
        self.WEEK_FLOW_MINVAL = activeParam.weekDistanceSTDDistance
        # if results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_DOWN and results[
        #     Constants.WEEK_FLOW_ABSVAL] >= self.WEEK_FLOW_MINVAL:

        self.closeAcumValue = activeParam.closeAcumvalue
        if self.closeAcumValue > activeParam.accumulate:
            self.closeAcumValue = activeParam.difference + (activeParam.difference * 0.20)

        #valuador para estado change por market tendence = True  o por indicator = False
        self.evaluateChangeMarketTendence = False

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

        # NO ENTRAR A MERCADO SI ESTAMOS EN INDEFINIDO
        if results[Constants.DIRECTION] == Constants.DIR_UP:
            self.evaluarAperturaUP(results, activeParam, flujo_count)
        if results[Constants.DIRECTION] == Constants.DIR_PRE_UP:
            self.evaluarAperturaPREUP(results, activeParam, flujo_count)
        elif results[Constants.DIRECTION] == Constants.DIR_DOWN:
            self.evaluarAperturaDOWN(results, activeParam, flujo_count)
        elif results[Constants.DIRECTION] == Constants.DIR_PRE_DOWN:
            self.evaluarAperturaPREDOWN(results, activeParam, flujo_count)
        elif results[Constants.DIRECTION] == Constants.DIR_CHANGE:
            self.evaluarAperturaCHANGE(results, activeParam, flujo_count)
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

    def evaluarAperturaCHANGE(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0
        multiplicador = 2
        difference_optimized, unit_diff = self.evaluarAperturaCHANGEDifference(results, activeParam, flujo_count)

#         print(
            f"DIFFERENCE_OPTIMIZED evaluarAperturaCHANGE {difference_optimized} original {activeParam.difference} unit_diffb {unit_diff}")


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

#         print(
            f"DIFFERENCE_OPTIMIZED evaluarAperturaDOWN {difference_optimized} original {activeParam.difference} unit_diffb {unit_diff}")

        # INDICADORES
        if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
            if results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_DOWN:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized):

                    if self.enableControlOpen:
                        if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
                            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
#                             print(" INICIO MERCADO DOWN SELL01")
                    else:
                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
#                         print(" INICIO MERCADO DOWN SELL02")
            # elif results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UP:
            #     if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
            #         Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP):
            #         results[Constants.NEW_ACTION] = Constants.ACTION_SELL
            #         print(" INICIO MERCADO SELL UP 1")
            # elif results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UNDEF:
            #     if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
            #         Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP):
            #         results[Constants.NEW_ACTION] = Constants.ACTION_SELL
            #         print(" INICIO MERCADO SELL undefined01")


        # elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
        #     if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_DOWN:
        #         if self.enableControlOpen:
        #             if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
        #                 results[Constants.NEW_ACTION] = Constants.ACTION_SELL
        #                 print(" INICIO MERCADO SELLX4")
        #         else:
        #             results[Constants.NEW_ACTION] = Constants.ACTION_SELL
        #             print(" INICIO MERCADO SELLX4")

        # inversa COMPRA
        elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
            if results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_UP or results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_DOWN_CHANGE:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP):
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
#                     print(" INICIO MERCADO DOWN BUYINVERSE01")


    def evaluarAperturaPREDOWN(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0

        difference_optimized, unit_diff = self.evaluarAperturaPREDOWNDifference(results, activeParam, flujo_count)

#         print(
            f"DIFFERENCE_OPTIMIZED evaluarAperturaPREDOWN {difference_optimized} original {activeParam.difference} unit_diffb {unit_diff}")

        # INDICADORES
        if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
            if results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_DOWN:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized):
                    if self.enableControlOpen:
                        if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
                            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
#                             print(" INICIO MERCADO PRE_DOWN SELL_01")
                    else:
                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
#                         print(" INICIO MERCADO SELL PRE_DOWN SELL_02")

            # elif results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_DOWN_CHANGE:
            #     if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
            #         Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP):
            #         results[Constants.NEW_ACTION] = Constants.ACTION_SELL
            #         print(" INICIO MERCADO SELL downchange01")
            elif results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_WAIT:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP):
                    results[Constants.NEW_ACTION] = Constants.ACTION_SELL
#                     print(" INICIO MERCADO PRE_DOWN SELLWAIT_01")

        # inversa COMPRA
        elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
            if results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_DOWN_CHANGE:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP):
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
#                     print(" INICIO MERCADO PRE_DOWN INVERSABUY01")



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
#         print(
            f"DIFFERENCE_OPTIMIZED evaluarAperturaPREUP {difference_optimized} original {activeParam.difference} unit_diffb {unit_diff}")

        # EVALUADORES
        if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
            if results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_UP or results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_DOWN_CHANGE:
            # if results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_UP:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
                    Constants.ACTION_MIN_DIST] >= (difference_optimized * self.multiplicadorUP):

                    if self.enableControlOpen:
                        if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
#                             print(" INICIO MERCADO PRE_UP BUY_01")
                    else:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
#                         print(" INICIO MERCADO PRE_UP BUY_01")
            # elif results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_DOWN:
            #     if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
            #         Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP):
            #         results[Constants.NEW_ACTION] = Constants.ACTION_BUY
            #         print(" INICIO MERCADO PREBUY02")
            # elif results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UNDEF:
            #     if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
            #         Constants.ACTION_MAX_DIST] >= (difference_optimized* self.multiplicadorUP):
            #         results[Constants.NEW_ACTION] = Constants.ACTION_BUY
            #         print(" INICIO MERCADO BUY UNDEFINED02")

        # EVALUADORES A LA INVERSA VENTA
        elif results[Constants.FLUJO] == Constants.FLUJO_BAJA:
            if results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_DOWN:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP):
                    if self.enableControlOpen:
                        if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
                            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
#                             print(" INICIO MERCADO SELL PRE_UP INVERSE1")
                    else:
                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
#                         print(" INICIO MERCADO SELL PRE_UP INVERSE1")


    def evaluarAperturaUP(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0

        difference_optimized, unit_diff = self.evaluarDifferenceUP(results, activeParam, flujo_count)

#         print(
            f"DIFFERENCE_OPTIMIZED evaluarAperturaUP {difference_optimized} original {activeParam.difference} unit_diffb {unit_diff}")

        if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
            if results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_UP:
                if self.enableControlOpen:
                    if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
#                         print(" INICIO MERCADO UP BUY01")
                else:
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
#                     print(" INICIO MERCADO UP BUY1")
            # elif results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_DOWN:
            #     if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
            #         Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP):
            #             results[Constants.NEW_ACTION] = Constants.ACTION_BUY
            #             print(" INICIO MERCADO BUYDOWN1")
            # elif results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UNDEF:
            #     if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
            #         Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP):
            #         results[Constants.NEW_ACTION] = Constants.ACTION_BUY
            #         print(" INICIO MERCADO BUY UNDEFINED01")

        # elif results[Constants.FLUJO] == Constants.FLUJO_BAJA:
        #     if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UP:
        #         if results[Constants.ACUMULADO_ABS] >= (difference_optimized * multiplicadorUP) or results[
        #             Constants.ACTION_MAX_DIST] >= (difference_optimized * multiplicadorUP):
        #             results[Constants.NEW_ACTION] = Constants.ACTION_BUY
        #             print(" INICIO MERCADO BUY3")
                # EVALUADORES A LA INVERSA VENTA
        elif results[Constants.FLUJO] == Constants.FLUJO_BAJA:
            if results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_UP_CHANGE:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP):
                    if self.enableControlOpen:
                        if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
                            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
#                             print(" INICIO MERCADO SELL UP INVERSE2")
                    else:
                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
#                         print(" INICIO MERCADO SELL UP CHANGE01")


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

        # cerramos si llega al minimo admisible de perdida
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

        # cerramos si tenemos ganancias y baja closeAcumValue/2
        if results[Constants.ACTION_ACUM] > 0:
            if results[Constants.ACTION_ACUM] >= self.closeAcumValue * 2:
                if results[Constants.ACUMULADO] <= 0:
                    if results[Constants.ACUMULADO_ABS] >= (self.closeAcumValue / 2):
#                         print(
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

    def evaluarFlujoSELL(self, results, activeParam):
        difference_optimized = activeParam.difference
        unit_diff = 0
        # valores
        flujo_count = results[Constants.FLUJO_COUNT]

        difference_optimized, unit_diff = self.evaluarDifferenceSELL(results, activeParam, flujo_count)

#         print(
            f"DIFFERENCE_OPTIMIZED  evaluarFlujoSELL {difference_optimized} original {activeParam.difference} unit_diffb {unit_diff}")

        # cerramos si llega al minimo admisible de perdida
        if results[Constants.ACTION_ACUM] > 0:
            # es negativo
            # vericicar si bajo mas de lo esperado
            if abs(results[Constants.ACTION_ACUM]) >= self.closeAcumValue:
#                 print(
                    f"CERRAMOS MERCADO BUY_CLOSE_ACUM profit:{results[Constants.ACTION_ACUM]} ")
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

        # #CERRAMOS SI BAJO mucho
        if results[Constants.ACUMULADO] > 0:
            if results[Constants.ACUMULADO_ABS] >= (self.closeAcumValue):
#                 print(
                    f"CERRAMOS MERCADO BUY_ACTION_DIST01 {results[Constants.ACUMULADO]} profit:{self.closeAcumValue}")
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

        # cerramos si tenemos ganancias y baja closeAcumValue/2
        if results[Constants.ACTION_ACUM] < 0:
            if abs(results[Constants.ACTION_ACUM]) >= self.closeAcumValue * 2:
                if results[Constants.ACUMULADO] > 0:
                    if results[Constants.ACUMULADO_ABS] >= (self.closeAcumValue / 2):
#                         print(
                            f"CERRAMOS MERCADO BUY_ACTION_PROFIT_DIST01 {results[Constants.ACTION_ACUM]} profit:{self.closeAcumValue}")
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return