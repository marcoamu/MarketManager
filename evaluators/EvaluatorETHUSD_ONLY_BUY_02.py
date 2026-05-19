from evaluators.CierreBase import CierreBase
from evaluators.EvaluatorBase import EvaluatorBase
from evaluators.AperturaBase import AperturaBase
from service.Constants import Constants


class EvaluatorETHUSD_ONLY_BUY_02(EvaluatorBase, AperturaBase, CierreBase):
    """
    EvaluatorETHUSD_ONLY_BUY_02 — Monitor ETH/USD solo COMPRA (LONG) v2
    =====================================================================

    Evolución de EvaluatorETHUSD_ONLY_BUY_01 incorporando las técnicas
    ganadoras de EvaluatorEMA_LONG_ONLY_UP_04_01 (mejor evaluador actual).

    Mejoras clave respecto a v01:
    ─────────────────────────────────────────────────
    1. Apertura UP usa evaluateUpOpen_EMA_OUP_03 (la del best performer)
       con isRisingFromWEEKNEW + weekNewFlow + control weekdirBotPercent
    2. Cierre BUY usa control_BUY_EMA_OUP_03 (week_new_flow early exit)
       ANTES de evaluar cierres secundarios → corta pérdidas más rápido
    3. Nuevo indicador RSI_MOMENTUM: RSI + RSI_DIFF + RSI_SLOPE combinados
       para detectar momentum ascendente antes de que RSI cruce 50
    4. Nuevo indicador MACD_HISTOGRAM_ACCEL: aceleración del histograma MACD
       para capturar cambios de momentum antes del cruce clásico
    5. closeDifference usa 10% extra (como el best performer) vs 4% de v01
    6. multiplicatorClose usa 1.2x (best performer) vs 1.4x de v01
    7. flujo_Count = 2 (best performer) vs 1 de v01 → menos cierres falsos
    8. Reglas de apertura DOWN más selectivas con Order Flow + RSI_MOMENTUM
    9. Trailing profit: cierre parcial cuando ganancia > 2x closeProfit

    Indicadores utilizados (confluencia multi-señal ampliada):
    ─────────────────────────────────────────────────
    1.  EMA            → dirección principal de tendencia
    2.  Bollinger Bands → posicionamiento de precio en el canal
    3.  RSI            → momentum clásico
    4.  RSI_MOMENTUM   → [NUEVO] momentum avanzado (RSI + slope + accel)
    5.  MACD           → cruce de momentum
    6.  MACD_HISTOGRAM → [NUEVO] aceleración del histograma
    7.  Order Flow     → presión compradora real (delta/ratio)
    8.  ANGLE / ANGLE_IMA1 → fuerza y aceleración de la tendencia
    9.  WEEK_FLOW / WEEK_NEW → tendencia semanal y flujo nuevo
    10. IMA5MA20       → cruce rápido de medias
    11. MEDSTD / MED   → desviación estándar de la media
    12. MARKET_TENDENCE → tendencia macro
    13. WEEK_DIR_BOT_DST_MED_NEW_FLOW → flujo semanal avanzado (del best performer)

    Reglas de apertura (SOLO BUY):
    ─────────────────────────────────────────────────
    A. [CORE] evaluateUpOpen_EMA_OUP_03 (del best performer) → entrada principal
    B. RSI_MOMENTUM alcista + BLG posición baja + WEEK UP → entrada momentum
    C. Order Flow BUY fuerte + MACD_HIST acelerando + medios UP → entrada agresiva
    D. IMA5MA20 BUY + FLUJO SUBE + ángulo rising + weekNewFlow > 0 → entrada trend
    E. Rebote V-shape: RSI<25 + BLG lower perforado + Order Flow BUY fuerte
    F. Market tendence UP + RSI_MOMENTUM positivo + no OF_SELL → entrada macro
    G. [DOWN] REBOUND: evaluateDownOpen_EMA_OUP_02 (solo BUY) → contratendencia
    H. [DOWN] RSI extremo< 26 + OF BUY + BLG lower cerca → panic buy

    Reglas de cierre:
    ─────────────────────────────────────────────────
    1. [CORE] control_BUY_EMA_OUP_03 (week_new_flow exit) → cierre principal
    2. RSI sobrecompra (>72) + ganancia → salida agresiva
    3. Order Flow invierte a SELL fuerte → salida defensiva
    4. Trailing profit: ganancia > 2x closeProfit + BLG upper < 10% → proteger
    5. MACD histograma decelerando fuerte → salida cautelar
    6. Ángulo bajista fuerte (contador >= 3) → salida preventiva
    7. Stop-loss: ACTION_ACUM negativo > closeDifference → limitar pérdidas
    8. EMA invierte a SELL + flujo baja + ACTION_COUNT >= 4 → salida inversionista

    Versión: ETHUSD_ONLY_BUY_02
    """

    def __init__(self):
        self.name = "EvaluatorETHUSD_ONLY_BUY_02"

    # ══════════════════════════════════════════════════════════════════════════
    # INDICADORES NUEVOS
    # ══════════════════════════════════════════════════════════════════════════

    def _calc_rsi_momentum(self, results):
        """
        RSI_MOMENTUM — indicador compuesto que combina:
        - RSI actual (zona)
        - RSI_DIFF (cambio reciente)
        - RSI_SLOPE (dirección del cambio)

        Retorna un score de -100 a +100:
        - > 30: momentum alcista fuerte → buena entrada
        - > 0: momentum alcista moderado
        - < -30: momentum bajista fuerte → no entrar
        """
        try:
            rsi = float(results.get(Constants.RSI, 50))
            rsi_diff = float(results.get(Constants.RSI_DIFF, 0))
            rsi_slope = float(results.get(Constants.RSI_SLOPE, 0))

            score = 0

            # Componente zona RSI (peso 40%)
            if rsi < 30:
                score += 40  # Sobreventa extrema → alta probabilidad de rebote
            elif rsi < 40:
                score += 25  # Zona de oportunidad
            elif rsi < 50:
                score += 10  # Neutral-bajo
            elif rsi < 60:
                score += 0   # Neutral
            elif rsi < 70:
                score -= 10  # Advertencia
            else:
                score -= 30  # Sobrecompra

            # Componente dirección RSI (peso 35%)
            if rsi_diff > 5:
                score += 35  # Aceleración fuerte alcista
            elif rsi_diff > 2:
                score += 20  # Aceleración moderada
            elif rsi_diff > 0:
                score += 10  # Subiendo
            elif rsi_diff > -2:
                score -= 5   # Bajando suave
            elif rsi_diff > -5:
                score -= 15  # Bajando moderado
            else:
                score -= 30  # Bajando fuerte

            # Componente slope RSI (peso 25%)
            if rsi_slope > 3:
                score += 25
            elif rsi_slope > 1:
                score += 15
            elif rsi_slope > 0:
                score += 5
            elif rsi_slope > -1:
                score -= 5
            else:
                score -= 20

            return max(-100, min(100, score))
        except Exception:
            return 0

    def _calc_macd_histogram_accel(self, results):
        """
        MACD_HISTOGRAM_ACCEL — detecta aceleración del histograma MACD.

        El histograma MACD = MACD - MACD_SIGNAL.
        Cuando el histograma está creciendo, el momentum se está acelerando.
        Esto detecta cambios de momentum ANTES del cruce clásico MACD.

        Retorna:
        - valor positivo: histograma creciendo (momentum alcista acelerando)
        - valor negativo: histograma decreaciendo (momentum bajista)
        - 0: sin dato suficiente
        """
        try:
            macd = float(results.get(Constants.MACD, 0))
            macd_signal = float(results.get(Constants.MACD_SIGNAL, 0))
            histogram = macd - macd_signal
            return histogram
        except Exception:
            return 0

    def _rsi_momentum_bullish(self, results, min_score=20):
        """RSI_MOMENTUM por encima de un umbral → momentum alcista."""
        return self._calc_rsi_momentum(results) >= min_score

    def _macd_hist_accelerating(self, results, min_value=0):
        """Histograma MACD acelerando (positivo y creciendo)."""
        return self._calc_macd_histogram_accel(results) > min_value

    # ══════════════════════════════════════════════════════════════════════════
    # MÉTODO PRINCIPAL
    # ══════════════════════════════════════════════════════════════════════════
    def evaluate(self, results, activeParam):
        results[Constants.EVAl_NAME] = self.name

        self.updateTimeZoneValues(results)

        # ─── MULTIPLICADORES (adoptados del best performer) ──────────────
        # Best performer usa 1.2x → menos agresivo pero más consistente
        self.multiplicatorClose = activeParam.difference * 1.2
        self.multiplicatorPREVIUS = activeParam.difference * 1.2

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

        # ─── PARÁMETROS BOLLINGER ─────────────────────────────────────────
        self.BLGDist = activeParam.bollingerDst
        # Valores del best performer (más conservadores y probados)
        self.blgLowerDist = 1.5
        self.blgLowerDistPercemt = 10
        self.bollingerClose = activeParam.bollingerClose

        # ─── PARÁMETROS DE CIERRE ─────────────────────────────────────────
        self.closeAcumValue = activeParam.closeProfit
        # Best performer usa 10% extra vs v01 que usaba 4%
        self.closeDifference = activeParam.difference + (activeParam.difference * 0.10)
        self.accumulate = activeParam.accumulate

        # ─── PARÁMETROS DE ÁNGULO ─────────────────────────────────────────
        self.angleUP = activeParam.angleUp
        self.angleDOWN = activeParam.angleDown

        # Publicar valores en results
        results[Constants.EVAl_CLOSE_ACUM] = self.closeAcumValue
        results[Constants.EVAl_CLOSE_DIFF] = self.closeDifference
        results[Constants.EVAl_ACUM] = self.accumulate

        # Best performer usa flujo_Count = 2 → menos cierres prematuros
        self.flujo_Count = 2

        # ─── CONTROL DE HORARIO ───────────────────────────────────────────
        currentTime = self.gettime(results)
        intime = False
        print(f'[ETHUSD_ONLY_BUY_02] EVALUATOR {self.name}  PARAM: {activeParam.name}')

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
                self.evaluarAperturaEMA_ETHUSD_V2(results, activeParam)
            else:
                print(f"[ETHUSD_ONLY_BUY_02] FUERA DE HORARIO")
        elif current == Constants.ACTION_BUY:
            self.evaluarFlujoBUY_ETHUSD_V2(results, activeParam)
        elif current == Constants.ACTION_SELL:
            # ── NUNCA OPERAMOS SELL: cerrar inmediatamente ──
            self._cerrar_sell_no_permitido(results, activeParam)

    # ══════════════════════════════════════════════════════════════════════════
    # APERTURA: despacha según EMA
    # ══════════════════════════════════════════════════════════════════════════
    def evaluarAperturaEMA_ETHUSD_V2(self, results, activeParam):
        flujo_count = results[Constants.FLUJO_COUNT]

        ema = results[Constants.INDICATOR_EMA]
        if ema == Constants.INDICATOR_EMA_BUY:
            self.evaluarAperturaUP_ETHUSD_V2(results, activeParam, flujo_count)
        elif ema == Constants.INDICATOR_EMA_SELL:
            # En tendencia bajista buscamos SOLO rebotes alcistas
            self.evaluarAperturaDOWN_ETHUSD_V2(results, activeParam, flujo_count)
        elif ema == Constants.INDICATOR_EMA_WAIT:
            # En WAIT evaluamos señales fuertes de compra
            self.evaluarAperturaWAIT_ETHUSD_V2(results, activeParam, flujo_count)
        else:
            print(f"[ETHUSD_ONLY_BUY_02] EMA sin definir — esperando señal")

    # ══════════════════════════════════════════════════════════════════════════
    # APERTURA EN TENDENCIA ALCISTA (EMA BUY) — entrada principal
    # Usa evaluateUpOpen_EMA_OUP_03 del best performer como regla CORE
    # ══════════════════════════════════════════════════════════════════════════
    def evaluarAperturaUP_ETHUSD_V2(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference

        self.printDifference(
            "evaluarAperturaUP_ETHUSD_V2", difference_optimized,
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

        # ════════════════════════════════════════════════════════════════
        # REGLA A [CORE]: evaluateUpOpen_EMA_OUP_03 del best performer
        # Esta es la regla que hace rentable al mejor evaluador.
        # Usa isRisingFromWEEKNEW + weekNewFlow + weekdirBotPercent
        # ════════════════════════════════════════════════════════════════
        res, action, num = self.evaluateUpOpen_EMA_OUP_03(results, activeParam)
        if res:
            if "BUY" in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                self.printInicioLog(f"ETH2_UP_OUP03_BUY_{num}", results, activeParam)
                return
            # ← SELL ignorado: solo compramos

        # ════════════════════════════════════════════════════════════════
        # REGLA B: RSI_MOMENTUM alcista + BLG posición baja + WEEK UP
        # [NUEVO] Usa el indicador RSI_MOMENTUM para capturar entradas
        # que el RSI clásico no detecta (momentum antes de cruce 50)
        # ════════════════════════════════════════════════════════════════
        if self._rsi_momentum_bullish(results, min_score=30):
            if self._blg_near_lower(results, activeParam, max_percent=20.0):
                week_flow = results.get(Constants.WEEK_FLOW, Constants.WEEK_FLOW_UNDEF)
                if "UP" in str(week_flow) or week_flow == Constants.WEEK_FLOW_UNDEF:
                    if (results[Constants.ACUMULADO_ABS] >= difference_optimized * 0.75 or
                            results[Constants.ACTION_MIN_DIST] >= difference_optimized * 0.75):
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        self.printInicioLog("ETH2_UP_RSI_MOM_BLG_BUY", results, activeParam)
                        return

        # ════════════════════════════════════════════════════════════════
        # REGLA C: Order Flow BUY fuerte + MACD acelerando + medios UP
        # [MEJORADO] Ahora usa MACD_HISTOGRAM_ACCEL para entrada más
        # temprana que esperar el cruce completo
        # ════════════════════════════════════════════════════════════════
        if self._order_flow_strong_buy(results):
            if self._macd_hist_accelerating(results, min_value=0):
                if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_UP:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized * 0.70:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        self.printInicioLog("ETH2_UP_OF_MACDH_BUY", results, activeParam)
                        return

        # ════════════════════════════════════════════════════════════════
        # REGLA D: IMA5MA20 BUY + FLUJO SUBE + ángulo rising + weekNewFlow
        # [MEJORADO] Añade weekNewFlow > 0 del best performer
        # ════════════════════════════════════════════════════════════════
        if results[Constants.IMA5MA20] == Constants.INDICATOR_EMA_BUY:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                weekNewFlow = results.get(Constants.WEEK_DIR_BOT_DST_MED_NEW_FLOW, 0)
                if weekNewFlow > 0:
                    if results[Constants.WEEK_DIR_BOT_DST] < 80:
                        isRising, angleDiff = self.isRisingAngleIma1(results)
                        if isRising:
                            if results[Constants.ACUMULADO_ABS] >= difference_optimized:
                                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                self.printInicioLog("ETH2_UP_IMA5_WFLOW_BUY", results, activeParam)
                                return

        # ════════════════════════════════════════════════════════════════
        # REGLA E: RSI sobreventa clásica + BLG lower cerca + OF BUY
        # [MANTENIDO] Buena regla de v01 para capturas de rebote
        # ════════════════════════════════════════════════════════════════
        if self._rsi_oversold(results) and self._blg_near_lower(results, activeParam):
            if self._order_flow_strong_buy(results) or self._rsi_momentum_bullish(results, min_score=15):
                if (results[Constants.ACUMULADO_ABS] >= difference_optimized * 0.65 or
                        results[Constants.ACTION_MIN_DIST] >= difference_optimized * 0.65):
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                    self.printInicioLog("ETH2_UP_RSI_OS_BLG_BUY", results, activeParam)
                    return

        # ════════════════════════════════════════════════════════════════
        # REGLA F: Market tendence UP + RSI_MOMENTUM positivo + no OF_SELL
        # [MEJORADO] Usa RSI_MOMENTUM en vez de RSI_BELOW clásico
        # ════════════════════════════════════════════════════════════════
        if results.get(Constants.MARKET_TENDENCE) == Constants.MARKET_TENDENCE_UP:
            if self._rsi_momentum_bullish(results, min_score=10):
                if not self._order_flow_strong_sell(results):
                    if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_UP:
                        if results[Constants.ACUMULADO_ABS] >= difference_optimized:
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            self.printInicioLog("ETH2_UP_MKTEND_RSIMOM_BUY", results, activeParam)
                            return

    # ══════════════════════════════════════════════════════════════════════════
    # APERTURA EN TENDENCIA BAJISTA (EMA SELL) — solo rebotes BUY agresivos
    # Más selectivo que v01: requiere confirmación más fuerte
    # ══════════════════════════════════════════════════════════════════════════
    def evaluarAperturaDOWN_ETHUSD_V2(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference

        self.printDifference(
            "evaluarAperturaDOWN_ETHUSD_V2", difference_optimized,
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

        # ════════════════════════════════════════════════════════════════
        # REGLA G: evaluateDownOpen_EMA_OUP_02 (solo BUY)
        # Del best performer — contratendencia con imaemadist + weekRising
        # ════════════════════════════════════════════════════════════════
        res, action, num = self.evaluateDownOpen_EMA_OUP_02(results, activeParam)
        if res:
            if "BUY" in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                self.printInicioLog(f"ETH2_DOWN_OUP02_BUY_{num}", results, activeParam)
                return
            # SELL ignorado

        # ════════════════════════════════════════════════════════════════
        # REGLA H: RSI extremo + BLG lower cerca + Order Flow BUY
        # [MEJORADO] Añade RSI_MOMENTUM como confirmación extra
        # ════════════════════════════════════════════════════════════════
        if self._rsi_extreme_oversold(results) and self._blg_near_lower(results, activeParam, max_percent=12.0):
            if self._order_flow_strong_buy(results):
                if self._rsi_momentum_bullish(results, min_score=0):
                    results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                    self.printInicioLog("ETH2_DOWN_RSI_EXT_BLG_BUY", results, activeParam)
                    return

        # ════════════════════════════════════════════════════════════════
        # REGLA I: Order Flow comprador muy fuerte + medios girando
        # [MANTENIDO] Pero con filtro MACD histograma positivo
        # ════════════════════════════════════════════════════════════════
        if self._order_flow_strong_buy(results):
            if results[Constants.INDICATOR_MED] == Constants.INDICATOR_TM_UP:
                if self._macd_hist_accelerating(results):
                    if results[Constants.IMA5MA20] == Constants.INDICATOR_EMA_BUY:
                        if results[Constants.ACUMULADO_ABS] >= difference_optimized * 0.85:
                            results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                            self.printInicioLog("ETH2_DOWN_OF_MACDH_BUY", results, activeParam)
                            return

        # ════════════════════════════════════════════════════════════════
        # REGLA J: V-shape ETH — BLG lower perforado + flujo sube + RSI bajo
        # [MANTENIDO] Clásico rebote V-shape de ETH
        # ════════════════════════════════════════════════════════════════
        if results[Constants.IND_BLG_LOWER_DST_PERCENT] < 0:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if self._rsi_oversold(results):
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized * 0.9:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        self.printInicioLog("ETH2_DOWN_BLG_VSHAPE_BUY", results, activeParam)
                        return

    # ══════════════════════════════════════════════════════════════════════════
    # APERTURA EN MODO WAIT (EMA sin dirección) — señales muy fuertes
    # ══════════════════════════════════════════════════════════════════════════
    def evaluarAperturaWAIT_ETHUSD_V2(self, results, activeParam, flujo_count):
        difference_optimized = activeParam.difference

        # ── Order Flow BUY + RSI_MOMENTUM alcista + WEEK UP ──────────────
        if self._order_flow_strong_buy(results) and self._rsi_momentum_bullish(results, min_score=25):
            if results.get(Constants.WEEK_FLOW) == Constants.WEEK_FLOW_UP:
                if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized * 0.90:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        self.printInicioLog("ETH2_WAIT_OF_RSIMOM_BUY", results, activeParam)
                        return

        # ── RSI extremo + Order Flow positivo + MACD acelerando ──────────
        if self._rsi_extreme_oversold(results, threshold=25.0):
            if self._order_flow_strong_buy(results):
                if self._macd_hist_accelerating(results):
                    if results[Constants.ACUMULADO_ABS] >= difference_optimized * 0.85:
                        results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                        self.printInicioLog("ETH2_WAIT_RSI_OF_MACD_BUY", results, activeParam)
                        return

    # ══════════════════════════════════════════════════════════════════════════
    # GESTIÓN DE POSICIÓN BUY: cierre multi-criterio mejorado
    # Primera línea de defensa: control_BUY_EMA_OUP_03 del best performer
    # ══════════════════════════════════════════════════════════════════════════
    def evaluarFlujoBUY_ETHUSD_V2(self, results, activeParam):
        difference_optimized = activeParam.difference
        flujo_count = results[Constants.FLUJO_COUNT]

        self.printDifference(
            "evaluarFlujoBUY_ETHUSD_V2", difference_optimized,
            self.closeAcumValue, self.closeDifference,
            self.accumulate
        )

        # ════════════════════════════════════════════════════════════════
        # CIERRE 1 [PRIORIDAD]: RSI sobrecompra con ganancia → salida rápida
        # Se evalúa ANTES del cierre core para no dejar escapar ganancias
        # ════════════════════════════════════════════════════════════════
        if self._rsi_overbought(results):
            if results[Constants.ACUMULADO] < 0:  # BUY: acum < 0 = ganancia
                if results[Constants.ACTION_COUNT] >= self.flujo_Count:
                    self.printFinLog("ETH2_CLOSE_BUY_RSI_OB", "evaluarFlujoBUY_ETHUSD_V2", results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

        # ════════════════════════════════════════════════════════════════
        # CIERRE 2: Order Flow invierte a SELL fuerte con ganancia
        # ════════════════════════════════════════════════════════════════
        if self._order_flow_strong_sell(results):
            if results[Constants.ACTION_COUNT] >= 2:
                if results[Constants.ACUMULADO] < 0:  # en ganancia
                    self.printFinLog("ETH2_CLOSE_BUY_OF_INVERT", "evaluarFlujoBUY_ETHUSD_V2", results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

        # ════════════════════════════════════════════════════════════════
        # CIERRE 3 [NUEVO]: Trailing profit — proteger ganancias grandes
        # Si ganancia > 2x closeProfit Y estamos cerca del BLG upper → salir
        # ════════════════════════════════════════════════════════════════
        if results[Constants.ACTION_ACUM] > 0:
            if results[Constants.ACTION_ACUM] >= self.closeAcumValue * 2:
                if results[Constants.IND_BLG_UPPER_DST_PERCENT] <= 10:
                    self.printFinLog("ETH2_CLOSE_BUY_TRAIL_PROFIT", "evaluarFlujoBUY_ETHUSD_V2", results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

        # ════════════════════════════════════════════════════════════════
        # CIERRE 4 [NUEVO]: MACD histograma decelerando fuerte con ganancia
        # Detecta pérdida de momentum antes del cruce clásico
        # ════════════════════════════════════════════════════════════════
        macd_hist = self._calc_macd_histogram_accel(results)
        if macd_hist < -0.5:  # Histograma negativo fuerte
            if results[Constants.ACTION_COUNT] >= 3:
                if results[Constants.ACUMULADO] < 0:  # en ganancia
                    if self._order_flow_strong_sell(results) or not self._rsi_momentum_bullish(results, min_score=0):
                        self.printFinLog("ETH2_CLOSE_BUY_MACDH_DECEL", "evaluarFlujoBUY_ETHUSD_V2", results, activeParam)
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return

        # ════════════════════════════════════════════════════════════════
        # CIERRE 5: Ángulo bajista fuerte con contador >= 3
        # ════════════════════════════════════════════════════════════════
        if self._strong_angle_down(results, activeParam):
            if results[Constants.ACTION_COUNT] >= 3:
                if results[Constants.ACUMULADO] < 0:
                    self.printFinLog("ETH2_CLOSE_BUY_ANGLE_DOWN", "evaluarFlujoBUY_ETHUSD_V2", results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

        # ════════════════════════════════════════════════════════════════
        # CIERRE 6: Stop-loss — limitar pérdidas
        # ════════════════════════════════════════════════════════════════
        if results[Constants.ACTION_ACUM] <= 0:
            if results[Constants.ACTION_COUNT] >= 2:
                if abs(results[Constants.ACTION_ACUM]) >= self.closeDifference:
                    self.printFinLog("ETH2_CLOSE_BUY_STOPLOSS", "evaluarFlujoBUY_ETHUSD_V2", results, activeParam)
                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                    return

        # ════════════════════════════════════════════════════════════════
        # CIERRE 7: EMA invierte a SELL + flujo baja
        # ════════════════════════════════════════════════════════════════
        if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if results[Constants.ACTION_COUNT] >= 4:
                    if results[Constants.ACUMULADO] < 0:  # en ganancia
                        self.printFinLog("ETH2_CLOSE_BUY_EMA_INVERT", "evaluarFlujoBUY_ETHUSD_V2", results, activeParam)
                        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                        return

        # ════════════════════════════════════════════════════════════════
        # CIERRE CORE: control_BUY_EMA_OUP_03 del best performer
        # Usa week_new_flow para early exit + isRisingFromWeekNew
        # Se pone al final para que los cierres de ganancia actúen primero
        # ════════════════════════════════════════════════════════════════
        self.control_BUY_EMA_OUP_03(results, activeParam, self.closeAcumValue, self.closeDifference)

    # ══════════════════════════════════════════════════════════════════════════
    # PROTECCIÓN: cierre inmediato de cualquier posición SELL no deseada
    # ══════════════════════════════════════════════════════════════════════════
    def _cerrar_sell_no_permitido(self, results, activeParam):
        """
        Este evaluador es ONLY BUY.
        Si por algún motivo externo hay una posición SELL abierta,
        la cerramos en el siguiente tick sin importar el resultado.
        """
        print(f"[ETHUSD_ONLY_BUY_02] ⚠️  POSICIÓN SELL DETECTADA — cerrando inmediatamente")
        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE

    # ══════════════════════════════════════════════════════════════════════════
    # HELPERS PRIVADOS: evaluación de indicadores individuales
    # ══════════════════════════════════════════════════════════════════════════

    def _rsi_overbought(self, results, threshold=72.0):
        """RSI en zona de sobrecompra (> threshold). ETH: 72."""
        try:
            rsi = float(results.get(Constants.RSI, 50))
            return rsi > threshold
        except Exception:
            return False

    def _rsi_oversold(self, results, threshold=32.0):
        """RSI en zona de sobreventa (< threshold). ETH: 32."""
        try:
            rsi = float(results.get(Constants.RSI, 50))
            return rsi < threshold
        except Exception:
            return False

    def _rsi_extreme_oversold(self, results, threshold=26.0):
        """RSI en zona de sobreventa extrema."""
        try:
            rsi = float(results.get(Constants.RSI, 50))
            return rsi < threshold
        except Exception:
            return False

    def _rsi_below(self, results, threshold=45.0):
        """RSI por debajo de un umbral dado (helper genérico)."""
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

    def _blg_near_lower(self, results, activeParam, max_percent=15.0):
        """Precio cerca del Bollinger Inferior (distancia % < max_percent)."""
        try:
            lower_pct = float(results[Constants.IND_BLG_LOWER_DST_PERCENT])
            return 0 <= lower_pct <= max_percent
        except Exception:
            return False

    def _blg_near_upper(self, results, activeParam, max_percent=15.0):
        """Precio cerca del Bollinger Superior (distancia % < max_percent)."""
        try:
            upper_pct = float(results[Constants.IND_BLG_UPPER_DST_PERCENT])
            return 0 <= upper_pct <= max_percent
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

    def _macd_bullish(self, results):
        """MACD por encima de su señal → momentum alcista activo."""
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
