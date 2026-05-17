from service.Parameters import Parameters

#AMZN
class ParamAMZN05(Parameters):

    def __init__(self, isDBData):
        super().__init__()
        self.paramName = "ParamAMZN05"
        self.difference = 0.20
        self.accumulate = 0.35
        self.unit = 0.04
        self.draw = False
        self.round = 2

        # self.tendence_measure =0.0001
        self.tendence_measure = 0.00
        self.tendence_distance = 3
        self.tendence_distance_moment = 6
        self.ima1 = 3
        self.ima2 = 5
        self.ima3 = 10
        self.ima4 = 1
        self.weekend = False
        self.operate = True
        self.reevaluateAction = False
        self.minimunCloseAmount = 5
        self.hourOffset = 0
        self.controlWin = True
        self.verifyMarketOpen = True
        self.minSTDNormal = 0.15
        self.maxSTDNormal = 0.17
        self.minMEDNormal = 0.10
        self.maxMEDNormal = 0.10
        self.weekDistanceMedDistance = 2#sobre este valor en med se ignora
        self.relativeDistance = 4.0#para indicar el maximo de distancia en relative
        self.relativeDistanceMultiplicator = 0.20#para sacar el porcentaje del valor minimo para relative
        self.weekMEDMinLevel = 0.5  # para indicar el rango en el cual el indicador deja de ser bajo
        self.weekDistanceSTDDistance = 0.5 # para indicar el rango en el cual el indicador week STD tiene un valor bajo
        self.closeAcumvalue = 0.30
        self.ima1minDistance = 0.30
        self.percent_distance = 6
        self.percent_min_distance = 1.5
        self.medstdminDiff = 0.15
        self.medstdmaxDiff = 2.30
        self.ima1maxDistance = 0.40
        self.ima3minDistance = 0.5
        self.valueIndDIST = 1.0
        self.closeProfit = 0.4
        self.bollingerDst = 3
        self.enableBollingerClose = True
        self.bollinger=10
        self.bollingerClose=1
        self.blgDistPercent=30
        self.angleUp = 2
        self.angleDown = 2
        self.weekMindiff=0.3
        self.emaMinDst = 0.30



        self.weekInterval = 10
        self.bollinger = 20
        self.angleUp = 2
        self.angleDown = 2
        self.ema10 = 15
        self.ema20 = 25
        self.blgDistPercent = 10
        self.weekMEDMinLevel = 2
        self.minAngleIma1 = 15
        self.ignoreProb = False
        self.minAngleFlow = 10  # grados para indicar que el angulo esta cambiando y evaluar otro indicador
        self.minAngleFlowCounter = 3  # numero de secuencias seguidas de flujo
        self.maxAngleUp = 60  # si supera este angulo es que esta en esa direccion con seguridad
        self.maxAngleDown = 68  # se creo par btc angulo de apertura maximo para closenxtup
        # self.endProbDef = 'getANGLE_END_BLG_01'
        # self.startProbDef = 'getANGLE_START_BLG_01'
        # self.endProbDef = 'getANGLE_END_BLG_01'
        # self.endProbDef = 'getProMEDSTD_END_BLG_08'
        self.endProbDef = 'getProb_END_HOURLY_ANGLE_02'
        self.startProbDef = 'getANGLE_START_EMA_RSI_01'
        # self.endProbDef = 'getProb_HOURLY_ANGLE_01'
        # self.startProbDef = 'getProb_WEEK_DIRECTION_02'
        self.continueFlow = True  # usado para continuar si el flujo esta en el mismo sentido en open-close
        self.ima1EmaMinValue = 0.10  # si esta mas alto que esto es que es una buena distancia
        self.closeWeekDiffNew = 2  # > valor diff para cerrar si sube o baja respecto a week

        if isDBData:
            self.rangehours = [22.5, 14.50]

        else:
            self.rangehours = [16, 9]
            # self.hourOffset = -4