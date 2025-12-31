"""
Logger module for Binance SPOT CLI Bot.
Provides a single global logger instance used by all modules.
"""

import logging
import os

# Get the project root directory (binance_bot folder)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOG_FILE = os.path.join(PROJECT_ROOT, "bot.log")

# Create logger
logger = logging.getLogger("binance_bot")
logger.setLevel(logging.DEBUG)

# Prevent duplicate handlers
if not logger.handlers:
    # File handler - writes to bot.log
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler - for error messages
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    
    # Formatter with timestamp, level, and message
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def get_logger():
    """Return the global logger instance."""
    return logger


if __name__ == "__main__":
    # Test the logger
    test_logger = get_logger()
    test_logger.debug("Debug message test")
    test_logger.info("Info message test")
    test_logger.warning("Warning message test")
    test_logger.error("Error message test")
    print(f"Log file created at: {LOG_FILE}")
