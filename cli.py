import argparse
import os
from dotenv import load_dotenv
from bot.logging_config import setup_logging
from bot.validators import validate_inputs
from bot.client import BinanceFuturesTestnetClient

load_dotenv()

def main():
    setup_logging()
    
    parser = argparse.ArgumentParser(description="Primetrade.ai Simplified Binance Futures Testnet Trading Bot")
    parser.add_argument("--symbol", required=True, help="Trading Pair (e.g., BTCUSDT)")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument("--type", required=True, choices=["MARKET", "LIMIT"], help="MARKET or LIMIT")
    parser.add_argument("--quantity", required=True, help="Order quantity")
    parser.add_argument("--price", help="Order price (Required for LIMIT orders)")
    
    args = parser.parse_args()
    
    # Get Keys from Environment
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    
    if not api_key or not api_secret:
        print("[ERROR] Please set your BINANCE_API_KEY and BINANCE_API_SECRET environmental variables (.env file).")
        return

    # 1. Validate Input
    try:
        symbol, side, order_type, quantity, price = validate_inputs(
            args.symbol, args.side, args.type, args.quantity, args.price
        )
    except ValueError as e:
        print(f"[INPUT ERROR] {str(e)}")
        return

    # 2. Execute Order
    client = BinanceFuturesTestnetClient(api_key, api_secret)
    success, response = client.place_order(symbol, side, order_type, quantity, price)
    
    # 3. Present Clean Output Summary
    print("\n" + "="*40)
    print("ORDER REQUEST SUMMARY")
    print("="*40)
    print(f"Symbol:    {symbol}")
    print(f"Side:      {side}")
    print(f"Type:      {order_type}")
    print(f"Quantity:  {quantity}")
    if price:
        print(f"Price:     {price}")
    print("-"*40)
    
    if success:
        print("STATUS: SUCCESS")
        print(f"OrderID:       {response.get('orderId')}")
        print(f"Order Status:  {response.get('status')}")
        print(f"Executed Qty:  {response.get('executedQty')}")
        print(f"Avg Price:     {response.get('avgPrice', 'N/A')}")
    else:
        print("STATUS: FAILED")
        print(f"Error Message: {response.get('msg', response.get('error', 'Unknown Error'))}")
    print("="*40 + "\n")

if __name__ == "__main__":
    main()