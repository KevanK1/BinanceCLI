"""
Market Order Module.
Handles execution of market orders.
"""

from client import get_client
from validators.input_validator import validate_market_order
from utils.logger import get_logger

logger = get_logger()


def execute_market_order(symbol: str, side: str, quantity: float) -> None:
    """
    Execute a market order.
    
    Args:
        symbol: Trading pair symbol (e.g., BTCUSDT)
        side: Order side (BUY or SELL)
        quantity: Order quantity
    """
    # Validate inputs
    symbol, side, quantity = validate_market_order(symbol, side, quantity)
    
    logger.info("Executing market order: %s %s %s", symbol, side, quantity)
    print(f"\n📤 Placing MARKET order...")
    print(f"   Symbol:   {symbol}")
    print(f"   Side:     {side}")
    print(f"   Quantity: {quantity}")
    
    # Get client and place order
    client = get_client()
    result = client.place_market_order(symbol, side, quantity)
    
    if result["success"]:
        data = result["data"]
        print(f"\n✅ Order Placed Successfully!")
        print(f"   Order ID:     {data.get('orderId')}")
        print(f"   Status:       {data.get('status')}")
        print(f"   Symbol:       {data.get('symbol')}")
        print(f"   Side:         {data.get('side')}")
        print(f"   Type:         {data.get('type')}")
        print(f"   Quantity:     {data.get('origQty')}")
        
        if data.get('avgPrice'):
            print(f"   Avg Price:    {data.get('avgPrice')}")
        
        logger.info("Market order completed: orderId=%s, status=%s", 
                   data.get('orderId'), data.get('status'))
    else:
        print(f"\n❌ Order Failed!")
        print(f"   Error: {result.get('error')}")
        logger.error("Market order failed: %s", result.get('error'))
