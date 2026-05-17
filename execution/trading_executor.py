"""
TradingExecutor - Ejecución de operaciones de trading.
Extraído de MarketManager.py para mejorar mantenibilidad.
"""

from typing import Dict, Optional, Any, Tuple


class TradingExecutor:
    """Ejecutor de operaciones de trading."""

    # Constantes de acción
    ACTION_BUY = 'BUY'
    ACTION_SELL = 'SELL'
    ACTION_WAIT = 'WAIT'
    ACTION_CLOSE = 'CLOSE'

    def __init__(
        self,
        alpaca_service=None,
        telegram_service=None,
        simulation: bool = False
    ):
        self.alpaca = alpaca_service
        self.telegram = telegram_service
        self.simulation = simulation

    def execute_signal(
        self,
        symbol: str,
        action: str,
        amount_usd: Optional[float] = None,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None
    ) -> Tuple[bool, str]:
        """
        Ejecuta una señal de trading.

        Args:
            symbol: Símbolo del activo
            action: Acción a ejecutar (BUY, SELL, CLOSE)
            amount_usd: Cantidad en USD
            stop_loss: Stop loss opcional
            take_profit: Take profit opcional

        Returns:
            Tupla (éxito, mensaje)
        """
        if self.simulation:
            return self._simulate_execution(symbol, action, amount_usd)

        try:
            if action == self.ACTION_BUY:
                return self._execute_buy(symbol, amount_usd, stop_loss)
            elif action == self.ACTION_SELL:
                return self._execute_sell(symbol, amount_usd, stop_loss)
            elif action == self.ACTION_CLOSE:
                return self._execute_close(symbol)
            else:
                return False, "Acción no válida"

        except Exception as e:
            error_msg = f"Error ejecutando {action} en {symbol}: {str(e)}"
            print(error_msg)
            return False, error_msg

    def _execute_buy(
        self,
        symbol: str,
        amount_usd: Optional[float],
        stop_loss: Optional[float]
    ) -> Tuple[bool, str]:
        """Ejecuta orden de compra."""
        try:
            if self.alpaca:
                # Usar método existente de Alpaca
                if stop_loss:
                    result = self.alpaca.buy_with_money_stop(
                        symbol,
                        amount_usd or 100,  # Default
                        stop_loss
                    )
                else:
                    # Orden simple
                    result = self.alpaca.execute_target_position(
                        symbol,
                        'buy',
                        amount_usd or 100
                    )
                return True, f"Compra ejecutada: {symbol}"
            return False, "Servicio Alpaca no disponible"
        except Exception as e:
            return False, f"Error en compra: {str(e)}"

    def _execute_sell(
        self,
        symbol: str,
        amount_usd: Optional[float],
        stop_loss: Optional[float]
    ) -> Tuple[bool, str]:
        """Ejecuta orden de venta."""
        try:
            if self.alpaca:
                result = self.alpaca.execute_target_position(
                    symbol,
                    'sell',
                    amount_usd or 100
                )
                return True, f"Venta ejecutada: {symbol}"
            return False, "Servicio Alpaca no disponible"
        except Exception as e:
            return False, f"Error en venta: {str(e)}"

    def _execute_close(self, symbol: str) -> Tuple[bool, str]:
        """Cierra posición existente."""
        try:
            if self.alpaca:
                # Verificar si hay posición abierta
                invested, revenue = self.alpaca.is_invested(symbol)
                if invested:
                    # Cerrar posición
                    self.alpaca.execute_target_position(symbol, 'sell', 0)
                    return True, f"Posición cerrada: {symbol}"
                return True, f"No había posición abierta en {symbol}"
            return False, "Servicio Alpaca no disponible"
        except Exception as e:
            return False, f"Error al cerrar posición: {str(e)}"

    def _simulate_execution(
        self,
        symbol: str,
        action: str,
        amount_usd: Optional[float]
    ) -> Tuple[bool, str]:
        """Simula ejecución (para backtesting)."""
        return True, f"[SIMULACIÓN] {action} {amount_usd or 100} USD de {symbol}"

    def close_and_open(
        self,
        symbol: str,
        new_action: str,
        amount_usd: Optional[float] = None
    ) -> Tuple[bool, str]:
        """
        Cierra posición existente y abre nueva en una operación.

        Args:
            symbol: Símbolo del activo
            new_action: Nueva acción (BUY o SELL)
            amount_usd: Cantidad en USD

        Returns:
            Tupla (éxito, mensaje)
        """
        try:
            # Cerrar posición actual
            close_success, close_msg = self._execute_close(symbol)

            if not close_success and "No había posición" not in close_msg:
                return False, f"Error cerrando posición: {close_msg}"

            # Abrir nueva posición
            if new_action in [self.ACTION_BUY, self.ACTION_SELL]:
                return self.execute_signal(symbol, new_action, amount_usd)

            return True, "Posición cerrada correctamente"

        except Exception as e:
            error_msg = f"Error en close_and_open: {str(e)}"
            print(error_msg)
            return False, error_msg

    def apply_stop_loss(
        self,
        symbol: str,
        max_loss_usd: float,
        protect_profit_usd: Optional[float] = None
    ) -> Tuple[bool, str]:
        """
        Aplica stop loss inteligente.

        Args:
            symbol: Símbolo del activo
            max_loss_usd: Pérdida máxima en USD
            protect_profit_usd: Protegel profit si está en ganancias

        Returns:
            Tupla (éxito, mensaje)
        """
        try:
            if self.alpaca:
                # Usar método de stop loss inteligente
                result = self.alpaca.add_smart_stop_usd_stock(
                    symbol,
                    max_loss_usd=max_loss_usd,
                    protect_profit_usd=protect_profit_usd
                )
                return True, f"Stop loss aplicado: {symbol}"
            return False, "Servicio Alpaca no disponible"
        except Exception as e:
            return False, f"Error aplicando stop loss: {str(e)}"

    def check_position(self, symbol: str) -> Dict[str, Any]:
        """
        Verifica el estado de una posición.

        Returns:
            Diccionario con estado de la posición
        """
        result = {
            'invested': False,
            'revenue': 0,
            'open_price': 0,
            'quantity': 0
        }

        try:
            if self.alpaca:
                invested, revenue, open_price, quantity = self.alpaca.is_invested_complete(symbol)
                result = {
                    'invested': invested,
                    'revenue': revenue,
                    'open_price': open_price,
                    'quantity': quantity
                }
        except Exception:
            pass

        return result

    def get_closed_pnl(
        self,
        symbol: str,
        entry_price: float,
        quantity: float
    ) -> Tuple[float, float]:
        """
        Obtiene el PnL de una posición cerrada.

        Returns:
            Tupla (pnl, precio_cierre)
        """
        try:
            if self.alpaca:
                return self.alpaca.get_closed_pnl(symbol, entry_price, quantity)
        except Exception:
            pass
        return 0, 0

    def send_notification(
        self,
        message: str,
        chat_id: Optional[int] = None
    ) -> bool:
        """
        Envía notificación por Telegram.

        Args:
            message: Mensaje a enviar
            chat_id: ID del chat (opcional)

        Returns:
            True si se envió correctamente
        """
        if self.telegram:
            try:
                self.telegram.enviarMensaje(
                    message,
                    self.telegram.tokenBot,
                    chat_id
                )
                return True
            except Exception as e:
                print(f"Error enviando notificación: {e}")
        return False
