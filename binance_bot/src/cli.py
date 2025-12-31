#!/usr/bin/env python3
"""
Binance SPOT CLI Bot - Command Line Interface.
Main entry point for all trading commands.
"""

import argparse
import sys

from orders.market import execute_market_order
from orders.limit import execute_limit_order
from orders.stop_limit import execute_stop_limit_order
from strategies.twap import execute_twap_strategy
from strategies.grid import execute_grid_strategy
from validators.input_validator import ValidationError
from utils.logger import get_logger

logger = get_logger()


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog="binance-bot",
        description="Binance SPOT CLI Trading Bot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py market BTCUSDT BUY 0.001
  python cli.py limit BTCUSDT SELL 0.001 50000
  python cli.py stop-limit BTCUSDT BUY 0.001 43000 43100
  python cli.py twap BTCUSDT BUY 0.003 5
  python cli.py grid BTCUSDT 40000 50000 5 0.001
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Market order command
    market_parser = subparsers.add_parser(
        "market",
        help="Place a market order"
    )
    market_parser.add_argument("symbol", type=str, help="Trading pair (e.g., BTCUSDT)")
    market_parser.add_argument("side", type=str, help="Order side: BUY or SELL")
    market_parser.add_argument("quantity", type=float, help="Order quantity")
    
    # Limit order command
    limit_parser = subparsers.add_parser(
        "limit",
        help="Place a limit order"
    )
    limit_parser.add_argument("symbol", type=str, help="Trading pair (e.g., BTCUSDT)")
    limit_parser.add_argument("side", type=str, help="Order side: BUY or SELL")
    limit_parser.add_argument("quantity", type=float, help="Order quantity")
    limit_parser.add_argument("price", type=float, help="Limit price")
    
    # Stop-limit order command
    stop_limit_parser = subparsers.add_parser(
        "stop-limit",
        help="Place a stop-limit order"
    )
    stop_limit_parser.add_argument("symbol", type=str, help="Trading pair (e.g., BTCUSDT)")
    stop_limit_parser.add_argument("side", type=str, help="Order side: BUY or SELL")
    stop_limit_parser.add_argument("quantity", type=float, help="Order quantity")
    stop_limit_parser.add_argument("stop_price", type=float, help="Stop trigger price")
    stop_limit_parser.add_argument("limit_price", type=float, help="Limit price after trigger")
    
    # TWAP strategy command
    twap_parser = subparsers.add_parser(
        "twap",
        help="Execute TWAP (Time-Weighted Average Price) strategy"
    )
    twap_parser.add_argument("symbol", type=str, help="Trading pair (e.g., BTCUSDT)")
    twap_parser.add_argument("side", type=str, help="Order side: BUY or SELL")
    twap_parser.add_argument("total_quantity", type=float, help="Total quantity to trade")
    twap_parser.add_argument("interval_seconds", type=int, help="Seconds between orders")
    
    # Grid strategy command
    grid_parser = subparsers.add_parser(
        "grid",
        help="Execute grid trading strategy"
    )
    grid_parser.add_argument("symbol", type=str, help="Trading pair (e.g., BTCUSDT)")
    grid_parser.add_argument("low_price", type=float, help="Lower bound of price range")
    grid_parser.add_argument("high_price", type=float, help="Upper bound of price range")
    grid_parser.add_argument("grid_count", type=int, help="Number of grid levels")
    grid_parser.add_argument("quantity", type=float, help="Quantity per grid level")
    
    return parser


def main():
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    logger.info("CLI command received: %s", args.command)
    
    try:
        if args.command == "market":
            execute_market_order(args.symbol, args.side, args.quantity)
            
        elif args.command == "limit":
            execute_limit_order(args.symbol, args.side, args.quantity, args.price)
            
        elif args.command == "stop-limit":
            execute_stop_limit_order(
                args.symbol, args.side, args.quantity,
                args.stop_price, args.limit_price
            )
            
        elif args.command == "twap":
            execute_twap_strategy(
                args.symbol, args.side, args.total_quantity, args.interval_seconds
            )
            
        elif args.command == "grid":
            execute_grid_strategy(
                args.symbol, args.low_price, args.high_price,
                args.grid_count, args.quantity
            )
            
    except ValidationError as e:
        logger.error("Validation error: %s", str(e))
        print(f"\n❌ Validation Error: {e}")
        sys.exit(1)
        
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        print("\n⚠️  Operation cancelled by user")
        sys.exit(130)
        
    except Exception as e:
        logger.exception("Unexpected error: %s", str(e))
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
