from service.Parameters import Parameters

# ParamAMD para EvaluatorIMA1Optimiz_MEDDIFF_01_CORRECTED
# Ajustes basados en análisis AMD Junio 2026
class ParamAMD_CORRECTED(Parameters):

    def __init__(self, isDBData):
        super().__init__()
        self.paramName = "ParamAMD_CORRECTED"
        self.difference = 0.25
        self.accumulate = 0.5
        self.unit = 0.06
        self.draw = False
        self.round = 2

        self.tendence_measure = 0
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
        self.relativeDistance = 4.0
        self.relativeDistanceMultiplicator = 0.12
        self.weekMEDMinLevel = 0.15
        self.weekDistanceSTDDistance = 0.10
        self.closeAcumvalue = 0.30
        self.ima1minDistance = 0.25
        self.percent_distance = 6
        self.percent_min_distance = 1.5
        # MEDSTDDIFF más estricto para filtrar señales
        self.medstdminDiff = 0.20  # era 0.15 - más estricto
        self.medstdmaxDiff = 0.30
        self.ima1maxDistance = 0.40
        self.ima3minDistance = 0.5
        self.valueIndDIST = 1.0
        self.closeProfit = 1.5
        self.ignoreProb = False
        self.bollingerDst = 4
        self.enableBollingerClose = True
        self.bollinger = 10
        self.bollingerClose = 3
        self.blgDistPercent = 30
        self.angleUp = 2
        self.angleDown = 2
        self.weekMindiff = 0.7
        self.emaMinDst = 0.30
        if isDBData:
            self.rangehours = [22.5, 14.50]
        else:
            self.rangehours = [16, 9]