"""Pure evaluation utility functions from MarketManager."""

import datetime
import numpy as np
import pandas as pd


def isHour(self, results):
    res = False
    currentTime = None
    from datetime import datetime
    if results[Constants.SIMULATION]:
        temp = results[Constants.DATE].values[0]
        t = datetime.strptime(temp, '%Y-%m-%d %H:%M:%S.%f')
        current_time_h = t.hour * 100
        current_time_min = t.minute
        # print(f" gettime hora : {current_time_h} minutos: {current_time_min}")
        currentTime = int(current_time_h + current_time_min)
    else:
        t = time.localtime()
        current_time_h = time.strftime("%H", t)
        current_time_min = time.strftime("%M", t)
        if current_time_min == 0:
            isHour = True
        currentTime = int(current_time_min)
    # Definir un rango de tolerancia en minutos
    tolerancia_minutos = 5

    # Verificar si el valor de t está cerca de una hora en punto
    minutos = t.minute
    segundos = t.second

    # Calcular la diferencia en minutos y segundos con la hora exacta
    if minutos <= tolerancia_minutos:
        res = True
        # print(f"isHour current time hour: {current_time_h} minutes :{current_time_min}")

    return res

# @mide_tiempo


def postcalculation(self, data, results, active):

    # UPDATE COUNTER
    angleimaPrev = float(results[Constants.ANGLE_IMA1_PREV])
    angleIma1 = float(results[Constants.ANGLE_IMA1])
    angleImaCounter = int(float(results[Constants.ANGLE_IMA1_COUNTER]))
    angle = float(results[Constants.ANGLE])
    anglePrev = float(results[Constants.ANGLE_PREV])
    angleCounter = int(float(results[Constants.ANGLE_COUNTER]))
    if angleimaPrev != 0:
        if angleimaPrev > 0:
            if angleIma1 > 0:
                angleImaCounter = angleImaCounter + 1
            else:
                angleImaCounter = 1
        else:
            if angleIma1 < 0:
                angleImaCounter = angleImaCounter + 1
            else:
                angleImaCounter = 1

    if anglePrev != 0:
        if anglePrev > 0:
            if angle > 0:
                angleCounter = angleCounter + 1
            else:
                angleCounter = 1
        else:
            if angle < 0:
                angleCounter = angleCounter + 1
            else:
                angleCounter = 1
    results[Constants.ANGLE_IMA1_COUNTER] = angleImaCounter
    results[Constants.ANGLE_COUNTER] = angleCounter




def _eval_init_parameters(self, active):
    ima1 = 5
    ima2 = 10
    ima3 = 20
    ima4 = 20
    passiveDistance = 0.00012
    elements_past = 10
    boolinger = 20
    if active is not None:
        passiveDistance = active.parameters.tendence_measure
        ima1 = active.parameters.ima1
        ima2 = active.parameters.ima2
        ima3 = active.parameters.ima3
        ima4 = active.parameters.ima4
        elements_past = active.parameters.tendence_distance
        boolinger = active.parameters.bollinger

    ema_10 = active.parameters.ema10
    ema_20 = active.parameters.ema20
    ema_50 = active.parameters.ema50
    
    return ima1, ima2, ima3, ima4, ema_10, ema_20, ema_50, passiveDistance, elements_past, boolinger



def _eval_bollinger_distances(self, results, currentVal, blgMA, blgUPPER, blgLOWER):
    blgAction = Constants.IND_BLG_MED_WAIT
    if not blgMA.isna().iloc[-1]:
        if currentVal > blgMA.values[-1]:
            blgAction = Constants.IND_BLG_MED_BUY
        else:
            blgAction = Constants.IND_BLG_MED_SELL
    results[Constants.IND_BLG] = blgAction

    blgMedDist = 0
    if not blgMA.isna().iloc[-1]:
        blgMedDist = currentVal - float(blgMA.values[-1])
    results[Constants.IND_BLG_MED_DST] = blgMedDist

    blgUpperDist, blgLowerDist = 0, 0
    if not blgUPPER.isna().iloc[-1]:
        blgUpperDist = float(blgUPPER.values[-1]) - currentVal
    results[Constants.IND_BLG_UPPER_DST] = blgUpperDist

    if not blgLOWER.isna().iloc[-1]:
        blgLowerDist = currentVal - float(blgLOWER.values[-1])
    results[Constants.IND_BLG_LOWER_DST] = blgLowerDist

    totalDst = blgUpperDist + blgLowerDist
    blgupperPercent, blgLowerPercent = 0, 0
    if blgUpperDist != 0:
        blgupperPercent = blgUpperDist * 100 / totalDst
    results[Constants.IND_BLG_UPPER_DST_PERCENT] = blgupperPercent

    if blgLowerDist != 0:
        blgLowerPercent = blgLowerDist * 100 / totalDst
    results[Constants.IND_BLG_LOWER_DST_PERCENT] = blgLowerPercent

    middlePercent = abs(blgLowerPercent) - 50
    results[Constants.IND_BLG_MIDDLE_DST_PERCENT] = middlePercent

    blgBandwidth = 0
    if not blgUPPER.isna().iloc[-1] and not blgLOWER.isna().iloc[-1] and not blgMA.isna().iloc[-1]:
        ma_val = float(blgMA.values[-1])
        if ma_val != 0:
            blgBandwidth = (float(blgUPPER.values[-1]) - float(blgLOWER.values[-1])) / ma_val
    results[Constants.BLG_BANDWIDTH] = float(blgBandwidth)



def _eval_set_final_defaults(self, results):
    results[Constants.WEEK_FLOW] = Constants.WEEK_FLOW_UNDEF
    results[Constants.WEEK_FLOW_PREV] = Constants.WEEK_FLOW_UNDEF
    results[Constants.WEEK_FLOW_PREV_MED] = 0
    results[Constants.WEEK_FLOW_ABSVAL] = 0
    results[Constants.WEEK_FLOW_MED] = 0
    results[Constants.WEEK_FLOW_MED_LEVEL] = Constants.WEEK_FLOW_MED_LEVEL_UNDEF
    results[Constants.WEEK_DIR] = Constants.WEEK_FLOW_UNDEF
    results[Constants.WEEK_MIN_DIR] = 0
    results[Constants.WEEK_MAX_DIR] = 0
    results[Constants.WEEK_DIR_TOP_DST] = 0
    results[Constants.WEEK_DIR_BOT_DST] = 0
    results[Constants.WEEK_DIR_BOT_DST_PREV] = 0
    results[Constants.WEEK_DIR_FLOW_DIFF] = 0
    results[Constants.WEEK_DIR_FLOW] = Constants.WEEK_FLOW_UNDEF
    results[Constants.IND_PROB_FLOW] = Constants.DIR_WAIT
    results[Constants.RSI] = 0
# @mide_tiempo


def determinarIndicatorTendenceMomentBest(self, maNEW, ma4, results, active):
    # DETERMINAMOS ANGULO DE TENDENCIA
    ma15Size = len(maNEW)
    elements_past = active.parameters.tendence_distance_moment
    minMEDNormal = active.parameters.minMEDNormal
    maxMEDNormal = active.parameters.maxMEDNormal

    if ma15Size >= elements_past:
        dataTemp = {}
        dataTemp['date'] = results[Constants.DATE]
        dataTemp['value'] = results[Constants.VALUE]

        # recorremos X elementos atras
        count = 0
        fin = False
        contador = len(maNEW) - 1
        posicion = elements_past
        valores = list()
        # currentDataValue = data.iloc[[contador]]
        valor = maNEW.iloc[[contador]].values[0]
        if pd.isna(valor) is True:
            valor = 0
        while fin != True:

            valorPre = maNEW.iloc[[contador - posicion]].values[0]

            if pd.isna(valorPre) is not True and valorPre is not None:
                valores.append(valorPre)
            else:
                valores.append(0)

            if posicion <= 0:
                break
            else:
                posicion = posicion - 1

        # calculamos el angulo
        cambios = [valores[-1] - valor for valor in valores]
        # print(f"valores LONG {valores}")
        # print(f"cambios LONG {cambios}")

        results[Constants.INDICATOR_MED_MOMENT] = Constants.INDICATOR_TM_UNDEF
        if len(valores) > 0:
            # Calcula la desviacion estandar
            desviacion_estandar = np.std(cambios)
            media = np.mean(cambios)
            marketAngle = media

            results[Constants.MEDIA_MOMENT] = media
            results[Constants.STD_MOMENT] = desviacion_estandar

            # marketAngle = maNEWValue - ma_past
            marketAngleAbs = abs(marketAngle)
            # print(f"indicator mediaLONG :  {media} desviacion_estandar {desviacion_estandar} fecha: {results[Constants.DATE]}")

            # print(f"ENTRA A EVALUAR MEDIA")
            indicador_MED = Constants.INDICATOR_TM_WAIT
            mediaABS = abs(media)

            if media > 0:
                if mediaABS > desviacion_estandar:
                    indicador_MED = Constants.INDICATOR_TM_UP
                else:
                    indicador_MED = Constants.INDICATOR_TM_WAIT
            elif media <= 0:
                if mediaABS > desviacion_estandar:
                    indicador_MED = Constants.INDICATOR_TM_DOWN
                else:
                    indicador_MED = Constants.INDICATOR_TM_WAIT

            results[Constants.INDICATOR_MED_MOMENT] = indicador_MED
            results[Constants.INDICATOR_MED_MOMENT_VALUE] = media





        else:
            # iniciamos con tendencia de indicadores
            results[Constants.INDICATOR_MED_MOMENT] = Constants.INDICATOR_TM_UNDEF
            results[Constants.INDICATOR_MED_MOMENT_VALUE] = 0
    else:
        # iniciamos con tendencia de indicadores
        results[Constants.INDICATOR_MED_MOMENT] = Constants.INDICATOR_TM_UNDEF
        results[Constants.INDICATOR_MED_MOMENT_VALUE] = 0
        results[Constants.MEDIA_MOMENT] = 0
        results[Constants.STD_MOMENT] = 0



def determinar_flujo_WEEK(self, data):
    res = 'MANTIENE'
    value = 0
    try:
        algo = ""
        if data is not None and len(data) > 0:
            current = data.iloc[[-1]]
            size = len(data)

            old = data.iloc[[- 2]]
            dif = float(current.values[0]) - float(old.values[0])
            value = dif
            if dif > 0:
                res = "SUBE"
            elif dif < 0:
                res = "BAJA"
            else:
                res = 'MANTIENE'
    except Exception as e:
        nada = ""
        # print(f"ERROR determinar_flujo {str(e)}")
    return res, value



