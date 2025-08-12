import time
from src.utils import logger, validate_symbol, validate_side, validate_quantity, validate_price

# Simple stop-limit: poll price; when price crosses stop, place a limit order at limit_price
def stop_limit_strategy(client, symbol: str, side: str, qty, stop_price, limit_price, poll_interval=1):
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    qty = validate_quantity(qty)
    stop_price = validate_price(stop_price)
    limit_price = validate_price(limit_price)
    logger.info('Starting stop-limit: %s %s qty=%s stop=%s limit=%s', symbol, side, qty, stop_price, limit_price)

    while True:
        price = client.get_symbol_price(symbol)
        logger.debug('Current price: %s', price)
        if side == 'BUY' and price <= float(stop_price):
            logger.info('Stop hit (BUY). Placing limit order')
            return client.place_limit_order(symbol, side, qty, limit_price)
        if side == 'SELL' and price >= float(stop_price):
            logger.info('Stop hit (SELL). Placing limit order')
            return client.place_limit_order(symbol, side, qty, limit_price)
        time.sleep(poll_interval)
