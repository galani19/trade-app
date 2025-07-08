import logging
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException

# Fallback for ORDER_TYPE_STOP if not present in binance.enums
try:
    from binance.enums import ORDER_TYPE_STOP
except ImportError:
    ORDER_TYPE_STOP = "STOP"
except AttributeError:
    ORDER_TYPE_STOP = "STOP"

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.logger = logging.getLogger("BasicBot")
        self.logger.debug("Initializing Binance Client")
        self.client = Client(api_key, api_secret)
        if testnet:
            self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
        self.logger.info("Binance Client initialized (testnet=%s)", testnet)

    def place_market_order(self, symbol, side, quantity):
        try:
            self.logger.info("Placing market order: %s %s %s", side, quantity, symbol)
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_MARKET,
                quantity=quantity
            )
            self.logger.info("Order response: %s", order)
            return order
        except BinanceAPIException as e:
            self.logger.error("API Error: %s", e)
            return {"error": str(e)}
        except Exception as e:
            self.logger.error("Unexpected Error: %s", e)
            return {"error": str(e)}

    def place_limit_order(self, symbol, side, quantity, price):
        try:
            self.logger.info("Placing limit order: %s %s %s @ %s", side, quantity, symbol, price)
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_LIMIT,
                quantity=quantity,
                price=price,
                timeInForce=TIME_IN_FORCE_GTC
            )
            self.logger.info("Order response: %s", order)
            return order
        except BinanceAPIException as e:
            self.logger.error("API Error: %s", e)
            return {"error": str(e)}
        except Exception as e:
            self.logger.error("Unexpected Error: %s", e)
            return {"error": str(e)}

    def place_stop_limit_order(self, symbol, side, quantity, price, stopPrice):
        try:
            self.logger.info("Placing stop-limit order: %s %s %s @ %s (stop: %s)", side, quantity, symbol, price, stopPrice)
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_STOP,  # Correct for stop-limit
                quantity=quantity,
                price=price,
                stopPrice=stopPrice,
                timeInForce=TIME_IN_FORCE_GTC
            )
            self.logger.info("Order response: %s", order)
            return order
        except BinanceAPIException as e:
            self.logger.error("API Error: %s", e)
            return {"error": str(e)}
        except Exception as e:
            self.logger.error("Unexpected Error: %s", e)
            return {"error": str(e)}
