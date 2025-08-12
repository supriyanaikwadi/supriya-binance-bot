from src.utils import logger, validate_symbol, validate_side, validate_quantity, validate_price

# OCO: place two orders and cancel one when the other fills.
# Implementation note: Binance futures do not support native OCO; this is simulated client-side.
def oco_order(client, symbol: str, side: str, qty, take_profit_price, stop_loss_price):
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    qty = validate_quantity(qty)
    take_profit_price = validate_price(take_profit_price)
    stop_loss_price = validate_price(stop_loss_price)

    logger.info('Placing OCO-like orders for %s %s qty=%s tp=%s sl=%s', symbol, side, qty, take_profit_price, stop_loss_price)

    # Place primary order (market entry)
    entry_side = side
    resp_entry = client.place_market_order(symbol, entry_side, qty)
    logger.info('Entry resp: %s', resp_entry)

    # Place TP and SL as limit orders of opposite side
    tp_side = 'SELL' if side == 'BUY' else 'BUY'
    sl_side = tp_side

    resp_tp = client.place_limit_order(symbol, tp_side, qty, take_profit_price)
    resp_sl = client.place_limit_order(symbol, sl_side, qty, stop_loss_price)

    logger.info('TP resp: %s', resp_tp)
    logger.info('SL resp: %s', resp_sl)

    # NOTE: A real implementation would watch executions and cancel the other order when one fills.
    return {'entry': resp_entry, 'tp': resp_tp, 'sl': resp_sl}
