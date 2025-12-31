"""
Grid Trading Strategy Module.
Places multiple buy and sell limit orders at predefined price levels.
"""

from client import get_client
from validators.input_validator import validate_grid_order
from utils.logger import get_logger

logger = get_logger()


def execute_grid_strategy(
    symbol: str,
    low_price: float,
    high_price: float,
    grid_count: int,
    quantity: float
) -> None:
    """
    Execute a grid trading strategy.
    
    Places limit buy orders below current price and limit sell orders above
    at predefined grid levels.
    
    Args:
        symbol: Trading pair symbol (e.g., BTCUSDT)
        low_price: Lower bound of the price range
        high_price: Upper bound of the price range
        grid_count: Number of grid levels
        quantity: Quantity per grid order
    """
    # Validate inputs
    symbol, low_price, high_price, grid_count, quantity = validate_grid_order(
        symbol, low_price, high_price, grid_count, quantity
    )
    
    # Calculate grid levels
    price_range = high_price - low_price
    grid_spacing = price_range / (grid_count - 1)
    
    # Generate grid price levels
    grid_levels = []
    for i in range(grid_count):
        price = round(low_price + (i * grid_spacing), 2)
        grid_levels.append(price)
    
    # Calculate midpoint to determine buy/sell zones
    mid_price = (low_price + high_price) / 2
    
    logger.info(
        "Starting grid strategy: %s range=[%s, %s], levels=%d, qty=%s",
        symbol, low_price, high_price, grid_count, quantity
    )
    
    print(f"\n📊 Starting Grid Strategy...")
    print(f"   Symbol:       {symbol}")
    print(f"   Price Range:  {low_price} - {high_price}")
    print(f"   Grid Levels:  {grid_count}")
    print(f"   Grid Spacing: {grid_spacing:.2f}")
    print(f"   Quantity:     {quantity}")
    print(f"   Mid Price:    {mid_price:.2f}")
    print(f"\n   Grid Levels: {grid_levels}")
    print("-" * 50)
    
    client = get_client()
    buy_orders = 0
    sell_orders = 0
    failed_orders = 0
    
    for price in grid_levels:
        # Below midpoint = BUY, Above midpoint = SELL
        if price < mid_price:
            side = "BUY"
            emoji = "🟢"
        else:
            side = "SELL"
            emoji = "🔴"
        
        print(f"\n   {emoji} Placing {side} order at {price}...")
        logger.info("Grid order: %s %s %s @ %s", symbol, side, quantity, price)
        
        result = client.place_limit_order(symbol, side, quantity, price)
        
        if result["success"]:
            data = result["data"]
            if side == "BUY":
                buy_orders += 1
            else:
                sell_orders += 1
            print(f"   ✅ Success - Order ID: {data.get('orderId')}")
            logger.info("Grid order placed: orderId=%s", data.get('orderId'))
        else:
            failed_orders += 1
            print(f"   ❌ Failed - {result.get('error')}")
            logger.error("Grid order failed at %s: %s", price, result.get('error'))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Grid Strategy Complete")
    print(f"   Buy Orders:    {buy_orders}")
    print(f"   Sell Orders:   {sell_orders}")
    print(f"   Failed Orders: {failed_orders}")
    print(f"   Total Orders:  {buy_orders + sell_orders}")
    print("=" * 50)
    
    logger.info(
        "Grid strategy completed: buys=%d, sells=%d, failed=%d",
        buy_orders, sell_orders, failed_orders
    )
