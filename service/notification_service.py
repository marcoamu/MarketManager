"""
NotificationService - Servicio unificado de notificaciones.
Unifica TelegramService + NewsFeed.
"""

from typing import Optional, List, Dict, Any
import logging
import datetime


class NotificationService:
    """
    Servicio unificado para notificaciones.

    Funcionalidades:
    - Telegram (mensajes, documentos, alertas)
    - NewsFeed (noticias)
    - Notificaciones push
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializa NotificationService.

        Args:
            config: Configuración opcional
        """
        self.config = config or {}
        self.log = logging.getLogger(__name__)

        # Inicializar servicios
        self._init_telegram()
        self._init_newsfeed()

    def _init_telegram(self):
        """Inicializa el servicio de Telegram."""
        try:
            from service.TelegramService import TelegramService
            self.telegram = TelegramService()
            self._telegram_available = True
        except Exception as e:
            self.log.warning(f"Telegram no disponible: {e}")
            self.telegram = None
            self._telegram_available = False

    def _init_newsfeed(self):
        """Inicializa el servicio de noticias."""
        try:
            from service.NewsFeed import NewsFeed
            self.newsfeed = NewsFeed()
            self._newsfeed_available = True
        except Exception as e:
            self.log.warning(f"NewsFeed no disponible: {e}")
            self.newsfeed = None
            self._newsfeed_available = False

    # ==================== TELEGRAM ====================

    def send_message(self, message: str, chat_id: Optional[int] = None) -> bool:
        """
        Envía un mensaje por Telegram.

        Args:
            message: Texto del mensaje
            chat_id: ID del chat (opcional)

        Returns:
            True si se envió correctamente
        """
        if not self._telegram_available or not self.telegram:
            self.log.warning("Telegram no disponible")
            return False

        try:
            chat_id = chat_id or self.config.get('default_chat_id')
            self.telegram.enviarMensaje(message, chat_id)
            return True
        except Exception as e:
            self.log.error(f"Error enviando mensaje: {e}")
            return False

    def send_alert(self, symbol: str, action: str, price: float,
                   chat_id: Optional[int] = None) -> bool:
        """
        Envía una alerta de trading.

        Args:
            symbol: Símbolo del activo
            action: Acción (BUY, SELL, etc.)
            price: Precio actual
            chat_id: ID del chat

        Returns:
            True si se envió correctamente
        """
        emoji = "🟢" if action == "BUY" else "🔴" if action == "SELL" else "⚪"
        message = f"{emoji} {action} {symbol} @ ${price:.2f}"
        return self.send_message(message, chat_id)

    def send_document(self, file_path: str, caption: Optional[str] = None,
                      chat_id: Optional[int] = None) -> bool:
        """
        Envía un documento por Telegram.

        Args:
            file_path: Ruta del archivo
            caption: Caption opcional
            chat_id: ID del chat

        Returns:
            True si se envió correctamente
        """
        if not self._telegram_available or not self.telegram:
            return False

        try:
            chat_id = chat_id or self.config.get('default_chat_id')
            self.telegram.enviarDocumento(file_path, chat_id, caption)
            return True
        except Exception as e:
            self.log.error(f"Error enviando documento: {e}")
            return False

    def send_chart(self, symbol: str, data, chat_id: Optional[int] = None) -> bool:
        """
        Envía un gráfico por Telegram.

        Args:
            symbol: Símbolo del activo
            data: Datos del gráfico
            chat_id: ID del chat

        Returns:
            True si se envió correctamente
        """
        # Esta función requeriría implementación de plotting
        # Por ahora delegamos a send_document
        message = f"📊 Chart for {symbol}"
        return self.send_message(message, chat_id)

    # ==================== NEWSFEED ====================

    def get_news(self, symbol: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Obtiene noticias financieras.

        Args:
            symbol: Símbolo opcional para filtrar
            limit: Número máximo de noticias

        Returns:
            Lista de noticias
        """
        if not self._newsfeed_available or not self.newsfeed:
            return []

        try:
            if symbol:
                return self.newsfeed.get_news_for_symbol(symbol, limit)
            else:
                return self.newsfeed.get_latest_news(limit)
        except Exception as e:
            self.log.error(f"Error obteniendo noticias: {e}")
            return []

    def get_market_news(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Obtiene noticias del mercado."""
        return self.get_news(limit=limit)

    def get_crypto_news(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Obtiene noticias de criptomonedas."""
        # Filtrar noticias relacionadas con crypto
        news = self.get_news(limit=limit * 2)
        crypto_keywords = ['BTC', 'ETH', 'crypto', 'bitcoin', 'ethereum']

        return [
            n for n in news
            if any(kw.lower() in n.get('title', '').lower() for kw in crypto_keywords)
        ][:limit]

    # ==================== COMBINED NOTIFICATIONS ====================

    def notify_trade(self, symbol: str, action: str, price: float,
                     quantity: float, pnl: Optional[float] = None,
                     chat_id: Optional[int] = None) -> bool:
        """
        Envía notificación de operación ejecutada.

        Args:
            symbol: Símbolo
            action: Acción (BUY/SELL)
            price: Precio
            quantity: Cantidad
            pnl: Profit/Loss (opcional)
            chat_id: Chat ID

        Returns:
            True si se envió
        """
        emoji = "✅" if action.upper() == "BUY" else "❌"
        message = f"{emoji} {action} {symbol}\n"
        message += f"💰 Price: ${price:.2f}\n"
        message += f"📊 Qty: {quantity}\n"

        if pnl is not None:
            pnl_emoji = "📈" if pnl >= 0 else "📉"
            message += f"{pnl_emoji} PnL: ${pnl:.2f}"

        return self.send_message(message, chat_id)

    def notify_signal(self, symbol: str, signal_type: str, probability: float,
                      indicators: Dict[str, Any],
                      chat_id: Optional[int] = None) -> bool:
        """
        Envía notificación de señal de trading.

        Args:
            symbol: Símbolo
            signal_type: Tipo de señal
            probability: Probabilidad
            indicators: Indicadores relevantes
            chat_id: Chat ID

        Returns:
            True si se envió
        """
        emoji = "🟢" if signal_type == "BUY" else "🔴" if signal_type == "SELL" else "⚪"

        message = f"🎯 Signal: {emoji} {signal_type} {symbol}\n"
        message += f"📊 Probability: {probability:.1f}%\n"
        message += "📈 Indicators:\n"

        for key, value in indicators.items():
            if isinstance(value, float):
                message += f"  - {key}: {value:.2f}\n"
            else:
                message += f"  - {key}: {value}\n"

        return self.send_message(message, chat_id)

    def notify_summary(self, results: Dict[str, Any],
                       chat_id: Optional[int] = None) -> bool:
        """
        Envía resumen diario de operaciones.

        Args:
            results: Diccionario con resultados
            chat_id: Chat ID

        Returns:
            True si se envió
        """
        total = results.get('total_trades', 0)
        wins = results.get('winning_trades', 0)
        losses = results.get('losing_trades', 0)
        pnl = results.get('total_pnl', 0)

        win_rate = (wins / total * 100) if total > 0 else 0

        message = "📊 Daily Summary\n"
        message += f"━━━━━━━━━━━━━━━━\n"
        message += f"Total Trades: {total}\n"
        message += f"✅ Wins: {wins}\n"
        message += f"❌ Losses: {losses}\n"
        message += f"📈 Win Rate: {win_rate:.1f}%\n"
        message += f"💰 PnL: ${pnl:.2f}"

        return self.send_message(message, chat_id)

    # ==================== CONFIG ====================

    def set_default_chat(self, chat_id: int):
        """Establece el chat por defecto."""
        self.config['default_chat_id'] = chat_id

    def enable_telegram(self, enabled: bool = True):
        """Habilita/deshabilita Telegram."""
        self._telegram_available = enabled and self.telegram is not None

    def enable_newsfeed(self, enabled: bool = True):
        """Habilita/deshabilita NewsFeed."""
        self._newsfeed_available = enabled and self.newsfeed is not None


# Alias para compatibilidad
TelegramServiceLegacy = NotificationService
