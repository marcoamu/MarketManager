from evaluators.CierreBase import CierreBase
from evaluators.EvaluatorBase import EvaluatorBase
from evaluators.AperturaBase import AperturaBase
from service.Constants import Constants

class EvaluatorSUPERBOT_ALPHA_01(EvaluatorBase, AperturaBase, CierreBase):
    """
    EvaluatorSUPERBOT_ALPHA_01 - Super Bot de Alto Riesgo / Alta Ganancia

    Estrategia multi-indicador agresiva que combina:
    - EMA (señal principal de dirección)
    - Bollinger Bands (posicionamiento y distancia)
    - RSI (momentum y sobrecompra/venta)
    - Order Flow / Footprint (presión compradora/vendedora)
    - ANGLE / ANGLE_IMA1 (fuerza de tendencia)
    - WEEK_FLOW (flujo semanal)
    - MEDSTD (desviación estándar de media)
    - IMA5MA20 (cruce de medias rápidas)

    Reglas de apertura agresivas:
    - Abre rápido cuando hay confluencia de 3+ indicadores
    - Tolera más riesgo en la posición: multiplicadores altos
    - Cierra rápido con beneficio (RSI extremo + Bollinger)
    - Stop loss agresivo cuando orden de flujo se invierte

    Versión: ALPHA_01
    """

    def __init__(self):
        self.name = 'EvaluatorSUPERBOT_ALPHA_01'

    def evaluate(self, results, activeParam):
        results[Constants.EVAl_NAME] = self.name
        self.updateTimeZoneValues(results)
        self.multiplicatorClose = activeParam.difference * 1.5
        self.multiplicatorPREVIUS = activeParam.difference * 1.5
        self.enableControlOpen = False
        self.multiplicadorOpen = 1
        self.multiplicadorUP = 1
        self.WEEK_FLOW_MINVAL = activeParam.weekDistanceSTDDistance
        self.medstdminDiff = activeParam.medstdminDiff
        self.medstdmaxDiff = activeParam.medstdmaxDiff
        self.evaluateChangeMarketTendence = True
        self.BLGDist = activeParam.bollingerDst
        self.blgLowerDist = 1.0
        self.blgLowerDistPercemt = 8
        self.bollingerClose = activeParam.bollingerClose
        self.closeAcumValue = activeParam.closeProfit
        self.closeDifference = activeParam.difference + activeParam.difference * 0.05
        self.accumulate = activeParam.accumulate
        self.angleUP = activeParam.angleUp
        self.angleDOWN = activeParam.angleDown
        results[Constants.EVAl_CLOSE_ACUM] = self.closeAcumValue
        results[Constants.EVAl_CLOSE_DIFF] = self.closeDifference
        results[Constants.EVAl_ACUM] = self.accumulate
        self.flujo_Count = 1
        currentTime = self.gettime(results)
        intime = False
        if currentTime >= int(self.iniStart) and currentTime < int(self.iniEnd):
            intime = True
        if currentTime >= int(self.closeStart) and currentTime < int(self.closeEnd):
            intime = True
        if Constants.ONLY_START_END in results:
            if results[Constants.ONLY_START_END] == False:
                intime = True
        if results[Constants.CURRENT_ACTION] == Constants.ACTION_WAIT or results[Constants.CURRENT_ACTION] == Constants.ACTION_CLOSE:
            if intime:
                self.evaluarAperturaEMA_SUPER(results, activeParam)
            else:
                pass
        elif results[Constants.CURRENT_ACTION] == Constants.ACTION_BUY:
            self.evaluarFlujoBUY_SUPER(results, activeParam)
        elif results[Constants.CURRENT_ACTION] == Constants.ACTION_SELL:
            self.evaluarFlujoSELL_SUPER(results, activeParam)

    def evaluarAperturaEMA_SUPER(self, results, activeParam):
        flujo_count = results[Constants.FLUJO_COUNT]
        if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_BUY:
            self.evaluarAperturaUP_SUPER(results, activeParam, flujo_count)
        elif results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
            self.evaluarAperturaDOWN_SUPER(results, activeParam, flujo_count)
        elif results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_WAIT:
            self.evaluarAperturaWAIT_SUPER(results, activeParam, flujo_count)
        else:
            pass

    def evaluarAperturaDOWN_SUPER(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        self.printDifference('evaluarAperturaDOWN_SUPER', difference_optimized, self.closeAcumValue, self.closeDifference)
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
                    if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
                        if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= activeParam.blgDistPercent:
                            results[Constants.CLOSE_NXT_UP] = 0
        res, action, num = self.evaluateDownOpen_EMA_WEEK_NEW_FLOW_01(results, activeParam)
        if res:
            if 'BUY' in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                self.printInicioLog(f'SUPERBOT_DOWN_BUY_{num}', results, activeParam)
                return
            elif 'SELL' in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                self.printInicioLog(f'SUPERBOT_DOWN_SELL_{num}', results, activeParam)
                return
        if self._rsi_overbought(results) and self._blg_near_upper(results, activeParam):
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
                    results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                    self.printInicioLog('SUPERBOT_DOWN_RSI_OB_BLG_SELL', results, activeParam)
                    return
        if self._order_flow_strong_sell(results):
            if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
                if results[Constants.IMA5MA20] == Constants.INDICATOR_EMA_SELL:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized * 0.8:
                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                        self.printInicioLog('SUPERBOT_DOWN_OF_SELL', results, activeParam)
                        return
        if self._strong_angle_down(results, activeParam):
            if abs(results[Constants.MEDSTDDIFF]) > self.medstdminDiff:
                if results[Constants.IND_BLG_LOWER_DST_PERCENT] > -5:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized:
                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                        self.printInicioLog('SUPERBOT_DOWN_ANGLE_SELL', results, activeParam)
                        return

    def evaluarAperturaUP_SUPER(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        self.printDifference('evaluarAperturaUP_SUPER', difference_optimized, self.closeAcumValue, self.closeDifference)
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
                    results[Constants.CLOSE_NXT_UP] = 0
                elif results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_UP:
                    if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
                        pass
            results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0
        res, action, num = self.evaluateUpOpen_EMA_WEEK_NEW_FLOW_01(results, activeParam)
        if res:
            if 'BUY' in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                self.printInicioLog(f'SUPERBOT_UP_BUY_{num}', results, activeParam)
                return
            elif 'SELL' in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                self.printInicioLog(f'SUPERBOT_UP_SELL_{num}', results, activeParam)
                return
        if self._rsi_oversold(results) and self._blg_near_lower(results, activeParam):
            if results[Constants.ACUMULADO_ABS] >= difference_optimized * 0.8 or results[Constants.ACTION_MIN_DIST] >= difference_optimized * 0.8:
                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                self.printInicioLog('SUPERBOT_UP_RSI_OS_BLG_BUY', results, activeParam)
                return
        if self._order_flow_strong_buy(results):
            if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_UP:
                if results[Constants.IMA5MA20] == Constants.INDICATOR_EMA_BUY:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized * 0.8:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        self.printInicioLog('SUPERBOT_UP_OF_BUY', results, activeParam)
                        return
        if self._strong_confluence_buy(results, activeParam):
            if results[Constants.ACUMULADO_ABS] >= difference_optimized:
                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                self.printInicioLog('SUPERBOT_UP_TRIPLE_BUY', results, activeParam)
                return
        if results[Constants.IMA5MA20] == Constants.INDICATOR_EMA_BUY:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.WEEK_DIR_BOT_DST] < 70:
                    if abs(results[Constants.MEDSTDDIFF]) > self.medstdminDiff:
                        isRising, angleDiff = self.isRisingAngleIma1(results)
                        if isRising:
                            if results[Constants.ACUMULADO_ABS] >= difference_optimized:
                                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                self.printInicioLog('SUPERBOT_UP_IMA5_BUY', results, activeParam)
                                return

    def evaluarAperturaWAIT_SUPER(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference
        if self._order_flow_strong_buy(results) and self._rsi_oversold(results):
            if results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_UP:
                if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        self.printInicioLog('SUPERBOT_WAIT_OF_RSI_BUY', results, activeParam)
                        return
        if self._order_flow_strong_sell(results) and self._rsi_overbought(results):
            if results[Constants.WEEK_FLOW] == Constants.WEEK_FLOW_DOWN:
                if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized:
                        results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                        self.printInicioLog('SUPERBOT_WAIT_OF_RSI_SELL', results, activeParam)
                        return

    def evaluarFlujoBUY_SUPER(self, results, activeParam):
        difference_optimized = activeParam.difference
        flujo_count = results[Constants.FLUJO_COUNT]
        self.printDifference('evaluarFlujoBUY_SUPER', difference_optimized, self.closeAcumValue, self.closeDifference, self.accumulate)
        if self._rsi_overbought(results):
            if results[Constants.ACUMULADO] < 0:
                if results[Constants.ACTION_COUNT] >= self.flujo_Count:
                    self.printFinLog('CLOSE_BUY_RSI_OB', 'evaluarFlujoBUY_SUPER', results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if self._order_flow_strong_sell(results):
            if results[Constants.ACTION_COUNT] >= 2:
                if results[Constants.ACUMULADO] < 0:
                    self.printFinLog('CLOSE_BUY_OF_INVERT', 'evaluarFlujoBUY_SUPER', results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if results[Constants.IND_BLG_UPPER_DST_PERCENT] <= self.blgLowerDistPercemt:
            if results[Constants.ACUMULADO] < 0:
                if results[Constants.ACTION_COUNT] >= self.flujo_Count:
                    self.printFinLog('CLOSE_BUY_BLG_UPPER', 'evaluarFlujoBUY_SUPER', results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        self.control_BUY_WEEK_NEW_DIFF_03(results, activeParam, self.closeAcumValue, self.closeDifference)

    def evaluarFlujoSELL_SUPER(self, results, activeParam):
        difference_optimized = activeParam.difference
        flujo_count = results[Constants.FLUJO_COUNT]
        self.printDifference('evaluarFlujoSELL_SUPER', difference_optimized, self.closeAcumValue, self.closeDifference, self.accumulate)
        if self._rsi_oversold(results):
            if results[Constants.ACUMULADO] > 0:
                if results[Constants.ACTION_COUNT] >= self.flujo_Count:
                    self.printFinLog('CLOSE_SELL_RSI_OS', 'evaluarFlujoSELL_SUPER', results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if self._order_flow_strong_buy(results):
            if results[Constants.ACTION_COUNT] >= 2:
                if results[Constants.ACUMULADO] > 0:
                    self.printFinLog('CLOSE_SELL_OF_INVERT', 'evaluarFlujoSELL_SUPER', results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        if results[Constants.IND_BLG_LOWER_DST_PERCENT] <= self.blgLowerDistPercemt:
            if results[Constants.ACUMULADO] > 0:
                if results[Constants.ACTION_COUNT] >= self.flujo_Count:
                    self.printFinLog('CLOSE_SELL_BLG_LOWER', 'evaluarFlujoSELL_SUPER', results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return
        self.control_SELL_EMA_WEEK_NEW_FLOW_03(results, activeParam, self.closeAcumValue, self.closeDifference)

    def _rsi_overbought(self, results, threshold=72.0):
        """RSI en zona de sobrecompra (> threshold). Señal de reversión bajista."""
        try:
            rsi = float(results.get(Constants.RSI, 50))
            rsi_slope = float(results.get(Constants.RSI_SLOPE, 0))
            return rsi > threshold
        except Exception:
            return False

    def _rsi_oversold(self, results, threshold=28.0):
        """RSI en zona de sobreventa (< threshold). Señal de reversión alcista."""
        try:
            rsi = float(results.get(Constants.RSI, 50))
            return rsi < threshold
        except Exception:
            return False

    def _order_flow_strong_buy(self, results):
        """Presión compradora fuerte en Order Flow (score >= 40)."""
        try:
            of_score = int(results.get(Constants.ORDER_FLOW_SCORE, 0))
            of_signal = results.get(Constants.ORDER_FLOW_SIGNAL, 'NEUTRAL')
            return of_score >= 40 or of_signal in ('STRONG_BUY_PRESSURE', 'BUY_PRESSURE')
        except Exception:
            return False

    def _order_flow_strong_sell(self, results):
        """Presión vendedora fuerte en Order Flow (score <= -40)."""
        try:
            of_score = int(results.get(Constants.ORDER_FLOW_SCORE, 0))
            of_signal = results.get(Constants.ORDER_FLOW_SIGNAL, 'NEUTRAL')
            return of_score <= -40 or of_signal in ('STRONG_SELL_PRESSURE', 'SELL_PRESSURE')
        except Exception:
            return False

    def _order_flow_imbalance(self, results):
        """Hay un desequilibrio de volumen notable en este tick."""
        try:
            return bool(results.get(Constants.ORDER_FLOW_IMBALANCE, False))
        except Exception:
            return False

    def _blg_near_upper(self, results, activeParam, max_percent=15.0):
        """Precio cerca del Bollinger Superior (distancia % < max_percent)."""
        try:
            upper_pct = float(results[Constants.IND_BLG_UPPER_DST_PERCENT])
            return 0 <= upper_pct <= max_percent
        except Exception:
            return False

    def _blg_near_lower(self, results, activeParam, max_percent=15.0):
        """Precio cerca del Bollinger Inferior (distancia % < max_percent)."""
        try:
            lower_pct = float(results[Constants.IND_BLG_LOWER_DST_PERCENT])
            return 0 <= lower_pct <= max_percent
        except Exception:
            return False

    def _strong_angle_down(self, results, activeParam):
        """Ángulo fuertemente bajista en EMA20 o IMA1."""
        try:
            angle_ema20 = float(results[Constants.ANGLE_EMA20])
            angle_ima1 = float(results[Constants.ANGLE_IMA1])
            angle_ima1_counter = float(results[Constants.ANGLE_IMA1_COUNTER])
            if angle_ema20 < 0 and abs(angle_ema20) > activeParam.angleDown:
                return True
            if angle_ima1 < 0 and angle_ima1_counter >= 2:
                return True
            return False
        except Exception:
            return False

    def _strong_confluence_buy(self, results, activeParam):
        """
        Confluencia triple para compra:
        1. ANGLE_FLOW en UP
        2. WEEK_FLOW en UP o alcista
        3. Bollinger posición baja (% > 50 desde la base)
        """
        try:
            angle_flow_up = 'UP' in str(results.get(Constants.ANGLE_FLOW, ''))
            week_flow = results.get(Constants.WEEK_FLOW, Constants.WEEK_FLOW_UNDEF)
            week_up = 'UP' in str(week_flow)
            blg_lower_pct = float(results[Constants.IND_BLG_LOWER_DST_PERCENT])
            blg_position_low = blg_lower_pct > 50
            flujo_sube = results[Constants.FLUJO] == Constants.FLUJO_SUBE
            return angle_flow_up and week_up and blg_position_low and flujo_sube
        except Exception:
            return False