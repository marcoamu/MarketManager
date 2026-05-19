"""Pure mathematical utility functions from MarketManager."""

import math
import datetime


def calcular_angulo(self,x1, y1, x2, y2):
    # Calcula la diferencia en y y en x
    delta_y = y2 - y1
    delta_x = x2 - x1

    # Calcula el arco tangente de la pendiente
    angulo_radianes = math.atan2(delta_y, delta_x)

    # Convertir el ángulo a grados
    angulo_grados = math.degrees(angulo_radianes)

    return angulo_grados



def calcular_minutos_entre_fechas(str, fecha1_str, fecha2_str):
    # from datetime import datetime
    # Convertir las cadenas de fecha a objetos datetime
    # fecha1 = datetime.strptime(fecha1_str, "%Y-%m-%d %H:%M:%S")
    try:
        fecha1 = datetime.datetime.strptime(fecha1_str, "%Y-%m-%d %H:%M:%S.%f")
    except Exception as error:
        # print("Error getAllWithNameForXdaysRangeDates  date format using second change", error)
        fecha1 = datetime.datetime.strptime(fecha1_str, "%Y-%m-%d")
    # fecha2 = datetime.strptime(fecha2_str, "%Y-%m-%d %H:%M:%S")

    try:
        fecha2 = datetime.datetime.strptime(fecha2_str, "%Y-%m-%d %H:%M:%S.%f")
    except Exception as error:
        # print("Error getAllWithNameForXdaysRangeDates  date format using second change", error)
        fecha2 = datetime.datetime.strptime(fecha2_str, "%Y-%m-%d")

    # Calcular la diferencia de tiempo entre las dos fechas
    diferencia = fecha2 - fecha1

    # Calcular la diferencia en minutos
    minutos = diferencia.total_seconds() / 60
    # Redondear hacia arriba al próximo entero más cercano
    minutos = math.ceil(minutos)

    return abs(minutos)




# @mide_tiempo


def determineFlow(self, min, max, val):
    res = Constants.IND_REL_FCST_WAIT
    dist_rel = 0
    dist = 0
    percent = 0
    try:
        if min is None or max is None:
            return Constants.IND_REL_FCST_WAIT
        min_dist = val - min
        max_dist = max - val
        if min_dist > max_dist:
            # SUBE
            dist_rel = float(min_dist) - float(max_dist)
            dist = float(max) - float(min)
            percent = (min_dist * 100) / dist
            if abs(percent) >= 50:
                res = Constants.IND_REL_FCST_UP
            else:
                res = Constants.IND_REL_FCST_PRE_UP

        elif min_dist < max_dist:
            # BAJA

            dist_rel = float(min_dist) - float(max_dist)
            dist = float(max) - float(min)
            percent = (min_dist * 100) / dist
            if abs(percent) >= 50:
                res = Constants.IND_REL_FCST_DOWN
            else:
                res = Constants.IND_REL_FCST_PRE_DOWN
    except Exception as error:
        print("Error determineFlow ", error)
        return res, dist_rel, dist, percent
    return res, dist_rel, dist, percent



def determineMedMomentFlow(self, medMoment, absMedMoment, stdMoment, direction):
    res = ""
    if medMoment < 0:
        # baja
        if absMedMoment > stdMoment:
            res = Constants.DIR_DOWN
        else:
            if direction == Constants.DIR_UP or direction == Constants.DIR_PRE_UP:
                res = Constants.DIR_PRE_UP
            elif direction == Constants.DIR_DOWN or direction == Constants.DIR_PRE_DOWN:
                res = Constants.DIR_PRE_DOWN
            else:
                res = Constants.DIR_PRE_DOWN
    else:
        # SUBE
        if absMedMoment > stdMoment:
            res = Constants.DIR_UP
        else:
            if direction == Constants.DIR_UP or direction == Constants.DIR_PRE_UP:
                res = Constants.DIR_PRE_UP
            elif direction == Constants.DIR_DOWN or direction == Constants.DIR_PRE_DOWN:
                res = Constants.DIR_PRE_DOWN
            else:
                res = Constants.DIR_PRE_UP
    return res



def determine_Direction_percent_Flow(self, direction, percentFlow):

    if direction == Constants.DIR_UP or direction == Constants.DIR_PRE_UP:
        if percentFlow == Constants.DIR_UP:
            res = Constants.DIR_PRE_UP
        else:
            res = Constants.DIR_PRE_DOWN
    else:
        if percentFlow == Constants.DIR_DOWN:
            res = Constants.DIR_PRE_DOWN
        else:
            res = Constants.DIR_PRE_UP
    return res



def calculatePercentFcst(self, min, max, val):

    percent = 0
    try:
        if val < min:
            min = val
        if val > max:
            max = val
        min_dist = val - min
        max_dist = max - val
        if min_dist > max_dist:
            # SUBE
            dist = float(max) - float(min)
            percent = (min_dist * 100) / dist

        elif min_dist < max_dist:
            # BAJA
            dist = float(max) - float(min)
            percent = (min_dist * 100) / dist
    except Exception as error:
        print("Error calculatePerfectFcst ", error)
    return percent



def getProMEDSTD_MID(self, results):
    res = Constants.DIR_WAIT
    try:
        percent = float(results[Constants.IND_REL_FCST_PERCENT])
        fcst = results[Constants.IND_REL_FCST]
        week = results[Constants.WEEK_FLOW]
        week_med = results[Constants.WEEK_FLOW_MED]
        week_med_abs = results[Constants.WEEK_FLOW_MED]
        week_std = results[Constants.WEEK_FLOW_STD]
        direction = Constants.DIR_WAIT
        if Constants.DIRECTION in results:
            direction = results[Constants.DIRECTION]
        # percent = results[Constants.IND_REL_FCST_PERCENT]
        prevPercent = results[Constants.IND_REL_FCST_PREV_PERCENT]
        if prevPercent is not None:
            prevPercent = float(prevPercent)

        med = results[Constants.MEDIA]
        absmed = abs(med)
        std = results[Constants.STDDESV]
        medMoment = results[Constants.INDICATOR_MED_MOMENT_VALUE]
        absMedMoment = abs(medMoment)
        stdMoment = results[Constants.STD_MOMENT]
        if med == 0:
            if direction == Constants.DIR_UP:
                med = 1
            elif direction == Constants.DIR_DOWN:
                med = -1
        percentFlow = Constants.DIR_WAIT
        if percent > prevPercent:
            percentFlow = Constants.DIR_UP
        else:
            # baja
            percentFlow = Constants.DIR_DOWN
        # CALCULOS final del dia
        if fcst == Constants.IND_REL_FCST_PRE_UP or fcst == Constants.IND_REL_FCST_UP:
            if percent >= 0 and percent < 95:
                if med > 0:
                    if absmed > std:
                        res = Constants.DIR_UP
                    else:
                        res = Constants.DIR_PRE_UP
                else:
                    if absmed > std:
                        res = Constants.DIR_DOWN
                    else:
                        # contradiccion revisar week
                        if week_med > 0:
                            # sube
                            if week_med_abs > week_std:
                                res = Constants.DIR_UP
                            else:
                                res = Constants.DIR_PRE_UP
                        else:
                            # baja
                            res = Constants.DIR_PRE_DOWN

            elif percent >= 95:
                if med < 0:
                    if absmed > std:
                        res = Constants.DIR_DOWN
                    else:
                        res = Constants.DIR_PRE_DOWN
                if med >= 0:
                    if absmed > std:
                        res = Constants.DIR_UP
                    else:
                        # fix se añade direction
                        if direction == Constants.DIR_UP or direction == Constants.DIR_PRE_UP:
                            res = Constants.DIR_UP
                        else:
                            if percentFlow == Constants.DIR_UP:
                                res = Constants.DIR_PRE_UP
                            else:
                                res = Constants.DIR_PRE_DOWN

        if fcst == Constants.IND_REL_FCST_DOWN_INV_REL:
            if percent > 10 and percent <= 100:
                if med > 0:
                    if absmed > std:
                        res = Constants.DIR_UP
                    else:
                        res = Constants.DIR_PRE_UP
                else:
                    if absmed > std:
                        res = Constants.DIR_DOWN
                    else:
                        res = Constants.DIR_PRE_DOWN
            elif percent <= 10:
                if med >= 0:
                    if absmed > std:
                        res = Constants.DIR_UP
                    else:
                        res = Constants.DIR_PRE_UP
                if med < 0:
                    if absmed > std:
                        res = Constants.DIR_DOWN
                    else:
                        # res = Constants.DIR_PRE_UP
                        # fix se añade direction
                        if direction == Constants.DIR_DOWN or direction == Constants.DIR_PRE_DOWN:
                            res = Constants.DIR_DOWN
                        else:
                            if percentFlow == Constants.DIR_UP:
                                res = Constants.DIR_PRE_UP
                            else:
                                res = Constants.DIR_PRE_DOWN

        if fcst == Constants.IND_REL_FCST_PRE_DOWN or fcst == Constants.IND_REL_FCST_DOWN:
            if percent > 10 and percent <= 100:
                if med < 0:
                    if absmed > std:
                        res = Constants.DIR_DOWN
                    else:
                        res = Constants.DIR_PRE_DOWN
                elif med > 0:
                    if absmed >= std:
                        res = Constants.DIR_UP
                    else:
                        # contradiccion revisar week
                        if week_med < 0:
                            # baja
                            if week_med_abs > week_std:
                                res = Constants.DIR_DOWN
                            else:
                                res = Constants.DIR_PRE_DOWN
                        else:
                            # sube
                            res = Constants.DIR_PRE_UP

            elif percent > 0 and percent <= 10:
                if med > 0:
                    if absmed > std:
                        res = Constants.DIR_UP
                    else:
                        res = Constants.DIR_PRE_UP
                elif med < 0:
                    if absmed > std:
                        res = Constants.DIR_DOWN
                    else:
                        if direction == Constants.DIR_DOWN or direction == Constants.DIR_PRE_DOWN:
                            res = Constants.DIR_DOWN
                        else:
                            if percentFlow == Constants.DIR_UP:
                                res = Constants.DIR_PRE_UP
                            else:
                                res = Constants.DIR_PRE_DOWN
            elif percent == 0:
                if medMoment >= 0:
                    if absMedMoment > stdMoment:
                        res = Constants.DIR_UP
                    else:
                        res = Constants.DIR_PRE_UP
                if medMoment < 0:
                    if absMedMoment > stdMoment:
                        res = Constants.DIR_DOWN
                    else:
                        # res = Constants.DIR_PRE_DOWN
                        if direction == Constants.DIR_DOWN or direction == Constants.DIR_PRE_DOWN:
                            res = Constants.DIR_DOWN
                        else:
                            if percentFlow == Constants.DIR_UP:
                                res = Constants.DIR_PRE_UP
                            else:
                                res = Constants.DIR_PRE_DOWN

        if fcst == Constants.IND_REL_FCST_UP_INV_REL:
            if percent >= 0 and percent < 95:
                if med > 0:
                    if absmed > std:
                        res = Constants.DIR_UP
                    else:
                        res = Constants.DIR_PRE_UP
                elif med < 0:
                    if absmed > std:
                        res = Constants.DIR_DOWN
                    else:
                        res = Constants.DIR_PRE_DOWN
            elif percent >= 95:
                if med < 0:
                    if absmed > std:
                        res = Constants.DIR_DOWN
                    else:
                        res = Constants.DIR_PRE_DOWN
                if med > 0:
                    if absmed > std:
                        res = Constants.DIR_UP
                    else:

                        # fix se añade direction
                        if direction == Constants.DIR_UP or direction == Constants.DIR_PRE_UP:
                            res = Constants.DIR_UP
                        else:
                            if percentFlow == Constants.DIR_UP:
                                res = Constants.DIR_PRE_UP
                            else:
                                res = Constants.DIR_PRE_DOWN
    except Exception as error:
        print("Error getProMEDSTD_MID ", error)
    return res


# @mide_tiempo


def determinePercentDistance(self, percentMinMax, results, med, std, med_prev, std_prev):
    res = None
    # determinar donde esta
    minMaxABS = abs(percentMinMax)
    week_std = results[Constants.WEEK_FLOW_STD]
    week_med = results[Constants.WEEK_FLOW_MED]
    resMedprev = None
    flujoweek = 0  # 0 indeciso 1 dube -1 baja
    # flujomedprev
    if med_prev > 0:
        # sube
        if abs(med_prev) > std_prev:
            resMedprev = Constants.UP_HIGH
        else:
            resMedprev = Constants.UP_LOW
    else:
        # baja
        if abs(med_prev) > std_prev:
            resMedprev = Constants.DOWN_HIGH
        else:
            resMedprev = Constants.DOWN_LOW

    # flujo week
    if week_med > 0:
        # SUBE
        if abs(week_med) > week_std:
            flujoweek = 1
        else:
            flujoweek = 1
    else:
        # BAJA
        if abs(week_med) > week_std:
            flujoweek = -1
        else:
            flujoweek = -1

    if med > 0:

        # sube
        if abs(med) > std:
            res = Constants.IND_REL_FCST_UP
            if percentMinMax > 80:
                # ya no puede subir tanto
                res = Constants.IND_REL_FCST_UP
        else:
            # el valor es pequeño determinar si sube o baja
            if resMedprev == Constants.UP_HIGH:
                # sube
                res = Constants.IND_REL_FCST_UP
                if percentMinMax > 80:
                    # ya no puede subir tanto
                    res = Constants.IND_REL_FCST_UP_INV_REL
            if resMedprev == Constants.UP_LOW:

                if flujoweek > 0:
                    res = Constants.IND_REL_FCST_UP
                    if abs(week_med) < week_std:
                        res = Constants.IND_REL_FCST_PRE_UP
                    if percentMinMax > 80:
                        # ya no puede subir tanto
                        res = Constants.IND_REL_FCST_UP_INV_REL
                else:
                    res = Constants.IND_REL_FCST_PRE_DOWN
            if resMedprev == Constants.DOWN_HIGH:
                # sube
                res = Constants.IND_REL_FCST_DOWN
                if percentMinMax < 20:
                    # ya no puede subir tanto
                    res = Constants.IND_REL_FCST_DOWN_INV_REL
            if resMedprev == Constants.DOWN_LOW:
                if flujoweek > 0:
                    res = Constants.IND_REL_FCST_DOWN
                    if abs(week_med) < week_std:
                        res = Constants.IND_REL_FCST_PRE_DOWN
                    if percentMinMax < 20:
                        # ya no puede subir tanto
                        res = Constants.IND_REL_FCST_DOWN_INV_REL
                else:
                    res = Constants.IND_REL_FCST_PRE_DOWN
    else:
        # baja
        if abs(med) > std:
            res = Constants.IND_REL_FCST_DOWN
            if percentMinMax < 20:
                # ya no puede bajar tanto
                res = Constants.IND_REL_FCST_DOWN
        else:
            # el valor es pequeño determinar si sube o baja
            if resMedprev == Constants.DOWN_HIGH:
                # baja
                res = Constants.IND_REL_FCST_DOWN
                if percentMinMax < 20:
                    # ya no puede subir tanto
                    res = Constants.IND_REL_FCST_DOWN_INV_REL
            if resMedprev == Constants.DOWN_LOW:

                if flujoweek < 0:
                    res = Constants.IND_REL_FCST_DOWN
                    if abs(week_med) < week_std:
                        res = Constants.IND_REL_FCST_PRE_DOWN
                        if percentMinMax < 20:
                            # ya no puede subir tanto
                            res = Constants.IND_REL_FCST_DOWN_INV_REL
                else:
                    res = Constants.IND_REL_FCST_PRE_DOWN
            if resMedprev == Constants.UP_HIGH:
                # sube
                res = Constants.IND_REL_FCST_UP
                if percentMinMax > 80:
                    # ya no puede subir tanto
                    res = Constants.IND_REL_FCST_UP_INV_REL
            if resMedprev == Constants.UP_LOW:

                if flujoweek > 0:
                    res = Constants.IND_REL_FCST_UP
                    if abs(week_med) < week_std:
                        res = Constants.IND_REL_FCST_PRE_UP
                        if percentMinMax > 80:
                            # ya no puede subir tanto
                            res = Constants.IND_REL_FCST_UP_INV_REL
                else:
                    res = Constants.IND_REL_FCST_PRE_DOWN

    return res

# @mide_tiempo


def determinarRelativePercent(self, data, results, active):
    # DETERMINAMOS ANGULO DE TENDENCIA
    datalen = len(data)
    elements_past = active.parameters.percent_distance
    results[Constants.IND_REL_PERCENT_MED] = 0
    results[Constants.IND_REL_PERCENT_STD] = 0
    media = 0
    desviacion_estandar = 0
    try:
        if datalen > elements_past:
            dataTemp = {}
            dataTemp['date'] = results[Constants.DATE]
            dataTemp['value'] = results[Constants.VALUE]

            # recorremos X elementos atras
            count = 0
            fin = False
            contador = len(data) - 1
            posicion = elements_past
            valores = list()
            # currentDataValue = data.iloc[[contador]]
            valor = data.iloc[[contador]]["rel_fcst_percent"].values[0]
            if pd.isna(valor) is True:
                nada = True
            while fin != True:

                valorPre = data.iloc[[contador - posicion]]["rel_fcst_percent"].values[0]

                if pd.isna(valorPre) is not True and valorPre is not None:
                    if valorPre > 0:
                        valores.append(valorPre)

                if posicion <= 0:
                    break
                else:
                    posicion = posicion - 1

            # cambios = [valores[-1] - valor for valor in valores]

            if len(valores) > 0:
                desviacion_estandar = np.std(valores)
                media = np.mean(valores)

            results[Constants.IND_REL_PERCENT_MED] = media
            results[Constants.IND_REL_PERCENT_STD] = desviacion_estandar

    except Exception as e:
        print(f"ERROR determinarRelativePercent {str(e)}")



