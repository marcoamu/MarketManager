from service.Parameters import Parameters

#AMZN
class ParamNVDA02(Parameters):

    def __init__(self, isDBData):
        super().__init__()
        self.paramName = "ParamNVDA02"
        self.difference = 0.65
        self.accumulate = 1.2
        self.unit = 0.15
        self.draw = False
        self.round = 2

        # self.tendence_measure =0.0001
        self.tendence_measure = 0.00
        self.tendence_distance = 3
        self.tendence_distance_moment = 6
        self.ima1 = 2
        self.ima2 = 5
        self.ima3 = 8
        self.ima4 = 50
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
        self.ima3minDistance = 3
        self.valueIndDIST = 1.0
        self.closeProfit = 2
        self.ignoreProb = False
        self.bollingerDst = 0.20
        self.enableBollingerClose = True
        self.bollinger=5
        self.bollingerClose=5
        self.blgDistPercent=15
        self.angleUp = 2
        self.angleDown = 2
        self.weekMindiff=0.7
        self.emaMinDst = 0.05
        if isDBData:
            self.rangehours = [22.5, 14.50]

        else:
            self.rangehours = [16, 9]
            # self.hourOffset = -4