"""
Input Validator for Binance SPOT CLI Bot.
Validates all user inputs before they reach the Binance API.
"""

import re
from typing import Tuple


class ValidationError(Exception):
    """Exception raised for input validation failures."""
    pass


def validate_symbol(symbol: str) -> str:
    """
    Validate trading pair symbol format.
    
    Args:
        symbol: Trading pair symbol (e.g., BTCUSDT)
        
    Returns:
        Uppercase symbol if valid
        
    Raises:
        ValidationError: If symbol format is invalid
    """
    if not symbol:
        raise ValidationError("Symbol cannot be empty")
    
    symbol = symbol.upper().strip()
    
    # Symbol should be alphanumeric, typically 6-12 characters
    if not re.match(r'^[A-Z0-9]{3,20}$', symbol):
        raise ValidationError(
            f"Invalid symbol format: '{symbol}'. "
            "Symbol must be alphanumeric (e.g., BTCUSDT, ETHUSDT)"
        )
    
    return symbol


def validate_side(side: str) -> str:
    """
    Validate order side.
    
    Args:
        side: Order side (BUY or SELL)
        
    Returns:
        Uppercase side if valid
        
    Raises:
        ValidationError: If side is not BUY or SELL
    """
    if not side:
        raise ValidationError("Side cannot be empty")
    
    side = side.upper().strip()
    
    if side not in ("BUY", "SELL"):
        raise ValidationError(
            f"Invalid side: '{side}'. Side must be 'BUY' or 'SELL'"
        )
    
    return side


def validate_quantity(quantity: float) -> float:
    """
    Validate order quantity.
    
    Args:
        quantity: Order quantity
        
    Returns:
        Quantity if valid
        
    Raises:
        ValidationError: If quantity is not positive
    """
    try:
        quantity = float(quantity)
    except (TypeError, ValueError):
        raise ValidationError(f"Invalid quantity: '{quantity}'. Must be a number")
    
    if quantity <= 0:
        raise ValidationError(
            f"Invalid quantity: {quantity}. Quantity must be greater than 0"
        )
    
    return quantity


def validate_price(price: float, field_name: str = "Price") -> float:
    """
    Validate price value.
    
    Args:
        price: Price value
        field_name: Name of the field for error messages
        
    Returns:
        Price if valid
        
    Raises:
        ValidationError: If price is not positive
    """
    try:
        price = float(price)
    except (TypeError, ValueError):
        raise ValidationError(f"Invalid {field_name}: '{price}'. Must be a number")
    
    if price <= 0:
        raise ValidationError(
            f"Invalid {field_name}: {price}. {field_name} must be greater than 0"
        )
    
    return price


def validate_market_order(symbol: str, side: str, quantity: float) -> Tuple[str, str, float]:
    """
    Validate all inputs for a market order.
    
    Returns:
        Tuple of (symbol, side, quantity)
    """
    return (
        validate_symbol(symbol),
        validate_side(side),
        validate_quantity(quantity)
    )


def validate_limit_order(
    symbol: str, 
    side: str, 
    quantity: float, 
    price: float
) -> Tuple[str, str, float, float]:
    """
    Validate all inputs for a limit order.
    
    Returns:
        Tuple of (symbol, side, quantity, price)
    """
    return (
        validate_symbol(symbol),
        validate_side(side),
        validate_quantity(quantity),
        validate_price(price)
    )


def validate_stop_limit_order(
    symbol: str,
    side: str,
    quantity: float,
    stop_price: float,
    limit_price: float
) -> Tuple[str, str, float, float, float]:
    """
    Validate all inputs for a stop-limit order.
    
    Returns:
        Tuple of (symbol, side, quantity, stop_price, limit_price)
    """
    return (
        validate_symbol(symbol),
        validate_side(side),
        validate_quantity(quantity),
        validate_price(stop_price, "Stop price"),
        validate_price(limit_price, "Limit price")
    )


def validate_twap_order(
    symbol: str,
    side: str,
    total_quantity: float,
    interval_seconds: int
) -> Tuple[str, str, float, int]:
    """
    Validate all inputs for a TWAP order.
    
    Returns:
        Tuple of (symbol, side, total_quantity, interval_seconds)
    """
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    total_quantity = validate_quantity(total_quantity)
    
    try:
        interval_seconds = int(interval_seconds)
    except (TypeError, ValueError):
        raise ValidationError(
            f"Invalid interval: '{interval_seconds}'. Must be an integer"
        )
    
    if interval_seconds <= 0:
        raise ValidationError(
            f"Invalid interval: {interval_seconds}. Interval must be greater than 0"
        )
    
    return (symbol, side, total_quantity, interval_seconds)


def validate_grid_order(
    symbol: str,
    low_price: float,
    high_price: float,
    grid_count: int,
    quantity: float
) -> Tuple[str, float, float, int, float]:
    """
    Validate all inputs for a grid order.
    
    Returns:
        Tuple of (symbol, low_price, high_price, grid_count, quantity)
    """
    symbol = validate_symbol(symbol)
    low_price = validate_price(low_price, "Low price")
    high_price = validate_price(high_price, "High price")
    quantity = validate_quantity(quantity)
    
    if low_price >= high_price:
        raise ValidationError(
            f"Invalid price range: low_price ({low_price}) must be less than "
            f"high_price ({high_price})"
        )
    
    try:
        grid_count = int(grid_count)
    except (TypeError, ValueError):
        raise ValidationError(
            f"Invalid grid count: '{grid_count}'. Must be an integer"
        )
    
    if grid_count < 2:
        raise ValidationError(
            f"Invalid grid count: {grid_count}. Grid count must be at least 2"
        )
    
    return (symbol, low_price, high_price, grid_count, quantity)
