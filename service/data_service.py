"""
DataService - Servicio unificado de datos.
Unifica MarketSQLManager + fetching de datos (Yahoo, DB, Alpaca).
"""

from typing import Optional, List, Dict, Any
import pandas as pd
import datetime
import logging


class DataService:
    """
    Servicio unificado para gestión de datos de mercado.

    Funcionalidades:
    - Base de datos (SQL)
    - Fetching de datos (Yahoo Finance, Alpaca)
    - Caché de datos
    """

    def __init__(self, simulation: bool = False, use_simulate_db: bool = False):
        """
        Inicializa DataService.

        Args:
            simulation: Modo simulación
            use_simulate_db: Usar base de datos simulada
        """
        self.simulation = simulation
        self.use_simulate_db = use_simulate_db
        self.log = logging.getLogger(__name__)

        # Caché de datos
        self._cache: Dict[str, pd.DataFrame] = {}
        self._cache_ttl = 300  # 5 minutos

        # Inicializar managers
        self._init_db_manager()
        self._init_market_client()

    def _init_db_manager(self):
        """Inicializa el gestor de base de datos."""
        try:
            from service.MarketSQLManager import MarketSQLManager
            self.db_manager = MarketSQLManager(self.use_simulate_db)
        except Exception as e:
            self.log.warning(f"DB Manager no disponible: {e}")
            self.db_manager = None

    def _init_market_client(self):
        """Inicializa el cliente de mercado."""
        self.market_client = None
        try:
            from service.AlpacaServiceBot import AlpacaServiceBot
            self.market_client = AlpacaServiceBot()
        except Exception as e:
            self.log.warning(f"Market client no disponible: {e}")

    # ==================== DATA FETCHING ====================

    def fetch_yahoo(self, symbol: str, period: str = "1mo", interval: str = "15m") -> Optional[pd.DataFrame]:
        """
        Obtiene datos desde Yahoo Finance.

        Args:
            symbol: Símbolo del activo
            period: Período (1d, 5d, 1mo, 3mo, 6mo, 1y, etc.)
            interval: Intervalo (1m, 5m, 15m, 1h, 1d, etc.)

        Returns:
            DataFrame con datos o None si falla
        """
        cache_key = f"yahoo_{symbol}_{period}_{interval}"

        # Verificar caché
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            import yfinance as yf
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)

            if data is not None and not data.empty:
                self._cache[cache_key] = data
                return data
        except Exception as e:
            self.log.error(f"Error fetching Yahoo {symbol}: {e}")

        return None

    def fetch_alpaca(self, symbol: str, timeframe: str = "15Min", limit: int = 100) -> Optional[pd.DataFrame]:
        """
        Obtiene datos desde Alpaca.

        Args:
            symbol: Símbolo del activo
            timeframe: Timeframe (1Min, 5Min, 15Min, 1H, 1D)
            limit: Número de barras

        Returns:
            DataFrame con datos o None si falla
        """
        if not self.market_client:
            return None

        cache_key = f"alpaca_{symbol}_{timeframe}_{limit}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            bars = self.market_client.getBars(symbol, limit)
            if bars:
                data = pd.DataFrame([{
                    'date': bar.timestamp,
                    'open': bar.open,
                    'high': bar.high,
                    'low': bar.low,
                    'close': bar.close,
                    'volume': bar.volume
                } for bar in bars])
                self._cache[cache_key] = data
                return data
        except Exception as e:
            self.log.error(f"Error fetching Alpaca {symbol}: {e}")

        return None

    def fetch_db(self, symbol: str, start: Optional[datetime.datetime] = None,
                 end: Optional[datetime.datetime] = None) -> Optional[pd.DataFrame]:
        """
        Obtiene datos desde la base de datos.

        Args:
            symbol: Símbolo del activo
            start: Fecha de inicio
            end: Fecha de fin

        Returns:
            DataFrame con datos o None si falla
        """
        if not self.db_manager:
            return None

        cache_key = f"db_{symbol}_{start}_{end}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            if start and end:
                data = self.db_manager.getAllWithNameForXdaysRangeDates(
                    symbol, start, end
                )
            else:
                data = self.db_manager.getAllWithNameForXdays(symbol)

            if data is not None and not data.empty:
                self._cache[cache_key] = data
                return data
        except Exception as e:
            self.log.error(f"Error fetching DB {symbol}: {e}")

        return None

    def fetch(self, symbol: str, source: str = "auto",
              period: str = "1mo", interval: str = "15m") -> Optional[pd.DataFrame]:
        """
        Obtiene datos automáticamente desde la mejor fuente disponible.

        Args:
            symbol: Símbolo del activo
            source: Fuente (auto, yahoo, alpaca, db)
            period: Período para Yahoo
            interval: Intervalo para Yahoo

        Returns:
            DataFrame con datos o None
        """
        if source == "auto":
            # Intentar en orden: DB, Alpaca, Yahoo
            data = self.fetch_db(symbol)
            if data is not None:
                return data

            data = self.fetch_alpaca(symbol)
            if data is not None:
                return data

            return self.fetch_yahoo(symbol, period, interval)

        elif source == "yahoo":
            return self.fetch_yahoo(symbol, period, interval)
        elif source == "alpaca":
            return self.fetch_alpaca(symbol)
        elif source == "db":
            return self.fetch_db(symbol)

        return None

    # ==================== DATABASE OPERATIONS ====================

    def save_price(self, symbol: str, price: float, timestamp: Optional[datetime.datetime] = None) -> bool:
        """Guarda un precio en la base de datos."""
        if not self.db_manager:
            return False

        try:
            self.db_manager.insertPrice(symbol, price, timestamp)
            return True
        except Exception as e:
            self.log.error(f"Error saving price {symbol}: {e}")
            return False

    def get_price_history(self, symbol: str, days: int = 30) -> Optional[pd.DataFrame]:
        """Obtiene historial de precios."""
        if not self.db_manager:
            return None

        try:
            return self.db_manager.getAllWithNameForXdays(symbol, days)
        except Exception as e:
            self.log.error(f"Error getting price history {symbol}: {e}")
            return None

    def get_latest_price(self, symbol: str) -> Optional[float]:
        """Obtiene el último precio conocido."""
        # Intentar desde caché
        cache_key = f"yahoo_{symbol}_1d_1d"
        if cache_key in self._cache:
            data = self._cache[cache_key]
            if not data.empty:
                return float(data['Close'].iloc[-1])

        # Fetch desde Yahoo
        data = self.fetch_yahoo(symbol, "1d", "1d")
        if data is not None and not data.empty:
            return float(data['Close'].iloc[-1])

        return None

    # ==================== ANALYSIS DATA ====================

    def get_ohlcv(self, symbol: str, days: int = 30) -> Optional[pd.DataFrame]:
        """
        Obtiene datos OHLCV consolidados.

        Returns:
            DataFrame con columnas: date, open, high, low, close, volume
        """
        data = self.fetch(symbol, source="auto")

        if data is None or data.empty:
            return None

        # Estandarizar columnas
        df = pd.DataFrame()

        # Mapear según disponibilidad
        col_map = {
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume',
            'Datetime': 'date',
            'date': 'date',
            'timestamp': 'date'
        }

        for old_col, new_col in col_map.items():
            if old_col in data.columns:
                df[new_col] = data[old_col]

        if 'date' not in df.columns and hasattr(data.index, 'name'):
            df['date'] = data.index

        return df

    # ==================== CACHE ====================

    def clear_cache(self, symbol: Optional[str] = None):
        """Limpia la caché."""
        if symbol:
            # Limpiar caché para símbolo específico
            keys_to_remove = [k for k in self._cache.keys() if symbol in k]
            for key in keys_to_remove:
                del self._cache[key]
        else:
            self._cache.clear()

    def get_cache_info(self) -> Dict[str, Any]:
        """Obtiene información de la caché."""
        return {
            'size': len(self._cache),
            'keys': list(self._cache.keys()),
            'ttl': self._cache_ttl
        }


# Alias para compatibilidad
DataManager = DataService
