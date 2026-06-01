# Simplified Binance Futures Testnet Trading Bot

A modular Python command-line interface (CLI) application that places Market and Limit orders on the Binance Futures Testnet using raw REST API integrations.

## Setup Instructions
1. Clone this repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file in the root directory and add your Binance Futures Testnet keys:
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here

## Execution Examples
- Market Order: `python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001`
- Limit Order: `python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 60000`

## Assumptions Made
- Handled authentication using safe query-string signing via HMAC SHA256 as required by private Binance endpoints.
- Assigned timeInForce=GTC (Good 'Til Cancelled) as a mandatory default condition for executing Limit orders on the exchange platform.
