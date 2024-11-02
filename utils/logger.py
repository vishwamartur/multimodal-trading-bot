import logging
import sys
from typing import Dict, Any
from datetime import datetime

def setup_logger(config: Dict[str, Any]) -> logging.Logger:
    """
    Configure and return a logger instance.
    
    Args:
        config: Dictionary containing logger configuration parameters
        
    Returns:
        Configured logger instance
    """
    # Get logger config
    log_level = config.get("log_level", "INFO")
    log_format = config.get("log_format", 
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_file = config.get("log_file")
    
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level))
    
    # Create formatters and handlers
    formatter = logging.Formatter(log_format)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler if log file specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    return logger

def log_market_data(logger: logging.Logger, market_data: Dict[str, Any]) -> None:
    """
    Log market data in a structured format.
    
    Args:
        logger: Logger instance
        market_data: Market data dictionary to log
    """
    logger.info(
        f"Market Data - Symbol: {market_data.get('symbol')} "
        f"Price: {market_data.get('price')} "
        f"Timestamp: {market_data.get('timestamp')}"
    )

def log_trade(logger: logging.Logger, trade_data: Dict[str, Any]) -> None:
    """
    Log trade execution details.
    
    Args:
        logger: Logger instance
        trade_data: Trade data dictionary to log
    """
    logger.info(
        f"Trade Executed - Action: {trade_data.get('action')} "
        f"Symbol: {trade_data.get('symbol')} "
        f"Price: {trade_data.get('price')} "
        f"Size: {trade_data.get('size')}"
    )
