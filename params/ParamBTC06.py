from service.Parameters import Parameters

#BTC
class ParamBTC06(Parameters):

    def __init__(self, isDBData):
        super().__init__()
        self.paramName = "ParamBTC06"
        self.difference = 45
        self.accumulate = 120
        self.unit = 5
        self.draw = False
        self.round = 5

        self.tendence_measure = 0
        # self.tendence_measure =0.04
        self.tendence_distance = 4
        self.tendence_distance_moment = 12
        self.ima1 = 3
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
        self.closeProfit = 550
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
        self.bollinger = 10
        self.angleUp = 2
        self.angleDown = 2
        self.minAngleIma1 = 10
        self.minAngleFlow = 20
        self.minAngleFlowCounter = 3
        self.maxOpenCount = 7
        self.maxWeekBootDist = 70
        self.maxAngleUp = 88  # si supera este angulo es que esta en esa direccion con seguridad
        self.maxAngleDown = 88  # se creo par btc angulo de apertura maximo para closenxtup
        self.min_ema_dst = 150  # > valor minimo entre ema_dst para abrir

        self.continueFlow = True  # usado para continuar si el flujo esta en el mismo sentido en open-close
        self.ima1EmaMinValue = 50
        self.closeAngleDiff = 1.2  # grados para cerrar una apertura
        self.hourlyAngleDiff = 25  # > X no necesita segundo criterio < X si necesita
        self.ema10 = 10
        self.ema20 = 25
        self.MinMaxDistance = 3  # para sacar el valor de minMax x elementos atras direction
        self.closeWeekDiffNew = 1.5  # > valor diff para cerrar si sube o baja respecto a week
        self.ema_change_dst = 0.2  # > valor minimo entre _dst paemara indicar si hay un cambio de flujo

        self.blg_max_min_value = 10  # > valor minimo entre para iniciar una compra o venta basado en la diferencia blg_max_X

        self.blgma_dst = 4  # valores sobre los cuales se hara la media de blgMA
        self.blgma_min_diff = 20  # minimo valor para identificar una tendencia sobre este valor si esta en tendencia
        self.weekNewMinFlow = 2  # valor minimo para abrir o cerrar en un weekflow
        self.minEmaAngle = 70  # evita mercado lateral
        self.minTrendIntensity = 0.3  # filtra ruido
        self.minEmaDistance = 100 # distancia mínima a EMA (ajustar)

        if isDBData:
            self.rangehours = None

        else:
            self.rangehours = [16, 9]
            # self.hourOffset = -4