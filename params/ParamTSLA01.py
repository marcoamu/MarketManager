from service.Parameters import Parameters

#TSLA
class ParamTSLA01(Parameters):

    def __init__(self, isDBData):
        super().__init__()
        self.paramName = "ParamTSLA01"
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
        self.ima2 = 8
        self.ima3 = 12
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
        # self.weekMEDMinLevel = 0.15  # para indicar el rango en el cual el indicador deja de ser bajo
        self.weekDistanceSTDDistance = 0.10
        self.closeAcumvalue = 0.5
        self.ima1minDistance = 0.02
        self.percent_distance = 6
        self.percent_min_distance = 1.5
        self.medstdminDiff = 0.05
        self.medstdmaxDiff = 2.60
        self.ima1maxDistance = 2.0
        self.ima3minDistance = 0.8
        self.valueIndDIST = 1.0
        self.closeProfit = 1
        self.bollingerDst = 0.20
        self.enableBollingerClose = True
        self.bollingerClose=1.5
        self.weekMindiff=0.7
        self.emaMinDst = 0.15
        self.weekDirectionInterval = '1H'
        # self.endProbDef = 'evaluate_WEEK_ANGLE_FLOW_END_02'
        # self.startProbDef = 'evaluate_WEEK_ANGLE_FLOW_START_02'
        # self.startProbDef = 'getProb_WEEK_DIRECTION_02'
        # self.endProbDef = 'getProMEDSTD_END_BLG_07'
        # self.normalProbDef = 'evaluate_NORMAL_ANGLE_FLOW_01'



        self.weekInterval = 10
        self.bollinger=20
        self.angleUp = 2
        self.angleDown = 2
        self.blgDistPercent = 10
        self.weekMEDMinLevel = 3
        self.minAngleIma1 = 10
        self.ignoreProb = False
        self.minAngleFlow = 10  # grados para indicar que el angulo esta cambiando y evaluar otro indicador
        self.minAngleFlowCounter = 3  # numero de secuencias seguidas de flujo
        self.maxAngleUp = 60  # si supera este angulo es que esta en esa direccion con seguridad
        self.maxAngleDown = 68  # se creo par btc angulo de apertura maximo para closenxtup
        # self.endProbDef = 'getANGLE_END_BLG_01'
        self.startProbDef = 'getProb_START_ANGLE_H_01'
        self.endProbDef = 'getProb_END_HOURLY_ANGLE_03'
        # self.startProbDef = 'getProb_START_ANGLE_H_01'
        self.continueFlow = True  # usado para continuar si el flujo esta en el mismo sentido en open-close
        self.ima1EmaMinValue = 0.10
        self.closeAngleDiff = 1.2  # grados para cerrar una apertura
        self.hourlyAngleDiff = 25  # > X no necesita segundo criterio < X si necesita

        if isDBData:
            self.rangehours = [22.5, 15.50]

        else:
            self.rangehours = [16, 9]
            # self.hourOffset = -4