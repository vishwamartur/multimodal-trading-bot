import logging
from typing import Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass

@dataclass
class StrategyResult:
    timestamp: datetime
    symbol: str
    signal: float  # Signal strength between -1 (strong sell) and 1 (strong buy)
    confidence: float  # Confidence level between 0 and 1
    metadata: Optional[Dict[str, Any]] = None

class BaseStrategy:
    """
    Base class for trading strategies. Implements common functionality and interface
    that specific strategies should follow.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the strategy with configuration settings.
        
        Args:
            config: Dictionary containing strategy configuration parameters
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Initializing {self.__class__.__name__}")

    async def generate_signal(self, market_data: Dict[str, Any]) -> StrategyResult:
        """
        Generate trading signal based on market data. Must be implemented by subclasses.
        
        Args:
            market_data: Dictionary containing processed market data
            
        Returns:
            StrategyResult containing signal and metadata
        """
        raise NotImplementedError("Subclasses must implement generate_signal()")
        
    def _validate_market_data(self, market_data: Dict[str, Any]) -> bool:
        """
        Validate that required market data fields are present.
        
        Args:
            market_data: Dictionary containing market data to validate
            
        Returns:
            Boolean indicating if data is valid
        """
        required_fields = ["symbol", "price", "timestamp"]
        return all(field in market_data for field in required_fields)
        
    def _calculate_confidence(self, signals: Dict[str, float]) -> float:
        """
        Calculate confidence level in strategy signals.
        
        Args:
            signals: Dictionary containing individual signal components
            
        Returns:
            Confidence score between 0 and 1
        """
        if not signals:
            return 0.0
            
        # Base confidence on signal agreement
        values = list(signals.values())
        avg_signal = sum(values) / len(values)
        variance = sum((x - avg_signal) ** 2 for x in values) / len(values)
        
        # Higher variance = lower confidence
        confidence = 1.0 - min(variance, 1.0)
        
        return confidence
