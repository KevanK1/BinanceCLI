"""
Limit Order Module.
Handles execution of limit orders.
"""

from client import get_client
from validators.input_validator import validate_limit_order
from utils.logger import get_logger

logger = get_logger()


def execute_limit_order(symbol: str, side: str, quantity: float, price: float) -> None:
    """
    Execute a limit order.
    
    Args:
        symbol: Trading pair symbol (e.g., BTCUSDT)
        side: Order side (BUY or SELL)
        quantity: Order quantity
        price: Limit price
    """
    # Validate inputs
    symbol, side, quantity, price = validate_limit_order(symbol, side, quantity, price)
    
    logger.info("Executing limit order: %s %s %s @ %s", symbol, side, quantity, price)
    print(f"\n📤 Placing LIMIT order...")
    print(f"   Symbol:   {symbol}")
    print(f"   Side:     {side}")
    print(f"   Quantity: {quantity}")
    print(f"   Price:    {price}")
    
    # Get client and place order
    client = get_client()
    result = client.place_limit_order(symbol, side, quantity, price)
    
    if result["success"]:
        data = result["data"]
        print(f"\n✅ Order Placed Successfully!")
        print(f"   Order ID:     {data.get('orderId')}")
        print(f"   Status:       {data.get('status')}")
        print(f"   Symbol:       {data.get('symbol')}")
        print(f"   Side:         {data.get('side')}")
        print(f"   Type:         {data.get('type')}")
        print(f"   Quantity:     {data.get('origQty')}")
        print(f"   Price:        {data.get('price')}")
        
        logger.info("Limit order completed: orderId=%s, status=%s", 
                   data.get('orderId'), data.get('status'))
    else:
        print(f"\n❌ Order Failed!")
        print(f"   Error: {result.get('error')}")
        logger.error("Limit order failed: %s", result.get('error'))
