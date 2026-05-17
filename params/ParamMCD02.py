from service.Parameters import Parameters

#AMZN
class ParamMCD02(Parameters):

    def __init__(self, isDBData):
        super().__init__()
        self.paramName = "ParamMCD02"
        self.difference = 0.25
        self.accumulate = 0.60
        self.unit = 0.04
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
        self.weekDistanceMedDistance = 1.5
        self.relativeDistance = 8.0#para indicar el maximo de distancia en relative
        self.relativeDistanceMultiplicator = 0.22#para sacar el porcentaje del valor minimo para relative
        self.weekMEDMinLevel = 0.15  # para indicar el rango en el cual el indicador deja de ser bajo
        self.weekDistanceSTDDistance = 0.10
        self.closeAcumvalue = 0.25
        self.ima1minDistance = 0.25
        self.percent_distance = 6
        self.percent_min_distance = 1.5
        self.medstdminDiff = 0.08
        self.medstdmaxDiff = 2.80
        self.ima1maxDistance = 0.40
        self.ima3minDistance = 0.5
        self.valueIndDIST = 1.0
        self.closeProfit = 0.5
        self.ignoreProb = False
        self.bollingerDst = 0.3
        self.enableBollingerClose = True
        self.bollinger=10
        self.bollingerClose=0.8
        self.blgDistPercent=30
        self.angleUp = 2
        self.angleDown = 2
        self.weekMindiff=0.7
        self.emaMinDst = 0.10
        self.weekInterval = 5
        # self.startProbDef = 'getProb_WEEK_DIRECTION_02'
        # self.endProbDef = 'getProb_WEEK_DIRECTION_01'

        self.weekInterval = 10
        self.bollinger = 5
        self.angleUp = 2
        self.angleDown = 2
        self.blgDistPercent = 10
        self.weekMEDMinLevel = 2
        self.minAngleIma1 = 5
        self.ignoreProb = False
        self.minAngleFlow = 25  # grados para indicar que el angulo esta cambiando y evaluar otro indicador
        self.minAngleFlowCounter = 3  # numero de secuencias seguidas de flujo
        self.maxAngleUp = 60  # si supera este angulo es que esta en esa direccion con seguridad
        self.maxAngleDown = 68  # se creo par btc angulo de apertura maximo para closenxtup
        # self.startProbDef = 'getProb_START_ANGLE_H_01'
        # self.endProbDef = 'getProb_HOURLY_ANGLE_01'
        self.continueFlow = True  # usado para continuar si el flujo esta en el mismo sentido en open-close
        self.ima1EmaMinValue = 0.10  # si esta mas alto que esto es que es una buena distancia
        self.closeAcumvalue = 0.085
        self.closeAngleDiff = 1.2  # grados para cerrar una apertura
        self.hourlyAngleDiff = 20  # > X no necesita segundo criterio < X si necesita

        if isDBData:
            self.rangehours = [22.5, 14.50]

        else:
            self.rangehours = [16, 9]
            # self.hourOffset = -4