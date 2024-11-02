import logging
from typing import Dict, Any, Optional, Callable, Awaitable
from datetime import datetime

class MarketDataHandler:
    """
    Handler for processing and managing real-time market data from websocket.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize market data handler.
        
        Args:
            config: Dictionary containing handler configuration parameters
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self._callbacks: Dict[str, Callable[[Dict[str, Any]], Awaitable[None]]] = {}

    async def process_market_data(self, market_data: Dict[str, Any]) -> None:
        """
        Process incoming market data and trigger registered callbacks.
        
        Args:
            market_data: Dictionary containing market data
        """
        if not self._validate_market_data(market_data):
            self.logger.warning(f"Received invalid market data: {market_data}")
            return

        symbol = market_data["symbol"]
        
        # Log market data
        self.logger.debug(
            f"Received market data - Symbol: {symbol} "
            f"Price: {market_data.get('price')} "
            f"Timestamp: {market_data.get('timestamp')}"
        )

        # Trigger callbacks for symbol
        if symbol in self._callbacks:
            try:
                await self._callbacks[symbol](market_data)
            except Exception as e:
                self.logger.error(f"Error in callback for {symbol}: {str(e)}")

    def register_callback(
        self, 
        symbol: str, 
        callback: Callable[[Dict[str, Any]], Awaitable[None]]
    ) -> None:
        """
        Register callback function for a specific symbol.
        
        Args:
            symbol: Trading symbol to register callback for
            callback: Async callback function to be called with market data
        """
        self._callbacks[symbol] = callback
        self.logger.info(f"Registered callback for symbol: {symbol}")

    def unregister_callback(self, symbol: str) -> None:
        """
        Unregister callback function for a specific symbol.
        
        Args:
            symbol: Trading symbol to unregister callback for
        """
        if symbol in self._callbacks:
            del self._callbacks[symbol]
            self.logger.info(f"Unregistered callback for symbol: {symbol}")

    def _validate_market_data(self, market_data: Dict[str, Any]) -> bool:
        """
        Validate market data contains required fields.
        
        Args:
            market_data: Dictionary containing market data
            
        Returns:
            Boolean indicating if market data is valid
        """
        required_fields = ["symbol", "price", "timestamp"]
        return all(field in market_data for field in required_fields)
