# Binance USDT-M Futures CLI Trading Bot

A CLI-based trading bot for Binance USDT-M Futures supporting market, limit, stop-limit, OCO, TWAP and Grid strategies. Includes validation and structured logging.

## Setup
1. Create a virtual environment and activate it.
2. Install dependencies:
   ```bash
   pip install python-binance==1.0.15 pyyaml
   ```
   *(If you don't want to install python-binance for testing, code has a `--dry-run` option.)*

3. Set environment variables for live trading (optional):
   ```bash
   export BINANCE_API_KEY=your_api_key
   export BINANCE_API_SECRET=your_api_secret
   ```

## Run examples
```bash
python run_bot.py market BTCUSDT BUY 0.001
python run_bot.py limit BTCUSDT SELL 0.001 67000
python run_bot.py stop_limit BTCUSDT BUY 0.001 65000 65100
python run_bot.py oco BTCUSDT SELL 0.001 70000 64000
python run_bot.py twap BTCUSDT BUY 0.01 5 60
python run_bot.py grid BTCUSDT BUY 0.01 60000 70000 5
```

