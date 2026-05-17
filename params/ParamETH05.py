from service.Parameters import Parameters


# ParamETH05 — ULTRA-AGRESIVO ETH/USD ONLY BUY (EvaluatorEMA_LONG_ONLY_UP_04_02)
class ParamETH05(Parameters):

    def __init__(self, isDBData):
        super().__init__()
        self.paramName = "ParamETH05"
        self.name = "ETH_USD"
        self.second_name = "ETHUSD"

        # Tiempo
        self.difference = 3.5
        self.accumulate = 5
        self.unit = 0.8
        self.draw = False
        self.round = 5

        # Tendencia
        self.tendence_measure = 0.5
        self.tendence_distance = 3
        self.tendence_distance_moment = 6
        self.ima1 = 8
        self.ima2 = 20
        self.ima3 = 15
        self.ima4 = 50
        self.weekend = True
        self.operate = False
        self.reevaluateAction = False
        self.minimunCloseAmount = 5
        self.hourOffset = 0
        self.controlWin = True
        self.verifyMarketOpen = False

        # Volatilidad ETH (mayor que BTC)
        self.minSTDNormal = 0.40
        self.maxSTDNormal = 0.45
        self.minMEDNormal = 0.15
        self.maxMEDNormal = 0.30

        # Week
        self.weekDistanceMedDistance = 1.5
        self.weekMEDMinLevel = 0.18
        self.weekDistanceSTDDistance = 0.12
        self.weekMindiff = 0.8
        self.closeWeekDiffNew = 3

        # Relative
        self.relativeDistance = 2.2
        self.relativeDistanceMultiplicator = 0.14

        # Acumulado
        self.closeAcumvalue = 0.70
        self.closeProfit = 1.8  # 1.8% — cierre rápido para ETH

        # Distancias
        self.ima1minDistance = 0.28
        self.ima1maxDistance = 0.45
        self.ima3minDistance = 0.55
        self.percent_distance = 6
        self.percent_min_distance = 1.5

        # MEDSTD
        self.medstdminDiff = 0.18
        self.medstdmaxDiff = 0.35
        self.valueIndDIST = 1.0

        # Bollinger (ETH — canal más amplio)
        self.bollingerDst = 4
        self.enableBollingerClose = True
        self.bollinger = 10
        self.bollingerClose = 3.5
        self.blgDistPercent = 35
        self.blgMaxMinValue = 1.3
        self.blgmaMinDiff = 0.55

        # Ángulos ETH (más sensibles por volatilidad)
        self.angleUp = 2.5
        self.angleDown = 2.5
        self.minAngleIma1 = 0.4

        # EMA
        self.emaMinDst = 0.35

        # Probabilidad
        self.ignoreProb = False

        # Horario ETH (16:00-09:00 UTC)
        if isDBData:
            self.rangehours = None
        else:
            self.rangehours = [16, 9]
