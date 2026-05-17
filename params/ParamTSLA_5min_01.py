from service.Parameters import Parameters

#TSLA
class ParamTSLA_5min_01(Parameters):

    def __init__(self, isDBData):
        super().__init__()
        self.paramName = "ParamTSLA_5min_01"
        self.difference = 0.85
        self.accumulate = 1
        self.unit = 0.07
        self.draw = False
        self.round = 2
        self.tele_group = -915224083
        # self.tendence_measure =0.0001
        self.tendence_measure = 0.04
        self.tendence_distance = 3
        self.ima1 = 5
        self.ima2 = 15
        self.ima3 = 20
        self.ima4 = 30
        self.weekend = False
        self.operate = True
        self.reevaluateAction = False
        self.hourOffset = 0
        self.minimunCloseAmount = 5
        self.controlWin = True
        self.verifyMarketOpen = True
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
            self.rangehours = [22.5, 14.50]

        else:
            self.rangehours = [16, 9]
            # self.hourOffset = -4