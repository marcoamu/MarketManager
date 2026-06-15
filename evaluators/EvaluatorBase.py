from service.Constants import Constants
import time
from datetime import datetime

class EvaluatorBase:

    def __init__(self):
        pass

    def _call_control(self, control_name, results, activeParam, closeAcumValue, closeDifference):
        """
        Llama dinámicamente a un control por su nombre.
        Si el control no existe, retorna sin acción.
        """
        if hasattr(self, control_name):
            method = getattr(self, control_name)
            # Los controles pueden tener diferente aridad
            import inspect
            sig = inspect.signature(method)
            params_count = len(sig.parameters)

            if params_count == 4:
                method(results, activeParam, closeAcumValue, closeDifference)
            elif params_count == 5:
                method(results, activeParam, closeAcumValue, closeDifference, self.accumulate)
            else:
                method(results, activeParam, closeAcumValue, closeDifference)
        else:
            pass  # Control no existe, no hace nada

    def updateTimeZoneValues(self, results=None):
        timedelta = None
        try:
            simulation = results[Constants.SIMULATION]
            if simulation:
                from datetime import datetime
                temp = results[Constants.DATE].values[0]
                t = datetime.strptime(temp, '%Y-%m-%d %H:%M:%S.%f')
                timedelta = int(t.astimezone().utcoffset().seconds / 3600)
            else:
                timedelta = -time.timezone / 3600
            if timedelta and timedelta == 1:
                self.prepareInvierno()
            else:
                self.prepareVerano()
        except Exception as e:
            message = f'{self.name}  fallo timedelta '
            self.telegram.enviarMensaje(message, self.telegram.tokenBot, self.errorTelegroup)
            self.addmessages(message, results)
            pass

    def prepareInvierno(self):
        self.closeStart = 2140
        self.closeEnd = 2200
        self.iniStart = 1530
        self.iniEnd = 1600
        self.normalIntervalStart = 1600
        self.normalIntervalEnd = 1605
        self.closeAnalisisIntervalStart = 2140
        self.closeAnalisisIntervalEnd = 2200
        self.prepRelStart = 1530
        self.prepRelEnd = 1535

    def prepareVerano(self):
        self.closeStart = 2140
        self.closeEnd = 2200
        self.iniStart = 1530
        self.iniEnd = 1600
        self.normalIntervalStart = 1600
        self.normalIntervalEnd = 1605
        self.closeAnalisisIntervalStart = 2140
        self.closeAnalisisIntervalEnd = 2200
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
            currentTime = int(current_time_h + current_time_min)
            openHour = 1530
            dif = currentTime - openHour
        else:
            t = time.localtime()
            current_time_h = time.strftime('%H', t)
            current_time_min = time.strftime('%M', t)
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
                currentTime = int(current_time_h + current_time_min)
            else:
                t = time.localtime()
                current_time_h = time.strftime('%H', t)
                current_time_min = time.strftime('%M', t)
                currentTime = int(current_time_h + current_time_min)
        except Exception as e:
            nada = ''
        return currentTime

    def isHour(self, results):
        res = False
        currentTime = None
        if results[Constants.SIMULATION]:
            temp = results[Constants.DATE].values[0]
            t = datetime.strptime(temp, '%Y-%m-%d %H:%M:%S.%f')
            current_time_h = t.hour * 100
            current_time_min = t.minute
            currentTime = int(current_time_h + current_time_min)
        else:
            t = time.localtime()
            current_time_h = time.strftime('%H', t)
            current_time_min = time.strftime('%M', t)
            if current_time_min == 0:
                isHour = True
            currentTime = int(current_time_min)
        tolerancia_minutos = 5
        minutos = t.minute
        segundos = t.second
        if minutos <= tolerancia_minutos and segundos == 0:
            res = True
            pass
        return res

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
                currentTime = int(current_time_h + current_time_min)
            else:
                t = time.localtime()
                current_time_h = time.strftime('%H', t)
                current_time_min = time.strftime('%M', t)
                currentTime = int(current_time_h + current_time_min)
        except Exception as e:
            nada = ''
        return currentTime

    def getProbFlow(self, results, activeParam):
        res = Constants.DIR_WAIT
        try:
            percent = results[Constants.IND_REL_FCST_PERCENT]
            fcst = results[Constants.IND_REL_FCST]
            week = results[Constants.WEEK_FLOW]
            med = results[Constants.MEDIA]
            absmed = abs(med)
            std = results[Constants.STDDESV]
            diftimeOpen = self.getDifTimeFromOpen(results)
            if diftimeOpen <= 60:
                if fcst == Constants.IND_REL_FCST_PRE_UP or fcst == Constants.IND_REL_FCST_UP:
                    if percent < 70:
                        res = Constants.DIR_UP
                if fcst == Constants.IND_REL_FCST_DOWN_INV_REL:
                    if percent < 7:
                        res = Constants.DIR_UP
                if fcst == Constants.IND_REL_FCST_PRE_DOWN or fcst == Constants.IND_REL_FCST_DOWN:
                    if percent > 40:
                        res = Constants.DIR_DOWN
                if fcst == Constants.IND_REL_FCST_UP_INV_REL:
                    if percent > 95:
                        res = Constants.DIR_DOWN
            else:
                if fcst == Constants.IND_REL_FCST_PRE_UP:
                    if percent > 30 and percent < 70:
                        res = Constants.DIR_UP
                    elif percent > 5 and percent <= 30:
                        if med > 0:
                            if absmed > std:
                                res = Constants.DIR_UP
                            else:
                                res = Constants.DIR_PRE_UP
                if fcst == Constants.IND_REL_FCST_UP:
                    if percent > 5 and percent < 70:
                        if med > 0:
                            if absmed > std:
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
                    elif med < 0:
                        if absmed > std:
                            res = Constants.DIR_DOWN
                if fcst == Constants.IND_REL_FCST_PRE_DOWN:
                    if percent > 40 and percent < 90:
                        res = Constants.DIR_DOWN
                    elif percent > 5 and percent <= 40:
                        if med < 0:
                            if absmed > std:
                                res = Constants.DIR_DOWN
                            else:
                                res = Constants.DIR_PRE_DOWN
                if fcst == Constants.IND_REL_FCST_DOWN:
                    if percent > 30 and percent < 95:
                        if med < 0:
                            if absmed > std:
                                res = Constants.DIR_DOWN
                            else:
                                res = Constants.DIR_PRE_DOWN
                if fcst == Constants.IND_REL_FCST_UP_INV_REL:
                    if percent > 95:
                        if med < 0:
                            if absmed > std:
                                res = Constants.DIR_DOWN
                            else:
                                res = Constants.DIR_PRE_DOWN
                    elif med > 0:
                        if absmed > std:
                            res = Constants.DIR_UP
        except Exception as error:
            pass
        return res

    def printDifference(self, flujoName, difference_optimized, closeAcumValue, closeDifference, accumulate=0):
        pass

    def evaluateAngleUP(self, results, angleUp, reviewAngle=False):
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

    def evaluateAngleUP_01(self, results):
        res = False
        if 'UP' in results[Constants.ANGLE_FLOW]:
            if results[Constants.WEEK_DIR_BOT_DST] < 90:
                if results[Constants.IND_BLG_LOWER_DST_PERCENT] < 90:
                    res = True
        return res

    def evaluateAngleNXTUP(self, results, angleUp):
        res = False
        if results[Constants.WEEK_DIR_BOT_DST] > 10 and results[Constants.WEEK_DIR_BOT_DST] < 95:
            if results[Constants.ANGLE_EMA20] > 0:
                if results[Constants.ANGLE_EMA20] > angleUp:
                    res = True
            elif results[Constants.ANGLE_EMA20] == 0:
                if results[Constants.ANGLE] > 0:
                    if results[Constants.ANGLE] > angleUp:
                        res = True
            elif abs(results[Constants.ANGLE_EMA20]) < angleUp:
                if results[Constants.ANGLEm1] < results[Constants.ANGLE]:
                    res = True
        elif results[Constants.WEEK_DIR_BOT_DST] < 10:
            if results[Constants.ANGLEm1] < results[Constants.ANGLE]:
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
            elif results[Constants.ANGLE_EMA20] == 0:
                if results[Constants.ANGLE] > 0:
                    if results[Constants.ANGLE] > angleUp:
                        res = True
            elif abs(results[Constants.ANGLE_EMA20]) < angleUp:
                if results[Constants.ANGLEm1] < results[Constants.ANGLE]:
                    res = True
        elif results[Constants.WEEK_DIR_BOT_DST] < 10:
            if results[Constants.ANGLEm1] < results[Constants.ANGLE]:
                res = True
        return res

    def isAngleHighDown(self, results, activeParam):
        res = False
        if results[Constants.ANGLE] < 0:
            if abs(results[Constants.ANGLE]) > activeParam.maxAngleDown:
                if results[Constants.ANGLE_COUNTER] > 2:
                    res = True
        return res