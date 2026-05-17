from service.Parameters import Parameters

#APPL
class ParamAAPL03(Parameters):

    def __init__(self, isDBData):
        super().__init__()
        self.paramName = "ParamAAPL03"
        self.difference = 0.20
        self.accumulate = 0.5
        self.unit = 0.06
        self.draw = False
        self.round = 2

        self.tendence_measure = 0
        # self.tendence_measure =0.04
        self.tendence_distance = 4
        self.tendence_distance_moment = 6
        self.ima1 = 3
        self.ima2 = 8
        self.ima3 = 15
        self.ima4 = 1
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
        # self.weekMEDMinLevel = 0.15  # para indicar el rango en el cual el indicador deja de ser bajo
        self.weekDistanceSTDDistance = 0.10
        self.closeAcumvalue = 0.25
        self.ima1minDistance = 0.25
        self.percent_distance = 5
        self.percent_min_distance = 1.5
        self.medstdminDiff = 0.04
        self.medstdmaxDiff = 2.25
        self.ima1maxDistance = 0.40
        self.ima3minDistance = 0.5
        self.valueIndDIST = 1.0
        self.closeProfit = 0.3
        self.bollingerDst = 3
        self.enableBollingerClose = True
        self.bollingerClose=0.33
        self.weekMindiff=0.7
        self.emaMinDst = 0.30

        self.weekInterval = 10
        self.bollinger = 20
        self.angleUp = 2
        self.angleDown = 2
        self.blgDistPercent = 10
        self.weekMEDMinLevel = 2
        self.minAngleIma1 = 10
        self.ignoreProb = False
        self.minAngleFlow = 10  # grados para indicar que el angulo esta cambiando y evaluar otro indicador
        self.minAngleFlowCounter = 3  # numero de secuencias seguidas de flujo
        self.maxAngleUp = 60  # si supera este angulo es que esta en esa direccion con seguridad
        self.maxAngleDown = 68  # se creo par btc angulo de apertura maximo para closenxtup
        # self.endProbDef = 'getProMEDSTD_END_BLG_08'
        # self.startProbDef = 'getProb_WEEK_DIRECTION_02'
        self.startProbDef = 'getProb_START_ANGLE_H_01'
        self.endProbDef = 'getProb_HOURLY_ANGLE_01'
        self.continueFlow = True  # usado para continuar si el flujo esta en el mismo sentido en open-close
        self.ima1EmaMinValue = 0.10  # si esta mas alto que esto es que es una buena distancia

        self.closeAngleDiff = 1.2 # grados para cerrar una apertura
        if isDBData:
            self.rangehours = [22.5, 14.50]

        else:
            self.rangehours = [16, 9]
            # self.hourOffset = -4