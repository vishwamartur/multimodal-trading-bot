import logging
from typing import Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass

@dataclass
class SentimentResult:
    timestamp: datetime
    symbol: str
    score: float  # Score between -1 (bearish) and 1 (bullish)
    confidence: float  # Confidence level between 0 and 1
    source: str  # Source of the sentiment analysis
    metadata: Optional[Dict[str, Any]] = None

class SentimentAnalyzer:
    """
    Handles sentiment analysis of market data using various sources and methods.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the SentimentAnalyzer with configuration settings.
        
        Args:
            config: Dictionary containing configuration parameters
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing SentimentAnalyzer")

    async def analyze_sentiment(self, market_data: Dict[str, Any]) -> SentimentResult:
        """
        Analyze market sentiment using configured sources.
        
        Args:
            market_data: Dictionary containing processed market data
            
        Returns:
            SentimentResult containing sentiment analysis
        """
        try:
            self.logger.debug(f"Analyzing sentiment for {market_data.get('symbol')}")
            
            # Combine different sentiment sources
            technical_score = self._analyze_technical_sentiment(market_data)
            price_score = self._analyze_price_action(market_data)
            
            # Calculate weighted average of sentiment scores
            combined_score = (technical_score * 0.6 + price_score * 0.4)
            
            return SentimentResult(
                timestamp=datetime.now(),
                symbol=market_data.get("symbol", ""),
                score=max(min(combined_score, 1.0), -1.0),  # Clamp between -1 and 1
                confidence=self._calculate_confidence(market_data),
                source="combined",
                metadata={
                    "technical_score": technical_score,
                    "price_score": price_score
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error analyzing sentiment: {str(e)}")
            raise

    def _analyze_technical_sentiment(self, data: Dict[str, Any]) -> float:
        """
        Analyze sentiment based on technical indicators.
        
        Args:
            data: Dictionary containing market data with indicators
            
        Returns:
            Sentiment score between -1 and 1
        """
        score = 0.0
        indicators = data.get("indicators", {})
        
        # RSI analysis
        if "rsi" in indicators:
            rsi = indicators["rsi"]
            if rsi > 70:
                score -= 0.5  # Overbought
            elif rsi < 30:
                score += 0.5  # Oversold
                
        # Volatility analysis
        if "volatility" in indicators:
            volatility = indicators["volatility"]
            avg_price = data.get("price", 0)
            if avg_price > 0:
                vol_ratio = volatility / avg_price
                if vol_ratio > 0.02:  # High volatility
                    score *= 0.8  # Reduce confidence in other signals
                    
        return score

    def _analyze_price_action(self, data: Dict[str, Any]) -> float:
        """
        Analyze sentiment based on price action.
        
        Args:
            data: Dictionary containing market data
            
        Returns:
            Sentiment score between -1 and 1
        """
        score = 0.0
        
        if all(k in data for k in ["open", "close", "high", "low"]):
            open_price = float(data["open"])
            close_price = float(data["close"])
            high_price = float(data["high"])
            low_price = float(data["low"])
            
            # Trend analysis
            if close_price > open_price:
                score += 0.3
            else:
                score -= 0.3
                
            # Price range analysis
            range_size = high_price - low_price
            if range_size > 0:
                close_position = (close_price - low_price) / range_size
                score += (close_position - 0.5) * 0.4
                
        return score

    def _calculate_confidence(self, data: Dict[str, Any]) -> float:
        """
        Calculate confidence level in sentiment analysis.
        
        Args:
            data: Dictionary containing market data
            
        Returns:
            Confidence score between 0 and 1
        """
        confidence = 0.5  # Base confidence
        
        # Adjust based on data quality
        if "metadata" in data and "data_quality" in data["metadata"]:
            confidence *= data["metadata"]["data_quality"]
            
        # Adjust based on available indicators
        indicators = data.get("indicators", {})
        confidence += 0.1 * len(indicators) / 5  # Boost confidence with more indicators
        
        # Cap confidence
        return min(1.0, confidence)
