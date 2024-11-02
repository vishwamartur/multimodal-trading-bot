# config/logging_config.py

import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    """
    Sets up logging configuration for the trading bot.
    """
    # Define log file path and log level from environment variables
    log_file = os.getenv("LOG_FILE_PATH", "logs/trading_bot.log")
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    # Create logs directory if it does not exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Define log format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Set up file handler with rotation (e.g., max 5 files, each up to 5 MB)
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=5
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    # Set up console handler (optional, useful for development/debugging)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)

    # Add handlers to the root logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Optional: Logging for third-party libraries (e.g., requests, websocket)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("websocket").setLevel(logging.WARNING)

    # Log initial startup message
    logger.info("Logging setup complete. Log level: %s", log_level)

    return logger
