from service.Parameters import Parameters

#ETH
class ParamETH04(Parameters):

    def __init__(self, isDBData):
        super().__init__()
        self.paramName = "ParamETH04"
        self.difference = 5
        self.accumulate = 8
        self.unit = 0.4
        self.draw = False
        self.round = 5

        self.tendence_measure = 0
        # self.tendence_measure =0.04
        self.tendence_distance = 4
        self.tendence_distance_moment = 6
        self.ima1 = 3
        self.ima2 = 10
        self.ima3 = 13
        self.ima4 = 2
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
        self.weekDistanceMedDistance = 1.5
        self.relativeDistance = 2.0#para indicar el maximo de distancia en relative
        self.relativeDistanceMultiplicator = 0.12#para sacar el porcentaje del valor minimo para relative
        # self.weekMEDMinLevel = 0.15  # para indicar el rango en el cual el indicador deja de ser bajo
        self.weekDistanceSTDDistance = 0.10
        self.closeAcumvalue = 0.65
        self.ima1minDistance = 0.25
        self.percent_distance = 6
        self.percent_min_distance = 1.5
        self.medstdminDiff = 0.25
        self.medstdmaxDiff = 20.0
        self.ima1maxDistance = 0.40
        self.ima3minDistance = 0.5
        self.valueIndDIST = 1.0
        self.closeProfit = 10
        self.ignoreProb = False
        self.bollingerDst = 10
        self.enableBollingerClose = True
        self.bollingerClose=15
        self.weekMindiff=10
        self.emaMinDst = 10
        self.flowDiffInterval = 10
        self.minflowDiff = 5
        self.weekDirectionInterval = '2H'
        self.MinMaxDistance=7


        self.weekInterval = 10
        self.weekMEDMinLevel = 10
        self.blgDistPercent = 10
        self.bollinger = 20
        self.angleUp = 2
        self.angleDown = 2
        self.minAngleIma1 = 10
        self.minAngleFlow = 5 #grados para indicar que el angulo esta cambiando
        self.minAngleFlowCounter = 3
        self.maxOpenCount = 7
        self.maxWeekBootDist = 70
        self.maxAngleUp = 88  # si supera este angulo es que esta en esa direccion con seguridad
        self.maxAngleDown = 88  # se
        self.closeAngleDiff = 2  # grados para cerrar una apertura


        if isDBData:
            self.rangehours = None

        else:
            self.rangehours = [16, 9]
            # self.hourOffset = -4