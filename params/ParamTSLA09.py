from service.Parameters import Parameters

#TSLA
class ParamTSLA09(Parameters):

    def __init__(self, isDBData):
        super().__init__()
        self.paramName = "ParamTSLA09"
        self.difference = 0.50
        self.accumulate = 1.0
        self.unit = 0.10
        self.draw = False
        self.round = 2

        # self.tendence_measure =0.0001
        self.tendence_measure = 0
        self.tendence_distance = 3
        self.tendence_distance_moment = 8
        self.ima1 = 3
        self.ima2 = 5
        self.ima3 = 8
        self.ima4 = 1
        self.weekend = False
        self.operate = True
        self.reevaluateAction = False
        self.hourOffset = 0
        self.minimunCloseAmount = 5
        self.controlWin = True
        self.verifyMarketOpen = True
        self.minSTDNormal = 0.37
        self.maxSTDNormal = 0.38
        self.minMEDNormal = 0.12
        self.maxMEDNormal = 0.25
        self.weekDistanceMedDistance = 1.5
        self.relativeDistance = 9.0 #para indicar el maximo de distancia en relative
        self.relativeDistanceMultiplicator = 0.22#para sacar el porcentaje del valor minimo para relative
        self.weekMEDMinLevel = 0.15  # para indicar el rango en el cual el indicador deja de ser bajo
        self.weekDistanceSTDDistance = 0.10
        self.closeAcumvalue = 0.5
        self.ima1minDistance = 0.20
        self.percent_distance = 6
        self.percent_min_distance = 1.5
        self.medstdminDiff = 0.08
        self.medstdmaxDiff = 0.40
        self.ima1maxDistance = 0.40
        self.ima3minDistance = 0.5
        self.valueIndDIST = 1.0
        self.closeProfit = 1.5
        self.ignoreProb = False
        self.bollingerDst = 4
        self.enableBollingerClose = True
        self.bollinger=10
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