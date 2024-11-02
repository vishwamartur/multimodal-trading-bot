import logging
from typing import Dict, Any
from datetime import datetime
from strategies.base_strategy import BaseStrategy, StrategyResult
from models.sentiment_analysis import SentimentAnalyzer
from models.chatgpt_integration import ChatGPTIntegration

class FuturesStrategy(BaseStrategy):
    """
    Strategy for trading futures contracts using sentiment analysis and technical indicators.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the futures trading strategy.
        
        Args:
            config: Dictionary containing strategy configuration parameters
        """
        super().__init__(config)
        self.sentiment_analyzer = SentimentAnalyzer(config)
        self.chatgpt = ChatGPTIntegration(config)
        
    async def generate_signal(self, market_data: Dict[str, Any]) -> StrategyResult:
        """
        Generate trading signal for futures based on market data and sentiment.
        
        Args:
            market_data: Dictionary containing processed market data
            
        Returns:
            StrategyResult containing signal and metadata
        """
        if not self._validate_market_data(market_data):
            self.logger.warning("Invalid market data received")
            return StrategyResult(
                timestamp=datetime.now(),
                symbol=market_data.get("symbol", ""),
                signal=0.0,
                confidence=0.0
            )
            
        # Analyze sentiment using multiple sources
        sentiment = await self.sentiment_analyzer.analyze_sentiment(market_data)
        chatgpt_score = await self.chatgpt.analyze_sentiment_async(market_data)
        
        # Combine signals
        signals = {
            "sentiment": sentiment.score,
            "chatgpt": chatgpt_score,
            "technical": self._analyze_technical_indicators(market_data)
        }
        
        # Calculate final signal and confidence
        signal = sum(signals.values()) / len(signals)
        confidence = self._calculate_confidence(signals)
        
        return StrategyResult(
            timestamp=datetime.now(),
            symbol=market_data["symbol"],
            signal=max(min(signal, 1.0), -1.0),  # Clamp between -1 and 1
            confidence=confidence,
            metadata={
                "signals": signals,
                "sentiment_confidence": sentiment.confidence
            }
        )
        
    def _analyze_technical_indicators(self, data: Dict[str, Any]) -> float:
        """
        Analyze technical indicators for futures trading signals.
        
        Args:
            data: Dictionary containing market data and indicators
            
        Returns:
            Technical analysis score between -1 and 1
        """
        score = 0.0
        indicators = data.get("indicators", {})
        
        if "rsi" in indicators:
            rsi = indicators["rsi"]
            if rsi > 70:
                score -= 0.4
            elif rsi < 30:
                score += 0.4
                
        if "macd" in indicators:
            macd = indicators["macd"]
            if macd > 0:
                score += 0.3
            else:
                score -= 0.3
                
        if "volume" in indicators:
            volume = indicators["volume"]
            avg_volume = data.get("average_volume", volume)
            if volume > avg_volume * 1.5:  # High volume
                score *= 1.2  # Amplify existing signal
                
        return max(min(score, 1.0), -1.0)  # Clamp between -1 and 1
