from service.Parameters import Parameters

#AMZN
class ParamHD01(Parameters):

    def __init__(self, isDBData):
        super().__init__()
        self.paramName = "ParamHD01"
        self.difference = 0.30
        self.accumulate = 1.2
        self.unit = 0.15
        self.draw = False
        self.round = 2

        # self.tendence_measure =0.0001
        self.tendence_measure = 0.00
        self.tendence_distance = 3
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
        self.closeAcumvalue = 0.65
        self.ima1minDistance = 0.10
        self.percent_distance = 10
        self.percent_min_distance = 1.5
        self.medstdminDiff = 0.15
        self.medstdmaxDiff = 1.50
        self.ima1maxDistance = 1.40
        self.ima3minDistance = 0.5
        self.valueIndDIST = 1.0
        self.closeProfit = 0.5
        self.ignoreProb = False
        self.bollingerDst = 4
        self.enableBollingerClose = True
        self.bollinger=10
        self.bollingerClose=1.5
        self.blgDistPercent=30
        self.angleUp = 2
        self.angleDown = 2
        self.weekMindiff=0.5
        self.emaMinDst = 0.30
        # self.normalProbDef = 'evaluate_WEEK_ANGLE_FLOW_START_01'

        self.weekInterval = 10
        self.bollinger = 20
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
        # self.endProbDef = 'getProMEDSTD_END_BLG_08'
        # self.startProbDef = 'getANGLE_START_BLG_02'
        # self.endProbDef = 'getProb_HOURLY_ANGLE_01'
        # self.startProbDef = 'getProb_WEEK_DIRECTION_02'
        self.continueFlow = True  # usado para continuar si el flujo esta en el mismo sentido en open-close
        self.ima1EmaMinValue = 0.10  # si esta mas alto que esto es que es una buena distancia

        self.closeAngleDiff = 0.1  # grados para cerrar una apertura
        self.hourlyAngleDiff = 20  # > X no necesita segundo criterio < X si necesita

        if isDBData:
            self.rangehours = [22.5, 14.50]

        else:
            self.rangehours = [16, 9]
            # self.hourOffset = -4