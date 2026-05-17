from service.Parameters import Parameters

#ETH
class ParamETH02(Parameters):

    def __init__(self, isDBData):
        super().__init__()
        self.paramName = "ParamETH02"
        self.difference = 9
        self.accumulate = 15
        self.unit = 1.2
        self.draw = False
        self.round = 5

        self.tendence_measure = 0
        # self.tendence_measure =0.04
        self.tendence_distance = 3
        self.tendence_distance_moment = 6
        self.ima1 = 5
        self.ima2 = 30
        self.ima3 = 15
        self.ima4 = 50
        self.weekend = True
        self.operate = False
        self.reevaluateAction = False
        self.minimunCloseAmount = 5
        self.hourOffset = 0
        self.controlWin = True
        self.verifyMarketOpen = False
        self.minSTDNormal = 0.37
        self.maxSTDNormal = 0.38
        self.minMEDNormal = 0.12
        self.maxMEDNormal = 0.25
        self.weekDistanceMedDistance = 1.5
        self.relativeDistance = 2.0#para indicar el maximo de distancia en relative
        self.relativeDistanceMultiplicator = 0.12#para sacar el porcentaje del valor minimo para relative
        self.weekMEDMinLevel = 0.15  # para indicar el rango en el cual el indicador deja de ser bajo
        self.weekDistanceSTDDistance = 0.10
        self.closeAcumvalue = 0.65
        self.ima1minDistance = 0.25
        self.percent_distance = 6
        self.percent_min_distance = 1.5
        self.medstdminDiff = 0.15
        self.medstdmaxDiff = 0.30
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
            self.rangehours = None

        else:
            self.rangehours = [16, 9]
            # self.hourOffset = -4