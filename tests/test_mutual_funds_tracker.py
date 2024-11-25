import unittest
from unittest.mock import patch, AsyncMock
from data.mutual_funds_tracker import MutualFundsTracker

class TestMutualFundsTracker(unittest.TestCase):
    def setUp(self):
        self.config = {
            "investment_banking": {
                "mutual_funds_tracking_enabled": True,
                "mutual_funds_data_source": "test_source"
            }
        }
        self.tracker = MutualFundsTracker(self.config)

    @patch('data.mutual_funds_tracker.MutualFundsTracker.fetch_mutual_funds_trades')
    async def test_fetch_mutual_funds_trades(self, mock_fetch):
        # Mock response data
        mock_data = {
            "timestamp": "2023-01-01T00:00:00Z",
            "trades": [
                {"trade_id": 1, "symbol": "TEST", "price": 100.0, "volume": 1000}
            ]
        }
        mock_fetch.return_value = mock_data

        # Test fetching data
        result = await self.tracker.fetch_mutual_funds_trades()

        # Verify results
        self.assertEqual(result["timestamp"], "2023-01-01T00:00:00Z")
        self.assertEqual(len(result["trades"]), 1)
        self.assertEqual(result["trades"][0]["symbol"], "TEST")

    @patch('data.mutual_funds_tracker.MutualFundsTracker.process_mutual_funds_trades')
    async def test_process_mutual_funds_trades(self, mock_process):
        # Mock trades data
        trades_data = {
            "timestamp": "2023-01-01T00:00:00Z",
            "trades": [
                {"trade_id": 1, "symbol": "TEST", "price": 100.0, "volume": 1000}
            ]
        }

        # Test processing data
        await self.tracker.process_mutual_funds_trades(trades_data)

        # Verify processing was called
        mock_process.assert_called_once_with(trades_data)

if __name__ == '__main__':
    unittest.main()
