from service.Parameters import Parameters

#BTC
class ParamBTC05(Parameters):

    def __init__(self, isDBData):
        super().__init__()
        self.paramName = "ParamBTC05"
        self.difference = 45
        self.accumulate = 120
        self.unit = 5
        self.draw = False
        self.round = 5

        self.tendence_measure = 0
        # self.tendence_measure =0.04
        self.tendence_distance = 4
        self.tendence_distance_moment = 12
        self.ima1 = 8
        self.ima2 = 10
        self.ima3 = 15
        self.ima4 = 1
        self.weekend = True
        self.operate = True
        self.reevaluateAction = False
        self.minimunCloseAmount = 5
        self.hourOffset = 0
        self.controlWin = True
        self.verifyMarketOpen = False
        self.minSTDNormal = 0.37
        self.maxSTDNormal = 0.38
        self.minMEDNormal = 0.12
        self.maxMEDNormal = 0.25
        self.relativeDistance = 600#para indicar el maximo de distancia en relative
        self.relativeDistanceMultiplicator = 0.12#para sacar el porcentaje del valor minimo para relative
        # self.weekMEDMinLevel = 0.15  # para indicar el rango en el cual el indicador deja de ser bajo
        self.weekDistanceSTDDistance = 0.10
        self.weekDistanceMedDistance = 1.5
        self.closeAcumvalue = 50
        self.ima1minDistance = 0.25
        self.percent_distance = 6
        self.percent_min_distance = 1.5
        self.medstdminDiff = 40
        self.medstdmaxDiff = 300
        self.ima1maxDistance = 0.40
        self.ima3minDistance = 0.5
        self.valueIndDIST = 1.0
        self.closeProfit = 450
        self.ignoreProb = False
        self.bollingerDst = 15
        self.enableBollingerClose = True
        self.bollingerClose=300
        self.emaDst = 100
        self.weekMindiff=600
        self.emaMinDst = 0.30
        self.MinMaxDistance = 3
        self.weekFlowMinDiff = 2

        self.weekInterval = 10
        self.weekMEDMinLevel = 10
        self.blgDistPercent = 15
        self.bollinger = 20
        self.angleUp = 2
        self.angleDown = 2
        self.minAngleIma1 = 10
        self.minAngleFlow = 20
        self.minAngleFlowCounter = 3
        self.maxOpenCount = 7
        self.maxWeekBootDist = 70
        self.maxAngleUp = 88  # si supera este angulo es que esta en esa direccion con seguridad
        self.maxAngleDown = 88  # se creo par btc angulo de apertura maximo para closenxtup

        if isDBData:
            self.rangehours = None

        else:
            self.rangehours = [16, 9]
            # self.hourOffset = -4