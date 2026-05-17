from evaluators.CierreBase import CierreBase
from evaluators.EvaluatorBase import EvaluatorBase
from evaluators.AperturaBase import AperturaBase
from service.Constants import Constants


class Evaluator04(EvaluatorBase,AperturaBase,CierreBase):

    def __init__(self):
        self.name = "Evaluator04"



    def evaluate(self, results, activeParam):
        results[Constants.EVAl_NAME] = self.name

        print(f'EVALUATOR  {self.name}   ACTIVO: {activeParam.name}')
        # for result in results:
        results['ALERT'] = False
        alert = False
        isTendence = False
        isAccumulated = False
        isSell = False
        isBuy = False
        isClose = False

        # valores
        flujo_count = results[Constants.FLUJO_COUNT]
        # SOLO PARA ALERTAS
        # if results[Constants.IMA_NEW] == Constants.IMA_NEW_BUY or results[Constants.IMA_NEW] == Constants.IMA_NEW_SELL:
        #     Constants.prepararYenviarMensaje(results,activeParam,data,True)

        if results[Constants.CURRENT_ACTION] == Constants.ACTION_WAIT or results[Constants.CURRENT_ACTION] == Constants.ACTION_CLOSE:
            #

            # NO ENTRAR A MERCADO SI ESTAMOS EN INDEFINIDO
            if results[Constants.IMA_NEW] == Constants.IMA_NEW_BUY:
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
                print(
                    f"DIFFERENCE_OPTIMIZED {difference_optimized} original {activeParam.difference} unit_diffb {unit_diff}")
                if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                    if results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_UP:
                        if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MIN_DIST]>= difference_optimized:
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            # alert = True
                            # isBuy = True
                            # operations.currentTupla['START'] = results[Constants.VALUE]
                            print(" INICIO MERCADO BUY1")
                            # Constants.prepararYenviarMensaje(results, activeParam, data, True)
                    elif results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_WAIT:
                        if results[Constants.ACTION_MIN_DIST] >= difference_optimized:
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            # alert = True
                            # isBuy = True
                            # operations.currentTupla['START'] = results[Constants.VALUE]
                            print(" INICIO MERCADO BUY2")
                            # Constants.prepararYenviarMensaje(results, activeParam, data, True)
                    else:
                        if results[Constants.IMA_NEW] == Constants.IMA_NEW_BUY:
                            if results[Constants.ACUMULADO_ABS] >= difference_optimized or\
                                    results[Constants.ACTION_MIN_DIST] >= difference_optimized:
                                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        # TDOWN
                        down = ""
                elif results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                        if results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_UP:
                            if results[Constants.ACTION_MIN_DIST] >= difference_optimized:
                                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                # alert = True
                                # isBuy = True
                                # operations.currentTupla['START'] = results[Constants.VALUE]
                                print(" INICIO MERCADO BUY3")
                                # Constants.prepararYenviarMensaje(results, activeParam, data, True)
            elif results[Constants.IMA_NEW] == Constants.IMA_NEW_SELL:
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
                print(
                    f"DIFFERENCE_OPTIMIZED {difference_optimized} original {activeParam.difference} unit_diffb {unit_diff}")

                if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                    if results[Constants.MARKET_TENDENCE] == Constants.MARKET_TENDENCE_DOWN:
                        if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
                            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                            # alert = True
                            # isSell = True
                            # operations.currentTupla['START'] = results[Constants.VALUE]
                            print(" INICIO MERCADO SELLX1")
                            # Constants.prepararYenviarMensaje(results, activeParam, data, True)
                    elif results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_WAIT:
                        if results[Constants.ACTION_MAX_DIST] >= difference_optimized:
                            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                            # alert = True
                            # isSell = True
                            # operations.currentTupla['START'] = results[Constants.VALUE]
                            print(" INICIO MERCADO SELLX2")
                            # Constants.prepararYenviarMensaje(results, activeParam, data, True)
                    else:
                        cosas = ""
                        # T INDICATOR_T_UP
                        # ENTRA SI EL CONTADOR ES BUENO Y SI IMA_NEW ESTA A FAVOR
                        if results[Constants.IMA_NEW] == Constants.IMA_NEW_SELL:
                            if results[Constants.ACTION_MAX_DIST] >= difference_optimized or \
                                    results[Constants.ACUMULADO_ABS] >= activeParam.difference:
                                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                        #         alert = True
                        #         isSell = True
                        #         Constants.currentTupla['START'] = results[Constants.VALUE]
                                print(" INICIO MERCADO SELLX3")
                        #         Constants.prepararYenviarMensaje(results, activeParam, data, True)
                elif results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                    if results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_DOWN:
                        if results[Constants.ACTION_MIN_DIST] >= difference_optimized:
                            results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                            # alert = True
                            # isSell = True
                            # Constants.currentTupla['START'] = results[Constants.VALUE]
                            print(" INICIO MERCADO SELLX4")
                            # Constants.prepararYenviarMensaje(results, activeParam, data, True)


            else:
                print(f"ESTAMOS A LA ESPERA DE INDICADORES BUENOS")
        elif results[Constants.CURRENT_ACTION] == Constants.ACTION_BUY:
            # CONTROL LIMITES MAXIMOS
            difference_optimized = activeParam.difference
            unit_diff = 0
            # if results[Constants.INDICATOR_TENDENCE] != Constants.INDICATOR_T_WAIT:
            #     if results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_DOWN:
            #         difference_optimized = activeParam.difference - (activeParam.difference / 3)
            #     elif results[Constants.INDICATOR_TENDENCE] == Constants.INDICATOR_T_UP:
            #         difference_optimized = activeParam.difference + (activeParam.difference / 4)
            # else:
            #     difference_optimized = activeParam.difference - (activeParam.difference / 4)
            #     print(f"estamos en WAIT no hay indicadores de diferencia")

            if results[Constants.INDICATOR] == Constants.INDICATOR_SELL or results[Constants.INDICATOR] == Constants.INDICATOR_SELLX:
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
                        #wait
                        difference_optimized = activeParam.difference - (activeParam.difference / 3)
            elif results[Constants.INDICATOR] == Constants.INDICATOR_BUY or results[Constants.INDICATOR] == Constants.INDICATOR_BUYX:
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
                    controlUP=None
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

            print(
                f"DIFFERENCE_OPTIMIZED {difference_optimized} original {activeParam.difference} unit_diffb {unit_diff}")
            if results[Constants.ACTION_MAX_DIST] >= difference_optimized:
                print(f"CONTROL PERDIDAS BUY!! CERRAMOS ACTION_MAX_DIST {results[Constants.ACTION_MAX_DIST]}")
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                # alert = True
                # isClose = True
                # Constants.addStopValues(results[Constants.VALUE], True)
                # Constants.prepararYenviarMensaje(results, activeParam, data, True)
                # self.updateMinMaxValues(results)
            # ya tengo una accion
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:

                if results[Constants.ACUMULADO_ABS] >= float(difference_optimized) and results[Constants.FLUJO_COUNT] >= 1:
                    print(
                        f"BAJO MUCHO  {Constants.ACUMULADO_ABS} CERRAMOS!! difference_optimized {difference_optimized}")
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    # alert = True
                    # isClose = True
                    # Constants.addStopValues(results[Constants.VALUE], True)
                    # Constants.prepararYenviarMensaje(results, activeParam, data, True)
                    # self.updateMinMaxValues(results)

                # verficiar si la distancia de apertura bajo mucho
                if results[Constants.ACTION_DISTANCE] < 0 and abs(results[Constants.ACTION_DISTANCE]) >= float(
                        activeParam.accumulate):
                    print(f"BAJO MUCHO ACTION DISTANCE {Constants.ACTION_DISTANCE} CERRAMOS!!")
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    # alert = True
                    # isClose = True
                    # Constants.addStopValues(results[Constants.VALUE], True)
                    #
                    # Constants.prepararYenviarMensaje(results, activeParam, data, True)
                    # self.updateMinMaxValues(results)

            if results[Constants.IMA5MA20] == Constants.INDICATOR_SELL:
                # mercado a venta
                # evaluamos si bajo mucho
                print("INDICADOR SELL cuando estamos en BUY ")
                # Constants.printValues(results)
                if results[Constants.FLUJO] == Constants.FLUJO_BAJA and results[Constants.ACUMULADO_ABS] >= float(
                        difference_optimized):
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    # alert = True
                    # isClose = True
                    # Constants.addStopValues(results[Constants.VALUE], True)
                    #
                    # Constants.prepararYenviarMensaje(results, activeParam, data, True)
                    # self.updateMinMaxValues(results)

            if results[Constants.IMA5MA20] == Constants.INDICATOR_SELLX:
                # mercado a venta fuerte
                print("INDICADOR SELLX cuando estamos en BUY ")
                # Constants.printValues(results)
                # if results[Constants.ACUMULADO_ABS] >= float(activeParam.accumulate):
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                # alert = True
                # isClose = True
                # Constants.addStopValues(results[Constants.VALUE], True)
                #
                # Constants.prepararYenviarMensaje(results, activeParam, data, True)
                # self.updateMinMaxValues(results)

        elif results[Constants.CURRENT_ACTION] == Constants.ACTION_SELL:
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
                    #wait
                    if flujo_count > 2:
                        unit_diff = activeParam.unit * (flujo_count) * 1.3
                        unit_diff = unit_diff * -1

            difference_optimized = difference_optimized + unit_diff

            print(
                f"DIFFERENCE_OPTIMIZED {difference_optimized} original {activeParam.difference} unit_diffb {unit_diff}")

            if results[Constants.ACTION_MIN_DIST] >= difference_optimized:
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                print(f"CONTROL PERDIDAS SELL!! CERRAMOS ACTION_MIN_DIST {results[Constants.ACTION_MIN_DIST]}")
                # alert = True
                # isClose = True
                # Constants.addStopValues(results[Constants.VALUE], False)
                #
                # Constants.prepararYenviarMensaje(results, activeParam, data, True)
                # self.updateMinMaxValues(results)
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:

                if results[Constants.ACUMULADO_ABS] >= float(difference_optimized):
                    print(f"SUBE MUCHO  {Constants.ACUMULADO_ABS} CERRAMOS!! differenceControl {difference_optimized}")
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    # alert = True
                    # isClose = True
                    # Constants.addStopValues(results[Constants.VALUE], False)
                    # self.updateMinMaxValues(results)
                    # Constants.prepararYenviarMensaje(results, activeParam, data, True)

                # verficiar si la distancia de apertura bajo mucho
                if results[Constants.ACTION_DISTANCE] > 0 and abs(results[Constants.ACTION_DISTANCE]) > float(
                        activeParam.accumulate):
                    print(f"SUBE MUCHO ACTION DISTANCE {Constants.ACTION_DISTANCE} CERRAMOS!!")
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    # alert = True
                    # isClose = True
                    # Constants.addStopValues(results[Constants.VALUE], False)
                    #
                    # Constants.prepararYenviarMensaje(results, activeParam, data, True)
                    # self.updateMinMaxValues(results)
            if results[Constants.IMA5MA20] == Constants.INDICATOR_BUY:
                # mercado a compra
                # evaluamos si bajo mucho

                # self.printValues(results)
                if results[Constants.FLUJO] == Constants.FLUJO_SUBE and results[Constants.ACUMULADO_ABS] >= float(
                        difference_optimized) and results[Constants.ACTION_DISTANCE] > 0:
                    print("CLOSE INDICADOR BUY cuando estamos en SELL  distance =0 ojo")
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    # alert = True
                    # isClose = True
                    # Constants.addStopValues(results[Constants.VALUE], False)
                    #
                    # Constants.prepararYenviarMensaje(results, activeParam, data, True)
                    # self.updateMinMaxValues(results)

            if results[Constants.IMA5MA20] == Constants.INDICATOR_BUYX:
                # mercado a venta fuerte
                print("INDICADOR BUYX cuando estamos en BUY ")
                # Constants.printValues(results)
                # if results[Constants.ACUMULADO_ABS] >= float(activeParam.difference):
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                # alert = True
                # isClose = True
                # Constants.addStopValues(results[Constants.VALUE], False)
                #
                # Constants.prepararYenviarMensaje(results, activeParam, data, True)
                # self.updateMinMaxValues(results)

        # Constants.processAlerts(alert, results, activeParam, isTendence, isAccumulated, isSell, isBuy, isClose)