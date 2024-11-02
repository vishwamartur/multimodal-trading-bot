import unittest
from unittest.mock import patch, AsyncMock
from datetime import datetime
from typing import Dict, Any

from websocket.websocket_client import WebsocketClient

class TestWebsocketClient(unittest.TestCase):
    def setUp(self):
        self.config = {
            "websocket": {
                "url": "wss://test.websocket.com",
                "api_key": "test_key"
            }
        }
        self.client = WebsocketClient(self.config)

    @patch('websockets.connect')
    async def test_connect(self, mock_connect):
        # Setup mock websocket connection
        mock_ws = AsyncMock()
        mock_connect.return_value = mock_ws

        # Test connection
        await self.client.connect()
        
        mock_connect.assert_called_once_with(
            self.config["websocket"]["url"],
            extra_headers={"X-API-Key": self.config["websocket"]["api_key"]}
        )
        self.assertTrue(self.client.is_connected())

    @patch('websockets.connect')
    async def test_subscribe(self, mock_connect):
        # Setup mock websocket
        mock_ws = AsyncMock()
        mock_connect.return_value = mock_ws
        await self.client.connect()

        # Test subscription
        symbol = "TEST"
        await self.client.subscribe(symbol)

        mock_ws.send.assert_called_once()
        sent_message = mock_ws.send.call_args[0][0]
        self.assertIn(symbol, sent_message)

    @patch('websockets.connect')
    async def test_receive_message(self, mock_connect):
        # Setup mock data
        mock_data = {
            "symbol": "TEST",
            "price": 100.0,
            "timestamp": datetime.now().isoformat()
        }

        # Setup mock websocket
        mock_ws = AsyncMock()
        mock_ws.recv.return_value = str(mock_data)
        mock_connect.return_value = mock_ws
        
        await self.client.connect()
        
        # Test receiving message
        message = await self.client.receive()
        self.assertEqual(message["symbol"], "TEST")
        self.assertEqual(message["price"], 100.0)

    @patch('websockets.connect')
    async def test_connection_error(self, mock_connect):
        # Setup mock to raise exception
        mock_connect.side_effect = Exception("Connection Error")

        # Test error handling
        with self.assertRaises(Exception):
            await self.client.connect()
        
        self.assertFalse(self.client.is_connected())

    async def test_disconnect(self):
        # Test disconnection when not connected
        await self.client.disconnect()
        self.assertFalse(self.client.is_connected())

        # Test disconnection when connected
        self.client._ws = AsyncMock()
        self.client._connected = True
        
        await self.client.disconnect()
        self.client._ws.close.assert_called_once()
        self.assertFalse(self.client.is_connected())

if __name__ == '__main__':
    unittest.main()
