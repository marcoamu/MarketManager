from service.Constants import Constants
import time
from datetime import datetime

class EvaluatorBase:

    def __init__(self):
        print("iniciando")

    def updateTimeZoneValues(self, results=None):
        timedelta = None
        try:
            simulation = results[Constants.SIMULATION]
            if simulation:
                from datetime import datetime
                temp = results[Constants.DATE].values[0]
                # if np.issubdtype(temp.dtype, np.datetime64):#para los valores de yahoo
                #     t = datetime.strptime(str(temp), '%Y-%m-%dT%H:%M:%S.%f000')
                #     timedelta = int(t.astimezone().utcoffset().seconds / 3600)
                # else:
                t = datetime.strptime(temp, '%Y-%m-%d %H:%M:%S.%f')

                timedelta = int(t.astimezone().utcoffset().seconds / 3600)

            else:
                timedelta = -time.timezone / 3600

            if timedelta and timedelta == 1:
                # print(f"EvaluatorBase TIMEZONE ES INVIERNO {timedelta}")
                self.prepareInvierno()
            else:
                # print(f"EvaluatorBase TIMEZONE ES VERANO {timedelta}")
                self.prepareVerano()
        except Exception as e:
            message = f"{self.name}  fallo timedelta "
            self.telegram.enviarMensaje(message, self.telegram.tokenBot, self.errorTelegroup)
            self.addmessages(message, results)
            print(f"ERROR updateTimeZoneValues {str(e)}")
    def prepareInvierno(self):
        self.closeStart = 2140
        self.closeEnd = 2200

        # caluclos iniciales
        self.iniStart = 1530
        self.iniEnd = 1600

        # retornar intervalo
        self.normalIntervalStart = 1600
        self.normalIntervalEnd = 1605

        self.closeAnalisisIntervalStart = 2140
        self.closeAnalisisIntervalEnd = 2200

        # prepare relative values
        self.prepRelStart = 1530
        self.prepRelEnd = 1535

    def prepareVerano(self):
        self.closeStart = 2140
        self.closeEnd = 2200

        # caluclos iniciales
        self.iniStart = 1530
        self.iniEnd = 1600

        # retornar intervalo
        self.normalIntervalStart = 1600
        self.normalIntervalEnd = 1605

        self.closeAnalisisIntervalStart = 2140
        self.closeAnalisisIntervalEnd = 2200

        # prepare relative values
        self.prepRelStart = 1530
        self.prepRelEnd = 1535
    def updateMinMaxValues(self, results):
        currentValue = results[Constants.VALUE]
        results[Constants.ACTION_MIN] = currentValue
        results[Constants.ACTION_MIN_DIST] = 0
        results[Constants.ACTION_MAX] = currentValue
        results[Constants.ACTION_MAX_DIST] = 0

    def getDifTimeFromOpen(self, results):

        if results[Constants.SIMULATION] is True:
            temp = results[Constants.DATE].values[0]
            t = datetime.strptime(temp, '%Y-%m-%d %H:%M:%S.%f')
            current_time_h = t.hour * 100
            current_time_min = t.minute
            # print(f" gettime hora : {current_time_h} minutos: {current_time_min}")
            currentTime = int(current_time_h + current_time_min)
            openHour = 1530
            dif = currentTime - openHour
        else:
            t = time.localtime()
            current_time_h = time.strftime("%H", t)
            current_time_min = time.strftime("%M", t)
            # print(f" gettime hora sistema: {current_time_h} minutos: {current_time_min}")
            currentTime = int(current_time_h + current_time_min)
            openHour = 1530
            dif = currentTime - openHour
        return dif
    def gettime(self, results):
        currentTime = None
        try:
            import time
            from datetime import datetime
            simulation = results[Constants.SIMULATION]
            if simulation:
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
                # print(f" gettime hora sistema: {current_time_h} minutos: {current_time_min}")
                currentTime = int(current_time_h + current_time_min)
        except Exception as e:
            nada = ""
            # print(f"ERROR determinar_flujo {str(e)}")

        # print(f"current time es : {currentTime}")
        return currentTime
    def getProbFlow(self, results,activeParam):
        res = Constants.DIR_WAIT
        try:
            percent = results[Constants.IND_REL_FCST_PERCENT]
            fcst = results[Constants.IND_REL_FCST]
            week = results[Constants.WEEK_FLOW]
            med = results[Constants.MEDIA]
            absmed= abs(med)
            std = results[Constants.STDDESV]
            diftimeOpen = self.getDifTimeFromOpen(results)
            if diftimeOpen<=60:
                #menos de 60 minutos de apertura
                if fcst == Constants.IND_REL_FCST_PRE_UP or fcst == Constants.IND_REL_FCST_UP:
                    if percent < 70:
                        res = Constants.DIR_UP
                if fcst == Constants.IND_REL_FCST_DOWN_INV_REL:
                    if percent<7:
                        res=Constants.DIR_UP
                if fcst == Constants.IND_REL_FCST_PRE_DOWN or fcst == Constants.IND_REL_FCST_DOWN:
                    if percent>40:
                        res=Constants.DIR_DOWN
                if fcst == Constants.IND_REL_FCST_UP_INV_REL:
                    if percent>95:
                        res=Constants.DIR_DOWN
            else:
                # mas de 60 minutos de apertura
                if fcst == Constants.IND_REL_FCST_PRE_UP:
                    if percent > 30 and percent < 70:
                        res = Constants.DIR_UP
                    elif percent > 5 and percent <= 30:
                        if med >0:
                            if absmed> std:
                                res = Constants.DIR_UP
                            else:
                                res = Constants.DIR_PRE_UP
                if fcst == Constants.IND_REL_FCST_UP:
                    if percent >5 and percent < 70:
                        if med >0:
                            if absmed> std:
                                res = Constants.DIR_UP
                            else:
                                res = Constants.DIR_PRE_UP
                if fcst == Constants.IND_REL_FCST_DOWN_INV_REL:
                    if percent < 7:
                        if med > 0:
                            if absmed > std:
                                res = Constants.DIR_UP
                            else:
                                res = Constants.DIR_PRE_UP
                    else:
                        if med < 0:
                            if absmed > std:
                                res = Constants.DIR_DOWN

                if fcst == Constants.IND_REL_FCST_PRE_DOWN:
                    if percent > 40 and percent < 90:
                        res = Constants.DIR_DOWN
                    elif percent > 5 and percent <= 40:
                        if med <0:
                            if absmed> std:
                                res = Constants.DIR_DOWN
                            else:
                                res = Constants.DIR_PRE_DOWN

                if fcst == Constants.IND_REL_FCST_DOWN:
                    if percent >30 and percent < 95:
                        if med <0:
                            if absmed> std:
                                res = Constants.DIR_DOWN
                            else:
                                res = Constants.DIR_PRE_DOWN
                if fcst == Constants.IND_REL_FCST_UP_INV_REL:
                    if percent >95:
                        if med < 0:
                            if absmed > std:
                                res = Constants.DIR_DOWN
                            else:
                                res = Constants.DIR_PRE_DOWN
                    else:
                        if med > 0:
                            if absmed > std:
                                res = Constants.DIR_UP
        except Exception as error:
            print("Error evaluateProbFlow ", error)
        return res

    def control_SELL_START_CLOSE_01(self, results, activeParam, closeAcumValue, closeDifference):
        name = "control_SELL_START_CLOSE_01"

        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] =0
                print(
                    f"CERRAMOS MERCADO name: {name} SELL action_acum: {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} SELL_CLOSE_NXT_MIDDLE_01 profit:{results[Constants.ACTION_ACUM]} ")
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                # results[Constants.CLOSE_NXT_DOWN] = 0
                results[Constants.CLOSE_NXT_UP] = 0

        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
                # results[Constants.CLOSE_NXT_UP] = 0

        if results[Constants.IND_BLG]== Constants.IND_BLG_MED_BUY:
            if results[Constants.ACTION_COUNT] > 2:
                if results[Constants.ACTION_ACUM] > 0:
                    print(
                        f"CERRAMOS MERCADO name: {name} SELL action_acum: {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} SELL_CLOSE_ISBUY 01 profit:{results[Constants.ACTION_ACUM]} ")
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
                else:
                    # if abs(results[Constants.ACTION_MIN_DIST]) >= (closeAcumValue):
                        #HAY GANANCIAS
                        print(
                            f"CERRAMOS MERCADO name: {name} SELL action_acum: {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} BUY_MID_PROFIT profit:{results[Constants.ACTION_ACUM]} ")
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return

        # # #CERRAMOS SI SUBIO mucho
        if results[Constants.ACTION_ACUM] > 0:
            if results[Constants.ACTION_COUNT]> 3:
                if abs(results[Constants.ACTION_ACUM]) >= (closeDifference):
                    print(
                        f"CERRAMOS MERCADO name: {name} {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} BUY_ACTION_DIST01 {results[Constants.ACUMULADO]} profit:{closeAcumValue}")
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
            else:
                if results[Constants.ACTION_COUNT] >= 2:
                    if abs(results[Constants.ACTION_ACUM]) >= (closeDifference):
                        print(
                            f"CERRAMOS MERCADO name: {name} {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} BUY_ACTION_DIST02 {results[Constants.ACUMULADO]} profit:{closeAcumValue}")
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return

        # OJO ES BUENO PERO CIERRA MUY RAPIDO
        if results[Constants.ACUMULADO] > 0:
            # vericicar si bajo mas de lo esperado
            if results[Constants.ACTION_ACUM] < 0:
                #tiene ganancias
                if abs(results[Constants.ACTION_ACUM]) > closeAcumValue:  # TIENE GANANCIAS
                    if abs(results[Constants.ACTION_MIN_DIST]) >= closeAcumValue:
                        print(
                            f"CERRAMOS MERCADO name: {name} SELL WINCLOSE action_acum: {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} SELL_CLOSE_ACUM profit:{results[Constants.ACTION_ACUM]} ")
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return

    def control_BUY_START_CLOSE_01(self, results, activeParam, closeAcumValue, closeDifference):
        name = "control_BUY_START_CLOSE_01"
        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] =0
                print(
                    f"CERRAMOS MERCADO name: {name} SELL action_acum: {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} SELL_CLOSE_NXT_MIDDLE_01 profit:{results[Constants.ACTION_ACUM]} ")
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                # results[Constants.CLOSE_NXT_DOWN] = 0
                results[Constants.CLOSE_NXT_UP] = 0

        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
                # results[Constants.CLOSE_NXT_UP] = 0

        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
            if results[Constants.ACTION_COUNT] > 5:
                if results[Constants.ACTION_ACUM] < 0:
                    print(
                        f"CERRAMOS MERCADO name: {name} BUY action_acum: {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} BUY_CLOSE_ISSELL 01 profit:{results[Constants.ACTION_ACUM]} ")
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
                else:
                    if abs(results[Constants.ACTION_MAX_DIST]) >= (closeAcumValue):
                        # HAY GANANCIAS
                        print(
                            f"CERRAMOS MERCADO BUY name: {name} action_acum: {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} BUY_MID_PROFIT profit:{results[Constants.ACTION_ACUM]} ")
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return
        # #si se acerca a la distancia minima de mid y baja
        # if results[Constants.ACUMULADO] <= 0:
        #     if abs(results[Constants.ACUMULADO]) > difference_optimized:
        #         if abs(results[Constants.IND_BLG_MED_DST]) <= self.midMinDst:
        #             print(
        #                 f"CERRAMOS MERCADO BUY action_acum: {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} BUY_MEDMINDIST_01 profit:{results[Constants.ACTION_ACUM]} ")
        #             results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
        #             return

        # OJO ES BUENO PERO CIERRA MUY RAPIDO
        if results[Constants.ACUMULADO] < 0:
            # vericicar si bajo mas de lo esperado
            if results[Constants.ACTION_ACUM] > 0:
                if results[Constants.ACTION_ACUM] > closeAcumValue:  # muchas ganancias
                    if abs(results[Constants.ACTION_MAX_DIST]) >= closeAcumValue:
                        print(
                            f"CERRAMOS MERCADO name: {name} BUY action_acum: {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} BUY_CLOSE_ACUM profit:{results[Constants.ACTION_ACUM]} ")
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return

        # # # #CERRAMOS SI BAJO mucho
        if results[Constants.ACTION_ACUM] <= 0:
            if results[Constants.ACTION_COUNT] > 3:
                if abs(results[Constants.ACTION_ACUM]) >= (closeDifference):
                    print(
                        f"CERRAMOS MERCADO name: {name} acmun: {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} BUY_ACTION_DIST02 {results[Constants.ACUMULADO]} profit:{closeAcumValue}")
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

        # CERRAMOS SI SALE DEL TOP BLG
        # if results[Constants.IND_BLG_UPPER_DST_PERCENT]<0:
        #     #HA pASADO EL TOP HAY GANANCIAS
        #     if results[Constants.ACTION_COUNT] > 3:
        #         if abs(results[Constants.IND_BLG_UPPER_DST_PERCENT])>1:
        #             print(
        #                 f"CERRAMOS MERCADO {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} BUY_MAXIMO_01 {results[Constants.ACUMULADO]} profit:{self.closeAcumValue}")
        #             results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
        #             return

        # CERRAMOS SI ESTA CERCA DEL TOP
        if abs(results[Constants.IND_BLG_UPPER_DST_PERCENT]) > 0 and abs(
                results[Constants.IND_BLG_UPPER_DST_PERCENT]) < 2:
            # HA pASADO EL TOP HAY GANANCIAS
            if results[Constants.ACTION_COUNT] > 3:
                # if abs(results[Constants.IND_BLG_UPPER_DST_PERCENT])>1:
                print(
                    f"CERRAMOS MERCADO name: {name} acum: {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} BUY_MAXIMO_02 {results[Constants.ACUMULADO]} profit:{closeAcumValue}")
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

    def control_BUY_START_CLOSE_03(self, results, activeParam, closeAcumValue, closeDifference):
        angleDown = activeParam.angleDown
        name = "control_BUY_START_CLOSE_03"

        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] =0
                print(
                    f"CERRAMOS MERCADO name: {name} SELL action_acum: {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} SELL_CLOSE_NXT_MIDDLE_01 profit:{results[Constants.ACTION_ACUM]} ")
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                # results[Constants.CLOSE_NXT_DOWN] = 0
                results[Constants.CLOSE_NXT_UP] = 0

        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
                # results[Constants.CLOSE_NXT_UP] = 0

        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
            if results[Constants.ACTION_COUNT] > 6:
                if results[Constants.ACTION_ACUM] < 0:
                    print(
                        f"CERRAMOS MERCADO name {name} BUY action_acum: {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} BUY_CLOSE_ISSELL 01 profit:{results[Constants.ACTION_ACUM]} ")
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
                else:
                    if abs(results[Constants.ACTION_MAX_DIST]) >= (closeDifference):
                        # HAY GANANCIAS
                        print(
                            f"CERRAMOS MERCADO name {name} BUY action_acum: {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} BUY_MID_PROFIT profit:{results[Constants.ACTION_ACUM]} ")
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return

        # # PARA CERRAR RAPIDO SI WEEK ES DOWN
        # if results[Constants.ACUMULADO] < 0:
        #     if "DOWN" in results[Constants.WEEK_FLOW]:
        #     # vericicar si bajo mas de lo esperado
        #      if abs(results[Constants.ACTION_MAX_DIST]) >= closeDifference:
        #         print(
        #             f"CERRAMOS MERCADO BUY action_acum: {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} BUY_CLOSE_ACUM_NXT_01:{results[Constants.ACTION_ACUM]} ")
        #         results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
        #         return

        # OJO ES BUENO PERO CIERRA MUY RAPIDO
        if results[Constants.ACUMULADO] < 0:
            # vericicar si bajo mas de lo esperado
            if results[Constants.ACTION_ACUM] > 0:
                if results[Constants.ACTION_ACUM] > closeAcumValue:  # muchas ganancias
                    if abs(results[Constants.ACTION_MAX_DIST]) >= closeAcumValue:
                        print(
                            f"CERRAMOS MERCADO name {name} BUY action_acum: {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} BUY_CLOSE_ACUM profit:{results[Constants.ACTION_ACUM]} ")
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return

        # # # #CERRAMOS SI BAJO mucho
        if results[Constants.ACTION_ACUM] <= 0:
            if results[Constants.ACTION_COUNT] >= 3:
                if abs(results[Constants.ACTION_ACUM]) >= (closeDifference):
                    print(
                        f"CERRAMOS MERCADO name {name} {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} BUY_ACTION_DIST02 {results[Constants.ACUMULADO]} profit:{closeAcumValue}")
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
            else:
                if results[Constants.ANGLE] <0:
                    if results[Constants.ACTION_COUNT] >= 2:
                        if results[Constants.ANGLE]< angleDown:
                            if abs(results[Constants.ACTION_ACUM]) >= (closeDifference):
                                print(
                                    f"CERRAMOS MERCADO name {name} {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} BUY_ACTION_CLOSE_ANGLE_NEG_01 {results[Constants.ACUMULADO]} profit:{closeAcumValue}")
                                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                                return

        # CERRAMOS SI ESTA CERCA DEL TOP
        if abs(results[Constants.IND_BLG_UPPER_DST_PERCENT]) > 0 and abs(
                results[Constants.IND_BLG_UPPER_DST_PERCENT]) < 2:
            # HA pASADO EL TOP HAY GANANCIAS
            if results[Constants.ACTION_COUNT] > 3:
                # if abs(results[Constants.IND_BLG_UPPER_DST_PERCENT])>1:
                print(
                    f"CERRAMOS MERCADO name {name} {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} BUY_MAXIMO_02 {results[Constants.ACUMULADO]} profit:{closeAcumValue}")
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

    def control_BUY_START_CLOSE_02(self, results, activeParam, closeAcumValue, closeDifference):
        name = "control_BUY_START_CLOSE_02"

        if results[Constants.CLOSE_NXT_MIDDLE] == 1:
            if abs(results[Constants.IND_BLG_MIDDLE_DST_PERCENT]) <= activeParam.middleDstPercent:
                results[Constants.CLOSE_NXT_MIDDLE] =0
                print(
                    f"CERRAMOS MERCADO name: {name} SELL action_acum: {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} SELL_CLOSE_NXT_MIDDLE_01 profit:{results[Constants.ACTION_ACUM]} ")
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                # results[Constants.CLOSE_NXT_DOWN] = 0
                results[Constants.CLOSE_NXT_UP] = 0

        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
                # results[Constants.CLOSE_NXT_UP] = 0

        if results[Constants.IND_BLG] == Constants.IND_BLG_MED_SELL:
            if results[Constants.ACTION_COUNT] > 5:
                if results[Constants.ACTION_ACUM] < 0:
                    print(
                        f"CERRAMOS MERCADO BUY  name: {name}  action_acum: {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} BUY_CLOSE_ISSELL 01 profit:{results[Constants.ACTION_ACUM]} ")
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
                else:
                    if abs(results[Constants.ACTION_MAX_DIST]) >= (closeAcumValue):
                        # HAY GANANCIAS
                        print(
                            f"CERRAMOS MERCADO BUY name: {name}  action_acum: {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} BUY_MID_PROFIT profit:{results[Constants.ACTION_ACUM]} ")
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return
        # #si se acerca a la distancia minima de mid y baja
        # if results[Constants.ACUMULADO] <= 0:
        #     if abs(results[Constants.ACUMULADO]) > difference_optimized:
        #         if abs(results[Constants.IND_BLG_MED_DST]) <= self.midMinDst:
        #             print(
        #                 f"CERRAMOS MERCADO BUY action_acum: {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} BUY_MEDMINDIST_01 profit:{results[Constants.ACTION_ACUM]} ")
        #             results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
        #             return

        # OJO ES BUENO PERO CIERRA MUY RAPIDO
        if results[Constants.ACUMULADO] < 0:
            # vericicar si bajo mas de lo esperado
            if results[Constants.ACTION_ACUM] > 0:
                if results[Constants.ACTION_ACUM] > closeAcumValue:  # muchas ganancias
                    if abs(results[Constants.ACTION_MAX_DIST]) >= closeAcumValue:
                        print(
                            f"CERRAMOS MERCADO name: {name} BUY action_acum: {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} BUY_CLOSE_ACUM profit:{results[Constants.ACTION_ACUM]} ")
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return

        # # # #CERRAMOS SI BAJO mucho
        if results[Constants.ACTION_ACUM] <= 0:
            if results[Constants.ACTION_COUNT] >= 2:
                if abs(results[Constants.ACTION_ACUM]) >= (closeDifference):
                    print(
                        f"CERRAMOS MERCADO name: {name} acum: {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} BUY_ACTION_DIST02 {results[Constants.ACUMULADO]} profit:{closeAcumValue}")
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

        # CERRAMOS SI SALE DEL TOP BLG
        # if results[Constants.IND_BLG_UPPER_DST_PERCENT]<0:
        #     #HA pASADO EL TOP HAY GANANCIAS
        #     if results[Constants.ACTION_COUNT] > 3:
        #         if abs(results[Constants.IND_BLG_UPPER_DST_PERCENT])>1:
        #             print(
        #                 f"CERRAMOS MERCADO {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} BUY_MAXIMO_01 {results[Constants.ACUMULADO]} profit:{self.closeAcumValue}")
        #             results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
        #             return

        # CERRAMOS SI ESTA CERCA DEL TOP
        if abs(results[Constants.IND_BLG_UPPER_DST_PERCENT]) > 0 and abs(
                results[Constants.IND_BLG_UPPER_DST_PERCENT]) < 2:
            # HA pASADO EL TOP HAY GANANCIAS
            if results[Constants.ACTION_COUNT] > 3:
                # if abs(results[Constants.IND_BLG_UPPER_DST_PERCENT])>1:
                print(
                    f"CERRAMOS MERCADO name: {name}  {results[Constants.ACTION_ACUM]} {results[Constants.DATE].values[0]} BUY_MAXIMO_02 {results[Constants.ACUMULADO]} profit:{closeAcumValue}")
                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                return

    def printDifference(self, flujoName, difference_optimized, closeAcumValue, closeDifference):
        print(
            f" DIFFERENCE_OPTIMIZED flujo {flujoName} difference_optimized {difference_optimized} closeAcumValue {closeAcumValue} closeDifference {closeDifference}")

    def printInicioLog(self, name, results, activeparameters):
        print(
            f" INICIO MERCADO {name} {results[Constants.DATE].values[0]} \tACUMULADO_ABS: {results[Constants.ACUMULADO_ABS]} \tWEEK_DIR_FLOW {results[Constants.WEEK_DIR_FLOW]} \tANGLE_EMA20: {results[Constants.ANGLE_EMA20]} \tANGLE: {results[Constants.ANGLE]}  \tANGLE_IMA1: {results[Constants.ANGLE_IMA1]} \tANGLE_IMA1_COUNTER: {results[Constants.ANGLE_IMA1_COUNTER]}  \tWEEK_DIR_BOT_DST {results[Constants.WEEK_DIR_BOT_DST]} \tIND_BLG_LOWER_DST_PERCENT {results[Constants.IND_BLG_LOWER_DST_PERCENT]} \tANGLE_EMA: {results[Constants.ANGLE_EMA]} \tWEEK_DIR_FLOW_DIFF {results[Constants.WEEK_DIR_FLOW_DIFF]} \tWEEK_DIR_FLOW_PREV {results[Constants.WEEK_DIR_FLOW_PREV]}  \tMEDSTDDIFF {results[Constants.MEDSTDDIFF]} \tINDICATOR_EMA: {results[Constants.INDICATOR_EMA]}  \tDIRECTION {results[Constants.DIRECTION]} \tINDICATOR_MED_MOMENT {results[Constants.INDICATOR_MED_MOMENT]}")

    def evaluateAngleUP(self, results, angleUp, reviewAngle = False):
        res = False
        if results[Constants.WEEK_DIR_BOT_DST] < 95:
            if results[Constants.ANGLE_EMA20] > 0:

                if results[Constants.ANGLE_EMA20] > angleUp:
                    res = True
                    if reviewAngle:
                        if results[Constants.ANGLEm1] < results[Constants.ANGLE]:
                            res = True
                        else:
                            res = False

            elif results[Constants.ANGLE_EMA20] == 0:
                if results[Constants.ANGLE] > 0:
                    if results[Constants.ANGLE] > angleUp:
                        res = True
        return res

    def evaluateAngleNXTUP(self, results, angleUp):
        res = False
        if results[Constants.WEEK_DIR_BOT_DST] > 10 and results[Constants.WEEK_DIR_BOT_DST] < 95:
            if results[Constants.ANGLE_EMA20] > 0:
                if results[Constants.ANGLE_EMA20] > angleUp:
                    res = True
            elif results[Constants.ANGLE_EMA20]==0:
                if results[Constants.ANGLE] > 0:
                    if results[Constants.ANGLE] > angleUp:
                        res = True
            else:
                if abs(results[Constants.ANGLE_EMA20]) < angleUp:
                    if results[Constants.ANGLEm1] <  results[Constants.ANGLE]:
                        # esta subiendo
                        res = True
        else:
            #posibilidades de subir
            if results[Constants.WEEK_DIR_BOT_DST] < 10:
                if results[Constants.ANGLEm1] < results[Constants.ANGLE]:
                    # esta subiendo
                    res = True

        return res

    def evaluateAngleDirection(self, results, activeParam):
        angleUp = activeParam.angleUp
        angleDown = activeParam.angleDown
        res = False
        if results[Constants.WEEK_DIR_BOT_DST] > 10 and results[Constants.WEEK_DIR_BOT_DST] < 95:
            if results[Constants.ANGLE_EMA20] > 0:
                if results[Constants.ANGLE_EMA20] > angleUp:
                    res = True
            elif results[Constants.ANGLE_EMA20]==0:
                if results[Constants.ANGLE] > 0:
                    if results[Constants.ANGLE] > angleUp:
                        res = True
            else:
                if abs(results[Constants.ANGLE_EMA20]) < angleUp:
                    if results[Constants.ANGLEm1] <  results[Constants.ANGLE]:
                        # esta subiendo
                        res = True
        else:
            #posibilidades de subir
            if results[Constants.WEEK_DIR_BOT_DST] < 10:
                if results[Constants.ANGLEm1] < results[Constants.ANGLE]:
                    # esta subiendo
                    res = True

        return res