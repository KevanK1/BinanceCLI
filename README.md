# Binance Futures CLI Bot

A command-line trading bot for Binance Futures Testnet with support for market, limit, stop-limit, TWAP, and grid orders.

## Features

- **Market Orders** - Execute instant market orders
- **Limit Orders** - Place limit orders at specific prices
- **Stop-Limit Orders** - Set stop-loss and take-profit orders
- **TWAP Strategy** - Time-weighted average price execution
- **Grid Strategy** - Automated grid trading

## Prerequisites

- Python 3.10+
- Binance Futures Testnet account

## Setup

### 1. Register for Binance Futures Testnet

1. Go to [Binance Futures Testnet](https://testnet.binancefuture.com)
2. Create an account or log in with your GitHub account
3. Navigate to API Management and create new API keys
4. Save your API Key and API Secret

### 2. Install Dependencies

```bash
cd binance_bot
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the `binance_bot` directory:

```env
API_KEY=your_testnet_api_key_here
API_SECRET=your_testnet_api_secret_here
```

Or set them directly in your terminal:

```bash
# Windows (PowerShell)
$env:API_KEY = "your_testnet_api_key_here"
$env:API_SECRET = "your_testnet_api_secret_here"

# Windows (CMD)
set API_KEY=your_testnet_api_key_here
set API_SECRET=your_testnet_api_secret_here

# Linux/Mac
export API_KEY=your_testnet_api_key_here
export API_SECRET=your_testnet_api_secret_here
```

## Usage

All commands are executed from the `src` directory:

```bash
cd binance_bot/src
```

### Market Order

Place an instant market order:

```bash
python cli.py market BTCUSDT BUY 0.001
python cli.py market ETHUSDT SELL 0.01
```

### Limit Order

Place a limit order at a specific price:

```bash
python cli.py limit BTCUSDT BUY 0.001 40000
python cli.py limit BTCUSDT SELL 0.001 50000
```

### Stop-Limit Order

Place a stop-limit order with trigger and limit prices:

```bash
python cli.py stop-limit BTCUSDT BUY 0.001 43000 43100
python cli.py stop-limit BTCUSDT SELL 0.001 45000 44900
```

### TWAP Strategy

Execute orders over time (splits into 5 orders):

```bash
python cli.py twap BTCUSDT BUY 0.005 10
# Places 5 orders of 0.001 each, 10 seconds apart
```

### Grid Strategy

Set up grid trading orders:

```bash
python cli.py grid BTCUSDT 40000 50000 5 0.001
# Creates 5 orders between $40,000 and $50,000
```

### Help

View all available commands:

```bash
python cli.py --help
python cli.py market --help
python cli.py limit --help
```

## Logs

All operations are logged to `binance_bot/bot.log`:

```
2024-01-01 12:00:00 | INFO     | Placing MARKET order: symbol=BTCUSDT, side=BUY, quantity=0.001
2024-01-01 12:00:01 | INFO     | MARKET order placed successfully: orderId=123456789
```

### Reading Logs

```bash
# View last 50 lines
tail -n 50 bot.log

# Follow logs in real-time (Linux/Mac)
tail -f bot.log

# Windows PowerShell
Get-Content bot.log -Tail 50 -Wait
```

## Project Structure

```
binance_bot/
├── requirements.txt
├── bot.log              # Generated logs
├── .env                 # Your API credentials (create this)
└── src/
    ├── cli.py           # Command-line interface
    ├── client.py        # Binance API wrapper
    ├── config.py        # Configuration loader
    ├── orders/
    │   ├── market.py    # Market order logic
    │   ├── limit.py     # Limit order logic  
    │   └── stop_limit.py# Stop-limit order logic
    ├── strategies/
    │   ├── twap.py      # TWAP strategy
    │   └── grid.py      # Grid strategy
    ├── validators/
    │   └── input_validator.py  # Input validation
    └── utils/
        └── logger.py    # Logging configuration
```

## Testing Invalid Inputs

The bot validates all inputs before sending to Binance:

```bash
# Invalid symbol format
python cli.py market INVALID! BUY 0.001
# ❌ Validation Error: Invalid symbol format

# Invalid side
python cli.py market BTCUSDT HOLD 0.001
# ❌ Validation Error: Side must be 'BUY' or 'SELL'

# Invalid quantity
python cli.py market BTCUSDT BUY -1
# ❌ Validation Error: Quantity must be greater than 0
```

## Troubleshooting

### "API_KEY environment variable is not set"
Make sure you've set your API credentials as environment variables or in a `.env` file.

### "Invalid API-key, IP, or permissions"
1. Verify you're using Testnet API keys (not mainnet)
2. Check that API keys are copied correctly without extra spaces

### Orders not appearing on Testnet
1. Log into [Binance Futures Testnet](https://testnet.binancefuture.com)
2. Navigate to "Open Orders" or "Order History"
3. Check `bot.log` for any error messages

## License

Copyright © 2025 Kevan

Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:

http://www.apache.org/licenses/LICENSE-2.0

## Disclaimer

This bot is for **educational purposes** and testnet trading only. Do not use with real funds without proper testing and risk management.
