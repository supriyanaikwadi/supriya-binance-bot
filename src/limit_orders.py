from src.utils import logger, validate_symbol, validate_side, validate_quantity, validate_price
from src.binance_client import BinanceFuturesClient

def limit_order(client: BinanceFuturesClient, symbol: str, side: str, qty, price):
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    qty = validate_quantity(qty)
    price = validate_price(price)
    logger.info('Submitting limit order: %s %s %s @ %s', symbol, side, qty, price)
    resp = client.place_limit_order(symbol, side, qty, price)
    logger.info('Limit order response: %s', resp)
    return resp
