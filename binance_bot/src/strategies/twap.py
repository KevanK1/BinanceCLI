"""
TWAP (Time-Weighted Average Price) Strategy Module.
Splits a large order into smaller orders executed over time.
"""

import time

from client import get_client
from validators.input_validator import validate_twap_order
from utils.logger import get_logger

logger = get_logger()

# Default number of slices for TWAP
DEFAULT_SLICES = 5


def execute_twap_strategy(
    symbol: str, 
    side: str, 
    total_quantity: float, 
    interval_seconds: int,
    num_slices: int = DEFAULT_SLICES
) -> None:
    """
    Execute a TWAP strategy.
    
    Splits the total quantity into N equal parts and places market orders
    at regular intervals.
    
    Args:
        symbol: Trading pair symbol (e.g., BTCUSDT)
        side: Order side (BUY or SELL)
        total_quantity: Total quantity to trade
        interval_seconds: Seconds between each sub-order
        num_slices: Number of order slices (default: 5)
    """
    # Validate inputs
    symbol, side, total_quantity, interval_seconds = validate_twap_order(
        symbol, side, total_quantity, interval_seconds
    )
    
    # Calculate slice quantity
    slice_quantity = round(total_quantity / num_slices, 8)
    
    logger.info(
        "Starting TWAP strategy: %s %s total=%s, slices=%d, interval=%ds",
        symbol, side, total_quantity, num_slices, interval_seconds
    )
    
    print(f"\n🔄 Starting TWAP Strategy...")
    print(f"   Symbol:         {symbol}")
    print(f"   Side:           {side}")
    print(f"   Total Quantity: {total_quantity}")
    print(f"   Slices:         {num_slices}")
    print(f"   Quantity/Slice: {slice_quantity}")
    print(f"   Interval:       {interval_seconds}s")
    print(f"\n   Estimated completion: {num_slices * interval_seconds}s")
    print("-" * 50)
    
    client = get_client()
    successful_orders = 0
    failed_orders = 0
    total_filled = 0
    
    for i in range(num_slices):
        slice_num = i + 1
        
        # Adjust last slice to account for rounding
        if slice_num == num_slices:
            current_qty = round(total_quantity - (slice_quantity * (num_slices - 1)), 8)
        else:
            current_qty = slice_quantity
        
        print(f"\n   [{slice_num}/{num_slices}] Placing order: {current_qty} {symbol}...")
        logger.info("TWAP slice %d/%d: placing %s %s", slice_num, num_slices, current_qty, symbol)
        
        result = client.place_market_order(symbol, side, current_qty)
        
        if result["success"]:
            data = result["data"]
            successful_orders += 1
            total_filled += float(data.get('executedQty', current_qty))
            print(f"   ✅ Success - Order ID: {data.get('orderId')}, Status: {data.get('status')}")
            logger.info("TWAP slice %d completed: orderId=%s", slice_num, data.get('orderId'))
        else:
            failed_orders += 1
            print(f"   ❌ Failed - {result.get('error')}")
            logger.error("TWAP slice %d failed: %s", slice_num, result.get('error'))
        
        # Sleep between orders (except after the last one)
        if slice_num < num_slices:
            print(f"   ⏳ Waiting {interval_seconds}s before next order...")
            time.sleep(interval_seconds)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TWAP Strategy Complete")
    print(f"   Successful Orders: {successful_orders}")
    print(f"   Failed Orders:     {failed_orders}")
    print(f"   Total Filled:      {total_filled}")
    print("=" * 50)
    
    logger.info(
        "TWAP strategy completed: success=%d, failed=%d, filled=%s",
        successful_orders, failed_orders, total_filled
    )
