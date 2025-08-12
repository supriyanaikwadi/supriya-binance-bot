import os
import logging
import time
from decimal import Decimal, InvalidOperation

LOG_FILE = os.path.join(os.getcwd(), 'bot.log')

# Configure logging once
logger = logging.getLogger('binance_bot')
logger.setLevel(logging.DEBUG)
if not logger.handlers:
    fh = logging.FileHandler(LOG_FILE)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

VALID_SIDE = {'BUY', 'SELL'}

def validate_symbol(symbol: str) -> str:
    if not isinstance(symbol, str) or len(symbol) < 6:
        raise ValueError('Invalid symbol')
    return symbol.upper()

def validate_side(side: str) -> str:
    sideu = side.upper()
    if sideu not in VALID_SIDE:
        raise ValueError('side must be BUY or SELL')
    return sideu

def validate_quantity(q) -> Decimal:
    try:
        d = Decimal(str(q))
    except (InvalidOperation, ValueError):
        raise ValueError('Invalid quantity')
    if d <= 0:
        raise ValueError('Quantity must be > 0')
    return d

def validate_price(p) -> Decimal:
    try:
        d = Decimal(str(p))
    except (InvalidOperation, ValueError):
        raise ValueError('Invalid price')
    if d <= 0:
        raise ValueError('Price must be > 0')
    return d

def timestamp_ms() -> int:
    return int(time.time() * 1000)
