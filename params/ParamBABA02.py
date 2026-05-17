from service.Parameters import Parameters

#APPL
class ParamBABA02(Parameters):

    def __init__(self, isDBData):
        super().__init__()
        self.paramName = "ParamBABA02"
        self.difference = 0.10
        self.accumulate = 0.6
        self.unit = 0.02
        self.draw = False
        self.round = 2

        self.tendence_measure = 0
        # self.tendence_measure =0.06
        self.tendence_distance = 4
        self.tendence_distance_moment = 6
        self.ima1 = 3
        self.ima2 = 8
        self.ima3 = 15
        self.ima4 = 2
        self.weekend = False
        self.operate = True
        self.reevaluateAction = False
        self.minimunCloseAmount = 5
        self.hourOffset = 0
        self.controlWin = True
        self.verifyMarketOpen = True
        self.minSTDNormal = 0.06
        self.maxSTDNormal = 0.06
        self.minMEDNormal = 0.03
        self.maxMEDNormal = 0.03
        self.weekDistanceMedDistance = 1.5
        self.relativeDistance = 4.0#para indicar el maximo de distancia en relative
        self.relativeDistanceMultiplicator = 0.12#para sacar el porcentaje del valor minimo para relative
        self.weekMEDMinLevel = 0.15  # para indicar el rango en el cual el indicador deja de ser bajo
        self.weekDistanceSTDDistance = 0.10
        self.closeAcumvalue = 0.20
        self.ima1minDistance = 0.25
        self.percent_distance = 6
        self.percent_min_distance = 1.5
        self.medstdminDiff = 0.05
        self.medstdmaxDiff = 2.60
        self.ima1maxDistance = 0.40
        self.ima3minDistance = 0.5
        self.valueIndDIST = 1.0
        self.closeProfit = 0.3
        self.ignoreProb = False
        self.bollingerDst = 3
        self.enableBollingerClose = True
        self.bollinger=20
        self.bollingerClose=3
        self.blgDistPercent=10
        self.angleUp = 1
        self.angleDown = 1
        self.weekMindiff=0.7
        self.emaMinDst = 0.30
        self.weekFlowMinDiff = 5
        # self.startProbDef = 'evaluate_WEEK_ANGLE_FLOW_START_02'
        self.middleDstPercent = 5
        # self.endProbDef = 'getProMEDSTD_END_BLG_07'
        self.bollinger = 20
        self.blgDistPercent = 10
        self.weekInterval = 5
        self.angleUp = 5
        self.angleDown = 5
        self.weekMEDMinLevel = 2
        self.minAngleIma1 = 5

        self.weekInterval = 10
        self.bollinger = 10
        self.angleUp = 5
        self.angleDown = 5
        self.blgDistPercent = 10
        self.weekMEDMinLevel = 2
        self.minAngleIma1 = 10
        self.ignoreProb = False
        self.minAngleFlow = 10  # grados para indicar que el angulo esta cambiando y evaluar otro indicador
        self.minAngleFlowCounter = 3  # numero de secuencias seguidas de flujo
        self.maxAngleUp = 60  # si supera este angulo es que esta en esa direccion con seguridad
        self.maxAngleDown = 68  # se creo par btc angulo de apertura maximo para closenxtup
        # self.endProbDef = 'getANGLE_END_BLG_01'
        # self.startProbDef = 'getANGLE_START_BLG_01'
        # self.endProbDef = 'getANGLE_END_BLG_01'
        # self.endProbDef = 'getProb_END_HOURLY_ANGLE_02'
        # self.startProbDef = 'getProb_START_ANGLE_H_02'
        self.continueFlow = True  # usado para continuar si el flujo esta en el mismo sentido en open-close
        self.ima1EmaMinValue = 0.10  # si esta mas alto que esto es que es una buena distancia
        self.closeAngleDiff = 0.10  # grados para cerrar una apertura
        self.hourlyAngleDiff = 20  # > X no necesita segundo criterio < X si necesita

        self.ima1EmaMinValue = 0.10
        self.closeAngleDiff = 1.2  # grados para cerrar una apertura
        self.hourlyAngleDiff = 25  # > X no necesita segundo criterio < X si necesita
        self.ema10 = 10
        self.ema20 = 15
        self.min_ema_dst = 2  # > valor minimo entre ema_dst para abrir
        self.MinMaxDistance = 3  # para sacar el valor de minMax x elementos atras direction
        self.closeWeekDiffNew = 1.2  # > valor diff para cerrar si sube o baja respecto a week
        self.ema_change_dst = 0.2  # > valor minimo entre _dst paemara indicar si hay un cambio de flujo

        if isDBData:
            self.rangehours = [22.5, 14.50]

        else:
            self.rangehours = [16, 9]
            # self.hourOffset = -4