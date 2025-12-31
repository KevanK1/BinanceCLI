"""
Binance SPOT Client Wrapper.
Provides abstraction layer for all Binance SPOT API calls.
"""

import time
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException

from config import API_KEY, API_SECRET, TESTNET, validate_config
from utils.logger import get_logger

logger = get_logger()


class BinanceClient:
    """Wrapper class for Binance SPOT API operations."""
    
    # Binance SPOT Testnet API endpoint
    SPOT_TESTNET_URL = "https://testnet.binance.vision"
    
    def __init__(self):
        """Initialize the Binance client with testnet configuration."""
        validate_config()
        
        # Initialize client with testnet enabled for SPOT trading
        self.client = Client(API_KEY, API_SECRET, testnet=TESTNET)
        
        # Override the API URL to use SPOT testnet endpoint
        self.client.API_URL = self.SPOT_TESTNET_URL + "/api"
        
        # Sync time with Binance server to fix timestamp issues
        try:
            server_time = self.client.get_server_time()
            local_time = int(time.time() * 1000)
            self.time_offset = server_time['serverTime'] - local_time
            logger.info("Time offset with Binance server: %dms", self.time_offset)
            
            # Apply time offset to client
            self.client.timestamp_offset = self.time_offset
        except Exception as e:
            logger.warning("Could not sync time with server: %s", str(e))
            self.time_offset = 0
        
        # Set default recvWindow to handle potential remaining timestamp issues
        self.recv_window = 60000  # 60 seconds tolerance
        
        logger.info("Binance SPOT client initialized (Testnet: %s)", TESTNET)
        logger.info("Using SPOT API URL: %s", self.client.API_URL)
    
    def place_market_order(self, symbol: str, side: str, quantity: float) -> dict:
        """
        Place a market order.
        
        Args:
            symbol: Trading pair symbol (e.g., BTCUSDT)
            side: Order side (BUY or SELL)
            quantity: Order quantity
            
        Returns:
            Order response dictionary or error info
        """
        logger.info(
            "Placing MARKET order: symbol=%s, side=%s, quantity=%s",
            symbol, side, quantity
        )
        
        try:
            response = self.client.create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=quantity,
                recvWindow=self.recv_window
            )
            logger.info("MARKET order placed successfully: orderId=%s", response.get("orderId"))
            logger.debug("Full response: %s", response)
            return {"success": True, "data": response}
            
        except BinanceAPIException as e:
            logger.error("Binance API error: %s (code: %s)", e.message, e.code)
            return {"success": False, "error": f"API Error: {e.message}", "code": e.code}
            
        except BinanceOrderException as e:
            logger.error("Binance Order error: %s (code: %s)", e.message, e.code)
            return {"success": False, "error": f"Order Error: {e.message}", "code": e.code}
            
        except Exception as e:
            logger.error("Unexpected error placing market order: %s", str(e))
            return {"success": False, "error": f"Unexpected error: {str(e)}"}
    
    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float) -> dict:
        """
        Place a limit order.
        
        Args:
            symbol: Trading pair symbol (e.g., BTCUSDT)
            side: Order side (BUY or SELL)
            quantity: Order quantity
            price: Limit price
            
        Returns:
            Order response dictionary or error info
        """
        logger.info(
            "Placing LIMIT order: symbol=%s, side=%s, quantity=%s, price=%s",
            symbol, side, quantity, price
        )
        
        try:
            response = self.client.create_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                quantity=quantity,
                price=price,
                timeInForce="GTC",
                recvWindow=self.recv_window
            )
            logger.info("LIMIT order placed successfully: orderId=%s", response.get("orderId"))
            logger.debug("Full response: %s", response)
            return {"success": True, "data": response}
            
        except BinanceAPIException as e:
            logger.error("Binance API error: %s (code: %s)", e.message, e.code)
            return {"success": False, "error": f"API Error: {e.message}", "code": e.code}
            
        except BinanceOrderException as e:
            logger.error("Binance Order error: %s (code: %s)", e.message, e.code)
            return {"success": False, "error": f"Order Error: {e.message}", "code": e.code}
            
        except Exception as e:
            logger.error("Unexpected error placing limit order: %s", str(e))
            return {"success": False, "error": f"Unexpected error: {str(e)}"}
    
    def place_stop_limit_order(
        self, 
        symbol: str, 
        side: str, 
        quantity: float, 
        stop_price: float, 
        limit_price: float
    ) -> dict:
        """
        Place a stop-limit order.
        
        Args:
            symbol: Trading pair symbol (e.g., BTCUSDT)
            side: Order side (BUY or SELL)
            quantity: Order quantity
            stop_price: Stop trigger price
            limit_price: Limit price after trigger
            
        Returns:
            Order response dictionary or error info
        """
        logger.info(
            "Placing STOP-LIMIT order: symbol=%s, side=%s, quantity=%s, "
            "stopPrice=%s, limitPrice=%s",
            symbol, side, quantity, stop_price, limit_price
        )
        
        try:
            # SPOT uses STOP_LOSS_LIMIT for SELL and TAKE_PROFIT_LIMIT is not standard
            # Use STOP_LOSS_LIMIT for both sides in SPOT trading
            response = self.client.create_order(
                symbol=symbol,
                side=side,
                type="STOP_LOSS_LIMIT",
                quantity=quantity,
                price=limit_price,
                stopPrice=stop_price,
                timeInForce="GTC",
                recvWindow=self.recv_window
            )
            logger.info("STOP-LIMIT order placed successfully: orderId=%s", response.get("orderId"))
            logger.debug("Full response: %s", response)
            return {"success": True, "data": response}
            
        except BinanceAPIException as e:
            logger.error("Binance API error: %s (code: %s)", e.message, e.code)
            return {"success": False, "error": f"API Error: {e.message}", "code": e.code}
            
        except BinanceOrderException as e:
            logger.error("Binance Order error: %s (code: %s)", e.message, e.code)
            return {"success": False, "error": f"Order Error: {e.message}", "code": e.code}
            
        except Exception as e:
            logger.error("Unexpected error placing stop-limit order: %s", str(e))
            return {"success": False, "error": f"Unexpected error: {str(e)}"}


# Global client instance
_client_instance = None


def get_client() -> BinanceClient:
    """Get or create the global Binance client instance."""
    global _client_instance
    if _client_instance is None:
        _client_instance = BinanceClient()
    return _client_instance
