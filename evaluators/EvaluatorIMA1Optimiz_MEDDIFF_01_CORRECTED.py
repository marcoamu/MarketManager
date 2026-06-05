from evaluators.CierreBase import CierreBase
from evaluators.EvaluatorBase import EvaluatorBase
from evaluators.AperturaBase import AperturaBase
from service.Constants import Constants


class EvaluatorIMA1Optimiz_MEDDIFF_01_CORRECTED(EvaluatorBase, AperturaBase, CierreBase):
    """
    Correcciones basadas en análisis AMD (Junio 2026):
    
    PROBLEMAS IDENTIFICADOS:
    1. TREND_DOWN + BUY = -10.88 (peor pérdida) - No debe comprar en downtrend
    2. IMA1_BUY en TREND_UP = follow trend, funciona moderadamente
    3. IMA1_SELL en TREND_UP = contrarian mean reversion = WINNER (+23.33)
    4. ACUMULADO > 2.0 en entrada = pérdidas (llegó tarde)
    5. RSI oversold (<30) en TREND_DOWN = continuación, no reversión
    6. 14/18 trades = breakeven (señales en rango sin dirección)
    
    FILTROS APLICADOS:
    - TREND_UP Only (no TREND_DOWN para LONG)
    - INTENSITY = ALTA en TREND_UP
    - ACUMULADO < 1.5 (entrada temprana, no extendida)
    - RSI 40-70 (zona neutral, no oversold/overbought)
    - IND_BLG = IND_BLG_MED_BUY (solo en estado BUY confirmado)
    - IMA1_SELL en TREND_UP = prioridad (mean reversion winner)
    - IMA1_BUY en TREND_UP = solo si RSI 50-65 + BLG confirmación
    """

    def __init__(self):
        self.name = 'EvaluatorIMA1Optimiz_MEDDIFF_01_CORRECTED'

    def evaluate(self, results, activeParam):
        results[Constants.EVAl_NAME] = self.name
        self.updateTimeZoneValues(results)
        self.multiplicatorClose = activeParam.difference * 1.2
        self.enableControlOpen = False
        self.multiplicadorOpen = 2.2
        self.multiplicadorUP = 1
        self.WEEK_FLOW_MINVAL = 0
        self.evaluateChangeMarketTendence = True
        self.medstdminDiff = activeParam.medstdminDiff
        self.maxAcumValue = activeParam.closeAcumvalue * 3
        self.closeAcumValue = activeParam.closeAcumvalue
        self.ima1minDistance = activeParam.ima1minDistance
        self.ima1maxDistance = activeParam.ima1maxDistance
        self.closeDifference = activeParam.difference + activeParam.difference * 0.1
        self.accumulate = activeParam.accumulate
        self.angleUP = activeParam.angleUp
        self.angleDOWN = activeParam.angleDown
        if self.closeAcumValue > activeParam.accumulate:
            self.closeAcumValue = activeParam.difference + activeParam.difference * 0.2
        results[Constants.EVAl_CLOSE_ACUM] = self.closeAcumValue
        results[Constants.EVAl_CLOSE_DIFF] = self.closeDifference
        results[Constants.EVAl_ACUM] = self.accumulate
        
        # === FILTRO CRÍTICO: No comprar si TREND_DOWN ===
        trend_direction = results.get(Constants.MARKET_TREND_DIRECTION, Constants.TREND_NEUTRAL)
        if trend_direction == Constants.TREND_DOWN:
            # En downtrend no hacemos LONG - esperamos cambio de tendencia
            if results[Constants.CURRENT_ACTION] == Constants.ACTION_WAIT:
                results[Constants.NEW_ACTION] = Constants.ACTION_WAIT
            elif results[Constants.CURRENT_ACTION] == Constants.ACTION_BUY:
                # En downtrend, cerrar posiciones largas existentes
                self.evaluarFlujoBUY(results, activeParam)
            elif results[Constants.CURRENT_ACTION] == Constants.ACTION_SELL:
                self.evaluarFlujoSELL(results, activeParam)
            return
        
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
                self.evaluarApertura(results, activeParam)
            else:
                pass
        elif results[Constants.CURRENT_ACTION] == Constants.ACTION_BUY:
            self.evaluarFlujoBUY(results, activeParam)
        elif results[Constants.CURRENT_ACTION] == Constants.ACTION_SELL:
            self.evaluarFlujoSELL(results, activeParam)

    def evaluarApertura(self, results, activeParam):
        flujo_count = results[Constants.FLUJO_COUNT]
        trend_direction = results.get(Constants.MARKET_TREND_DIRECTION, Constants.TREND_NEUTRAL)
        trend_intensity = results.get(Constants.MARKET_TREND_INTENSITY, Constants.TREND_INTENSITY_LOW)
        
        # === FILTRO: TREND_UP + INTENSITY check ===
        if trend_direction == Constants.TREND_UP:
            if trend_intensity != Constants.TREND_INTENSITY_HIGH:
                # Intensidad BAJA en TREND_UP = weaker momentum, esperar
                # Pero no bloqueamos, solo esperamos mejor confirmación
                pass
        
        # === FILTRO: RSI check ===
        rsi = results.get(Constants.RSI, 50)
        if rsi is not None:
            # RSI < 40 = oversold (posible continuación downtrend)
            # RSI > 70 = overbought (retroceso inminente)
            # Solo permitir entradas en zona neutral 40-70
            if rsi < 40 or rsi > 70:
                # Demasiado extremo, no entrar
                if results[Constants.CURRENT_ACTION] == Constants.ACTION_WAIT:
                    results[Constants.NEW_ACTION] = Constants.ACTION_WAIT
                return
        
        # === FILTRO: ACUMULADO check (entrada temprana) ===
        acumulado_abs = results.get(Constants.ACUMULADO_ABS, 0)
        if acumulado_abs is not None and abs(acumulado_abs) > 1.5:
            # ACUMULADO > 1.5 = entrada tarde, el movimiento ya se extendió
            # El winner tuvo ACUM = 0.115, pérdidas tuvieron ACUM > 2.0
            if results[Constants.CURRENT_ACTION] == Constants.ACTION_WAIT:
                results[Constants.NEW_ACTION] = Constants.ACTION_WAIT
            return
        
        # === FILTRO: IND_BLG check ===
        ind_blg = results.get(Constants.IND_BLG, Constants.IND_BLG_MED_WAIT)
        if ind_blg != Constants.IND_BLG_MED_BUY:
            # Solo entrar cuando BLG confirma estado BUY
            # IND_BLG_MED_WAIT = sin dirección clara
            # IND_BLG_MED_SELL = continuación downtrend
            if results[Constants.CURRENT_ACTION] == Constants.ACTION_WAIT:
                results[Constants.NEW_ACTION] = Constants.ACTION_WAIT
            return
        
        # Dispatch basado en IMA1 con filtros de trend
        if results[Constants.IMA1] == Constants.IMA1_BUY:
            self.evaluarAperturaUP(results, activeParam, flujo_count)
        elif results[Constants.IMA1] == Constants.IMA1_SELL:
            self.evaluarAperturaDOWN(results, activeParam, flujo_count)
        elif results[Constants.IMA1] == Constants.IMA1_WAIT:
            self.evaluarAperturaCHANGE(results, activeParam, flujo_count)
        else:
            pass

    def evaluarAperturaOPT(self, results, activeParam):
        """Versión optimizada con filtros estrictos."""
        flujo_count = results[Constants.FLUJO_COUNT]
        blg_bandwidth = results[Constants.BLG_BANDWIDTH]
        ema_spread = results[Constants.EMA_SPREAD]
        if blg_bandwidth is None or ema_spread is None:
            return
        if blg_bandwidth < 0.02:
            return
        if ema_spread < 0.04:
            return
        ema10_slope = results[Constants.EMA10_SLOPE]
        ema20_slope = results[Constants.EMA20_SLOPE]
        week_flow = results[Constants.WEEK_FLOW]
        tendencia_alcista = ema10_slope > 0 and ema20_slope > 0 and (week_flow == Constants.UP)
        tendencia_bajista = ema10_slope < 0 and ema20_slope < 0 and (week_flow == Constants.DOWN)
        if not tendencia_alcista and (not tendencia_bajista):
            return
        angle_ema = results[Constants.ANGLE_EMA]
        if angle_ema is None or abs(angle_ema) < 10:
            return
        ema_dist = results[Constants.CURRVAL_EMA_DST]
        if ema_dist is None:
            return
        if abs(ema_dist) > 0.01:
            return
        rsi = results[Constants.RSI]
        if rsi is None:
            return
        ima1 = results[Constants.IMA1]
        if tendencia_alcista:
            if ima1 == Constants.IMA1_BUY:
                if 50 <= rsi <= 65:
                    self.evaluarAperturaUP(results, activeParam, flujo_count)
        elif tendencia_bajista:
            if ima1 == Constants.IMA1_SELL:
                if 35 <= rsi <= 50:
                    self.evaluarAperturaDOWN(results, activeParam, flujo_count)
        elif ima1 == Constants.IMA1_WAIT:
            self.evaluarAperturaCHANGE(results, activeParam, flujo_count)

    def evaluarAperturaCHANGE(self, results, activeParam, flujo_count):
        """Apertura en cambio de tendencia - solo si TREND_UP y filtros pasan."""
        trend_direction = results.get(Constants.MARKET_TREND_DIRECTION, Constants.TREND_NEUTRAL)
        if trend_direction != Constants.TREND_UP:
            return  # Solo operar cambios en TREND_UP
        
        difference_optimized = activeParam.difference
        unit_diff = 0
        multiplicador = 2
        self.printDifference('evaluarAperturaCHANGE', difference_optimized, self.closeAcumValue, self.closeDifference)
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MIN_DIST] >= difference_optimized:
                    results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
                    results[Constants.CLOSE_NXT_DOWN] = 0
        res, action, num = self.evaluateChance_Ima1_02(results, activeParam)
        if res:
            if 'BUY' in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                self.printInicioLog(f'BUY_CHANGE_BUY_{num}', results, activeParam)
                return
            elif 'SELL' in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                self.printInicioLog(f'SELL_CHANGE_BUY_{num}', results, activeParam)
                return

    def evaluarAperturaDOWN(self, results, activeParam, flujo_count):
        """
        Apertura en IMA1_SELL (precio bajo media) en TREND_UP.
        ESTO ES CONTRARIAN MEAN REVERSION - el winner +23.33 fue aquí.
        """
        trend_direction = results.get(Constants.MARKET_TREND_DIRECTION, Constants.TREND_NEUTRAL)
        trend_intensity = results.get(Constants.MARKET_TREND_INTENSITY, Constants.TREND_INTENSITY_LOW)
        
        # Solo en TREND_UP con ALTA intensidad
        if trend_direction != Constants.TREND_UP:
            return
        if trend_intensity != Constants.TREND_INTENSITY_HIGH:
            return  # PRIORIDAD: intensity ALTA para mean reversion
        
        # RSI filter - no entrar si sobrecomprado
        rsi = results.get(Constants.RSI, 50)
        if rsi is not None and (rsi < 40 or rsi > 70):
            return
        
        # ACUMULADO filter - entrada temprana
        acumulado_abs = results.get(Constants.ACUMULADO_ABS, 0)
        if acumulado_abs is not None and abs(acumulado_abs) > 1.5:
            return
        
        difference_optimized = activeParam.difference
        unit_diff = 0
        self.printDifference('evaluarAperturaDOWN', difference_optimized, self.closeAcumValue, self.closeDifference)
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
                    results[Constants.CLOSE_NXT_DOWN] = 0
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MIN_DIST] >= difference_optimized:
                    results[Constants.CLOSE_NXT_UP] = 0
        res, action, num = self.evaluateDownOpen_IMA1_03(results, activeParam)
        if res:
            if 'SELL' in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                self.printInicioLog(f'SELL_DOWN_{num}', results, activeParam)
                return
            elif 'BUY' in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                self.printInicioLog(f'BUY_DOWN_INV_{num}', results, activeParam)
                return

    def evaluarAperturaUP(self, results, activeParam, flujo_count):
        """
        Apertura en IMA1_BUY (precio sobre media) en TREND_UP.
        Esto es follow-trend, menos agresivo que contrarian.
        Requiere mejor confirmación: RSI 50-65 + BLG + ACUM bajo.
        """
        trend_direction = results.get(Constants.MARKET_TREND_DIRECTION, Constants.TREND_NEUTRAL)
        trend_intensity = results.get(Constants.MARKET_TREND_INTENSITY, Constants.TREND_INTENSITY_LOW)
        
        # Solo en TREND_UP
        if trend_direction != Constants.TREND_UP:
            return
        
        # RSI filter - zona neutral 50-65 para follow-trend
        rsi = results.get(Constants.RSI, 50)
        if rsi is not None:
            if rsi < 50 or rsi > 65:
                return  # Fuera de zona óptima para follow-trend
        
        # ACUMULADO filter - muy estricto para follow-trend
        acumulado_abs = results.get(Constants.ACUMULADO_ABS, 0)
        if acumulado_abs is not None and abs(acumulado_abs) > 1.0:
            return  # Más estricto que contrarian (1.0 vs 1.5)
        
        # IND_BLG filter - confirmación obligatoria
        ind_blg = results.get(Constants.IND_BLG, Constants.IND_BLG_MED_WAIT)
        if ind_blg != Constants.IND_BLG_MED_BUY:
            return
        
        difference_optimized = activeParam.difference
        unit_diff = 0
        self.printDifference('evaluarAperturaUP', difference_optimized, self.closeAcumValue, self.closeDifference)
        if results[Constants.CLOSE_NXT_UP] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_SUBE:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MIN_DIST] >= difference_optimized:
                    results[Constants.CLOSE_NXT_UP] = 0
        if results[Constants.CLOSE_NXT_DOWN] == 1:
            if results[Constants.FLUJO] == Constants.FLUJO_BAJA:
                if results[Constants.ACUMULADO_ABS] >= difference_optimized or results[Constants.ACTION_MAX_DIST] >= difference_optimized:
                    results[Constants.CLOSE_NXT_DOWN] = 0
        res, action, num = self.evaluateUpOpen_Ima1_02(results, activeParam)
        if res:
            if 'BUY' in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                self.printInicioLog(f'BUY_UP_BUY_{num}', results, activeParam)
                return
            elif 'SELL' in action:
                results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                self.printInicioLog(f'SELL_UP_BUY_{num}', results, activeParam)
                return

    def evaluarFlujoBUY(self, results, activeParam):
        difference_optimized = activeParam.difference
        unit_diff = 0
        flujo_count = results[Constants.FLUJO_COUNT]
        self.printDifference('evaluarFlujoBUY', difference_optimized, self.closeAcumValue, self.closeDifference, self.accumulate)
        
        # === FILTRO DE CIERRE: TREND_DOWN = cerrar todo ===
        trend_direction = results.get(Constants.MARKET_TREND_DIRECTION, Constants.TREND_NEUTRAL)
        if trend_direction == Constants.TREND_DOWN:
            # Cambio a downtrend = cerrar posiciones largas inmediatamente
            self.printFinLog('CLOSE_TREND_REVERSAL', 'evaluarFlujoBUY', results, activeParam)
            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
            return
        
        # === FILTRO: ACUMULADO > 2.0 = entrada muy tarde, cerrar ===
        acumulado = results.get(Constants.ACUMULADO, 0)
        if acumulado is not None and abs(acumulado) > 2.0:
            self.printFinLog('CLOSE_ACUM_EXTENDED', 'evaluarFlujoBUY', results, activeParam)
            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
            return
        
        self.control_BUY_IMA_02(results, activeParam, self.closeAcumValue, self.closeDifference, self.accumulate)

    def evaluarFlujoSELL(self, results, activeParam):
        difference_optimized = activeParam.difference
        unit_diff = 0
        flujo_count = results[Constants.FLUJO_COUNT]
        self.printDifference('evaluarFlujoSELL', difference_optimized, self.closeAcumValue, self.closeDifference, self.accumulate)
        
        # === FILTRO: TREND_UP = cerrar shorts ===
        trend_direction = results.get(Constants.MARKET_TREND_DIRECTION, Constants.TREND_NEUTRAL)
        if trend_direction == Constants.TREND_UP:
            # Cambio a uptrend = cerrar posiciones cortas
            self.printFinLog('CLOSE_TREND_REVERSAL_SHORT', 'evaluarFlujoSELL', results, activeParam)
            results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
            return
        
        self.control_SELL_IMA1_02(results, activeParam, self.closeAcumValue, self.closeDifference, self.accumulate)