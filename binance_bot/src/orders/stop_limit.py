"""
Stop-Limit Order Module.
Handles execution of stop-limit orders.
"""

from client import get_client
from validators.input_validator import validate_stop_limit_order
from utils.logger import get_logger

logger = get_logger()


def execute_stop_limit_order(
    symbol: str, 
    side: str, 
    quantity: float, 
    stop_price: float, 
    limit_price: float
) -> None:
    """
    Execute a stop-limit order.
    
    Args:
        symbol: Trading pair symbol (e.g., BTCUSDT)
        side: Order side (BUY or SELL)
        quantity: Order quantity
        stop_price: Stop trigger price
        limit_price: Limit price after trigger
    """
    # Validate inputs
    symbol, side, quantity, stop_price, limit_price = validate_stop_limit_order(
        symbol, side, quantity, stop_price, limit_price
    )
    
    logger.info(
        "Executing stop-limit order: %s %s %s @ stop=%s limit=%s", 
        symbol, side, quantity, stop_price, limit_price
    )
    print(f"\n📤 Placing STOP-LIMIT order...")
    print(f"   Symbol:      {symbol}")
    print(f"   Side:        {side}")
    print(f"   Quantity:    {quantity}")
    print(f"   Stop Price:  {stop_price}")
    print(f"   Limit Price: {limit_price}")
    
    # Get client and place order
    client = get_client()
    result = client.place_stop_limit_order(symbol, side, quantity, stop_price, limit_price)
    
    if result["success"]:
        data = result["data"]
        print(f"\n✅ Order Placed Successfully!")
        print(f"   Order ID:     {data.get('orderId')}")
        print(f"   Status:       {data.get('status')}")
        print(f"   Symbol:       {data.get('symbol')}")
        print(f"   Side:         {data.get('side')}")
        print(f"   Type:         {data.get('type')}")
        print(f"   Quantity:     {data.get('origQty')}")
        print(f"   Stop Price:   {data.get('stopPrice')}")
        print(f"   Limit Price:  {data.get('price')}")
        
        logger.info("Stop-limit order completed: orderId=%s, status=%s", 
                   data.get('orderId'), data.get('status'))
    else:
        print(f"\n❌ Order Failed!")
        print(f"   Error: {result.get('error')}")
        logger.error("Stop-limit order failed: %s", result.get('error'))
