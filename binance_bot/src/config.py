"""
Configuration module for Binance SPOT CLI Bot.
Loads API credentials from environment variables and configures testnet.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file in parent directory (binance_bot/)
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Binance API Credentials
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Binance SPOT Testnet Configuration
TESTNET = True
TESTNET_BASE_URL = "https://testnet.binance.vision"

# Validate required configuration
def validate_config():
    """Validate that required configuration is present."""
    if not API_KEY:
        print("ERROR: API_KEY environment variable is not set.")
        print("Please set API_KEY with your Binance SPOT API key.")
        sys.exit(1)
    
    if not API_SECRET:
        print("ERROR: API_SECRET environment variable is not set.")
        print("Please set API_SECRET with your Binance SPOT API secret.")
        sys.exit(1)
    
    return True


if __name__ == "__main__":
    if validate_config():
        print("Configuration validated successfully.")
        print(f"Testnet enabled: {TESTNET}")
