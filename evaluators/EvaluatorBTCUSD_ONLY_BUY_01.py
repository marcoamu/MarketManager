from evaluators.CierreBase import CierreBase
from evaluators.EvaluatorBase import EvaluatorBase
from evaluators.AperturaBase import AperturaBase
from service.Constants import Constants


class EvaluatorBTCUSD_ONLY_BUY_01(EvaluatorBase, AperturaBase, CierreBase):
    """
    EvaluatorBTCUSD_ONLY_BUY_01 — Monitor BTC/USD solo COMPRA (LONG)
    ===================================================================

    Estrategia ULTRA-AGRESIVA de solo compra para BTC/USD.
    NO abre posiciones SELL en ningún caso.

    Indicadores utilizados (confluencia multi-señal):
    ─────────────────────────────────────────────────
    1.  EMA            → dirección principal de tendencia
    2.  Bollinger Bands → posicionamiento de precio en el canal
    3.  RSI            → momentum, sobreventa (<30) como entrada agresiva
    4.  Order Flow / Footprint (delta) → presión compradora real
    5.  ANGLE / ANGLE_IMA1 → fuerza y aceleración de la tendencia
    6.  WEEK_FLOW      → tendencia semanal (bias alcista global)
    7.  IMA5MA20       → cruce rápido de medias (momentum a corto plazo)
    8.  MEDSTD / MED   → desviación estándar de la media (volatilidad)
    9.  MACD           → confirmación de momentum
    10. MARKET_TENDENCE → tendencia macro confirmada

    Reglas de apertura (SOLO BUY):
    ─────────────────────────────────────────────────
    A. EMA BUY + Week UP + RSI < 40 + Order Flow BUY → entrada inmediata
    B. RSI sobreventa (<30) + Bollinger inferior cerca + Order Flow BUY
    C. Confluencia triple: ANGLE alcista + WEEK_UP + BLG posición baja
    D. IMA5MA20 BUY + FLUJO SUBE + MEDSTD activo + ángulo rising
    E. EMA SELL pero rebote: RSI<28 + BLG lower near + Order Flow BUY fuerte
       (contra-tendencia permitida en BTC por alta volatilidad)

    Reglas de cierre:
    ─────────────────────────────────────────────────
    1. RSI sobrecompra (>70) → salida agresiva con ganancia
    2. Order Flow invierte a SELL fuerte → salida defensiva rápida
    3. Bollinger upper alcanzado → salida en máximo técnico
    4. MACD cruza a bajista → salida cautelar
    5. Cierre estándar heredado (EMA + WEEK)

    Versión: BTCUSD_ONLY_BUY_01
    """

    def __init__(self):
        self.name = "EvaluatorBTCUSD_ONLY_BUY_01"

    # ══════════════════════════════════════════════════════════════════════════
    # MÉTODO PRINCIPAL
    # ══════════════════════════════════════════════════════════════════════════
    def evaluate(self, results, activeParam):
        results[Constants.EVAl_NAME] = self.name

        self.updateTimeZoneValues(results)

        # ─── MULTIPLICADORES AGRESIVOS ─────────────────────────────────────
        # Multiplicador de cierre: 1.3x — acepta más swing antes de cerrar
        self.multiplicatorClose = activeParam.difference * 1.3
        self.multiplicatorPREVIUS = activeParam.difference * 1.3

        # Control de apertura desactivado → máxima agresividad
        self.enableControlOpen = False
        self.multiplicadorOpen = 1
        self.multiplicadorUP = 1

        # Parámetros de semana y medstd
        self.WEEK_FLOW_MINVAL = activeParam.weekDistanceSTDDistance
        self.medstdminDiff = activeParam.medstdminDiff
        self.medstdmaxDiff = activeParam.medstdmaxDiff

        # Activar evaluación de cambio por tendencia de mercado
        self.evaluateChangeMarketTendence = True

        # ─── PARÁMETROS BOLLINGER ──────────────────────────────────────────
        self.BLGDist = activeParam.bollingerDst
        # Umbral de distancia al lower para considerar que estamos cerca (%)
        self.blgLowerDist = 0.8           # muy agresivo (normal 1.5)
        self.blgLowerDistPercemt = 6      # muy agresivo (normal 10)
        self.bollingerClose = activeParam.bollingerClose

        # ─── PARÁMETROS DE CIERRE ─────────────────────────────────────────
        self.closeAcumValue = activeParam.closeProfit
        # Diferencia mínima para abrir: 3% extra sobre activeParam
        self.closeDifference = activeParam.difference + (activeParam.difference * 0.03)
        self.accumulate = activeParam.accumulate

        # ─── PARÁMETROS DE ÁNGULO ─────────────────────────────────────────
        self.angleUP = activeParam.angleUp
        self.angleDOWN = activeParam.angleDown

        # Publicar valores en results
        results[Constants.EVAl_CLOSE_ACUM] = self.closeAcumValue
        results[Constants.EVAl_CLOSE_DIFF] = self.closeDifference
        results[Constants.EVAl_ACUM] = self.accumulate

        # Empieza a evaluar cierre desde el tick 1 (máxima agilidad)
        self.flujo_Count = 1

        # ─── CONTROL DE HORARIO ───────────────────────────────────────────
        currentTime = self.gettime(results)
        intime = False
        print(f'[BTCUSD_ONLY_BUY] EVALUATOR {self.name}  PARAM: {activeParam.name}')

        if currentTime >= int(self.iniStart) and currentTime < int(self.iniEnd):
            intime = True
        if currentTime >= int(self.closeStart) and currentTime < int(self.closeEnd):
            intime = True

        if Constants.ONLY_START_END in results:
            if results[Constants.ONLY_START_END] == False:
                intime = True

        # ─── DISPATCH PRINCIPAL ───────────────────────────────────────────
        current = results[Constants.CURRENT_ACTION]
        if current == Constants.ACTION_WAIT or current == Constants.ACTION_CLOSE:
            if intime:
                self.evaluarAperturaEMA_BTCUSD(results, activeParam)
            else:
                print(f"[BTCUSD_ONLY_BUY] FUERA DE HORARIO")
        elif current == Constants.ACTION_BUY:
            self.evaluarFlujoBUY_BTCUSD(results, activeParam)
        elif current == Constants.ACTION_SELL:
            # ── NUNCA OPERAMOS SELL: cerrar inmediatamente si por algún ──
            # ── motivo externo se abrió una posición corta              ──
            self._cerrar_sell_no_permitido(results, activeParam)

    # ══════════════════════════════════════════════════════════════════════════
    # APERTURA: despacha según EMA
    # ══════════════════════════════════════════════════════════════════════════
    def evaluarAperturaEMA_BTCUSD(self, results, activeParam):
        flujo_count = results[Constants.FLUJO_COUNT]

        ema = results[Constants.INDICATOR_EMA]
        if ema == Constants.INDICATOR_EMA_BUY:
            self.evaluarAperturaUP_BTCUSD(results, activeParam, flujo_count)
        elif ema == Constants.INDICATOR_EMA_SELL:
            # En tendencia bajista buscamos SOLO rebotes alcistas en BTC
            self.evaluarAperturaDOWN_BTCUSD(results, activeParam, flujo_count)
        elif ema == Constants.INDICATOR_EMA_WAIT:
            # En WAIT también evaluamos señales fuertes de compra
            self.evaluarAperturaWAIT_BTCUSD(results, activeParam, flujo_count)
        else:
            print(f"[BTCUSD_ONLY_BUY] EMA sin definir — esperando señal")

    # ══════════════════════════════════════════════════════════════════════════
    # APERTURA EN TENDENCIA ALCISTA (EMA BUY) — máxima prioridad de compra
    # ══════════════════════════════════════════════════════════════════════════
    def evaluarAperturaUP_BTCUSD(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference

        self.printDifference(
            "evaluarAperturaUP_BTCUSD", difference_optimized,
            self.closeAcumValue, self.closeDifference
        )

        # ── Limpiar señales NXT contradictorias ─────────────────────────
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
                    results[Constants.CLOSE_NXT_UP] = 0
            results[Constants.CLOSE_NXT_UP] = 0

        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0

        # ── REGLA A: Señal hereda EMA+WEEK FLOW (solo BUY) ─────────────
        res, action, num = self.evaluateUpOpen_EMA_WEEK_NEW_FLOW_01(results, activeParam)
        if res:
            if "BUY" in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                self.printInicioLog(f"BTCUSD_UP_EMA_BUY_{num}", results, activeParam)
                return
            # ← SELL ignorado: solo compramos

        # ── REGLA B: RSI sobreventa + Bollinger inferior ─────────────────
        if self._rsi_oversold(results) and self._blg_near_lower(results, activeParam):
            if (results[Constants.ACUMULADO_ABS] >= difference_optimized * 0.7 or
                    results[Constants.ACTION_MIN_DIST] >= difference_optimized * 0.7):
                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                self.printInicioLog("BTCUSD_UP_RSI_OS_BLG_BUY", results, activeParam)
                return

        # ── REGLA C: Order Flow comprador fuerte + Medios alcistas ───────
        if self._order_flow_strong_buy(results):
            if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_UP:
                if results[Constants.IMA5MA20] == Constants.INDICATOR_EMA_BUY:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized * 0.75:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        self.printInicioLog("BTCUSD_UP_OF_BUY", results, activeParam)
                        return

        # ── REGLA D: Confluencia triple alcista ──────────────────────────
        if self._strong_confluence_buy(results, activeParam):
            if results[Constants.ACUMULADO_ABS] >= difference_optimized:
                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                self.printInicioLog("BTCUSD_UP_TRIPLE_BUY", results, activeParam)
                return

        # ── REGLA E: IMA5MA20 alcista + FLUJO SUBE + MEDSTD activo ──────
        if results[Constants.IMA5MA20] == Constants.INDICATOR_EMA_BUY:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.WEEK_DIR_BOT_DST] < 75:
                    if abs(results[Constants.MEDSTDDIFF]) > self.medstdminDiff:
                        isRising, angleDiff = self.isRisingAngleIma1(results)
                        if isRising:
                            if results[Constants.ACUMULADO_ABS] >= difference_optimized:
                                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                self.printInicioLog("BTCUSD_UP_IMA5_BUY", results, activeParam)
                                return

        # ── REGLA F: MACD bullish crossover con WEEK alcista ─────────────
        if self._macd_bullish(results):
            if results.get(Constants.WEEK_FLOW) == Constants.WEEK_FLOW_UP:
                if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized * 0.8:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        self.printInicioLog("BTCUSD_UP_MACD_WEEK_BUY", results, activeParam)
                        return

    # ══════════════════════════════════════════════════════════════════════════
    # APERTURA EN TENDENCIA BAJISTA (EMA SELL) — solo rebotes BUY
    # En BTC el mercado puede rebotar violentamente incluso en tendencia bajista
    # ══════════════════════════════════════════════════════════════════════════
    def evaluarAperturaDOWN_BTCUSD(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference

        self.printDifference(
            "evaluarAperturaDOWN_BTCUSD", difference_optimized,
            self.closeAcumValue, self.closeDifference
        )

        # ── Limpiar señales NXT ──────────────────────────────────────────
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                results[Constants.CLOSE_NXT_DOWN] = 0

        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_DOWN:
                    if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
                        if results[Constants.IND_BLG_LOWER_DST_PERCENT] >= activeParam.blgDistPercent:
                            results[Constants.CLOSE_NXT_UP] = 0

        # ── REGLA 1: Rebote en EMA SELL con señal heredada BUY ───────────
        res, action, num = self.evaluateDownOpen_EMA_WEEK_NEW_FLOW_01(results, activeParam)
        if res:
            if "BUY" in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                self.printInicioLog(f"BTCUSD_DOWN_REBOUND_BUY_{num}", results, activeParam)
                return
            # SELL ignorado

        # ── REGLA 2: RSI extremo (<28) + BLG lower muy cerca (rebote fuerte)
        if self._rsi_extreme_oversold(results) and self._blg_near_lower(results, activeParam, max_percent=10.0):
            if self._order_flow_strong_buy(results):
                if results[Constants.WEEK_FLOW] != Constants.WEEK_FLOW_DOWN:
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                    self.printInicioLog("BTCUSD_DOWN_RSI_EXT_BLG_BUY", results, activeParam)
                    return

        # ── REGLA 3: Order Flow comprador muy fuerte + precio cerca del mín
        if self._order_flow_strong_buy(results):
            if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_UP:
                if results[Constants.IMA5MA20] == Constants.INDICATOR_EMA_BUY:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized * 0.9:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        self.printInicioLog("BTCUSD_DOWN_OF_REBOUND_BUY", results, activeParam)
                        return

        # ── REGLA 4: Bollinger inferior perforado + flujo sube (V-shape)
        if results[Constants.IND_BLG_LOWER_DST_PERCENT] < 0:
            # el precio está por debajo del lower band — posible bounce
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if self._rsi_oversold(results):
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        self.printInicioLog("BTCUSD_DOWN_BLG_BREAK_BOUNCE_BUY", results, activeParam)
                        return

    # ══════════════════════════════════════════════════════════════════════════
    # APERTURA EN MODO WAIT (EMA sin dirección) — señales muy fuertes de compra
    # ══════════════════════════════════════════════════════════════════════════
    def evaluarAperturaWAIT_BTCUSD(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference

        # ── Order Flow BUY extremo + RSI en sobreventa + WEEK UP ─────────
        if self._order_flow_strong_buy(results) and self._rsi_oversold(results):
            if results.get(Constants.WEEK_FLOW) == Constants.WEEK_FLOW_UP:
                if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        self.printInicioLog("BTCUSD_WAIT_OF_RSI_BUY", results, activeParam)
                        return

        # ── Confluencia triple en WAIT ────────────────────────────────────
        if self._strong_confluence_buy(results, activeParam):
            if self._macd_bullish(results):
                if results[Constants.ACUMULADO_ABS] >= difference_optimized * 0.9:
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                    self.printInicioLog("BTCUSD_WAIT_TRIPLE_MACD_BUY", results, activeParam)
                    return

    # ══════════════════════════════════════════════════════════════════════════
    # GESTIÓN DE POSICIÓN BUY: cierre agresivo multi-criterio
    # ══════════════════════════════════════════════════════════════════════════
    def evaluarFlujoBUY_BTCUSD(self, results, activeParam):
        difference_optimized = activeParam.difference
        flujo_count = results[Constants.FLUJO_COUNT]

        self.printDifference(
            "evaluarFlujoBUY_BTCUSD", difference_optimized,
            self.closeAcumValue, self.closeDifference,
            self.accumulate
        )

        # ── CIERRE 1: RSI en sobrecompra + ganancia → salida agresiva ────
        if self._rsi_overbought(results):
            if results[Constants.ACUMULADO] < 0:  # BUY: acum < 0 = ganancia
                if results[Constants.ACTION_COUNT] >= self.flujo_Count:
                    self.printFinLog("BTCUSD_CLOSE_BUY_RSI_OB", "evaluarFlujoBUY_BTCUSD", results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

        # ── CIERRE 2: Order Flow invierte a SELL fuerte → reversión ──────
        if self._order_flow_strong_sell(results):
            if results[Constants.ACTION_COUNT] >= 2:
                if results[Constants.ACUMULADO] < 0:  # en ganancia
                    self.printFinLog("BTCUSD_CLOSE_BUY_OF_INVERT", "evaluarFlujoBUY_BTCUSD", results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

        # ── CIERRE 3: Bollinger upper alcanzado con ganancia ──────────────
        if results[Constants.IND_BLG_UPPER_DST_PERCENT] <= self.blgLowerDistPercemt:
            if results[Constants.ACUMULADO] < 0:
                if results[Constants.ACTION_COUNT] >= self.flujo_Count:
                    self.printFinLog("BTCUSD_CLOSE_BUY_BLG_UPPER", "evaluarFlujoBUY_BTCUSD", results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

        # ── CIERRE 4: MACD cruza bajista → salida cautelar ───────────────
        if self._macd_bearish(results):
            if results[Constants.ACTION_COUNT] >= 3:
                if results[Constants.ACUMULADO] < 0:  # en ganancia
                    self.printFinLog("BTCUSD_CLOSE_BUY_MACD_BEAR", "evaluarFlujoBUY_BTCUSD", results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

        # ── CIERRE 5: Ángulo fuertemente bajista con contador alto ────────
        if self._strong_angle_down(results, activeParam):
            if results[Constants.ACTION_COUNT] >= 4:
                if results[Constants.ACUMULADO] < 0:
                    self.printFinLog("BTCUSD_CLOSE_BUY_ANGLE_DOWN", "evaluarFlujoBUY_BTCUSD", results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

        # ── CIERRE 6: Stop-loss agresivo — limitar pérdidas en BTC ────────
        if results[Constants.ACTION_ACUM] <= 0:
            # estamos en pérdida
            if results[Constants.ACTION_COUNT] >= 2:
                if abs(results[Constants.ACTION_ACUM]) >= self.closeDifference:
                    self.printFinLog("BTCUSD_CLOSE_BUY_STOPLOSS", "evaluarFlujoBUY_BTCUSD", results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

        # ── CIERRE ESTÁNDAR: método heredado EMA/WEEK FLOW ────────────────
        self.control_BUY_WEEK_NEW_DIFF_03(results, activeParam, self.closeAcumValue, self.closeDifference)

    # ══════════════════════════════════════════════════════════════════════════
    # PROTECCIÓN: cierre inmediato de cualquier posición SELL no deseada
    # ══════════════════════════════════════════════════════════════════════════
    def _cerrar_sell_no_permitido(self, results, activeParam):
        """
        Este evaluador es ONLY BUY.
        Si por algún motivo externo hay una posición SELL abierta,
        la cerramos en el siguiente tick sin importar el resultado.
        """
        print(f"[BTCUSD_ONLY_BUY] ⚠️  POSICIÓN SELL DETECTADA — cerrando inmediatamente")
        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE

    # ══════════════════════════════════════════════════════════════════════════
    # HELPERS PRIVADOS: evaluación de indicadores individuales
    # ══════════════════════════════════════════════════════════════════════════

    def _rsi_overbought(self, results, threshold=70.0):
        """RSI en zona de sobrecompra (> threshold). Señal de techo de mercado."""
        try:
            rsi = float(results.get(Constants.RSI, 50))
            return rsi > threshold
        except Exception:
            return False

    def _rsi_oversold(self, results, threshold=30.0):
        """RSI en zona de sobreventa (< threshold). Señal de suelo de mercado."""
        try:
            rsi = float(results.get(Constants.RSI, 50))
            return rsi < threshold
        except Exception:
            return False

    def _rsi_extreme_oversold(self, results, threshold=25.0):
        """RSI en zona de sobreventa extrema (< 25). Señal de pánico vendedor."""
        try:
            rsi = float(results.get(Constants.RSI, 50))
            return rsi < threshold
        except Exception:
            return False

    def _order_flow_strong_buy(self, results):
        """Presión compradora fuerte en Order Flow (score >= 40)."""
        try:
            of_score = int(results.get(Constants.ORDER_FLOW_SCORE, 0))
            of_signal = results.get(Constants.ORDER_FLOW_SIGNAL, "NEUTRAL")
            return of_score >= 40 or of_signal in ("STRONG_BUY_PRESSURE", "BUY_PRESSURE")
        except Exception:
            return False

    def _order_flow_strong_sell(self, results):
        """Presión vendedora fuerte en Order Flow (score <= -40)."""
        try:
            of_score = int(results.get(Constants.ORDER_FLOW_SCORE, 0))
            of_signal = results.get(Constants.ORDER_FLOW_SIGNAL, "NEUTRAL")
            return of_score <= -40 or of_signal in ("STRONG_SELL_PRESSURE", "SELL_PRESSURE")
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
            if angle_ima1 < 0 and angle_ima1_counter >= 3:
                return True
            return False
        except Exception:
            return False

    def _strong_confluence_buy(self, results, activeParam):
        """
        Confluencia triple para compra en BTC/USD:
        1. ANGLE_FLOW en UP (aceleración positiva)
        2. WEEK_FLOW en UP o alcista (bias semanal)
        3. BLG posición baja (% > 40 desde la base) — precio en zona de valor
        """
        try:
            angle_flow_up = "UP" in str(results.get(Constants.ANGLE_FLOW, ""))
            week_flow = results.get(Constants.WEEK_FLOW, Constants.WEEK_FLOW_UNDEF)
            week_up = "UP" in str(week_flow)
            blg_lower_pct = float(results[Constants.IND_BLG_LOWER_DST_PERCENT])
            blg_position_low = blg_lower_pct > 40   # precio en zona baja-media del canal
            flujo_sube = results[Constants.FLUJO] == Constants.FLUJO_SUBE
            return angle_flow_up and week_up and blg_position_low and flujo_sube
        except Exception:
            return False

    def _macd_bullish(self, results):
        """
        MACD por encima de su señal → momentum alcista activo.
        Usa MACD y MACD_SIGNAL de Constants.
        """
        try:
            macd = float(results.get(Constants.MACD, 0))
            macd_signal = float(results.get(Constants.MACD_SIGNAL, 0))
            return macd > macd_signal
        except Exception:
            return False

    def _macd_bearish(self, results):
        """
        MACD por debajo de su señal → momentum bajista → señal de cierre.
        """
        try:
            macd = float(results.get(Constants.MACD, 0))
            macd_signal = float(results.get(Constants.MACD_SIGNAL, 0))
            return macd < macd_signal
        except Exception:
            return False
