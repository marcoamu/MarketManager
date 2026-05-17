class Parameters:


    def __init__(self):
        self.name = None
        self.second_name = None
        self.url = None
        self.monitorType = None
        self.difference = None
        self.accumulate = None
        self.tele_group = -4150708541
        self.round = None
        self.draw = None
        self.unit = None
        self.tendence_measure = None
        self.ima1 = None
        self.ima2 = None
        self.ima3 = None
        self.ima4 = None
        self.ema10= 10
        self.ema20= 20
        self.ema50= 50
        self.weekend = None
        self.tendence_distance = None
        self.operate = None
        self.rangehours = None
        self.hourOffset = 0
        self.reevaluateAction = False
        self.minimunCloseAmount = 5
        self.verifyMarketOpen = True
        self.controlWin = False
        self.minSTDNormal = 0.25
        self.maxSTDNormal = 0.50
        self.minMEDNormal = 0.25
        self.maxMEDNormal = 0.50
        self.flowDiffInterval = 4
        self.minflowDiff = 5
        self.weekDirectionInterval = '1H'
        # self.startProbDef = 'getProb_WEEK_DIRECTION_02'
        # self.endProbDef = 'getProMEDSTD_END_BLG_07'
        # self.startProbDef = 'getProb_START_ANGLE_H_01'
        # self.endProbDef = 'getProb_HOURLY_ANGLE_01'
        self.normalProbDef = 'evaluate_NORMAL_ANGLE_FLOW_01'

        # self.endProbDef = 'getANGLE_END_WEEK_NEW_01'
        # self.startProbDef = 'getANGLE_START_WEEK_NEW_01'

        # self.startProbDef = 'getANGLE_START_BLG_03'
        # self.endProbDef = 'getANGLE_END_WEEK_NEW_02'

        self.startProbDef = 'getANGLE_START_EMA_RSI_01'
        self.endProbDef = 'getProb_END_EMA_RSI_01'

        # self.startProbDef = 'evaluate_WEEK_ANGLE_FLOW_START_01'
        # self.endProbDef = 'evaluate_WEEK_ANGLE_FLOW_END_01'
        # self.normalProbDef = 'evaluate_NORMAL_ANGLE_FLOW_01'
        self.weekInterval = 10

        self.weekFlowMinDiff = 5#valores para weekdirflow
        self.angleUp = 20
        self.maxAngleUp = 60 #si supera este angulo es que esta en esa direccion con seguridad
        self.maxAngleDown = 60 ##si supera este angulo es que esta en esa direccion con seguridad
        self.angleDown = 20
        self.minAngleIma1 = 0.5
        self.middleDstPercent = 8 #distancia en porcentaje hacia el centro de anglulo blg
        self.weekMEDMinLevel = 0.10
        self.minAngleFlow = 10 #grados para indicar que el angulo esta cambiando y evaluar otro indicador
        self.minAngleFlowCounter = 3  # numero de secuencias seguidas de flujo
        self.maxWeekBootDist = 70 #usado para discriminar abrir muy tarde en BTC
        self.maxOpenCount = 8
        self.continueFlow = False #usado para continuar si el flujo esta en el mismo sentido en open-close
        self.ima1EmaMinValue = 0.10 #valor para indicar cuando sube o baja segun ima1Ema
        self.closeAngleDiff = 1.2  #grados para cerrar una apertura
        self.hourlyAngleDiff = 20  #> X no necesita segundo criterio < X si necesita
        self.ma_dist_int = 3  #> numero de dias atras para ver el flujo en MA(20)
        self.ma_dist_min = 1.5  #> valor minimo para considerarse que ha cambiado, ejemplo -2 si pasan de -2 entonces es un valor valido
        self.closeWeekDiffNew = 3  #> valor diff para cerrar si sube o baja respecto a week
        self.min_ema_dst = 2  #> valor minimo entre ema_dst para abrir
        self.ema_change_dst = 0.2  # > valor minimo entre _dst paemara indicar si hay un cambio de flujo
        self.blg_max_min_value = 1.2  # > valor minimo entre para iniciar una compra o venta basado en la diferencia blg_max_X

        self.blgma_dst = 4 #valores sobre los cuales se hara la media de blgMA
        self.blgma_min_diff = 0.5 #minimo valor para identificar una tendencia sobre este valor si esta en tendencia

        self.MinMaxDistance = 3  # para sacar el valor de minMax x elementos atras direction
        self.weekNewMinFlow = 1 #valor minimo para abrir o cerrar en un weekflow
        self.controlSELL = "1" #metodo para control sell dinamico
        self.controlBUY = "1" #metodo para control sell dinamico
        self.dinamicControl = False
        self.profit = 5
        self.max_loss_usd = 5
        self.protect_profit_usd = 5

        #recomendaciones IA
        self.minEmaAngle = 5  # evita mercado lateral
        self.minTrendIntensity = 0.3  # filtra ruido
        self.minEmaDistance = 0.002  # distancia mínima a EMA (ajustar)
        self.bollingerLowThreshold = 20  # % cerca banda inferior
        self.bollingerHighThreshold = 80  # % cerca banda superior
        self.cross_periods= 24
        self.price_range_periods= 24
        self.cross_count=3



