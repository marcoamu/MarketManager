from service.Parameters import Parameters

#AMZN
class ParamINTC05(Parameters):

    def __init__(self, isDBData):
        super().__init__()
        self.paramName = "ParamINTC05"
        self.difference = 0.080
        self.accumulate = 0.18
        self.unit = 0.002
        self.draw = False
        self.round = 2

        # self.tendence_measure =0.0001
        self.tendence_measure = 0.00
        self.tendence_distance = 3
        self.tendence_distance_moment = 6
        self.ima1 = 5
        self.ima2 = 8
        self.ima3 = 12
        self.ima4 = 1
        self.weekend = False
        self.operate = True
        self.reevaluateAction = False
        self.minimunCloseAmount = 5
        self.hourOffset = 0
        self.controlWin = True
        self.verifyMarketOpen = True
        self.minSTDNormal = 0.04
        self.maxSTDNormal = 0.04
        self.minMEDNormal = 0.04
        self.maxMEDNormal = 0.04
        self.relativeDistance = 2.0#para indicar el maximo de distancia en relative
        self.relativeDistanceMultiplicator = 0.22#para sacar el porcentaje del valor minimo para relative
        self.weekDistanceMedDistance = 1.5
        self.weekMEDMinLevel = 0.15#para indicar el rango en el cual el indicador deja de ser bajo
        self.weekDistanceSTDDistance = 0.20
        self.closeAcumvalue = 0.085
        self.ima1minDistance = 0.25
        self.percent_distance = 6
        self.percent_min_distance = 1.5
        self.medstdminDiff = 0.020
        self.medstdmaxDiff = 2.30
        self.ima1maxDistance = 0.40
        self.ima3minDistance = 0.5
        self.valueIndDIST = 1.0
        self.closeProfit = 0.3
        self.ignoreProb = False
        self.bollingerDst = 0.20
        self.enableBollingerClose = True
        self.bollinger=40
        self.bollingerClose=3
        self.blgDistPercent=30
        self.angleUp = 2
        self.angleDown = 2
        self.weekMindiff=0.7
        self.emaMinDst = 0.30
        if isDBData:
            self.rangehours = [22.5, 14.50]

        else:
            self.rangehours = [16, 9]
            # self.hourOffset = -4