import logging
import asyncio
from typing import Dict, Any, Optional
import websockets # type: ignore
from websocket.market_data_handler import MarketDataHandler
from websocket.order_execution import OrderExecution

class WebsocketClient:
    """
    Client for handling websocket connections to exchange.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize websocket client.
        
        Args:
            config: Dictionary containing client configuration parameters
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.market_data_handler = MarketDataHandler(config)
        self.order_execution = OrderExecution(config)
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self._keep_running = False

    async def connect(self) -> None:
        """Connect to websocket endpoint."""
        try:
            uri = self.config["websocket_uri"]
            self.websocket = await websockets.connect(uri)
            self.logger.info(f"Connected to websocket at {uri}")
            self._keep_running = True
        except Exception as e:
            self.logger.error(f"Failed to connect to websocket: {str(e)}")
            raise

    async def disconnect(self) -> None:
        """Disconnect from websocket endpoint."""
        self._keep_running = False
        if self.websocket:
            await self.websocket.close()
            self.websocket = None
            self.logger.info("Disconnected from websocket")

    async def subscribe(self, symbols: list[str]) -> None:
        """
        Subscribe to market data for specified symbols.
        
        Args:
            symbols: List of trading symbols to subscribe to
        """
        if not self.websocket:
            raise RuntimeError("Not connected to websocket")
            
        subscribe_message = {
            "type": "subscribe",
            "symbols": symbols
        }
        
        await self.websocket.send(str(subscribe_message))
        self.logger.info(f"Subscribed to symbols: {symbols}")

    async def run(self) -> None:
        """Run websocket client message loop."""
        if not self.websocket:
            raise RuntimeError("Not connected to websocket")
            
        while self._keep_running:
            try:
                message = await self.websocket.recv()
                await self._handle_message(message)
            except websockets.exceptions.ConnectionClosed:
                self.logger.error("Websocket connection closed unexpectedly")
                break
            except Exception as e:
                self.logger.error(f"Error handling message: {str(e)}")
                continue

    async def _handle_message(self, message: str) -> None:
        """
        Handle incoming websocket message.
        
        Args:
            message: Raw message string from websocket
        """
        try:
            # Parse message and route to appropriate handler
            message_data = eval(message)  # In production use proper JSON parsing
            
            if message_data.get("type") == "market_data":
                await self.market_data_handler.process_market_data(message_data)
            elif message_data.get("type") == "order_update":
                await self.order_execution.handle_order_update(message_data)
            else:
                self.logger.warning(f"Received unknown message type: {message_data}")
                
        except Exception as e:
            self.logger.error(f"Failed to handle message: {str(e)}")
