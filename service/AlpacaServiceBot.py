import os
import time
from math import floor

from alpaca.trading import TradingClient
from alpaca_trade_api.common import URL
from alpaca_trade_api.rest import REST
from alpaca_trade_api.rest import REST, TimeFrame
from alpaca_trade_api.stream import Stream
from alpaca.trading.requests import MarketOrderRequest, StopLossRequest, TakeProfitRequest, StopOrderRequest, \
    GetOrdersRequest, StopLimitOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce, OrderClass, OrderStatus
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import QueryOrderStatus
import logging

from service.AlpacaService import AlpacaService
from core.config import get_config


class AlpacaServiceBot:
    def __init__(self):
        self.init()

    def init(self):
        # Load configuration from environment variables
        config = get_config()
        self.base_url = config.trading.alpaca_bot_base_url
        self.api_key = config.trading.alpaca_bot_api_key
        self.api_secret = config.trading.alpaca_bot_api_secret
        self.paper_mode = config.trading.alpaca_bot_paper_mode

        # Initialize API client with environment credentials
        self.api = TradingClient(self.api_key, self.api_secret, paper=self.paper_mode)
        self.log = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        self.alpacainfo = AlpacaService()

    def accountStatus(self):
        account = self.api.get_account()
        print(account)
    def accountInfo(self):
        account = self.api.get_account()
        for property_name, value in account:
            print(f"\"{property_name}\": {value}")

    def ethStatus(self):
        start = "2023-04-13"
        end = "2023-04-14"
        symbol = "ETHUSD"
        timeframe = "15Min"
        # eth = self.api.get_bars('ETH/USD', '15Min', start, end).df
        eth = self.api.get_bars(symbol, timeframe, start, end).df
        print(eth.head())
        # appl = eth['ETH/USD']

    def test2(self):
        btc = "BTCUSD"
        eth = "ETHUSD"
        btc_snapshot = self.api.get_crypto_snapshot(symbol=btc, exchange="CBSE")
        eth_snapshot = self.api.get_crypto_snapshot(symbol=eth, exchange="CBSE")

        # Get the latest ask price for each cryptocurrency,
        btc_latest_price = btc_snapshot.latest_quote.ap
        eth_latest_price = eth_snapshot.latest_quote.ap
    def getTrades(self,symbol):
        limit = 10000
        print(f"trades for {symbol}")
        aapl_trades = self.api.get_trades(symbol, limit=limit).df
        print(aapl_trades.head())

    def getSnapShot(self, symbol):
        print(f"snapshot  for {symbol}")
        snapshot = self.api.get_snapshot(symbol=symbol)
        print(snapshot)

    def getBars(self, symbol):
        # res = self.api.get_bars(symbol, '1Min', "2023-04-15", "2023-04-15", adjustment='raw').df
        res = self.api.get_bars(symbol, '1Min').df
        # res = self.api.get_latest_bar(symbol).df
        print(res)

    async def trade_callback(self,t):
        print('trade', t)

    async def quote_callback(self, q):
        print('quote', q)


    def asincTradesSymbol(self,symbol):
        # Initiate Class Instance
        # stream = Stream( self.api_key,
        # self.api_secret,
        #   base_url = URL(self.base_url),
        #              data_feed = 'iex')  # <- replace to SIP if you have PRO subscription

        # stream = trade_api.Stream(self.api_key, self.api_secret)
        stream = Stream(self.api_key, self.api_secret, raw_data=True)

        # subscribing to event
        # stream.subscribe_trades(self.trade_callback, 'AAPL')
        # stream.subscribe_quotes(self.quote_callback, 'IBM')
        stream.subscribe_crypto_quotes(self.quote_callback, symbol)
        # stream.subscribe_crypto_bars(self.quote_callback, symbol)

        stream.run()

    def is_invested(self,symbol):
        """Returns True if we own some Bitcoin"""
        ganancia = 0
        try:
            res =  self.api.get_open_position(symbol)
            print("Total qty:", res.qty)
            print("Available qty:", res.qty_available)
            ganancia = res.unrealized_pl
            print(f" ganancia {symbol} es {float(ganancia)}")
            return True, ganancia
        except Exception as e:
            print("is_invested ERROR "+str(e))
            self.log.error(f"error {str(e)}")
        return False, ganancia

    def get_closed_pnl(self, symbol, entry_price, qty):
        """Devuelve el PnL de la última posición cerrada de symbol"""
        from datetime import datetime, timedelta
        today = datetime.now().date()
        start = datetime.combine(today, datetime.min.time())
        end = datetime.combine(today, datetime.max.time())

        # Buscar órdenes cerradas hoy
        request = GetOrdersRequest(
            status="closed",
            after=start.isoformat(),
            until=end.isoformat(),
            limit=1000,
            symbols=[symbol]
        )
        orders = self.api.get_orders(request)

        for o in orders:
            filled_qty = float(o.filled_qty)
            if filled_qty == 0:
                continue

            # Detectar orden que cerró tu posición
            if filled_qty == qty:
                price = float(o.filled_avg_price)
                side = o.side.value

                # Calcular PnL según side
                if side == "sell":  # cerrando long
                    pnl = (price - entry_price) * qty
                else:  # cerrando short
                    pnl = (entry_price - price) * qty

                return pnl, price

        # Si no encuentra la orden exacta, devuelve None
        return None, None
    def is_investedComplete(self,symbol):
        """Returns True if we own some Bitcoin"""
        ganancia = 0
        open = 0
        qty = 0
        try:
            res =  self.api.get_open_position(symbol)
            ganancia = res.unrealized_pl
            open = res.avg_entry_price
            qty = res.qty
            print(f" ganancia {symbol} es {float(ganancia)} se abrio {float(open)} qty  {float(qty)}")
            return True, ganancia, open, qty
        except Exception as e:
            print("is_invested ERROR "+str(e))
            self.log.error(f"error {str(e)}")
        return False, ganancia, open, qty
    def listPositions(self):
        res = self.api.get_all_positions()
        return res
    def allPositions(self):
        positions = self.api.get_all_positions()
        for position in positions:
            for property_name, value in position:
                print(f"\"{property_name}\": {value}")

    def getAsset(self,symbol):
        res =self.api.get_asset(symbol)
        print(res)
    def getClock(self):
        res =self.api.get_clock()
        print(res)
    def getAssets(self):
        active_assets = self.api.list_assets(status='active')
        for x in active_assets:
            print(x)
    def getCashInfo(self):
        account = self.api.get_account()
        print(f"account {account}")
        self.log.info(f"account {account}")
        account_cash = float(account.cash)
        print(f" cash {account_cash}")
        cash_to_spend = account_cash / 2
        print(f" cash  to spend {cash_to_spend}")

    def getlatestPrice(self,symbol):
        # Grabs latest snapshot from Alpaca using the Coinbase exchange.
        # btc_snapshot = alpaca.get_crypto_snapshot(symbol=btc, exchange="CBSE")
        snapshot = self.api.get_crypto_snapshot(symbol)

        # Get the latest ask price for each cryptocurrency,
        # btc_latest_price = btc_snapshot.latest_quote.ap
        self.log.info(f" active {snapshot[symbol]}")
        latest_price = snapshot[symbol].latest_quote
        self.log.info(f" price for {symbol} : {latest_price}")

    def calculate_order_size(self,cash_to_spend, latest_price):
        precision_factor = 10000
        units_to_buy = floor(float(cash_to_spend) * precision_factor / float(latest_price))
        units_to_buy /= precision_factor
        return units_to_buy
    def getCurrentPrice(self,symbol):
        return self.alpacainfo.getCurrentPrice(symbol)
        # current_price = None
        # cambio = None
        # try:
        #     res = self.alpacainfo.get_open_position(symbol)
        #     # print(res)
        #     if res:
        #         current_price=res.current_price
        #     # self.log.info(f" inversion {symbol} es {res}")
        #
        # except Exception as e:
        #     print(e)
        #     self.log.error(f"error {str(e)}")
        # return current_price
    # def getCurrentPrice(self, symbol):
    #     value = self.api.get_asset(symbol, TimeFrame.Minute, exchanges=["CBSE"])
    #     print(f" value {value}")
    def submitOrder(self,symbol, units, latest_price, order_type = "limit"):
        self.api.submit_order(symbol=symbol, qty=units, type=order_type, limit_price=latest_price)

    def submitOrderNow(self,symbol, amount):
        if self.is_invested(symbol):
            current_price, cambio = self.getCurrentPrice(symbol)
            print(f"current price :{current_price}  variacion dia : {cambio}")
            units_to_buy = self.calculate_order_size(amount, current_price)
            print(f"units to buy {units_to_buy} for  amount :{amount}")
            self.submitOrder(symbol,units_to_buy,current_price)
    # def buyOrder(self,symbol, symbol2, amount):
    #     current_price = self.alpacainfo.getCurrentPrice(symbol2)
    #     print(f"current price :{current_price} ")
    #     units_to_buy = self.calculate_order_size(amount, current_price)
    #     print(f"units to buy {units_to_buy} for  amount :{amount}")
    #     market_order_data = MarketOrderRequest(
    #         symbol=symbol,
    #         qty=units_to_buy,
    #         side=OrderSide.BUY,
    #         time_in_force=TimeInForce.GTC
    #     )
    #     market_order = self.api.submit_order(market_order_data)
    #     for property_name, value in market_order:
    #         print(f"\"{property_name}\": {value}")

    # def sellOrder(self,symbol, symbol2, amount):
    #     current_price, cambio =self.alpacainfo.getCurrentPrice(symbol)
    #     print(f"current price :{current_price}  ")
    #     units_to_buy = self.calculate_order_size(amount, current_price)
    #     print(f"units to buy {units_to_buy} for  amount :{amount}")
    #     market_order_data = MarketOrderRequest(
    #         symbol=symbol,
    #         qty=units_to_buy,
    #         side=OrderSide.SELL,
    #         time_in_force=TimeInForce.GTC
    #     )
    #     market_order = self.api.submit_order(market_order_data)
    #
    #     for property_name, value in market_order:
    #         print(f"\"{property_name}\": {value}")










    #Versi�n Profesional � Stop Loss basado en dinero real
    def buy_with_money_stop(self, symbol, amount_usd, max_loss_usd):

        # 1?? Obtener precio estimado
        current_price, _ = self.alpacainfo.getCurrentPrice(symbol)

        # 2?? Calcular cantidad
        qty = self.calculate_order_size(amount_usd, current_price)

        print(f"Sending market order for {qty} shares of {symbol}")

        # 3?? Enviar orden de compra
        buy_order = self.api.submit_order(
            MarketOrderRequest(
                symbol=symbol,
                qty=qty,
                side=OrderSide.BUY,
                time_in_force=TimeInForce.DAY
            )
        )

        # 4?? Esperar a que se ejecute completamente
        filled_order = None
        while True:
            order_status = self.api.get_order_by_id(buy_order.id)

            if order_status.status == "filled":
                filled_order = order_status
                break

            print("Waiting for fill...")
            time.sleep(1)

        entry_price = float(filled_order.filled_avg_price)
        filled_qty = float(filled_order.filled_qty)

        print(f"Filled at {entry_price} for {filled_qty} shares")

        # 5?? Calcular stop basado en p�rdida REAL
        loss_per_share = max_loss_usd / filled_qty
        stop_price = round(entry_price - loss_per_share, 2)

        print(f"Stop loss price calculated: {stop_price}")

        # 6?? Enviar orden STOP
        stop_order = self.api.submit_order(
            StopOrderRequest(
                symbol=symbol,
                qty=filled_qty,
                side=OrderSide.SELL,
                stop_price=stop_price,
                time_in_force=TimeInForce.GTC
            )
        )

        print("Stop loss order submitted")
        print(stop_order)

        return {
            "entry_price": entry_price,
            "stop_price": stop_price,
            "qty": filled_qty
        }
    #protege el dinero ya ganado
    #bot.add_profit_stop_usd("AAPL", protect_usd=30)
    def add_profit_stop_usd(self, symbol, protect_usd):
        """
        Coloca un stop loss basado en beneficio flotante (USD).
        protect_usd = dinero máximo que permites perder desde AHORA
        """

        # 1️ Obtener posición actual
        position = self.api.get_position(symbol)

        qty = float(position.qty)
        entry_price = float(position.avg_entry_price)

        # 2️ Precio actual
        current_price, _ = self.alpacainfo.getCurrentPrice(symbol)

        if current_price <= entry_price:
            print(" No hay beneficio aún, no se coloca stop")
            return None

        # 3️ Cancelar stops previos (recomendado)
        orders = self.api.get_orders(status="open", symbols=[symbol])
        for o in orders:
            if o.side == "sell" and o.type == "stop":
                self.cancel_order(o.id)

        # 4️ Calcular stop desde beneficio
        loss_per_share = protect_usd / qty
        stop_price = round(current_price - loss_per_share, 2)

        # 5️ Nunca por debajo del entry (break-even)
        stop_price = max(stop_price, round(entry_price, 2))

        print(f" Profit stop calculado: {stop_price}")

        # 6️ Enviar orden STOP
        stop_order = self.api.submit_order(
            StopOrderRequest(
                symbol=symbol,
                qty=qty,
                side=OrderSide.SELL,
                stop_price=stop_price,
                time_in_force=TimeInForce.GTC
            )
        )

        print(" Profit stop enviado")
        print(stop_order)

        return {
            "entry_price": entry_price,
            "current_price": current_price,
            "stop_price": stop_price,
            "qty": qty
        }

    def add_profit_stop_usd_crypto(self, symbol, protect_usd):
        position = self.api.get_open_position(symbol)

        qty = float(position.qty)
        entry_price = float(position.avg_entry_price)

        current_price, _ = self.alpacainfo.getCurrentPrice(symbol)
        current_price = float(current_price)

        if current_price <= entry_price:
            print(" Aún no hay beneficio, no se coloca stop")
            return None

        request = GetOrdersRequest(
            status=OrderStatus.ALL,
            symbols=[symbol]
        )
        orders = self.api.get_orders(request)

        for o in orders:
            if (
                    o.status.value == "open"
                    and o.side.value == "sell"
                    and o.type.value == "stop"
            ):
                self.cancel_order(o.id)

        loss_per_unit = protect_usd / qty
        stop_price = current_price - loss_per_unit
        stop_price = max(stop_price, entry_price)
        stop_price = round(stop_price, 2)

        stop_order = self.api.submit_order(
            StopOrderRequest(
                symbol=symbol,
                qty=qty,
                side=OrderSide.SELL,
                stop_price=stop_price,
                time_in_force=TimeInForce.GTC
            )
        )

        print(f" Stop BTC colocado en {stop_price}")

        return {
            "entry_price": entry_price,
            "current_price": current_price,
            "stop_price": stop_price,
            "qty": qty
        }
    #max_loss_usd=5,        # nunca perder más de 5$
    # protect_profit_usd=2   # proteger 2$ de ganancia
    def add_smart_stop_usd_crypto(
            self,
            symbol,
            symbol2,
            max_loss_usd,
            protect_profit_usd
    ):
        # 1️ Obtener posición
        print(f" evaluateNewAction  paso2_1 ")
        position = self.api.get_open_position(symbol)

        qty = float(position.qty)
        entry_price = float(position.avg_entry_price)

        current_price, _ = self.alpacainfo.getCurrentPrice(symbol)
        current_price = float(current_price)
        print(f" evaluateNewAction  paso2_2 ")
        # obtener órdenes existentes y detectar stop previo
        # request = GetOrdersRequest(
        #     status="open",
        #     symbols=[symbol]
        # )
        request = GetOrdersRequest(status="open")
        orders = self.api.get_orders(request)

        symbol_plain = symbol  # BTCUSD
        symbol_slash = symbol2  # BTC/USD

        filtered_orders = []

        for o in orders:
            if o.symbol in (symbol_plain, symbol_slash):
                filtered_orders.append(o)

        orders = filtered_orders


        existing_stop = None

        for o in orders:
            if (
                    o.side.value == "sell"
                    and o.type.value in ("stop", "stop_limit")
            ):
                existing_stop = float(o.stop_price)
                self.cancel_order(o.id)
        print(f" evaluateNewAction  paso2_3 ")
        # 3️ Calcular stop según estado
        if current_price <= entry_price:
            #  Protección de pérdida
            stop_price = entry_price - (max_loss_usd / qty)
        else:
            #  Protección de beneficio
            stop_price = current_price - (protect_profit_usd / qty)
        print(f" evaluateNewAction  paso2_4 ")
        # 4⃣Nunca vender en pérdida si ya estás en positivo
        if current_price > entry_price:
            stop_price = max(stop_price, entry_price)
        print(f" evaluateNewAction  paso2_5 ")
        # 5️ Nunca empeorar el stop
        if existing_stop is not None:
            stop_price = max(stop_price, existing_stop)

        # 6️ Redondeo
        stop_price = round(stop_price, 2)
        limit_price = round(stop_price * 0.999, 2)

        print(f" evaluateNewAction  paso2_6 ")
        # 7️ Crear orden stop
        self.api.submit_order(
            StopLimitOrderRequest(
                symbol=symbol,
                qty=qty,
                side=OrderSide.SELL,
                stop_price=stop_price,
                limit_price=limit_price,
                time_in_force=TimeInForce.GTC
            )
        )

        print(
            f"️ Stop inteligente colocado en {stop_price} "
            f"(entrada {entry_price}, actual {current_price})"
        )

        return {
            "entry_price": entry_price,
            "current_price": current_price,
            "stop_price": stop_price,
            "qty": qty,
            "max_loss_usd": max_loss_usd,
            "protect_profit_usd": protect_profit_usd
        }

    def add_smart_stop_usd_crypto_special(
            self,
            symbol,
            symbol2,
            max_loss_usd,
            protect_profit_usd
    ):
        import time

        print(f" evaluateNewAction  paso2_1 ")

        # 1️ Obtener posición
        position = self.api.get_open_position(symbol)

        total_qty = float(position.qty)
        entry_price = float(position.avg_entry_price)

        current_price, _ = self.alpacainfo.getCurrentPrice(symbol)
        current_price = float(current_price)

        print(f" evaluateNewAction  paso2_2 ")

        # 2️ Obtener órdenes abiertas
        request = GetOrdersRequest(
            status="open",
            symbols=[symbol]
        )
        orders = self.api.get_orders(request)

        existing_stop = None
        locked_qty = 0

        for o in orders:
            if o.side.value == "sell":
                locked_qty += float(o.qty)

                if o.type.value in ("stop", "stop_limit"):
                    existing_stop = float(o.stop_price)

        # 3️⃣ Calcular cantidad REAL disponible
        qty = max(total_qty - locked_qty, 0)

        print(f" TOTAL QTY: {total_qty} | LOCKED: {locked_qty} | AVAILABLE: {qty}")

        #  Si no hay balance disponible, salir
        if qty <= 0:
            print(" Balance bloqueado, no se puede colocar nueva orden aún")
            return

        print(f" evaluateNewAction  paso2_3 ")

        # 4️ Calcular stop
        if current_price <= entry_price:
            stop_price = entry_price - (max_loss_usd / qty)
        else:
            stop_price = current_price - (protect_profit_usd / qty)

        print(f" evaluateNewAction  paso2_4 ")

        # 5️ Nunca vender en pérdida si ya estás en positivo
        if current_price > entry_price:
            stop_price = max(stop_price, entry_price)

        print(f" evaluateNewAction  paso2_5 ")

        # 6⃣ Nunca empeorar stop existente
        if existing_stop is not None:
            if stop_price <= existing_stop:
                print(" Stop actual es mejor, no se actualiza")
                return
            else:
                print(" Mejorando stop, cancelando anterior...")
                for o in orders:
                    if (
                            o.side.value == "sell"
                            and o.type.value in ("stop", "stop_limit")
                    ):
                        self.cancel_order(o.id)

                #  MUY IMPORTANTE para ETH
                time.sleep(2)

        # 7️ Redondeo (más preciso para crypto)
        stop_price = round(stop_price, 4)
        limit_price = round(stop_price * 0.999, 4)

        print(f" evaluateNewAction  paso2_6 ")

        # 8️ Crear orden
        try:
            self.api.submit_order(
                StopLimitOrderRequest(
                    symbol=symbol,
                    qty=qty,
                    side=OrderSide.SELL,
                    stop_price=stop_price,
                    limit_price=limit_price,
                    time_in_force=TimeInForce.GTC
                )
            )

            print(
                f" Stop colocado en {stop_price} "
                f"(entrada {entry_price}, actual {current_price}, qty {qty})"
            )

        except Exception as e:
            print("⚠️ Error al colocar orden:", e)

            #  Retry típico para ETH (balance tarda en liberarse)
            time.sleep(2)

            try:
                position = self.api.get_open_position(symbol)
                total_qty = float(position.qty)

                qty = max(total_qty - locked_qty, 0)

                if qty > 0:
                    self.api.submit_order(
                        StopLimitOrderRequest(
                            symbol=symbol,
                            qty=qty,
                            side=OrderSide.SELL,
                            stop_price=stop_price,
                            limit_price=limit_price,
                            time_in_force=TimeInForce.GTC
                        )
                    )
                    print("✅ Orden colocada en retry")

            except Exception as e2:
                print("❌ Fallo definitivo:", e2)

        return {
            "entry_price": entry_price,
            "current_price": current_price,
            "stop_price": stop_price,
            "qty": qty,
            "total_qty": total_qty,
            "locked_qty": locked_qty,
            "max_loss_usd": max_loss_usd,
            "protect_profit_usd": protect_profit_usd
        }

    def close_all_positions_and_orders(self, symbol):
        try:
            # 1. Obtener órdenes abiertas
            request = GetOrdersRequest(
                status=QueryOrderStatus.OPEN,
                symbols=[symbol]
            )

            orders = self.api.get_orders(request)

            # 2. Cancelarlas
            for order in orders:
                try:
                    self.api.cancel_order_by_id(order.id)
                    print(f"Orden cancelada: {order.id}")
                except Exception as e:
                    error_msg = str(e).lower()

                    if "pending cancel" in error_msg or "already" in error_msg:
                        # ✅ Esto NO es error real
                        print(f"Orden ya en cancelación: {order.id}")
                    else:
                        print(f"Error cancelando orden {order.id}: {e}")

            # 3. Esperar a que se cancelen
            for _ in range(5):
                request = GetOrdersRequest(
                    status=QueryOrderStatus.OPEN,
                    symbols=[symbol]
                )
                orders = self.api.get_orders(request)

                if not orders:
                    break

                time.sleep(0.5)

            # 4. Cerrar posición
            try:
                position = self.api.get_open_position(symbol)

                qty = abs(float(position.qty))
                side = "sell" if float(position.qty) > 0 else "buy"

                from alpaca.trading.requests import MarketOrderRequest
                from alpaca.trading.enums import OrderSide, TimeInForce

                order_data = MarketOrderRequest(
                    symbol=symbol,
                    qty=qty,
                    side=OrderSide.SELL if side == "sell" else OrderSide.BUY,
                    time_in_force=TimeInForce.GTC
                )
                self.api.submit_order(order_data)

                return f"Posición cerrada {symbol} ({qty} {side})"

            except Exception as e:
                return f"No había posición {symbol} o error cerrando: {e}"

        except Exception as e:
            return f"Error en cierre {symbol}total: {str(e)}"

    def add_smart_stop_usd_stock(
            self,
            symbol,
            max_loss_usd,
            protect_profit_usd
    ):
        # 1️⃣ Posición
        position = self.api.get_open_position(symbol)

        qty = abs(float(position.qty))
        entry_price = float(position.avg_entry_price)
        side = position.side  # "long" o "short"

        current_price, _ = self.alpacainfo.getCurrentPrice(symbol)
        current_price = float(current_price)

        # 2️⃣ Órdenes abiertas
        request = GetOrdersRequest(
            status="open",
            symbols=[symbol]
        )
        orders = self.api.get_orders(request)

        existing_stop = None

        for o in orders:
            if (
                    o.side.value in ("sell", "buy")
                    and o.type.value == "stop"
            ):
                existing_stop = float(o.stop_price)
                self.cancel_order(o.id)

        # 3️⃣ Calcular stop según tipo de posición
        if side == "long":
            if current_price <= entry_price:
                #  pérdida
                stop_price = entry_price - (max_loss_usd / qty)
            else:
                #  beneficio
                stop_price = current_price - (protect_profit_usd / qty)

            # Nunca vender en pérdida si ya estás en positivo
            if current_price > entry_price:
                stop_price = max(stop_price, entry_price)

            # Nunca empeorar
            if existing_stop is not None:
                stop_price = max(stop_price, existing_stop)

            order_side = OrderSide.SELL

        else:  # SHORT
            if current_price >= entry_price:
                #  pérdida
                stop_price = entry_price + (max_loss_usd / qty)
            else:
                #  beneficio
                stop_price = current_price + (protect_profit_usd / qty)

            # Nunca recomprar peor que entrada si ya vas ganando
            if current_price < entry_price:
                stop_price = min(stop_price, entry_price)

            # Nunca empeorar
            if existing_stop is not None:
                stop_price = min(stop_price, existing_stop)

            order_side = OrderSide.BUY

        stop_price = round(stop_price, 2)

        # 4️⃣ Enviar STOP simple (stocks)
        self.api.submit_order(
            StopOrderRequest(
                symbol=symbol,
                qty=qty,
                side=order_side,
                stop_price=stop_price,
                time_in_force=TimeInForce.GTC
            )
        )

        print(
            f" Stop stock colocado en {stop_price} "
            f"(side={side}, entry={entry_price}, current={current_price})"
        )

        return {
            "symbol": symbol,
            "side": side,
            "entry_price": entry_price,
            "current_price": current_price,
            "stop_price": stop_price,
            "qty": qty
        }

    def cancel_order(self, order_id):
        """
        Cancela una orden abierta por su ID.
        """
        try:
            res = self.api.cancel_order_by_id(order_id)
            self.log.info(f"Orden cancelada: {order_id}")
            return res
        except Exception as e:
            self.log.error(f"Error cancelando orden {order_id}: {str(e)}")
            return None

    def execute_target_position(self, symbol, target_side, amount_usd):
        """
        target_side: "LONG", "SHORT", "FLAT"
        """

        try:

            print("DEBUG SYMBOL TYPE:", type(symbol), symbol)

            # 1 Cancelar órdenes abiertas del símbolo
            request = GetOrdersRequest(status="open", symbols=[symbol])
            open_orders = self.api.get_orders(request)

            for o in open_orders:
                self.cancel_order(o.id)

            # 2️ Obtener posición actual
            try:
                position = self.api.get_open_position(symbol)
                current_qty = float(position.qty)
                current_side = "LONG" if current_qty > 0 else "SHORT"
            except:
                position = None
                current_qty = 0
                current_side = None

            # 3️ Si queremos quedar FLAT
            if target_side == "FLAT":
                if current_side is None:
                    return f"{symbol} already flat"

                result = self._close_position(symbol)
                return result

            # 4️ Si estamos en el mismo lado
            if current_side == target_side:
                return f"{symbol} already in {target_side}"

            # 5 Si hay posición opuesta → cerrar primero
            if current_side is not None:
                result = self._close_position(symbol)


            # 6️ Calcular qty según USD
            current_price, _ = self.alpacainfo.getCurrentPrice(symbol)
            current_price = float(current_price)  # <- aseguramos float


            # Detectar crypto simple
            is_crypto = symbol.endswith("USD") and len(symbol) > 5

            if is_crypto:
                qty = round(amount_usd / current_price, 6)
            else:
                qty = int(amount_usd / current_price)

            if qty <= 0:
                return "Invalid size"

            side = OrderSide.BUY if target_side == "LONG" else OrderSide.SELL
            tif = self._get_time_in_force(symbol)

            order = self.api.submit_order(
                MarketOrderRequest(
                    symbol=symbol,
                    qty=qty,
                    side=side,
                    time_in_force=tif
                )
            )
            if not is_crypto:
                self._wait_until_filled(order.id)


            return f"{symbol} switched to {target_side}"

        except Exception as e:
            self.log.error(f"Execution error: {str(e)}")
            return f"Execution failed: {str(e)}"

    def _get_time_in_force(self, symbol):
        if symbol.endswith("USD") and len(symbol) > 5:
            return TimeInForce.GTC
        return TimeInForce.DAY

    def _close_position(self, symbol, qty=None, retries=5):
        """
        Cierra la posición de un símbolo de forma confiable.
        qty: opcional, si quieres cerrar solo parte
        """
        for attempt in range(1, retries + 1):
            try:
                position = self.api.get_open_position(symbol)
                current_qty = float(position.qty)
                if current_qty == 0:
                    return f"{symbol} already flat"

                # Cerrar toda la posición
                self.api.close_position(symbol)
                print(f"Intentando cerrar {symbol}, intento {attempt}")

                # Esperar a que se actualice
                time.sleep(1)
                position = self.api.get_open_position(symbol)
                if float(position.qty) == 0:
                    return f"{symbol} closed successfully"
            except Exception as e:
                # Si no hay posición, ya está cerrado
                if "position does not exist" in str(e).lower():
                    return f"{symbol} already flat"
                self.log.error(f"_close_position error attempt {attempt}: {str(e)}")
                time.sleep(1)

        return f"Failed to close {symbol} after {retries} attempts"

    def _wait_until_filled(self, order_id, timeout=15):
        start = time.time()

        while time.time() - start < timeout:
            order = self.api.get_order_by_id(order_id)

            if order.status == ["filled", "partially_filled"]:
                return True

            if order.status in ["canceled", "rejected"]:
                raise Exception(f"Order {order.status}")

            time.sleep(0.5)

        raise Exception("Order timeout")

    def getGanancias(self):
        account = self.api.get_account()

        # Check our current balance vs. our balance at the last market close
        balance_change = float(account.equity) - float(account.last_equity)
        print(f'Today\'s portfolio balance change: ${balance_change}')

    def getbarSet(self, symbol):
        res = self.api.g(symbol,'15Min')
        print(f" res :{res}")

    def ismarketOpen(self):
        clock = self.api.get_clock()
        result = False
        if clock.is_open:
            result = True
        return result

    def get_daily_pnl_by_asset(self):
        """
        Devuelve un DataFrame con las ganancias y pérdidas realizadas del día
        agrupadas por símbolo (activo), considerando operaciones long y short.
        """
        # Fecha de hoy
        from datetime import datetime
        import pandas as pd
        today = datetime.now().date()
        start = datetime.combine(today, datetime.min.time())
        end = datetime.combine(today, datetime.max.time())

        # Traer órdenes cerradas hoy
        request = GetOrdersRequest(
            status="closed",
            after=start.isoformat(),
            until=end.isoformat(),
            limit=1000
        )

        orders = self.api.get_orders(request)

        data = []

        for o in orders:
            # Solo órdenes con cantidad ejecutada
            if o.filled_at is not None and float(o.filled_qty) > 0:
                symbol = o.symbol
                qty = float(o.filled_qty)
                side = o.side.value  # "buy" o "sell"
                price = float(o.filled_avg_price)

                # Determinar PnL según side y tipo de operación
                # Long: sell - buy
                # Short: buy back - sell
                if side == "sell":
                    # Buscamos la entrada correspondiente
                    entry_price = float(o.filled_avg_price)  # simplificado, puedes mejorar
                    pnl = (price - entry_price) * qty
                elif side == "buy":
                    pnl = 0  # si es compra parcial, no cerró la operación
                else:
                    pnl = 0

                data.append({"symbol": symbol, "pnl": pnl})

        # Agrupar por activo
        if len(data) == 0:

            return pd.DataFrame(columns=["symbol", "pnl"])

        df = pd.DataFrame(data)
        pnl_by_symbol = df.groupby("symbol").sum().reset_index()

        return pnl_by_symbol


    def get_asset_activity(self, symbol, date=None):
        """
        Extrae toda la actividad de trading de Alpaca para un activo específico en un día.
        Incluye: aperturas, cierres, long, short, y PnL por cada operación.
        
        Returns dict con:
          - opens: lista de ordenes de apertura
          - closes: lista de ordenes de cierre  
          - long_opens, long_closes, short_opens, short_closes: counts
          - total_pnl: PnL neto realizado
          - trades_detail: list of {side, qty, price, pnl} por cada orden
        """
        from datetime import datetime, date as date_type
        from alpaca.trading.requests import GetOrdersRequest
        from alpaca.trading.enums import OrderSide
        
        if date is None:
            date = datetime.now().date()
        elif isinstance(date, str):
            date = datetime.fromisoformat(date).date()
        
        start = datetime.combine(date, datetime.min.time())
        end = datetime.combine(date, datetime.max.time())
        
        request = GetOrdersRequest(
            status="all",
            after=start.isoformat(),
            until=end.isoformat(),
            limit=1000
        )
        orders = self.api.get_orders(request)
        
        symbol_orders = [o for o in orders if o.symbol == symbol]
        
        activity = {
            "symbol": symbol,
            "date": str(date),
            "long_opens": 0, "long_closes": 0,
            "short_opens": 0, "short_closes": 0,
            "total_opens": 0, "total_closes": 0,
            "total_pnl": 0.0,
            "trades": [],
            "orders": []
        }
        
        long_stack = []
        short_stack = []
        
        for o in symbol_orders:
            if o.filled_at is None or float(o.filled_qty) == 0:
                continue
            
            qty = abs(float(o.filled_qty))
            price = float(o.filled_avg_price)
            side = o.side.value
            filled_at = o.filled_at.isoformat() if o.filled_at else ""
            order_id = o.id
            status = o.status.value
            
            trade_info = {
                "order_id": str(order_id)[:8],
                "side": side,
                "qty": qty,
                "price": price,
                "filled_at": filled_at,
                "status": status,
                "pnl": 0.0,
                "position_type": None
            }
            
            if side == "buy":
                temp_qty = qty
                while temp_qty > 0 and short_stack:
                    entry_price, entry_qty = short_stack[0]
                    if entry_qty <= temp_qty:
                        cover_qty = entry_qty
                        pnl = (entry_price - price) * cover_qty
                        trade_info["pnl"] += pnl
                        trade_info["position_type"] = "SHORT_COVER"
                        activity["short_closes"] += 1
                        activity["total_closes"] += 1
                        activity["total_pnl"] += pnl
                        temp_qty -= entry_qty
                        short_stack.pop(0)
                    else:
                        cover_qty = temp_qty
                        pnl = (entry_price - price) * cover_qty
                        trade_info["pnl"] += pnl
                        trade_info["position_type"] = "SHORT_COVER_PARTIAL"
                        activity["short_closes"] += 1
                        activity["total_closes"] += 1
                        activity["total_pnl"] += pnl
                        short_stack[0] = (entry_price, entry_qty - cover_qty)
                        temp_qty = 0
                
                if temp_qty > 0:
                    long_stack.append((price, temp_qty))
                    trade_info["position_type"] = "LONG_OPEN"
                    activity["long_opens"] += 1
                    activity["total_opens"] += 1
                    
            elif side == "sell":
                temp_qty = qty
                while temp_qty > 0 and long_stack:
                    entry_price, entry_qty = long_stack[0]
                    if entry_qty <= temp_qty:
                        close_qty = entry_qty
                        pnl = (price - entry_price) * close_qty
                        trade_info["pnl"] += pnl
                        trade_info["position_type"] = "LONG_CLOSE"
                        activity["long_closes"] += 1
                        activity["total_closes"] += 1
                        activity["total_pnl"] += pnl
                        temp_qty -= entry_qty
                        long_stack.pop(0)
                    else:
                        close_qty = temp_qty
                        pnl = (price - entry_price) * close_qty
                        trade_info["pnl"] += pnl
                        trade_info["position_type"] = "LONG_CLOSE_PARTIAL"
                        activity["long_closes"] += 1
                        activity["total_closes"] += 1
                        activity["total_pnl"] += pnl
                        long_stack[0] = (entry_price, entry_qty - close_qty)
                        temp_qty = 0
                
                if temp_qty > 0:
                    short_stack.append((price, temp_qty))
                    trade_info["position_type"] = "SHORT_OPEN"
                    activity["short_opens"] += 1
                    activity["total_opens"] += 1
            
            activity["trades"].append(trade_info)
        
        activity["open_positions"] = {
            "long": long_stack,
            "short": short_stack
        }
        
        activity["summary"] = (
            f"{symbol} | {date} | "
            f"Opens: {activity['total_opens']} (L:{activity['long_opens']} S:{activity['short_opens']}) | "
            f"Closes: {activity['total_closes']} (L:{activity['long_closes']} S:{activity['short_closes']}) | "
            f"PnL: ${activity['total_pnl']:.2f}"
        )
        
        return activity



def main():
    # actives.append(btc)
    # symbol2 = 'BTC/USD'
    symbol = 'BTCUSD'

    symbol2 = 'AMZN'
    # symbol = 'AMZN'

    # symbol = 'NFLX'
    # symbol2 = 'NFLX'

    # symbol = 'TSLA'
    # symbol2 = 'TSLA'

    # symbol = 'AMZN'
    # symbol2 = 'AMZN'

    # symbol = 'DIS'
    # symbol2 = 'DIS'
    amount = 1000

    # symbol = 'ETH/USD'

    # symbol2 = 'ETHUSD'
    alpaca = AlpacaServiceBot()
    # alpaca.accountStatus()
    # alpaca.ethStatus()
    # alpaca.getTrades('ETHUSD')
    # alpaca.getTrades(symbol2)
    # alpaca.getSnapShot('BTCUSD')
    # alpaca.test2()
    # alpaca.getBars()
    # alpaca.asincTradesSymbol('ETH/USD')
    # alpaca.is_invested(symbol)
    # alpaca.is_invested(symbol2)
    # alpaca.is_invested('DIS')
    # alpaca.listPositions()
    # alpaca.getAsset(symbol2)
    # alpaca.getClock()
    # alpaca.getBars('ETHUSD')
    # alpaca.getAssets()
    # alpaca.getCashInfo()
    # alpaca.getlatestPrice(symbol)
    # current_price, cambio = alpaca.getCurrentPrice(symbol2)
    # print(f"current price :{current_price}  variacion dia : {cambio}")
    # amount = 1000
    # units_to_buy = alpaca.calculate_order_size(amount,current_price)
    # print(f"units to buy {units_to_buy} for  amoun :{amount}")
    # alpaca.submitOrderNow(symbol2,1000)
    # alpaca.buyOrder(symbol2,1000)

    ##IMPORTANTES
    # alpaca.accountInfo()
    print(f"")
    # alpaca.buyOrder(symbol,symbol2,1000)
    # orderId ='20e2b17b-8e05-42de-820c-d2d2d85c05fe'
    # alpaca.closeOrder(orderId)
    # alpaca.allPositions()
    # alpaca.is_invested(symbol)
    # alpaca.getGanancias()
    # alpaca.closeOrder()
    #ORDENES
    # alpaca.buyOrder(symbol, symbol2, 1000)
    # alpaca.sellOrder(symbol, symbol2, 1000)
    # alpaca.sellOrderInteger(symbol, symbol2, 1000)
    # alpaca.buyOrderInteger(symbol, symbol2, 1000)
    # alpaca.sellOrderUnit(symbol, symbol2, 0.031274)
    # alpaca.buyOrderUnit(symbol, symbol2, 0.031274)
    # alpaca.getGanancias()
    # alpaca.getCurrentPrice(symbol)

    # alpaca.getbarSet(symbol)
    # alpaca.sellOrder(symbol, symbol2, 1000)
    # alpaca.buyOrder(symbol, symbol2, 1000)
    # alpaca.is_invested(symbol)

    # alpaca.closeOrder(symbol)
    # alpaca.getCurrentPrice(symbol)
    # res = alpaca.is_invested(symbol)
    # print(res)
    # alpaca.getCurrentPrice(symbol2)
    # alpaca.ismarketOpen()
    # alpaca.getAsset(symbol)
    # alpaca.buyOrder(symbol, symbol2, amount)
    # alpaca.sellOrder(symbol, symbol2, amount)
    symbol = "BTCUSD"
    symbol2 = "ETH/USD"
    # res, revenue = alpaca.is_invested(symbol2)
    # print(f"valor para {symbol2} ganancia: {revenue}")

    # alpaca.getCurrentPrice(symbol2)
    # alpaca.add_profit_stop_usd_crypto(symbol2,protect_usd=3)
    # alpaca.add_smart_stop_usd_crypto(symbol2,max_loss_usd=3,protect_profit_usd=3)
    # alpaca.add_smart_stop_usd_stock(symbol2,max_loss_usd=3,protect_profit_usd=3)
    # pnl_today = alpaca.get_daily_pnl_by_asset()
    # print(pnl_today)
    # invested, profit, openPrice, qty = alpaca.is_investedComplete(symbol2)

    # position = alpaca.is_invested(symbol2)
    # print("Total qty:", position.qty)
    # print("Available qty:", position.qty_available)

    target_side = 'LONG'
    alpaca.execute_target_position(
        symbol,
        target_side,
        amount
    )

if __name__ == "__main__":
    main()