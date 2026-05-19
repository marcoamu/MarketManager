from evaluators.CierreBase import CierreBase
from evaluators.EvaluatorBase import EvaluatorBase
from evaluators.AperturaBase import AperturaBase
from service.Constants import Constants


class EvaluatorMEDMOMENT_CLEAN_Optimiz02(EvaluatorBase,AperturaBase,CierreBase):

    def __init__(self):
        self.name = "EvaluatorMEDMOMENT_CLEAN_Optimiz02"


    def evaluate(self, results, activeParam):
        results[Constants.EVAl_NAME] = self.name

        # MULTIPLICADORES
        #para cerrar cuanto antes se usa para cuando el valor es negativo mas pequeño cierra mas rapido
        self.multiplicatorClose = activeParam.difference /2
        #control para ver si abre cuando ya hay una cantidad X usada
        self.enableControlOpen = True
        self.multiplicadorOpen = 2.2
        #usado para abrir en tendencia inversa
        self.multiplicadorUP= 1

        #valuador para estado change por market tendence = True  o por indicator = False
        self.evaluateChangeMarketTendence = True
        self.closeAcumValue = activeParam.closeAcumvalue
        if self.closeAcumValue > activeParam.accumulate:
            self.closeAcumValue = activeParam.difference+(activeParam.difference*0.20)

        self.ima1minDistance = activeParam.ima1minDistance



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

        if results[Constants.INDICATOR_MED_MOMENT] == Constants.INDICATOR_TM_UP:
            self.evaluarAperturaUP(results, activeParam, flujo_count)
        elif results[Constants.INDICATOR_MED_MOMENT] == Constants.INDICATOR_TM_DOWN:
            self.evaluarAperturaDOWN(results, activeParam, flujo_count)
        elif results[Constants.INDICATOR_MED_MOMENT] == Constants.INDICATOR_TM_WAIT:
            nada=""
            self.evaluarAperturaWAIT(results, activeParam, flujo_count)
        elif results[Constants.INDICATOR_MED_MOMENT] == Constants.INDICATOR_TM_UNDEF:
            nada=""
            # self.evaluarAperturaCHANGE(results, activeParam, flujo_count)
        else:
#             print(f"ESTAMOS A LA ESPERA DE INDICADORES BUENOS")

    def evaluarAperturaCHANGEDifference(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0
        if results[Constants.INDICATOR_MED_MOMENT_VALUE]>0:
            difference_optimized = activeParam.difference - (activeParam.difference / 3)
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if flujo_count > 1:
                    unit_diff = activeParam.unit * (flujo_count) * 1.3
                    unit_diff = unit_diff * -1

        elif results[Constants.INDICATOR_MED_MOMENT_VALUE]<0:
            difference_optimized = activeParam.difference - (activeParam.difference / 3)
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if flujo_count > 1:
                    unit_diff = activeParam.unit * (flujo_count) * 1.3
                    unit_diff = unit_diff * -1

        difference_optimized = difference_optimized + unit_diff
        return difference_optimized, unit_diff

    def evaluarAperturaWAIT(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0
        multiplicador = 2
        difference_optimized, unit_diff = self.evaluarAperturaCHANGEDifference(results, activeParam, flujo_count)

#         print(
            f"DIFFERENCE_OPTIMIZED evaluarAperturaCHANGE {difference_optimized} original {activeParam.difference} unit_diffb {unit_diff}")

        if results[Constants.INDICATOR_MED_MOMENT_VALUE]>0:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                # if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[
                #     Constants.ACTION_MIN_DIST] >= difference_optimized:
                    # if self.enableControlOpen:
                    #     if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
                    #         if results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_UP or results[
                    #             Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_DOWN_CHANGE:
                    #             results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                    #             print(" INICIO MERCADO WAIT_UP_BUY01")
                    #
                    # else:
                    if results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_UP or results[
                        Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_DOWN_CHANGE:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
#                         print(" INICIO MERCADO WAIT_UP_BUY02")

        elif results[Constants.INDICATOR_MED_MOMENT_VALUE]<0:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                # if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[
                #     Constants.ACTION_MAX_DIST] >= difference_optimized:
                    # if self.enableControlOpen:
                    #     if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
                    #         if results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_DOWN or results[
                    #             Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_UP_CHANGE:
                    #             results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                    #             print(" INICIO MERCADO WAIT_DON_SELL01")
                    # else:
                    if results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_DOWN or results[
                        Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_UP_CHANGE:
                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
#                         print(" INICIO MERCADO WAIT_DON_SELL02")


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
            # if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_DOWN:
        # if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
        #     Constants.ACTION_MAX_DIST] >= (difference_optimized):

        if self.enableControlOpen:
            # if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
                if results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_DOWN or results[
                    Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_UP_CHANGE:
                    results[Constants.NEW_ACTION] = Constants.ACTION_SELL
#                     print(" INICIO MERCADO DOWN_DOWN_SELL01")
            # else:
            #     if results[Constants.INDICATOR] == Constants.INDICATOR_SELLX:
            #         results[Constants.NEW_ACTION] = Constants.ACTION_SELL
            #         print(" INICIO MERCADO DOWN_DOWN_SELLX01")

        else:
            if abs(results[Constants.PREVIOUS_DIST]) < activeParam.difference:
                if results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_DOWN or results[
                    Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_UP_CHANGE:
                    results[Constants.NEW_ACTION] = Constants.ACTION_SELL
#                     print(" INICIO MERCADO DOWN_DOWN_SELL02")




    def evaluarAperturaPREDOWN(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0

        difference_optimized, unit_diff = self.evaluarAperturaPREDOWNDifference(results, activeParam, flujo_count)

#         print(
            f"DIFFERENCE_OPTIMIZED evaluarAperturaPREDOWN {difference_optimized} original {activeParam.difference} unit_diffb {unit_diff}")

        # INDICADORES
        if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
            if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_DOWN:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized):
                    if self.enableControlOpen:
                        if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
                            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
#                             print(" INICIO MERCADO SELL PREDOWN01")
                    else:
                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
#                         print(" INICIO MERCADO SELL PREDOWN01")
            elif results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UP:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP):
                    results[Constants.NEW_ACTION] = Constants.ACTION_SELL
#                     print(" INICIO MERCADO SELL PREDOWN02")
            elif results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UNDEF:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP):
                    results[Constants.NEW_ACTION] = Constants.ACTION_SELL
#                     print(" INICIO MERCADO SELL undefined02")

        # inversa COMPRA
        elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
            if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UP:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP):
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
#                     print(" INICIO MERCADO BUY INVERSA01")



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
            if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UP:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized) or results[
                    Constants.ACTION_MIN_DIST] >= (difference_optimized):

                    if self.enableControlOpen:
                        if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
#                             print(" INICIO MERCADO BUYPREBUY01")
                    else:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
#                         print(" INICIO MERCADO BUYPREBUY01")
            elif results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_DOWN:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP):
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
#                     print(" INICIO MERCADO PREBUY02")
            elif results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_UNDEF:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized* self.multiplicadorUP):
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
#                     print(" INICIO MERCADO BUY UNDEFINED02")

        # EVALUADORES A LA INVERSA VENTA
        elif results[Constants.FLUJO] == Constants.FLUJO_BAJA:
            if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_DOWN:
                if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
                    Constants.ACTION_MAX_DIST] >= (difference_optimized * self.multiplicadorUP):
                    if self.enableControlOpen:
                        if results[Constants.ACUMULADO_ABS] <= (difference_optimized * self.multiplicadorOpen):
                            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
#                             print(" INICIO MERCADO SELL INVERSE1")
                    else:
                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
#                         print(" INICIO MERCADO SELL INVERSE1")


    def evaluarAperturaUP(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0

        difference_optimized, unit_diff = self.evaluarDifferenceUP(results, activeParam, flujo_count)

#         print(
            f"DIFFERENCE_OPTIMIZED evaluarAperturaUP {difference_optimized} original {activeParam.difference} unit_diffb {unit_diff}")

        # if results[Constants.ACUMULADO_ABS] >= (difference_optimized * self.multiplicadorUP) or results[
        #     Constants.ACTION_MIN_DIST] >= (difference_optimized * self.multiplicadorUP):
        if self.enableControlOpen:
            # if results[Constants.ACUMULADO_ABS] <= (difference_optimized  * self.multiplicadorOpen):
                if results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_UP or results[
                    Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_DOWN_CHANGE:
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
#                     print(" INICIO MERCADO UP_UP_BUY01")
            # else:
            #     if results[Constants.INDICATOR] == Constants.INDICATOR_BUYX:
            #         results[Constants.NEW_ACTION] = Constants.ACTION_BUY
            #         print(" INICIO MERCADO UP_UP_BUYX01")
        else:
            if abs(results[Constants.PREVIOUS_DIST])<=activeParam.difference:
                if results[Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_UP or results[
                    Constants.RELATIVE] == Constants.INDICATOR_RELATIVE_DOWN_CHANGE:
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
#                     print(" INICIO MERCADO UP_UP_BUY2")




    def evaluarDifferenceBUY(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        unit_diff = 0

        if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
            # FIX PARA CERRAR CUANTO ANTES SI BAJA Y HAY GANANCIAS
            if results[Constants.DIRECTION] == Constants.DIR_UP:
                if flujo_count > 1:
#                     print(f"CORRECTION BUY DOWN COUNT")
                    unit_diff = activeParam.unit * (flujo_count)*2.3
                    unit_diff = unit_diff * -1
            elif results[Constants.DIRECTION] == Constants.DIR_DOWN or results[Constants.DIRECTION] == Constants.DIR_CHANGE:
                if flujo_count >=1:
                    unit_diff = activeParam.unit * (flujo_count) * 2.3
                    unit_diff = unit_diff * -1

        elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
            if results[Constants.DIRECTION] == Constants.DIR_UP:
                if flujo_count > 1:
                    unit_diff = activeParam.unit * (flujo_count) * 1.3

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

        #cerramos si tenemos ganancias y baja closeAcumValue/2
        if results[Constants.ACTION_ACUM] > 0:
            if results[Constants.ACTION_ACUM] >= self.closeAcumValue*2:
                if results[Constants.ACUMULADO] <= 0:
                    if results[Constants.ACUMULADO_ABS] >= (self.closeAcumValue/2):
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