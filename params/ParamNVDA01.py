from service.Parameters import Parameters

#AMZN
class ParamNVDA01(Parameters):

    def __init__(self, isDBData):
        super().__init__()
        self.paramName = "ParamNVDA01"
        self.difference = 0.46
        self.accumulate = 1.5
        self.unit = 0.15
        self.draw = False
        self.round = 2

        # self.tendence_measure =0.0001
        self.tendence_measure = 0.00
        self.tendence_distance = 4
        self.tendence_distance_moment = 6
        self.ima1 = 3
        self.ima2 = 5
        self.ima3 = 8
        self.ima4 = 1
        self.weekend = False
        self.operate = True
        self.reevaluateAction = False
        self.minimunCloseAmount = 5
        self.hourOffset = 0
        self.controlWin = True
        self.verifyMarketOpen = True
        self.minSTDNormal = 0.10
        self.maxSTDNormal = 0.14
        self.minMEDNormal = 0.10
        self.maxMEDNormal = 0.13
        self.weekDistanceMedDistance = 8.0 #si los valores week superan este valor se consideran muy altos y se dejan undeff
        self.relativeDistance = 20#para indicar el maximo de distancia si lo supera indica que esta por hacer el cambio
        self.relativeDistanceMultiplicator = 0.22#para sacar el porcentaje del valor minimo para entraar en change en relative
        self.weekMEDMinLevel = 0.15  # para indicar el rango en el cual el indicador deja de ser bajo
        self.weekDistanceSTDDistance = 0.10

        self.ima1minDistance = 0.10
        self.percent_distance = 10
        self.percent_min_distance = 1.5
        self.medstdminDiff = 0.15
        self.medstdmaxDiff = 1.50
        self.ima1maxDistance = 1.40
        self.ima3minDistance = 3
        self.valueIndDIST = 1.0
        self.closeProfit = 0.56
        # self.ignoreProb = True
        self.bollingerDst = 3
        self.enableBollingerClose = True
        self.bollinger=10
        self.bollingerClose=4
        self.blgDistPercent=5
        self.weekMindiff=0.7
        self.emaMinDst = 0.10



        self.weekInterval = 10
        self.bollinger = 20
        self.angleUp = 5
        self.angleDown = 5
        self.blgDistPercent = 10
        self.weekMEDMinLevel = 2
        self.minAngleIma1 = 20
        self.ignoreProb = True
        self.minAngleFlow = 20  # grados para indicar que el angulo esta cambiando y evaluar otro indicador
        self.minAngleFlowCounter = 3  # numero de secuencias seguidas de flujo
        self.maxAngleUp = 60  # si supera este angulo es que esta en esa direccion con seguridad
        self.maxAngleDown = 68  # se creo par btc angulo de apertura maximo para closenxtup

        # self.startProbDef = 'getANGLE_START_BLG_04'

        # self.startProbDef = 'getANGLE_START_BLG_02'
        # self.endProbDef = 'getProb_END_HOURLY_ANGLE_04'
        # self.endProbDef = 'getANGLE_END_WEEK_NEW_01'
        # self.startProbDef = 'getANGLE_START_WEEK_NEW_01'

        # self.startProbDef = 'getANGLE_START_BLG_02'
        # self.endProbDef = 'getProb_END_HOURLY_ANGLE_03'


        self.continueFlow = False  # usado para continuar si el flujo esta en el mismo sentido en open-close
        self.ima1EmaMinValue = 0.10  # si esta mas alto que esto es que es una buena distancia
        self.hourlyAngleDiff = 25
        self.closeAcumvalue = 0.65

        self.ema10 = 10
        self.ema20 = 20
        self.min_ema_dst = 2  # > valor minimo entre ema_dst para abrir
        self.MinMaxDistance = 3  # para sacar el valor de minMax x elementos atras direction
        self.closeWeekDiffNew = 3  # > valor diff para cerrar si sube o baja respecto a week
        self.ema_change_dst = 0.2  # > valor minimo entre _dst para indicar si hay un cambio de flujo

        self.closeAngleDiff = 1.2  # grados para cerrar una apertura
        self.hourlyAngleDiff = 25  # > X no necesita segundo criterio < X si necesita
        if isDBData:
            self.rangehours = [22.5, 14.50]

        else:
            self.rangehours = [16, 9]
            # self.hourOffset = -4