def validate_inputs(symbol, side, order_type, quantity, price):
    if not symbol or not isinstance(symbol, str):
        raise ValueError("Invalid symbol. Example: BTCUSDT")
        
    if side.upper() not in ["BUY", "SELL"]:
        raise ValueError("Side must be either 'BUY' or 'SELL'")
        
    if order_type.upper() not in ["MARKET", "LIMIT"]:
        raise ValueError("Order type must be either 'MARKET' or 'LIMIT'")
        
    try:
        qty = float(quantity)
        if qty <= 0:
            raise ValueError()
    except ValueError:
        raise ValueError("Quantity must be a positive number")
        
    if order_type.upper() == "LIMIT":
        try:
            p = float(price)
            if p <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            raise ValueError("Price is required and must be a positive number for LIMIT orders")
            
    return symbol.upper(), side.upper(), order_type.upper(), float(quantity), float(price) if price else None