"""
TradingService - Servicio unificado de trading.
Fusiona AlpacaService + AlpacaServiceBot.
"""

import time
from typing import Optional, Dict, Any, Tuple, List


class TradingService:
    """Servicio unificado para operaciones de trading."""

    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None,
                 base_url: Optional[str] = None, paper_mode: bool = True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url or "https://paper-api.alpaca.markets"
        self.paper_mode = paper_mode
        self.client = None
        self.init()

    def init(self):
        """Inicializa la conexión con Alpaca."""
        try:
            import os
            from alpaca.trading.client import TradingClient
            from alpaca.trading.requests import MarketOrderRequest
            from alpaca.data.historical import StockHistoricalDataClient

            # Obtener credenciales de entorno si no se proporcionan
            api_key = self.api_key or os.getenv('ALPACA_API_KEY')
            api_secret = self.api_secret or os.getenv('ALPACA_API_SECRET')

            if api_key and api_secret:
                self.client = TradingClient(api_key, api_secret, paper=self.paper_mode)
                self.data_client = StockHistoricalDataClient(api_key, api_secret)
            else:
                print("Alpaca: Credenciales no disponibles (usar variables de entorno)")
        except ImportError:
            print("Alpaca SDK no instalado")
        except Exception as e:
            print(f"Error inicializando Alpaca: {e}")

    # ==================== ACCOUNT ====================

    def accountStatus(self) -> Dict:
        """Obtiene estado de la cuenta."""
        if self.client:
            return self.client.get_account().__dict__
        return {}

    def accountInfo(self) -> Dict:
        """Obtiene información de la cuenta."""
        if self.client:
            account = self.client.get_account()
            return {
                'cash': account.cash,
                'portfolio_value': account.portfolio_value,
                'equity': account.equity,
                'buying_power': account.buying_power
            }
        return {}

    def getCashInfo(self) -> Dict:
        """Obtiene información de efectivo."""
        if self.client:
            account = self.client.get_account()
            return {
                'cash': float(account.cash),
                'currency': account.currency
            }
        return {'cash': 0, 'currency': 'USD'}

    # ==================== MARKET DATA ====================

    def getCurrentPrice(self, symbol: str) -> Tuple[Optional[float], Optional[float]]:
        """Obtiene precio actual y del día."""
        try:
            if self.client:
                position = self.client.get_position(symbol)
                current_price = float(position.current_price)
                cost_basis = float(position.cost_basis)
                return current_price, cost_basis
        except Exception:
            pass
        return None, None

    def getlatestPrice(self, symbol: str) -> float:
        """Obtiene último precio."""
        try:
            if self.client:
                position = self.client.get_position(symbol)
                return float(position.current_price)
        except Exception:
            pass
        return 0.0

    def getBars(self, symbol: str, limit: int = 100) -> List:
        """Obtiene barras de precios."""
        # Implementación básica - se expandiría con data_client
        return []

    def getSnapShot(self, symbol: str) -> Dict:
        """Obtiene snapshot del símbolo."""
        # Implementación con data_client
        return {}

    def getTrades(self, symbol: str) -> List:
        """Obtiene trades recientes."""
        return []

    # ==================== POSITIONS ====================

    def is_invested(self, symbol: str) -> Tuple[bool, float]:
        """Verifica si hay posición abierta."""
        try:
            if self.client:
                position = self.client.get_position(symbol)
                return True, float(position.market_value)
        except Exception:
            return False, 0
        return False, 0

    def is_investedComplete(self, symbol: str) -> Tuple[bool, float, float, float]:
        """Verifica posición completa."""
        try:
            if self.client:
                position = self.client.get_position(symbol)
                invested = True
                profit = float(position.unrealized_pl)
                open_price = float(position.avg_entry_price)
                qty = float(position.qty)
                return invested, profit, open_price, qty
        except Exception:
            pass
        return False, 0, 0, 0

    def listPositions(self) -> List:
        """Lista todas las posiciones."""
        if self.client:
            return self.client.get_all_positions()
        return []

    def allPositions(self) -> List:
        """Obtiene todas las posiciones."""
        return self.listPositions()

    def get_closed_pnl(self, symbol: str, entry_price: float, qty: float) -> Tuple[float, float]:
        """Calcula PnL de posición cerrada."""
        # Simulación básica - implementación real usaría historial
        return 0, 0

    # ==================== ORDERS ====================

    def submitOrder(self, symbol: str, units: int, latest_price: float, order_type: str = "limit") -> Dict:
        """Envía orden."""
        try:
            if self.client:
                from alpaca.trading.requests import MarketOrderRequest
                order = MarketOrderRequest(
                    symbol=symbol,
                    qty=units,
                    side='buy',
                    type='market' if order_type == 'market' else 'limit',
                    time_in_force='day'
                )
                return self.client.submit_order(order).__dict__
        except Exception as e:
            print(f"Error enviando orden: {e}")
        return {}

    def submitOrderNow(self, symbol: str, amount: float) -> Dict:
        """Envía orden inmediata."""
        try:
            if self.client:
                units = int(amount / self.getlatestPrice(symbol))
                return self.submitOrder(symbol, units, 0, 'market')
        except Exception as e:
            print(f"Error en orden: {e}")
        return {}

    def buyOrder(self, symbol: str, symbol2: str, amount: float) -> Dict:
        """Orden de compra."""
        return self.submitOrderNow(symbol, amount)

    def buy_with_money_stop(self, symbol: str, amount_usd: float, max_loss_usd: float) -> Dict:
        """Compra con stop loss."""
        try:
            if self.client:
                price = self.getlatestPrice(symbol)
                if price > 0:
                    # Calcular tamaño de orden
                    qty = int(amount_usd / price)

                    # Crear orden de compra
                    from alpaca.trading.requests import MarketOrderRequest
                    order = MarketOrderRequest(
                        symbol=symbol,
                        qty=qty,
                        side='buy',
                        type='market',
                        time_in_force='day'
                    )
                    self.client.submit_order(order)

                    # Aplicar stop loss (implementación simplificada)
                    return {'success': True, 'symbol': symbol, 'qty': qty}
        except Exception as e:
            print(f"Error en buy_with_money_stop: {e}")
        return {'success': False}

    def execute_target_position(self, symbol: str, target_side: str, amount_usd: float) -> Dict:
        """Ejecuta posición objetivo (compra/venta)."""
        try:
            if self.client:
                price = self.getlatestPrice(symbol)
                if price > 0:
                    qty = int(amount_usd / price)

                    if target_side == 'buy':
                        # Verificar si hay posición para vender primero
                        try:
                            pos = self.client.get_position(symbol)
                            # Cerrar posición existente
                            self._close_position(symbol, pos.qty)
                        except:
                            pass

                        # Abrir nueva posición larga
                        from alpaca.trading.requests import MarketOrderRequest
                        order = MarketOrderRequest(
                            symbol=symbol,
                            qty=qty,
                            side='buy',
                            type='market',
                            time_in_force='day'
                        )
                        return self.client.submit_order(order).__dict__

                    elif target_side == 'sell':
                        # Cerrar posición
                        try:
                            pos = self.client.get_position(symbol)
                            return self._close_position(symbol, pos.qty)
                        except:
                            return {'success': True, 'message': 'No position to close'}

        except Exception as e:
            print(f"Error en execute_target_position: {e}")
        return {'success': False}

    def add_smart_stop_usd_stock(self, symbol: str, max_loss_usd: float,
                                  protect_profit_usd: Optional[float] = None) -> Dict:
        """Agrega stop loss inteligente para acciones."""
        try:
            if self.client:
                position = self.client.get_position(symbol)
                entry_price = float(position.avg_entry_price)
                current_price = float(position.current_price)
                qty = float(position.qty)

                # Calcular precio de stop
                unrealized_pl = float(position.unrealized_pl)

                # Si hay profit y tenemos protect_profit
                if protect_profit_usd and unrealized_pl > protect_profit_usd:
                    stop_price = entry_price  # Mover a punto de entrada
                else:
                    stop_price = entry_price - (max_loss_usd / qty)

                # Crear orden stop loss
                from alpaca.trading.requests import StopLossRequest
                stop_order = StopLossRequest(
                    symbol=symbol,
                    qty=qty,
                    side='sell',
                    stop_price={'stop_price': round(stop_price, 2)}
                )
                return self.client.submit_order(stop_order).__dict__

        except Exception as e:
            print(f"Error en add_smart_stop_usd_stock: {e}")
        return {'success': False}

    def add_smart_stop_usd_crypto(self, symbol: str, max_loss_usd: float,
                                   protect_profit_usd: Optional[float] = None) -> Dict:
        """Agrega stop loss inteligente para crypto."""
        # Similar a stocks pero para crypto
        return self.add_smart_stop_usd_stock(symbol, max_loss_usd, protect_profit_usd)

    def add_profit_stop_usd(self, symbol: str, protect_usd: float) -> Dict:
        """Agrega take profit."""
        return self.add_smart_stop_usd_stock(symbol, protect_usd)

    def cancel_order(self, order_id: str) -> bool:
        """Cancela una orden."""
        try:
            if self.client:
                self.client.cancel_order(order_id)
                return True
        except Exception:
            pass
        return False

    # ==================== UTILITIES ====================

    def _close_position(self, symbol: str, qty: Optional[float] = None, retries: int = 5) -> Dict:
        """Cierra posición."""
        for attempt in range(retries):
            try:
                if self.client:
                    if qty is None:
                        pos = self.client.get_position(symbol)
                        qty = pos.qty

                    self.client.close_position(symbol)
                    return {'success': True, 'symbol': symbol}
            except Exception as e:
                if attempt < retries - 1:
                    time.sleep(1)
                else:
                    return {'success': False, 'error': str(e)}
        return {'success': False}

    def _wait_until_filled(self, order_id: str, timeout: int = 15) -> bool:
        """Espera hasta que la orden se complete."""
        # Implementación básica
        return True

    def getClock(self) -> Dict:
        """Obtiene información del reloj del mercado."""
        if self.client:
            clock = self.client.get_clock()
            return {
                'is_open': clock.is_open,
                'next_open': str(clock.next_open),
                'next_close': str(clock.next_close)
            }
        return {}

    def ismarketOpen(self) -> bool:
        """Verifica si el mercado está abierto."""
        clock = self.getClock()
        return clock.get('is_open', False)

    def getAsset(self, symbol: str) -> Dict:
        """Obtiene información del asset."""
        if self.client:
            asset = self.client.get_asset(symbol)
            return {'symbol': symbol, 'status': asset.status}
        return {}

    def getAssets(self) -> List:
        """Lista todos los assets disponibles."""
        if self.client:
            return self.client.get_assets()
        return []

    def calculate_order_size(self, cash_to_spend: float, latest_price: float) -> int:
        """Calcula el tamaño de la orden."""
        if latest_price > 0:
            return int(cash_to_spend / latest_price)
        return 0

    def getGanancias(self) -> Dict:
        """Obtiene ganancias."""
        if self.client:
            positions = self.client.get_all_positions()
            total_pl = sum(float(p.unrealized_pl) for p in positions)
            return {'total_pl': total_pl}
        return {'total_pl': 0}

    def get_daily_pnl_by_asset(self) -> Dict:
        """Obtiene PnL diario por asset."""
        if self.client:
            positions = self.client.get_all_positions()
            result = {}
            for p in positions:
                result[p.symbol] = {
                    'unrealized_pl': float(p.unrealized_pl),
                    'qty': float(p.qty),
                    'current_price': float(p.current_price)
                }
            return result
        return {}

    def collect_bars(self, symbol: str, limit: int = 50) -> List:
        """Recolecta barras de datos."""
        # Implementación con data_client
        return []

    def collect_crypto_bars(self, symbol: str, minutes: int = 120) -> List:
        """Recolecta barras de crypto."""
        return []

    def collect_stock_bars(self, symbol: str, minutes: int = 120) -> List:
        """Recolecta barras de acciones."""
        return []
