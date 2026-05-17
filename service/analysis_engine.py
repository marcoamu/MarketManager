"""
AnalysisEngine - Motor unificado de análisis.
Fusiona AnalisisHelper + ProbEvaluator + SignalEngine.
"""

from typing import Dict, Any, Optional, Tuple
import pandas as pd


class AnalysisEngine:
    """Motor unificado de análisis técnico y probabilidades."""

    # Constantes de dirección
    DIR_UP = 'DIR_UP'
    DIR_DOWN = 'DIR_DOWN'
    DIR_WAIT = 'DIR_WAIT'

    # Constantes de acción
    ACTION_BUY = 'BUY'
    ACTION_SELL = 'SELL'
    ACTION_WAIT = 'WAIT'

    def __init__(self):
        self.name = "AnalysisEngine"

    # ==================== MAIN ANALYSIS ====================

    def analyze(self, data: pd.DataFrame, active, results: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Ejecuta análisis completo.

        Args:
            data: DataFrame con datos históricos
            active: Activo a analizar
            results: Diccionario existente para actualizar

        Returns:
            Diccionario con todos los indicadores calculados
        """
        if results is None:
            results = {}

        # Calcular indicadores técnicos
        self.calculate_technical_indicators(data, active, results)

        # Calcular análisis de flujo
        self.calculate_flow_analysis(data, active, results)

        # Calcular probabilidades
        self.calculate_probabilities(data, active, results)

        return results

    def calculate_technical_indicators(self, data: pd.DataFrame, active, results: Dict) -> Dict:
        """Calcula indicadores técnicos."""
        close_col = 'Close'

        # RSI
        self._calculate_rsi(data, results, period=14)

        # Medias móviles
        self._calculate_moving_averages(data, active, results)

        # Bollinger Bands
        self._calculate_bollinger(data, active, results)

        # MACD
        self._calculate_macd(data, results)

        return results

    def _calculate_rsi(self, data: pd.DataFrame, results: Dict, period: int = 14):
        """Calcula RSI."""
        close_col = 'Close'
        delta = data[close_col].diff()

        gain = delta.where(delta > 0, 0).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        results['RSI'] = rsi.iloc[-1] if len(rsi) > 0 else 50

    def _calculate_moving_averages(self, data: pd.DataFrame, active, results: Dict):
        """Calcula medias móviles."""
        close_col = 'Close'

        # Parámetros
        ima1 = getattr(active.parameters, 'ima1', 5)
        ima2 = getattr(active.parameters, 'ima2', 10)
        ima3 = getattr(active.parameters, 'ima3', 20)

        results['IMA1'] = data[close_col].rolling(window=ima1).mean().iloc[-1]
        results['IMA2'] = data[close_col].rolling(window=ima2).mean().iloc[-1]
        results['IMA3'] = data[close_col].rolling(window=ima3).mean().iloc[-1]

    def _calculate_bollinger(self, data: pd.DataFrame, active, results: Dict):
        """Calcula Bandas de Bollinger."""
        close_col = 'Close'
        window = getattr(active.parameters, 'bollinger', 20)

        ma = data[close_col].rolling(window=window).mean()
        std = data[close_col].rolling(window=window).std()

        results['BLG_UPPER'] = ma + (std * 2)
        results['BLG_MIDDLE'] = ma
        results['BLG_LOWER'] = ma - (std * 2)

    def _calculate_macd(self, data: pd.DataFrame, results: Dict):
        """Calcula MACD."""
        close_col = 'Close'
        ema12 = data[close_col].ewm(span=12, adjust=False).mean()
        ema26 = data[close_col].ewm(span=26, adjust=False).mean()

        macd = ema12 - ema26
        signal = macd.ewm(span=9, adjust=False).mean()

        results['MACD'] = macd.iloc[-1] if len(macd) > 0 else 0
        results['MACD_SIGNAL'] = signal.iloc[-1] if len(signal) > 0 else 0

    # ==================== FLOW ANALYSIS ====================

    def calculate_flow_analysis(self, data: pd.DataFrame, active, results: Dict):
        """Calcula análisis de flujo."""
        close_col = 'Close'

        # Flujo de precio
        current = data[close_col].iloc[-1]
        prev = data[close_col].iloc[-2] if len(data) > 1 else current

        diff = current - prev
        results['FLOW_DIFF'] = diff
        results['DIRECTION'] = self.DIR_UP if diff > 0 else (self.DIR_DOWN if diff < 0 else self.DIR_WAIT)

        # Media y desviación
        changes = data[close_col].diff().dropna()
        if len(changes) > 0:
            results['MEDIA'] = changes.mean()
            results['STDDESV'] = changes.std()

    # ==================== PROBABILITIES ====================

    def calculate_probabilities(self, data: pd.DataFrame, active, results: Dict):
        """Calcula probabilidades."""
        # Calcular probabilidad de compra
        buy_prob = self._calculate_buy_probability(results)
        sell_prob = self._calculate_sell_probability(results)

        results['BUY_PROBABILITY'] = buy_prob
        results['SELL_PROBABILITY'] = sell_prob

        # Mejor dirección
        if buy_prob > 60 and buy_prob > sell_prob:
            results['BEST_DIRECTION'] = self.DIR_UP
        elif sell_prob > 60 and sell_prob > buy_prob:
            results['BEST_DIRECTION'] = self.DIR_DOWN
        else:
            results['BEST_DIRECTION'] = self.DIR_WAIT

    def _calculate_buy_probability(self, results: Dict) -> float:
        """Calcula probabilidad de compra."""
        probability = 0

        # Factor dirección
        direction = results.get('DIRECTION', self.DIR_WAIT)
        if direction == self.DIR_UP:
            probability += 30
        elif direction == 'DIR_PRE_UP':
            probability += 15

        # Factor RSI
        rsi = results.get('RSI', 50)
        if rsi < 30:
            probability += 30  # Sobreventa
        elif rsi < 40:
            probability += 15

        # Factor media
        ima1 = results.get('IMA1', 0)
        ima2 = results.get('IMA2', 0)
        if ima1 > ima2:
            probability += 20

        return min(probability, 100)

    def _calculate_sell_probability(self, results: Dict) -> float:
        """Calcula probabilidad de venta."""
        probability = 0

        # Factor dirección
        direction = results.get('DIRECTION', self.DIR_WAIT)
        if direction == self.DIR_DOWN:
            probability += 30
        elif direction == 'DIR_PRE_DOWN':
            probability += 15

        # Factor RSI
        rsi = results.get('RSI', 50)
        if rsi > 70:
            probability += 30  # Sobrecompra
        elif rsi > 60:
            probability += 15

        # Factor media
        ima1 = results.get('IMA1', 0)
        ima2 = results.get('IMA2', 0)
        if ima1 < ima2:
            probability += 20

        return min(probability, 100)

    # ==================== SIGNALS ====================

    def evaluate_signal(self, results: Dict, active) -> str:
        """
        Evalúa señal de trading.

        Returns:
            ACTION_BUY, ACTION_SELL, o ACTION_WAIT
        """
        direction = results.get('BEST_DIRECTION', self.DIR_WAIT)
        buy_prob = results.get('BUY_PROBABILITY', 0)
        sell_prob = results.get('SELL_PROBABILITY', 0)

        threshold = 60

        if buy_prob >= threshold and direction == self.DIR_UP:
            return self.ACTION_BUY
        elif sell_prob >= threshold and direction == self.DIR_DOWN:
            return self.ACTION_SELL
        else:
            return self.ACTION_WAIT

    # ==================== MIN/MAX ====================

    def calculate_min_max(self, results: Dict, data: pd.DataFrame, active) -> Dict:
        """Calcula valores mínimos y máximos."""
        close_col = 'Close'

        # Min/Max del día
        results['MIN'] = data[close_col].min()
        results['MAX'] = data[close_col].max()

        # Min/Max de la semana
        if len(data) >= 5:
            week_data = data.tail(5)
            results['MIN_WEEK'] = week_data[close_col].min()
            results['MAX_WEEK'] = week_data[close_col].max()

        return results

    # ==================== WEEK DIRECTION ====================

    def get_week_direction(self, results: Dict, data: pd.DataFrame, active,
                          start: int, end: int) -> str:
        """Determina dirección semanal."""
        close_col = 'Close'

        if len(data) < 2:
            return self.DIR_WAIT

        first = data[close_col].iloc[start]
        last = data[close_col].iloc[end]

        if last > first:
            results['WEEK_FLOW'] = 'WEEK_FLOW_UP'
            return self.DIR_UP
        elif last < first:
            results['WEEK_FLOW'] = 'WEEK_FLOW_DOWN'
            return self.DIR_DOWN
        else:
            results['WEEK_FLOW'] = 'WEEK_FLOW_UNDEF'
            return self.DIR_WAIT

    # ==================== RSI METRICS ====================

    def calculate_rsi_metrics(self, results: Dict, data: pd.DataFrame,
                             active, period: int = 14, lookback: int = 5):
        """Calcula métricas avanzadas de RSI."""
        self._calculate_rsi(data, results, period)

        rsi = results.get('RSI', 50)

        # RSI anterior
        if len(data) > lookback:
            prev_data = data.iloc[:-lookback]
            self._calculate_rsi(prev_data, results, period)
            results['RSI_PREV5'] = results.get('RSI', 50)

        # Restaurar RSI actual
        self._calculate_rsi(data, results, period)

        # Diferencia
        results['RSI_DIFF'] = rsi - results.get('RSI_PREV5', rsi)

        # RSI Slope
        results['RSI_SLOPE'] = results.get('RSI_DIFF', 0)

        return results
