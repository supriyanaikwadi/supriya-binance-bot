import os
from typing import Optional
from src.utils import logger

try:
    from binance.client import Client
    BINANCE_AVAILABLE = True
except Exception:
    BINANCE_AVAILABLE = False

class BinanceFuturesClient:
    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None, testnet: bool = True):
        self.api_key = api_key or os.environ.get('BINANCE_API_KEY')
        self.api_secret = api_secret or os.environ.get('BINANCE_API_SECRET')
        self.testnet = testnet
        self.client = None
        if BINANCE_AVAILABLE and self.api_key and self.api_secret:
            try:
                self.client = Client(self.api_key, self.api_secret)
                if self.testnet:
                    # configure testnet endpoints if supported
                    self.client.FUTURES_URL = 'https://testnet.binancefuture.com'
                logger.info('Initialized real Binance client (testnet=%s)', testnet)
            except Exception as e:
                logger.exception('Failed to initialize Binance client: %s', e)
                self.client = None
        else:
            logger.info('Binance python client not available or no keys provided — dry-run mode')

    def place_market_order(self, symbol, side, quantity):
        logger.info('place_market_order %s %s %s', symbol, side, quantity)
        if self.client:
            return self.client.futures_create_order(symbol=symbol, side=side, type='MARKET', quantity=float(quantity))
        return {'status': 'dry-run', 'op': 'market', 'symbol': symbol, 'side': side, 'qty': str(quantity)}

    def place_limit_order(self, symbol, side, quantity, price, time_in_force='GTC'):
        logger.info('place_limit_order %s %s %s %s', symbol, side, quantity, price)
        if self.client:
            return self.client.futures_create_order(symbol=symbol, side=side, type='LIMIT', price=str(price), quantity=float(quantity), timeInForce=time_in_force)
        return {'status': 'dry-run', 'op': 'limit', 'symbol': symbol, 'side': side, 'qty': str(quantity), 'price': str(price)}

    def cancel_order(self, symbol, orderId=None, origClientOrderId=None):
        logger.info('cancel_order %s', symbol)
        if self.client:
            return self.client.futures_cancel_order(symbol=symbol, orderId=orderId, origClientOrderId=origClientOrderId)
        return {'status': 'dry-run', 'op': 'cancel', 'symbol': symbol}

    def get_symbol_price(self, symbol):
        logger.info('get_symbol_price %s', symbol)
        if self.client:
            ticker = self.client.futures_symbol_ticker(symbol=symbol)
            return float(ticker['price'])
        # dry-run: return a mocked price
        return 70000.0
