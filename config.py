import os
from dotenv import load_dotenv

load_dotenv()

# Quotex Configuration
QUOTEX_EMAIL = os.getenv("QUOTEX_EMAIL", "")
QUOTEX_PASSWORD = os.getenv("QUOTEX_PASSWORD", "")

# Strategy Configuration
FAST_MA = 10  # Fast moving average period
SLOW_MA = 20  # Slow moving average period

# Trading Configuration
ASSET = "EURUSD"  # Default trading asset
TIMEFRAME = "1m"  # 1 minute timeframe
INVESTMENT_AMOUNT = 10  # Amount per trade in USD

# Bot Configuration
POLLING_INTERVAL = 60  # Check for signals every 60 seconds
ENABLE_TRADING = False  # Set to True to enable actual trading (use with caution!)
DEBUG_MODE = True  # Enable debug logging
