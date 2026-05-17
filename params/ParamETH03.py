from service.Parameters import Parameters

#ETH
class ParamETH03(Parameters):

    def __init__(self, isDBData):
        super().__init__()
        self.paramName = "ParamETH03"
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
        self.MinMaxDistance=3


        self.weekInterval = 10
        self.weekMEDMinLevel = 10
        self.blgDistPercent = 10
        self.bollinger = 10
        self.angleUp = 5
        self.angleDown = 5
        self.minAngleIma1 = 20
        self.minAngleFlow = 10 #grados para indicar que el angulo esta cambiando
        self.minAngleFlowCounter = 3
        self.maxOpenCount = 7
        self.maxWeekBootDist = 70
        self.maxAngleUp = 88  # si supera este angulo es que esta en esa direccion con seguridad
        self.maxAngleDown = 88  # se
        self.closeAngleDiff = 1.2  #  < grados para cerrar una apertura
        self.ma_dist_min = 1.5

        self.ema10 = 5
        self.ema20 = 20
        self.closeWeekDiffNew = 1.2  # > valor diff para cerrar si sube o baja respecto a week
        self.min_ema_dst = 4  # > valor minimo entre ema_dst para abrir

        self.continueFlow = True  # usado para continuar si el flujo esta en el mismo sentido en open-close
        self.ima1EmaMinValue = 3
        self.closeAngleDiff = 1.2  # grados para cerrar una apertura
        self.hourlyAngleDiff = 25  # > X no necesita segundo criterio < X si necesita
        self.MinMaxDistance = 3  # para sacar el valor de minMax x elementos atras direction
        self.closeWeekDiffNew = 2  # > valor diff para cerrar si sube o baja respecto a week
        self.ema_change_dst = 0.2  # > valor minimo entre _dst paemara indicar si hay un cambio de flujo
        self.ma_dist_int = 3  # > numero de dias atras para ver el flujo en BLG_MA_X
        self.blg_max_min_value = 1.5  # > valor minimo entre para iniciar una compra o venta basado en la diferencia blg_max_X
        self.minEmaAngle = 50  # evita mercado lateral
        self.minTrendIntensity = 0.3  # filtra ruido
        self.minEmaDistance = 50  # distancia mínima a EMA (ajustar)

        self.cross_periods = 25
        self.price_range_periods = 25
        self.cross_count = 3

        if isDBData:
            self.rangehours = None

        else:
            self.rangehours = [16, 9]
            # self.hourOffset = -4