import time
from src.utils import logger, validate_symbol, validate_side, validate_quantity

# TWAP: split order into n slices over total_time seconds.
def twap_strategy(client, symbol: str, side: str, total_qty, slices: int, total_time: int):
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    total_qty = validate_quantity(total_qty)
    if slices <= 0 or total_time <= 0:
        raise ValueError('slices and total_time must be > 0')

    slice_qty = total_qty / slices
    interval = total_time / slices
    logger.info('TWAP: %s %s total=%s slices=%s interval=%s', symbol, side, total_qty, slices, interval)

    results = []
    for i in range(int(slices)):
        logger.info('TWAP slice %d: placing market order for %s', i + 1, slice_qty)
        resp = client.place_market_order(symbol, side, slice_qty)
        results.append(resp)
        time.sleep(interval)
    return results
