from service.Parameters import Parameters

#APPL
class ParamBABA01(Parameters):

    def __init__(self, isDBData):
        super().__init__()
        self.paramName = "ParamBABA01"
        self.difference = 0.20
        self.accumulate = 0.3
        self.unit = 0.02
        self.draw = False
        self.round = 2

        self.tendence_measure = 0
        # self.tendence_measure =0.06
        self.tendence_distance = 4
        self.tendence_distance_moment = 6
        self.ima1 = 3
        self.ima2 = 8
        self.ima3 = 15
        self.ima4 = 2
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
        self.weekMEDMinLevel = 0.15  # para indicar el rango en el cual el indicador deja de ser bajo
        self.weekDistanceSTDDistance = 0.10
        self.closeAcumvalue = 0.20
        self.ima1minDistance = 0.25
        self.percent_distance = 6
        self.percent_min_distance = 1.5
        self.medstdminDiff = 0.05
        self.medstdmaxDiff = 2.60
        self.ima1maxDistance = 0.40
        self.ima3minDistance = 0.5
        self.valueIndDIST = 1.0
        self.closeProfit = 0.3
        self.ignoreProb = False
        self.bollingerDst = 3
        self.enableBollingerClose = True
        self.bollinger=10
        self.bollingerClose=3
        self.blgDistPercent=10
        self.angleUp = 1
        self.angleDown = 1
        self.weekMindiff=0.7
        self.emaMinDst = 0.30
        self.startProbDef = 'evaluate_WEEK_ANGLE_FLOW_START_02'


        if isDBData:
            self.rangehours = [22.5, 14.50]

        else:
            self.rangehours = [16, 9]
            # self.hourOffset = -4