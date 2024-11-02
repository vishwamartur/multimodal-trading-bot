import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import numpy as np # type: ignore
from dataclasses import dataclass

@dataclass
class ProcessedData:
    timestamp: datetime
    symbol: str
    price: float
    volume: Optional[float] = None
    indicators: Optional[Dict[str, float]] = None
    metadata: Optional[Dict[str, Any]] = None

class DataProcessor:
    """
    Handles processing and transformation of market data.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the DataProcessor with configuration settings.
        
        Args:
            config: Dictionary containing configuration parameters
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing DataProcessor")

    def process_raw_data(self, raw_data: Dict[str, Any]) -> ProcessedData:
        """
        Process raw market data into standardized format.
        
        Args:
            raw_data: Dictionary containing raw market data
            
        Returns:
            ProcessedData object containing processed market data
        """
        try:
            self.logger.debug("Processing raw market data")
            
            # Extract basic fields
            processed = ProcessedData(
                timestamp=datetime.fromisoformat(raw_data.get("timestamp", datetime.now().isoformat())),
                symbol=raw_data.get("symbol", ""),
                price=float(raw_data.get("price", 0.0)),
                volume=float(raw_data.get("volume", 0.0))
            )

            # Calculate technical indicators
            indicators = self._calculate_indicators(raw_data)
            processed.indicators = indicators

            # Add any additional metadata
            processed.metadata = {
                "source": raw_data.get("source"),
                "data_quality": self._assess_data_quality(raw_data)
            }

            return processed

        except Exception as e:
            self.logger.error(f"Error processing market data: {str(e)}")
            raise

    def _calculate_indicators(self, data: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate technical indicators from raw data.
        
        Args:
            data: Dictionary containing market data
            
        Returns:
            Dictionary containing calculated indicators
        """
        indicators = {}
        
        try:
            if all(k in data for k in ["high", "low", "close"]):
                # Calculate RSI if enough data points available
                if "price_history" in data:
                    prices = data["price_history"]
                    if len(prices) >= 14:  # Minimum points needed for RSI
                        indicators["rsi"] = self._calculate_rsi(prices)

                # Calculate basic indicators
                indicators["hl_avg"] = (float(data["high"]) + float(data["low"])) / 2
                indicators["volatility"] = float(data["high"]) - float(data["low"])

        except Exception as e:
            self.logger.warning(f"Error calculating indicators: {str(e)}")
            
        return indicators

    def _calculate_rsi(self, prices: List[float], periods: int = 14) -> float:
        """
        Calculate the Relative Strength Index.
        
        Args:
            prices: List of historical prices
            periods: Number of periods for RSI calculation
            
        Returns:
            Calculated RSI value
        """
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains[:periods])
        avg_loss = np.mean(losses[:periods])
        
        if avg_loss == 0:
            return 100
            
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return float(rsi)

    def _assess_data_quality(self, data: Dict[str, Any]) -> float:
        """
        Assess the quality and reliability of the data.
        
        Args:
            data: Dictionary containing market data
            
        Returns:
            Quality score between 0 and 1
        """
        required_fields = ["symbol", "price", "timestamp"]
        optional_fields = ["volume", "high", "low", "open", "close"]
        
        # Check required fields
        quality_score = sum(1 for field in required_fields if field in data) / len(required_fields)
        
        # Add bonus for optional fields
        quality_score += 0.2 * (sum(1 for field in optional_fields if field in data) / len(optional_fields))
        
        # Cap at 1.0
        return min(1.0, quality_score)
