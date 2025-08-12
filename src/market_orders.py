from src.utils import logger, validate_symbol, validate_side, validate_quantity
from src.binance_client import BinanceFuturesClient

def market_order(client: BinanceFuturesClient, symbol: str, side: str, qty):
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    qty = validate_quantity(qty)
    logger.info('Submitting market order: %s %s %s', symbol, side, qty)
    resp = client.place_market_order(symbol, side, qty)
    logger.info('Market order response: %s', resp)
    return resp
