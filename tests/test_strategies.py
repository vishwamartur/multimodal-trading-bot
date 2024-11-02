import unittest
from unittest.mock import patch, AsyncMock
from datetime import datetime
from typing import Dict, Any

from strategies.base_strategy import BaseStrategy, StrategyResult
from strategies.futures_strategy import FuturesStrategy
from strategies.options_strategy import OptionsStrategy

class TestBaseStrategy(unittest.TestCase):
    def setUp(self):
        self.config = {
            "test_param": "test_value"
        }
        self.strategy = BaseStrategy(self.config)

    def test_validate_market_data(self):
        valid_data = {
            "symbol": "TEST",
            "price": 100.0,
            "timestamp": datetime.now().isoformat()
        }
        self.assertTrue(self.strategy._validate_market_data(valid_data))

        invalid_data = {
            "symbol": "TEST"
        }
        self.assertFalse(self.strategy._validate_market_data(invalid_data))

    def test_calculate_confidence(self):
        signals = {
            "signal1": 0.5,
            "signal2": 0.7,
            "signal3": 0.6
        }
        confidence = self.strategy._calculate_confidence(signals)
        self.assertGreater(confidence, 0.0)
        self.assertLessEqual(confidence, 1.0)

        # Test empty signals
        self.assertEqual(self.strategy._calculate_confidence({}), 0.0)

class TestFuturesStrategy(unittest.TestCase):
    def setUp(self):
        self.config = {
            "test_param": "test_value"
        }
        self.strategy = FuturesStrategy(self.config)

    @patch('strategies.futures_strategy.FuturesStrategy._analyze_technical_indicators')
    async def test_generate_signal(self, mock_technical):
        mock_technical.return_value = 0.5
        
        market_data = {
            "symbol": "TEST",
            "price": 100.0,
            "timestamp": datetime.now().isoformat(),
            "indicators": {
                "rsi": 45,
                "macd": 0.5,
                "volume": 1000000
            }
        }

        # Mock sentiment analysis
        self.strategy.chatgpt.analyze_sentiment_async = AsyncMock(return_value=0.3)
        
        result = await self.strategy.generate_signal(market_data)
        
        self.assertIsInstance(result, StrategyResult)
        self.assertGreaterEqual(result.signal, -1.0)
        self.assertLessEqual(result.signal, 1.0)
        self.assertGreaterEqual(result.confidence, 0.0)
        self.assertLessEqual(result.confidence, 1.0)

class TestOptionsStrategy(unittest.TestCase):
    def setUp(self):
        self.config = {
            "test_param": "test_value"
        }
        self.strategy = OptionsStrategy(self.config)

    def test_analyze_options_metrics(self):
        market_data = {
            "symbol": "TEST",
            "price": 100.0,
            "timestamp": datetime.now().isoformat(),
            "options_metrics": {
                "implied_volatility": 0.3,
                "put_call_ratio": 0.8,
                "open_interest": 10000
            }
        }
        
        score = self.strategy._analyze_options_metrics(market_data)
        self.assertGreaterEqual(score, -1.0)
        self.assertLessEqual(score, 1.0)

    async def test_generate_signal(self):
        market_data = {
            "symbol": "TEST",
            "price": 100.0,
            "timestamp": datetime.now().isoformat(),
            "indicators": {
                "rsi": 45,
                "macd": 0.5,
                "volatility": 0.2
            },
            "options_metrics": {
                "implied_volatility": 0.3,
                "put_call_ratio": 0.8,
                "open_interest": 10000
            }
        }
        
        result = await self.strategy.generate_signal(market_data)
        
        self.assertIsInstance(result, StrategyResult)
        self.assertGreaterEqual(result.signal, -1.0)
        self.assertLessEqual(result.signal, 1.0)
        self.assertGreaterEqual(result.confidence, 0.0)
        self.assertLessEqual(result.confidence, 1.0)

if __name__ == '__main__':
    unittest.main()
