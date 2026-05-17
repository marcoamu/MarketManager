"""
DataProvider - Obtención de datos de mercado.
Extraído de MarketManager.py para mejorar mantenibilidad.
"""

import datetime
import time
from typing import Optional, List, Dict, Any


class DataProvider:
    """Proveedor de datos de mercado desde múltiples fuentes."""

    def __init__(self, alpaca_service=None, db_manager=None, is_db_data: bool = False):
        self.alpaca = alpaca_service
        self.db_manager = db_manager
        self.is_db_data = is_db_data
        self.closeValue = 'Close' if not is_db_data else 'value'

    def get_current_price(self, symbol: str) -> tuple:
        """Obtiene el precio actual y del día."""
        if self.alpaca:
            return self.alpaca.getCurrentPrice(symbol)
        return None, None

    def is_market_open(self) -> bool:
        """Verifica si el mercado está abierto."""
        if self.alpaca:
            return self.alpaca.ismarketOpen()
        return False

    def is_invested(self, symbol: str, second_name: Optional[str] = None) -> tuple:
        """Verifica si hay posición abierta."""
        if self.alpaca:
            if second_name:
                return self.alpaca.is_invested(second_name)
            return self.alpaca.is_invested(symbol)
        return False, 0

    def is_invested_complete(self, symbol: str) -> tuple:
        """Verifica posición completa (invertido, profit, precio apertura, cantidad)."""
        if self.alpaca:
            return self.alpaca.is_investedComplete(symbol)
        return 0, 0, 0, 0

    def get_closed_pnl(self, symbol: str, entry_price: float, qty: float) -> tuple:
        """Obtiene PnL de posición cerrada."""
        if self.alpaca:
            return self.alpaca.get_closed_pnl(symbol, entry_price, qty)
        return 0, 0

    def get_historical_data(
        self,
        symbol: str,
        days: int = 4,
        start: Optional[datetime.datetime] = None,
        end: Optional[datetime.datetime] = None,
        use_range_dates: bool = False
    ):
        """Obtiene datos históricos desde la base de datos."""
        if not self.db_manager:
            return None

        if use_range_dates and start and end:
            return self.db_manager.getAllWithNameForXdaysRangeDates(symbol, start, end)
        elif use_range_dates and start and end:
            return self.db_manager.getAllWithNameForXdaysRangeDatesExactdays(symbol, start, end)
        else:
            return self.db_manager.getAllWithNameForXdays(symbol, days)

    def get_last_value(self, symbol: str) -> Optional[float]:
        """Obtiene el último valor del símbolo."""
        if self.db_manager:
            return self.db_manager.getLastValueWithName(symbol)
        return None

    def insert_value(
        self,
        symbol: str,
        current_value: float,
        old_value: float,
        dif: float,
        acumulate: float,
        tendence_acu: float,
        tendence_count: int,
        direction: str,
        min_dir: float,
        max_dir: float,
        indi_dir: str,
        motion_min: float,
        motion_max: float,
        global_min: float,
        global_max: float,
        action_acum: float,
        action_count: int,
        week_flow: str,
        week_flow_med: float,
        week_flow_std: float,
        week_min_dir: float,
        week_max_dir: float,
        rel_fcst: str,
        rel_fcst_std: float,
        rel_fcst_med: float,
        rel_fcst_min: float,
        rel_fcst_max: float,
        rel_fcst_percent: float,
        close_nxt_up: float,
        close_nxt_down: float,
        close_nxt_middle: float,
    ):
        """Inserta un nuevo valor en la base de datos."""
        if self.db_manager:
            self.db_manager.inserValue(
                symbol, current_value, old_value, dif, acumulate, tendence_acu,
                tendence_count, direction, min_dir, max_dir, indi_dir,
                motion_min, motion_max, global_min, global_max,
                action_acum, action_count, week_flow, week_flow_med,
                week_flow_std, week_min_dir, week_max_dir, rel_fcst,
                rel_fcst_std, rel_fcst_med, rel_fcst_min, rel_fcst_max,
                rel_fcst_percent, close_nxt_up, close_nxt_down, close_nxt_middle
            )

    def get_minmax_3days(self, symbol: str, current_date: datetime.datetime):
        """Obtiene valores min/max para 3 días."""
        if self.db_manager:
            return self.db_manager.getMinMaxFor3days(symbol, current_date)
        return None

    def get_actives_for_interval(self, interval: int) -> List:
        """Obtiene activos para un intervalo específico."""
        if self.db_manager:
            return self.db_manager.getActivesforInterval(interval)
        return []

    def get_all_actives_control_time(self) -> List[Dict]:
        """Obtiene todos los activos con control de tiempo."""
        if self.db_manager:
            return self.db_manager.getALLActivesControlTime()
        return []

    def update_interval_for_active(
        self, symbol: str, interval: int, counter: int
    ):
        """Actualiza el intervalo para un activo."""
        if self.db_manager:
            self.db_manager.updateIntervalForActive(symbol, interval, counter)

    def get_current_revenues(self) -> Dict:
        """Obtiene los ingresos/revenues actuales."""
        if self.db_manager:
            return self.db_manager.getCurrentRevenues()
        return {}

    def get_resume_for_range_dates(
        self, start: datetime.datetime, end: datetime.datetime
    ):
        """Obtiene resumen para un rango de fechas."""
        if self.db_manager:
            return self.db_manager.getResumeForRangeDatesExact(start, end)
        return None

    def update_value_with_data(self, results: Dict):
        """Actualiza valor con datos de resultados."""
        if self.db_manager:
            self.db_manager.updateValueWithData(results)

    def update_simulation_values(self, results: Dict):
        """Actualiza valores de simulación."""
        if self.db_manager:
            self.db_manager.updateSimulationValues(results)

    def get_predict_for_active(self, symbol: str) -> str:
        """Obtiene predicción para un activo."""
        if self.db_manager:
            return self.db_manager.getPredictForActive(symbol)
        return '0'

    def update_predict_for_active(
        self, symbol: str, up_value: str, down_value: str
    ):
        """Actualiza predicción para un activo."""
        if self.db_manager:
            self.db_manager.updatePredictForActive(symbol, up_value, down_value)
