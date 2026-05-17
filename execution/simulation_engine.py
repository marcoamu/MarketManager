"""
SimulationEngine - Motor de simulación y backtesting.
Extraído de MarketManager.py para mejorar mantenibilidad.
"""

import datetime
from typing import Dict, List, Optional, Any, Tuple


class SimulationEngine:
    """Motor de simulación y backtesting."""

    def __init__(
        self,
        data_provider=None,
        indicator_calculator=None,
        flow_analyzer=None,
        probability_engine=None
    ):
        self.data_provider = data_provider
        self.indicator_calculator = indicator_calculator
        self.flow_analyzer = flow_analyzer
        self.probability_engine = probability_engine

    def run_simulation(
        self,
        active,
        data,
        start_index: int = 1,
        end_index: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Ejecuta una simulación sobre datos históricos.

        Args:
            active: Activo a simular
            data: DataFrame con datos históricos
            start_index: Índice de inicio de simulación
            end_index: Índice de fin de simulación (None = hasta el final)

        Returns:
            Diccionario con resultados de simulación
        """
        if end_index is None:
            end_index = len(data)

        results = {
            'trades': [],
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'total_profit': 0,
            'max_drawdown': 0,
            'win_rate': 0
        }

        current_position = None
        entry_price = 0

        for i in range(start_index, end_index):
            # Obtener datos hasta el punto actual
            current_data = data.head(i)

            if len(current_data) < 2:
                continue

            # Calcular indicadores
            if self.indicator_calculator:
                indicators = self.indicator_calculator.calculate_all_indicators(current_data)
            else:
                indicators = {}

            # Analizar flujo
            if self.flow_analyzer:
                flow = self.flow_analyzer.get_flow_diff(current_data)
            else:
                flow = 0

            # Evaluar señal
            signal = self._evaluate_signal(indicators, flow)

            # Ejecutar lógica de trading
            if current_position is None:
                # Sin posición, evaluar entrada
                if signal == 'BUY':
                    current_position = 'LONG'
                    entry_price = current_data['close'].iloc[-1]
            else:
                # Con posición, evaluar salida
                current_price = current_data['close'].iloc[-1]

                if signal == 'SELL' or signal == 'CLOSE':
                    # Cerrar posición
                    pnl = current_price - entry_price
                    results['trades'].append({
                        'entry_price': entry_price,
                        'exit_price': current_price,
                        'pnl': pnl,
                        'pnl_pct': (pnl / entry_price) * 100
                    })

                    if pnl > 0:
                        results['winning_trades'] += 1
                    else:
                        results['losing_trades'] += 1

                    results['total_profit'] += pnl
                    current_position = None

        # Calcular estadísticas finales
        results['total_trades'] = len(results['trades'])
        if results['total_trades'] > 0:
            results['win_rate'] = (results['winning_trades'] / results['total_trades']) * 100

        return results

    def _evaluate_signal(
        self,
        indicators: Dict,
        flow: float
    ) -> str:
        """Evalúa señal de trading."""
        # Señal simple basada en momentum
        if self.probability_engine:
            return self.probability_engine.evaluate_signal(indicators, None)
        return 'WAIT'

    def simulate_date_range(
        self,
        active,
        start_date: datetime.datetime,
        end_date: datetime.datetime
    ) -> Dict[str, Any]:
        """
        Simula para un rango de fechas específico.

        Args:
            active: Activo a simular
            start_date: Fecha de inicio
            end_date: Fecha de fin

        Returns:
            Resultados de simulación
        """
        if not self.data_provider:
            return {'error': 'Data provider no disponible'}

        # Obtener datos
        data = self.data_provider.get_historical_data(
            active.parameters.name,
            start=start_date,
            end=end_date,
            use_range_dates=True
        )

        if data is None or len(data) == 0:
            return {'error': 'Sin datos disponibles'}

        return self.run_simulation(active, data)

    def calculate_metrics(
        self,
        trades: List[Dict]
    ) -> Dict[str, float]:
        """
        Calcula métricas de rendimiento.

        Args:
            trades: Lista de trades ejecutados

        Returns:
            Diccionario con métricas
        """
        if not trades:
            return {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0,
                'avg_profit': 0,
                'avg_loss': 0,
                'profit_factor': 0,
                'max_drawdown': 0
            }

        winning_trades = [t for t in trades if t['pnl'] > 0]
        losing_trades = [t for t in trades if t['pnl'] < 0]

        total_wins = len(winning_trades)
        total_losses = len(losing_trades)

        avg_profit = sum(t['pnl'] for t in winning_trades) / total_wins if total_wins > 0 else 0
        avg_loss = sum(t['pnl'] for t in losing_trades) / total_losses if total_losses > 0 else 0

        total_profit = sum(t['pnl'] for t in winning_trades)
        total_loss = abs(sum(t['pnl'] for t in losing_trades))

        profit_factor = total_profit / total_loss if total_loss > 0 else 0

        # Calcular drawdown máximo
        cumulative = 0
        max_dd = 0
        peak = 0

        for trade in trades:
            cumulative += trade['pnl']
            if cumulative > peak:
                peak = cumulative
            dd = peak - cumulative
            if dd > max_dd:
                max_dd = dd

        return {
            'total_trades': len(trades),
            'winning_trades': total_wins,
            'losing_trades': total_losses,
            'win_rate': (total_wins / len(trades)) * 100 if trades else 0,
            'avg_profit': avg_profit,
            'avg_loss': avg_loss,
            'profit_factor': profit_factor,
            'max_drawdown': max_dd,
            'total_profit': sum(t['pnl'] for t in trades)
        }

    def optimize_parameters(
        self,
        active,
        data,
        param_ranges: Dict[str, List]
    ) -> Dict[str, Any]:
        """
        Optimiza parámetros de estrategia.

        Args:
            active: Activo a simular
            data: Datos históricos
            param_ranges: Diccionario con rangos de parámetros

        Returns:
            Mejores parámetros encontrados
        """
        # Implementación básica de optimización
        # En una versión completa, usaría grid search o similar

        best_params = {}
        best_result = None

        # Por ahora, retornar parámetros por defecto
        return {
            'params': best_params,
            'result': best_result,
            'message': 'Optimización no implementada completamente'
        }

    def run_walk_forward(
        self,
        active,
        data,
        train_size: int = 100,
        test_size: int = 20,
        step: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Ejecuta walk-forward analysis.

        Args:
            active: Activo a simular
            data: Datos históricos
            train_size: Tamaño del conjunto de entrenamiento
            test_size: Tamaño del conjunto de prueba
            step: Paso entre simulaciones

        Returns:
            Lista de resultados por cada iteración
        """
        results = []
        total_length = len(data)

        for i in range(0, total_length - train_size - test_size, step):
            train_end = i + train_size
            test_end = train_end + test_size

            train_data = data.iloc[i:train_end]
            test_data = data.iloc[train_end:test_end]

            # Simular en conjunto de prueba
            test_result = self.run_simulation(active, test_data, start_index=1)

            # Calcular métricas
            metrics = self.calculate_metrics(test_result['trades'])

            results.append({
                'train_start': i,
                'train_end': train_end,
                'test_start': train_end,
                'test_end': test_end,
                'metrics': metrics
            })

        return results
