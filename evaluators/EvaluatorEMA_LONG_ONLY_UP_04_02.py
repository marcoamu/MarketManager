from evaluators.CierreBase import CierreBase
from evaluators.EvaluatorBase import EvaluatorBase
from evaluators.AperturaBase import AperturaBase
from service.Constants import Constants


class EvaluatorEMA_LONG_ONLY_UP_04_02(EvaluatorBase, AperturaBase, CierreBase):
    """
    EvaluatorEMA_LONG_ONLY_UP_04_02 — ULTRA-AGRESIVO ETH/USD ONLY BUY
    =================================================================

    Versión ultra-agresiva para maximizar rendimiento en Ethereum.
    Basado en EvaluatorEMA_LONG_ONLY_UP_04_01 adaptado para ETH.

    Indicadores clave (confluencia multi-señal):
    1.  EMA           → dirección principal
    2.  Bollinger     → posicionamiento en canal (umbral ETH 8%)
    3.  RSI           → momentum (<38 entrada, >72 cierre agresivo)
    4.  Order Flow    → presión compradora real (score >= 40)
    5.  MACD          → confirmación momentum
    6.  ANGLE_IMA1    → aceleración tendencia
    7.  WEEK_FLOW     → bias semanal alcista
    8.  MEDSTD        → volatilidad activa
    9.  IMA5MA20      → cruce rápido medias

    Reglas apertura BUY:
    A. EMA BUY + Week rising + angle rising → entrada principal
    B. RSI < 38 + BLG lower cerca + Order Flow BUY
    C. MACD bullish + Week UP + MEDSTD activo
    D. Confluencia triple: angle UP + BLG bajo + Order Flow BUY
    E. IMA5MA20 BUY + FLUJO SUBE + angle rising

    Reglas cierre (multi-criterio agresivo):
    1. RSI > 72 → salida inmediata con ganancia
    2. Order Flow invierte → cierre defensivo rápido
    3. Bollinger upper cerca + ganancia → recoger beneficios
    4. MACD bajista → salida cautelar
    5. Angle IMA1 baja fuerte (contador >= 2)
    6. Stop-loss dinámico por volatilidad ETH
    7. Cierre estándar EMA + WEEK FLOW

    Versión: 04_02 — ultra-agresivo ETH
    """

    def __init__(self):
        self.name = "EvaluatorEMA_LONG_ONLY_UP_04_02"

    def evaluate(self, results, activeParam):
        results[Constants.EVAl_NAME] = self.name

        self.updateTimeZoneValues(results)

        # MULTIPLICADORES ULTRA-AGRESIVOS ETH
        # Mayor volatilidad ETH → multiplicadores más altos para cerrar antes
        self.multiplicatorClose = activeParam.difference * 1.5
        self.multiplicatorPREVIUS = activeParam.difference * 1.5

        # Control apertura desactivado → máxima agresividad
        self.enableControlOpen = False
        self.multiplicadorOpen = 1
        self.multiplicadorUP = 1

        # Week flow mínimo
        self.WEEK_FLOW_MINVAL = activeParam.weekDistanceSTDDistance

        self.medstdminDiff = activeParam.medstdminDiff
        self.medstdmaxDiff = activeParam.medstdmaxDiff

        # Evaluación cambio por tendencia mercado
        self.evaluateChangeMarketTendence = True

        # PARÁMETROS BOLLINGER (ETH más amplio)
        self.BLGDist = activeParam.bollingerDst
        self.blgLowerDist = 0.9  # ETH: más próximo al inferior
        self.blgLowerDistPercemt = 8  # ETH: umbral 8% (más amplio que BTC)
        self.bollingerClose = activeParam.bollingerClose

        # PARÁMETROS CIERRE
        self.closeAcumValue = activeParam.closeProfit
        # ETH: 5% extra sobre difference para cierre rápido
        self.closeDifference = activeParam.difference + (activeParam.difference * 0.05)
        self.accumulate = activeParam.accumulate

        self.angleUP = activeParam.angleUp
        self.angleDOWN = activeParam.angleDown

        results[Constants.EVAl_CLOSE_ACUM] = self.closeAcumValue
        results[Constants.EVAl_CLOSE_DIFF] = self.closeDifference
        results[Constants.EVAl_ACUM] = self.accumulate

        # ETH: cierra desde tick 1 (máxima agilidad)
        self.flujo_Count = 1

        # CONTROL HORARIO
        currentTime = self.gettime(results)
        intime = False
        print(f'[EMA_LONG_04_02] EVALUATOR {self.name}  PARAM: {activeParam.name}')

        if currentTime >= int(self.iniStart) and currentTime < int(self.iniEnd):
            intime = True
        if currentTime >= int(self.closeStart) and currentTime < int(self.closeEnd):
            intime = True

        if Constants.ONLY_START_END in results:
            if results[Constants.ONLY_START_END] == False:
                intime = True

        # DISPATCH PRINCIPAL
        current = results[Constants.CURRENT_ACTION]
        if current == Constants.ACTION_WAIT or current == Constants.ACTION_CLOSE:
            if intime:
                self.evaluarAperturaEMA(results, activeParam)
            else:
                print(f"[EMA_LONG_04_02] FUERA DE HORARIO")
        elif current == Constants.ACTION_BUY:
            self.evaluarFlujoBUY(results, activeParam)
        elif current == Constants.ACTION_SELL:
            # SELL ignorado — solo operamos BUY
            self._cerrar_sell_inmediato(results, activeParam)

    # =========================================================================
    # APERTURA
    # =========================================================================
    def evaluarAperturaEMA(self, results, activeParam):
        flujo_count = results[Constants.FLUJO_COUNT]

        ema = results[Constants.INDICATOR_EMA]
        if ema == Constants.INDICATOR_EMA_BUY:
            self.evaluarAperturaUP(results, activeParam, flujo_count)
        elif ema == Constants.INDICATOR_EMA_SELL:
            # En tendencia bajista solo buscamos rebotes alcistas fuertes
            self.evaluarAperturaDOWN(results, activeParam, flujo_count)
        elif ema == Constants.INDICATOR_EMA_WAIT:
            # En WAIT también evaluamos señales fuertes
            self.evaluarAperturaWAIT(results, activeParam, flujo_count)
        else:
            print(f"[EMA_LONG_04_02] EMA sin definir — esperando señal")

    # =========================================================================
    # APERTURA EN TENDENCIA ALCISTA (EMA BUY)
    # =========================================================================
    def evaluarAperturaUP(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference

        self.printDifference(
            "evaluarAperturaUP", difference_optimized,
            self.closeAcumValue, self.closeDifference
        )

        # Limpiar señales NXT contradictorias
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
                    results[Constants.CLOSE_NXT_UP] = 0
            results[Constants.CLOSE_NXT_UP] = 0

        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0

        # ---- REGLA A: EMA + WEEK FLOW principal (heredada) ----
        res, action, num = self.evaluateUpOpen_EMA_OUP_03(results, activeParam)
        if res:
            if "BUY" in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                self.printInicioLog(f"UP_BUY_{num}", results, activeParam)
                return

        # ---- REGLA B: EMA BUY + Week rising + Angle UP ----
        if self._ema_buy_week_rising(results, activeParam):
            isRising, angleDiff = self.isRisingAngleIma1(results)
            if isRising:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized * 0.85:
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                    self.printInicioLog("UP_EMA_WEEK_ANGLE_BUY", results, activeParam)
                    return

        # ---- REGLA C: RSI < 38 + Bollinger inferior cerca + Order Flow BUY ----
        # Threshold ETH: 38 (más bajo = más selectivo)
        if self._rsi_oversold_eth(results, threshold=38.0):
            if self._blg_near_lower_eth(results, activeParam, max_percent=10.0):
                if self._order_flow_strong_buy(results):
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized * 0.75:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        self.printInicioLog("UP_RSI_BLG_OF_BUY", results, activeParam)
                        return

        # ---- REGLA D: MACD bullish + Week UP + MEDSTD activo ----
        if self._macd_bullish(results):
            if results.get(Constants.WEEK_FLOW) == Constants.WEEK_FLOW_UP:
                if abs(results[Constants.MEDSTDDIFF]) > self.medstdminDiff:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized * 0.80:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        self.printInicioLog("UP_MACD_WEEK_BUY", results, activeParam)
                        return

        # ---- REGLA E: IMA5MA20 BUY + FLUJO SUBE + Angle rising ----
        if results[Constants.IMA5MA20] == Constants.INDICATOR_EMA_BUY:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.WEEK_DIR_BOT_DST] < 80:
                    if abs(results[Constants.MEDSTDDIFF]) > self.medstdminDiff:
                        isRising, angleDiff = self.isRisingAngleIma1(results)
                        if isRising:
                            if results[Constants.ACUMULADO_ABS] >= difference_optimized * 0.90:
                                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                self.printInicioLog("UP_IMA5MA20_ANGLE_BUY", results, activeParam)
                                return

        # ---- REGLA F: Order Flow BUY extremo + RSI < 42 + Week UP ----
        if self._order_flow_strong_buy(results):
            if self._rsi_oversold_eth(results, threshold=42.0):
                if results.get(Constants.WEEK_FLOW) == Constants.WEEK_FLOW_UP:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized * 0.70:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        self.printInicioLog("UP_OF_RSI_WEEK_BUY", results, activeParam)
                        return

        # ---- REGLA G: Confluencia triple (angle UP + BLG bajo + Week UP) ----
        if self._confluence_triple_buy(results, activeParam):
            if results[Constants.ACUMULADO_ABS] >= difference_optimized * 0.90:
                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                self.printInicioLog("UP_CONFLUENCE_BUY", results, activeParam)
                return

    # =========================================================================
    # APERTURA EN TENDENCIA BAJISTA (EMA SELL) — SOLO REBOTES BUY
    # =========================================================================
    def evaluarAperturaDOWN(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference

        self.printDifference(
            "evaluarAperturaDOWN", difference_optimized,
            self.closeAcumValue, self.closeDifference
        )

        # Limpiar señales NXT
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0

        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
                    if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
                        if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= activeParam.blgDistPercent:
                            results[Constants.CLOSE_NXT_UP] = 0

        # ---- REGLA 1: Señal heredada DOWN con WEEK rising ----
        res, action, num = self.evaluateDownOpen_EMA_WEEK_NEW_FLOW_01(results, activeParam)
        if res:
            if "BUY" in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                self.printInicioLog(f"DOWN_REBOUND_BUY_{num}", results, activeParam)
                return

        # ---- REGLA 2: RSI extremo < 28 + BLG lower + Order Flow BUY ----
        if self._rsi_extreme_oversold(results, threshold=28.0):
            if self._blg_near_lower_eth(results, activeParam, max_percent=12.0):
                if self._order_flow_strong_buy(results):
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized * 0.85:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        self.printInicioLog("DOWN_RSI_EXT_BLG_OF_BUY", results, activeParam)
                        return

        # ---- REGLA 3: Order Flow BUY muy fuerte + MED girando ----
        if self._order_flow_strong_buy(results):
            if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_UP:
                if results[Constants.IMA5MA20] == Constants.INDICATOR_EMA_BUY:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized * 0.80:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        self.printInicioLog("DOWN_OF_REBOUND_BUY", results, activeParam)
                        return

        # ---- REGLA 4: BLG lower perforado + flujo sube (V-shape ETH) ----
        if results[Constants.IND_BLG_LOWER_DST_PERCENT] < 0:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if self._rsi_oversold_eth(results, threshold=35.0):
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized * 0.85:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        self.printInicioLog("DOWN_BLG_VSHAPE_BUY", results, activeParam)
                        return

        # ---- REGLA 5: MACD bullish + RSI < 30 + Week no DOWN ----
        if self._macd_bullish(results):
            if self._rsi_oversold_eth(results, threshold=30.0):
                if results.get(Constants.WEEK_FLOW) != Constants.WEEK_FLOW_DOWN:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized * 0.90:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        self.printInicioLog("DOWN_MACD_RSI_BUY", results, activeParam)
                        return

    # =========================================================================
    # APERTURA EN MODO WAIT — señales muy fuertes
    # =========================================================================
    def evaluarAperturaWAIT(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference

        # Order Flow BUY extremo + RSI < 38 + Week UP
        if self._order_flow_strong_buy(results):
            if self._rsi_oversold_eth(results, threshold=38.0):
                if results.get(Constants.WEEK_FLOW) == Constants.WEEK_FLOW_UP:
                    if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                        if results[Constants.ACUMULADO_ABS] >= difference_optimized * 0.90:
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            self.printInicioLog("WAIT_OF_RSI_BUY", results, activeParam)
                            return

        # Confluencia triple + MACD bullish
        if self._confluence_triple_buy(results, activeParam):
            if self._macd_bullish(results):
                if results[Constants.ACUMULADO_ABS] >= difference_optimized * 0.80:
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                    self.printInicioLog("WAIT_CONFLUENCE_MACD_BUY", results, activeParam)
                    return

        # RSI extremo + Order Flow positivo en WAIT
        if self._rsi_extreme_oversold(results, threshold=25.0):
            if self._order_flow_strong_buy(results):
                if results[Constants.ACUMULADO_ABS] >= difference_optimized * 0.85:
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                    self.printInicioLog("WAIT_RSI_EXT_OF_BUY", results, activeParam)
                    return

    # =========================================================================
    # GESTIÓN POSICIÓN BUY — cierre ultra-agresivo multi-criterio
    # =========================================================================
    def evaluarFlujoBUY(self, results, activeParam):
        difference_optimized = activeParam.difference
        flujo_count = results[Constants.FLUJO_COUNT]

        self.printDifference(
            "evaluarFlujoBUY", difference_optimized,
            self.closeAcumValue, self.closeDifference,
            self.accumulate
        )

        # ---- CIERRE 1: RSI sobrecompra > 72 + ganancia → salida inmediata ----
        if self._rsi_overbought_eth(results):
            if results[Constants.ACUMULADO] < 0:  # BUY: acum < 0 = ganancia
                if results[Constants.ACTION_COUNT] >= self.flujo_Count:
                    self.printFinLog("CLOSE_RSI_OVERB", "evaluarFlujoBUY", results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

        # ---- CIERRE 2: Order Flow invierte a SELL fuerte → reversión rápida ----
        if self._order_flow_strong_sell(results):
            if results[Constants.ACTION_COUNT] >= 2:
                if results[Constants.ACUMULADO] < 0:  # en ganancia
                    self.printFinLog("CLOSE_OF_INVERT", "evaluarFlujoBUY", results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

        # ---- CIERRE 3: Bollinger upper cerca + ganancia → recoger beneficios ----
        if results[Constants.IND_BLG_UPPER_DST_PERCENT] <= self.blgLowerDistPercemt:
            if results[Constants.ACUMULADO] < 0:
                if results[Constants.ACTION_COUNT] >= self.flujo_Count:
                    self.printFinLog("CLOSE_BLG_UPPER", "evaluarFlujoBUY", results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

        # ---- CIERRE 4: MACD cruza bajista → salida cautelosa ----
        if self._macd_bearish(results):
            if results[Constants.ACTION_COUNT] >= 3:
                if results[Constants.ACUMULADO] < 0:
                    self.printFinLog("CLOSE_MACD_BEAR", "evaluarFlujoBUY", results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

        # ---- CIERRE 5: Angle IMA1 bajista con contador >= 2 ----
        if self._angle_ima1_strong_down(results, activeParam):
            if results[Constants.ACTION_COUNT] >= 2:
                if results[Constants.ACUMULADO] < 0:
                    self.printFinLog("CLOSE_ANGLE_DOWN", "evaluarFlujoBUY", results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

        # ---- CIERRE 6: Stop-loss dinámico por volatilidad ETH ----
        if results[Constants.ACTION_ACUM] <= 0:
            if results[Constants.ACTION_COUNT] >= 2:
                if abs(results[Constants.ACTION_ACUM]) >= self.closeDifference:
                    self.printFinLog("CLOSE_STOPLOSS", "evaluarFlujoBUY", results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

        # ---- CIERRE 7: EMA invierte a SELL + flujo baja + count >= 3 ----
        if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if results[Constants.ACTION_COUNT] >= 3:
                    if results[Constants.ACUMULADO] < 0:
                        self.printFinLog("CLOSE_EMA_INVERT", "evaluarFlujoBUY", results, activeParam)
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return

        # ---- CIERRE 8: Week angle deja de subir + count >= 2 ----
        isRising, angleDiff = self.isRisingFromWEEKNEW(results)
        if not isRising:
            if abs(angleDiff) >= activeParam.closeWeekDiffNew:
                if results[Constants.ACTION_COUNT] >= 2:
                    if results[Constants.ACUMULADO] < 0:
                        self.printFinLog("CLOSE_WEEK_ANGLE_DROP", "evaluarFlujoBUY", results, activeParam)
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return

        # ---- CIERRE ESTÁNDAR heredado ----
        self.control_BUY_EMA_OUP_03(results, activeParam, self.closeAcumValue, self.closeDifference)

    # =========================================================================
    # PROTECCIÓN: cierre inmediato de cualquier posición SELL no deseada
    # =========================================================================
    def _cerrar_sell_inmediato(self, results, activeParam):
        print(f"[EMA_LONG_04_02] SELL detected — closing immediately")
        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE

    # =========================================================================
    # HELPERS PRIVADOS
    # =========================================================================

    def _rsi_overbought_eth(self, results, threshold=72.0):
        """RSI en zona de sobrecompra ETH (>72, más alto que BTC por mayor volatilidad)."""
        try:
            rsi = float(results.get(Constants.RSI, 50))
            return rsi > threshold
        except Exception:
            return False

    def _rsi_oversold_eth(self, results, threshold=38.0):
        """RSI en zona de sobreventa ETH (<threshold)."""
        try:
            rsi = float(results.get(Constants.RSI, 50))
            return rsi < threshold
        except Exception:
            return False

    def _rsi_extreme_oversold(self, results, threshold=26.0):
        """RSI en sobreventa extrema ETH."""
        try:
            rsi = float(results.get(Constants.RSI, 50))
            return rsi < threshold
        except Exception:
            return False

    def _order_flow_strong_buy(self, results):
        """Presión compradora fuerte (score >= 40)."""
        try:
            of_score = int(results.get(Constants.ORDER_FLOW_SCORE, 0))
            of_signal = results.get(Constants.ORDER_FLOW_SIGNAL, "NEUTRAL")
            return of_score >= 40 or of_signal in ("STRONG_BUY_PRESSURE", "BUY_PRESSURE")
        except Exception:
            return False

    def _order_flow_strong_sell(self, results):
        """Presión vendedora fuerte (score <= -40)."""
        try:
            of_score = int(results.get(Constants.ORDER_FLOW_SCORE, 0))
            of_signal = results.get(Constants.ORDER_FLOW_SIGNAL, "NEUTRAL")
            return of_score <= -40 or of_signal in ("STRONG_SELL_PRESSURE", "SELL_PRESSURE")
        except Exception:
            return False

    def _blg_near_lower_eth(self, results, activeParam, max_percent=10.0):
        """Precio cerca del Bollinger Inferior ETH (distancia % < max_percent)."""
        try:
            lower_pct = float(results[Constants.IND_BLG_LOWER_DST_PERCENT])
            return 0 <= lower_pct <= max_percent
        except Exception:
            return False

    def _macd_bullish(self, results):
        """MACD por encima de su señal → momentum alcista."""
        try:
            macd = float(results.get(Constants.MACD, 0))
            macd_signal = float(results.get(Constants.MACD_SIGNAL, 0))
            return macd > macd_signal
        except Exception:
            return False

    def _macd_bearish(self, results):
        """MACD por debajo de su señal → momentum bajista."""
        try:
            macd = float(results.get(Constants.MACD, 0))
            macd_signal = float(results.get(Constants.MACD_SIGNAL, 0))
            return macd < macd_signal
        except Exception:
            return False

    def _ema_buy_week_rising(self, results, activeParam):
        """EMA BUY + Week rising (angleDiff > 0)."""
        try:
            if results[Constants.INDICATOR_EMA] != Constants.INDICATOR_EMA_BUY:
                return False
            isRising, angleDiff = self.isRisingFromWEEKNEW(results)
            return isRising and angleDiff > 0
        except Exception:
            return False

    def _angle_ima1_strong_down(self, results, activeParam):
        """Angle IMA1 fuertemente bajista (contador >= 2)."""
        try:
            angle_ima1 = float(results[Constants.ANGLE_IMA1])
            angle_ima1_counter = float(results[Constants.ANGLE_IMA1_COUNTER])
            if angle_ima1 < 0 and abs(angle_ima1) > activeParam.angleDown:
                if angle_ima1_counter >= 2:
                    return True
            return False
        except Exception:
            return False

    def _confluence_triple_buy(self, results, activeParam):
        """
        Confluencia triple para compra:
        1. ANGLE_FLOW UP (aceleración positiva)
        2. WEEK_FLOW UP (bias semanal)
        3. BLG posición baja (% > 35)
        4. FLUJO SUBE
        """
        try:
            angle_flow_up = "UP" in str(results.get(Constants.ANGLE_FLOW, ""))
            week_flow = results.get(Constants.WEEK_FLOW, Constants.WEEK_FLOW_UNDEF)
            week_up = "UP" in str(week_flow)
            blg_lower_pct = float(results[Constants.IND_BLG_LOWER_DST_PERCENT])
            blg_position_low = blg_lower_pct > 35
            flujo_sube = results[Constants.FLUJO] == Constants.FLUJO_SUBE
            return angle_flow_up and week_up and blg_position_low and flujo_sube
        except Exception:
            return False
