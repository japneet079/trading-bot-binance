import hmac
import hashlib
import time
import requests
import logging

class BinanceFuturesTestnetClient:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://testnet.binancefuture.com"
        
    def _generate_signature(self, query_string):
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def place_order(self, symbol, side, order_type, quantity, price=None):
        endpoint = "/fapi/v1/order"
        url = self.base_url + endpoint
        
        timestamp = int(time.time() * 1000)
        
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
            "timestamp": timestamp
        }
        
        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC" 

        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        signature = self._generate_signature(query_string)
        query_string += f"&signature={signature}"
        
        headers = {
            "X-MBX-APIKEY": self.api_key
        }
        
        logging.info(f"Sending Order Request: {symbol} | {side} | {order_type} | Qty: {quantity}")
        
        try:
            response = requests.post(url, data=query_string, headers=headers, timeout=10)
            response_json = response.json()
            
            if response.status_code == 200:
                logging.info(f"Order Successful! OrderID: {response_json.get('orderId')}")
                return True, response_json
            else:
                logging.error(f"Binance API Error: {response_json.get('msg')} (Code: {response_json.get('code')})")
                return False, response_json
                
        except requests.exceptions.RequestException as e:
            logging.error(f"Network Connection Failure: {str(e)}")
            return False, {"error": "Network/Timeout failure"}