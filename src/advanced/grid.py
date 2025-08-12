from decimal import Decimal
from src.utils import logger, validate_symbol, validate_side, validate_quantity, validate_price

# Simple grid: place alternating buy/sell limit orders across price levels
def grid_strategy(client, symbol: str, side: str, total_qty, low_price, high_price, steps: int):
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    total_qty = validate_quantity(total_qty)
    low_price = validate_price(low_price)
    high_price = validate_price(high_price)

    if steps <= 1:
        raise ValueError('steps must be > 1')
    step_size = (Decimal(str(high_price)) - Decimal(str(low_price))) / (steps - 1)
    per_order_qty = total_qty / steps
    logger.info('Grid: %s %s qty=%s low=%s high=%s steps=%s', symbol, side, total_qty, low_price, high_price, steps)

    orders = []
    for i in range(steps):
        price = (Decimal(str(low_price)) + step_size * i)
        # alternate sides: if initial side is BUY, place buy orders on lower half
        ord_side = 'BUY' if i < steps/2 else 'SELL'
        ord_side = ord_side if side == 'BUY' else ('SELL' if ord_side=='BUY' else 'BUY')
        logger.info('Placing grid order %s %s @ %s qty=%s', symbol, ord_side, price, per_order_qty)
        resp = client.place_limit_order(symbol, ord_side, per_order_qty, price)
        orders.append(resp)
    return orders
