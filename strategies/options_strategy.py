import logging
from typing import Dict, Any
from datetime import datetime
from .base_strategy import BaseStrategy, StrategyResult


class OptionsStrategy(BaseStrategy):
    """
    Strategy for options trading using sentiment analysis, technical indicators,
    and options-specific metrics.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize options trading strategy.
        
        Args:
            config: Dictionary containing strategy configuration parameters
        """
        super().__init__(config)
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing OptionsStrategy")

    async def generate_signal(self, market_data: Dict[str, Any]) -> StrategyResult:
        """
        Generate trading signal for options based on market data.
        
        Args:
            market_data: Dictionary containing processed market data and options metrics
            
        Returns:
            StrategyResult containing signal and metadata
        """
        if not self._validate_market_data(market_data):
            self.logger.warning("Invalid market data received")
            return StrategyResult(
                timestamp=datetime.now(),
                symbol=market_data.get("symbol", ""),
                signal=0.0,
                confidence=0.0,
                metadata={"error": "Invalid market data"}
            )

        # Analyze options-specific indicators
        options_score = self._analyze_options_metrics(market_data)
        
        # Analyze technical indicators
        technical_score = self._analyze_technical_indicators(market_data)
        
        # Calculate final signal
        signals = {
            "options": options_score,
            "technical": technical_score
        }
        
        signal = sum(signals.values()) / len(signals)
        confidence = self._calculate_confidence(signals)
        
        return StrategyResult(
            timestamp=datetime.now(),
            symbol=market_data["symbol"],
            signal=max(min(signal, 1.0), -1.0),  # Clamp between -1 and 1
            confidence=confidence,
            metadata={
                "signals": signals
            }
        )

    def _analyze_options_metrics(self, data: Dict[str, Any]) -> float:
        """
        Analyze options-specific metrics for trading signals.
        
        Args:
            data: Dictionary containing market data and options metrics
            
        Returns:
            Options analysis score between -1 and 1
        """
        score = 0.0
        metrics = data.get("options_metrics", {})
        
        # Implied Volatility analysis
        if "iv" in metrics:
            iv = metrics["iv"]
            iv_percentile = metrics.get("iv_percentile", 50)
            
            if iv_percentile > 80:  # High IV
                score -= 0.3  # Favor selling options
            elif iv_percentile < 20:  # Low IV
                score += 0.3  # Favor buying options
                
        # Put/Call ratio analysis
        if "put_call_ratio" in metrics:
            pc_ratio = metrics["put_call_ratio"]
            if pc_ratio > 1.5:  # High put/call ratio - bearish sentiment
                score -= 0.4
            elif pc_ratio < 0.5:  # Low put/call ratio - bullish sentiment
                score += 0.4
                
        # Open Interest analysis
        if "open_interest" in metrics:
            oi = metrics["open_interest"]
            avg_oi = metrics.get("average_oi", oi)
            if oi > avg_oi * 1.5:  # High open interest
                score *= 1.2  # Amplify existing signal
                
        return max(min(score, 1.0), -1.0)  # Clamp between -1 and 1
        
    def _analyze_technical_indicators(self, data: Dict[str, Any]) -> float:
        """
        Analyze technical indicators for options trading signals.
        
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
                score -= 0.3
            elif rsi < 30:
                score += 0.3
                
        if "macd" in indicators:
            macd = indicators["macd"]
            if macd > 0:
                score += 0.2
            else:
                score -= 0.2
                
        if "volatility" in indicators:
            volatility = indicators["volatility"]
            avg_vol = data.get("average_volatility", volatility)
            if volatility > avg_vol * 1.3:
                score *= 0.8  # Reduce signal strength in high volatility
                
        return max(min(score, 1.0), -1.0)  # Clamp between -1 and 1
