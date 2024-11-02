import unittest
from unittest.mock import patch, AsyncMock
from datetime import datetime
from typing import Dict, Any

from data.data_fetcher import DataFetcher

class TestDataFetcher(unittest.TestCase):
    def setUp(self):
        self.config = {
            "api": {
                "base_url": "https://api.test.com",
                "api_key": "test_key"
            }
        }
        self.fetcher = DataFetcher(self.config)

    @patch('aiohttp.ClientSession')
    async def test_fetch_market_data(self, mock_session):
        # Mock response data
        mock_data = {
            "symbol": "TEST",
            "price": 100.0,
            "timestamp": datetime.now().isoformat(),
            "indicators": {
                "rsi": 45,
                "macd": 0.5,
                "volume": 1000000
            }
        }

        # Setup mock response
        mock_response = AsyncMock()
        mock_response.json.return_value = mock_data
        mock_session.return_value.__aenter__.return_value.get.return_value.__aenter__.return_value = mock_response

        # Test fetching data
        result = await self.fetcher.fetch_market_data("TEST")

        # Verify results
        self.assertEqual(result["symbol"], "TEST")
        self.assertEqual(result["price"], 100.0)
        self.assertIn("indicators", result)
        self.assertIn("rsi", result["indicators"])

    @patch('aiohttp.ClientSession')
    async def test_fetch_market_data_error(self, mock_session):
        # Setup mock to raise exception
        mock_session.return_value.__aenter__.return_value.get.side_effect = Exception("API Error")

        # Test error handling
        with self.assertRaises(Exception):
            await self.fetcher.fetch_market_data("TEST")

    def test_validate_market_data(self):
        # Test valid data
        valid_data = {
            "symbol": "TEST",
            "price": 100.0,
            "timestamp": datetime.now().isoformat(),
            "indicators": {}
        }
        self.assertTrue(self.fetcher._validate_market_data(valid_data))

        # Test invalid data
        invalid_data = {
            "symbol": "TEST"
        }
        self.assertFalse(self.fetcher._validate_market_data(invalid_data))

if __name__ == '__main__':
    unittest.main()
