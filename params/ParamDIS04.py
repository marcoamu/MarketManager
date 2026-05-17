from service.Parameters import Parameters

#DIS
class ParamDIS04(Parameters):

    def __init__(self, isDBData):
        super().__init__()
        self.paramName = "ParamDIS04"
        self.difference = 0.12
        self.accumulate = 0.26
        self.unit = 0.03
        self.draw = False
        self.round = 2

        # self.tendence_measure =0.0001
        self.tendence_measure = 0
        self.tendence_distance = 4
        self.tendence_distance_moment = 6
        self.ima1 = 3
        self.ima2 = 10
        self.ima3 = 13
        self.ima4 = 1
        self.weekend = False
        self.operate = True
        self.reevaluateAction = True
        self.minimunCloseAmount = 5
        self.hourOffset = 0
        self.controlWin = True
        self.verifyMarketOpen = True
        self.minSTDNormal = 0.06
        self.maxSTDNormal = 0.06
        self.minMEDNormal = 0.04
        self.maxMEDNormal = 0.04
        self.weekDistanceMedDistance = 1.5
        self.relativeDistance = 2.0#para indicar el maximo de distancia en relative
        self.relativeDistanceMultiplicator = 0.12#para sacar el porcentaje del valor minimo para relative
        self.weekMEDMinLevel = 0.15  # para indicar el rango en el cual el indicador deja de ser bajo
        self.weekDistanceSTDDistance = 0.10
        self.closeAcumvalue = 0.12
        self.ima1minDistance = 0.05
        self.percent_distance = 6
        self.percent_min_distance = 1.5
        self.medstdminDiff = 0.017
        self.medstdmaxDiff = 2.20
        self.ima1maxDistance = 0.40
        self.ima3minDistance = 0.2
        self.valueIndDIST = 1.0
        self.closeProfit = 0.5
        self.ignoreProb = False
        self.bollingerDst = 0.10
        self.enableBollingerClose = True
        self.bollinger=10
        self.bollingerClose=0.8
        self.blgDistPercent=30
        self.angleUp = 2
        self.angleDown = 2
        self.weekMindiff=0.7
        self.emaMinDst = 0.20
        # self.startProbDef = 'getProb_WEEK_DIRECTION_02'
        # self.endProbDef = 'getProb_WEEK_DIRECTION_01'

        self.weekInterval = 10
        self.bollinger = 20
        self.angleUp = 5
        self.angleDown = 5
        self.blgDistPercent = 10
        self.weekMEDMinLevel = 2
        self.minAngleIma1 = 15

        self.minAngleFlow = 12  # grados para indicar que el angulo esta cambiando y evaluar otro indicador
        self.minAngleFlowCounter = 3  # numero de secuencias seguidas de flujo
        self.maxAngleUp = 60  # si supera este angulo es que esta en esa direccion con seguridad
        self.maxAngleDown = 68  # se creo par btc angulo de apertura maximo para closenxtup
        # self.endProbDef = 'getANGLE_END_BLG_01'
        # self.startProbDef = 'getProb_WEEK_DIRECTION_03'
        # self.endProbDef = 'getANGLE_END_BLG_01'
        # self.endProbDef = 'getProMEDSTD_END_BLG_08'
        # self.startProbDef = 'getProb_WEEK_DIRECTION_02'
        self.continueFlow = True  # usado para continuar si el flujo esta en el mismo sentido en open-close
        self.ima1EmaMinValue = 0.10  # si esta mas alto que esto es que es una buena distancia
        self.middleDstPercent = 8  # distancia en porcentaje hacia el centro de anglulo blg

        if isDBData:
            self.rangehours = [22.5, 14.50]

        else:
            self.rangehours = [16, 9]
            # self.hourOffset = -4