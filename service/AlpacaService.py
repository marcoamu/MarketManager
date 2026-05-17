from datetime import timedelta, datetime, timezone
from math import floor

from alpaca.data import StockBarsRequest, CryptoHistoricalDataClient, CryptoBarsRequest, StockHistoricalDataClient
from alpaca.trading import TradingClient
from alpaca_trade_api.common import URL
from alpaca_trade_api.rest import REST
from alpaca_trade_api.stream import Stream
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.timeframe import TimeFrame

import logging
from core.config import get_config

class AlpacaService:
    def __init__(self):
        self.init()
    def init(self):
        # Load configuration from environment variables
        config = get_config()
        self.base_url = config.trading.alpaca_data_base_url
        self.api_key = config.trading.alpaca_data_api_key
        self.api_secret = config.trading.alpaca_data_api_secret

        self.api = REST(self.api_key, self.api_secret, self.base_url, api_version='v2')
        self.crypto_client = CryptoHistoricalDataClient(api_key=self.api_key, secret_key=self.api_secret)
        self.stock_client = StockHistoricalDataClient(api_key=self.api_key, secret_key=self.api_secret)

        self.log = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

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

        try:
            res = self.api.get_position(symbol)
            # print(res)
            self.log.info(f" inversion {symbol} es {res}")
            return True
        except Exception as e:
            print(e)
            self.log.error(f"error {str(e)}")
    def listPositions(self):
        res = self.api.list_positions()
        print(res)
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
        current_price = None
        cambio = None
        print(f"alcapa info getCurrentPrice for {symbol}")
        try:

            res = self.api.get_position(symbol)
            # print(res)
            if res:
                current_price=res._raw['current_price']
                # cambio = res._raw['unrealized_plpc']
                print(f" precio actual para {symbol} es {current_price}")

        except Exception as e:
            print(f"getCurrentPrice error {str(e)}")
            self.log.error(f" getCurrentPrice error {str(e)}")
        return current_price,cambio
    def submitOrder(self,symbol, units, latest_price, order_type = "limit"):
        self.api.submit_order(symbol=symbol, qty=units, type=order_type, limit_price=latest_price)

    def submitOrderNow(self,symbol, amount):
        if self.is_invested(symbol):
            current_price, cambio = self.getCurrentPrice(symbol)
            print(f"current price :{current_price}  variacion dia : {cambio}")
            units_to_buy = self.calculate_order_size(amount, current_price)
            print(f"units to buy {units_to_buy} for  amount :{amount}")
            self.submitOrder(symbol,units_to_buy,current_price)
    def buyOrder(self,symbol, symbol2, amount):
        current_price, cambio = self.getCurrentPrice(symbol2)
        print(f"current price :{current_price}  variacion dia : {cambio}")
        units_to_buy = self.calculate_order_size(amount, current_price)
        print(f"units to buy {units_to_buy} for  amount :{amount}")
        market_order_data = MarketOrderRequest(
            symbol=symbol,
            qty=units_to_buy,
            side=OrderSide.BUY,
            time_in_force=TimeInForce.GTC
        )
        market_order = self.api.submit_order(market_order_data)
        for property_name, value in market_order:
            print(f"\"{property_name}\": {value}")

    def collect_bars(self, symbol, limit=50):
        bars = self.api.get_bars(
            symbol,
            TimeFrame.Minute,
            limit=limit
        ).df.reset_index()

        return bars

    def collect_crypto_bars(self, symbol, minutes=120):
        end = datetime.utcnow()
        start = end - timedelta(minutes=minutes)

        request = CryptoBarsRequest(
            symbol_or_symbols=symbol,   # "BTC/USD"
            timeframe=TimeFrame.Minute,
            start=start,
            end=end
        )

        bars = self.crypto_client.get_crypto_bars(request).df
        return bars if not bars.empty else None

    def collect_stock_bars(self, symbol, minutes=120):
        request = StockBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=TimeFrame.Minute,
            limit=minutes
        )

        bars = self.stock_client.get_stock_bars(request).df
        return bars if not bars.empty else None

    def collect_crypto_barsOK(self, symbol="BTC/USD", minutes=120):
        end = datetime.utcnow()
        start = end - timedelta(minutes=minutes)

        request = CryptoBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=TimeFrame.Minute,
            start=start,
            end=end
        )

        bars = self.crypto_client.get_crypto_bars(request).df

        if bars.empty:
            print(f"⚠️ Sin datos para {symbol}")
            return None

        return bars


def main():
    # actives.append(btc)
    # symbol = 'BTC/USD'
    symbol = 'ETH/USD'
    # symbol2 = 'BTCUSD'
    symbol2 = 'ETHUSD'
    alpaca = AlpacaService()
    # alpaca.accountStatus()
    # alpaca.ethStatus()
    # alpaca.getTrades('ETHUSD')
    # alpaca.getTrades(symbol2)
    # alpaca.getSnapShot('BTCUSD')
    # alpaca.test2()
    # alpaca.getBars()
    # alpaca.asincTradesSymbol('ETH/USD')
    # alpaca.is_invested(symbol)
    alpaca.is_invested(symbol2)
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
    symbol2 = "GLD"
    current_price, cambio = alpaca.getCurrentPrice(symbol2)
    alpaca.is_invested(symbol2)
    # print(f"current price :{current_price}  variacion dia : {cambio}")

    # df = alpaca.collect_crypto_barsOK(symbol)
    # df = alpaca.collect_bars2(symbol2)

    ##IMPORTANTES
    # alpaca.accountInfo()
    print(f"")
    # alpaca.buyOrder(symbol,symbol2,1000)
    # alpaca.allPositions()
    # alpaca.is_invested(symbol)
if __name__ == "__main__":
    main()