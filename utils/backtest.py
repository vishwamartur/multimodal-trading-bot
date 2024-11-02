import logging
from typing import Dict, Any, List
from datetime import datetime
from strategies.base_strategy import StrategyResult

class Backtest:
    """
    Class for backtesting trading strategies using historical market data.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize backtester.
        
        Args:
            config: Dictionary containing backtest configuration parameters
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.results: List[Dict[str, Any]] = []

    async def run(self, strategy, historical_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Run backtest using provided strategy and historical data.
        
        Args:
            strategy: Trading strategy instance to test
            historical_data: List of historical market data points
            
        Returns:
            List of backtest results including signals and simulated trades
        """
        self.logger.info("Starting backtest run")
        
        for data_point in historical_data:
            # Generate trading signal
            signal: StrategyResult = await strategy.generate_signal(data_point)
            
            # Simulate trade execution
            trade_result = self._simulate_trade(signal, data_point)
            
            # Store results
            self.results.append({
                "timestamp": data_point["timestamp"],
                "symbol": data_point["symbol"],
                "price": data_point["price"],
                "signal": signal.signal,
                "confidence": signal.confidence,
                "trade_result": trade_result
            })
            
        return self.results

    def _simulate_trade(self, signal: StrategyResult, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate trade execution based on strategy signal.
        
        Args:
            signal: Strategy signal result
            market_data: Current market data point
            
        Returns:
            Dictionary containing trade simulation results
        """
        # Simple trade simulation - can be expanded based on requirements
        trade_size = self.config.get("trade_size", 1.0)
        slippage = self.config.get("slippage", 0.001)
        
        if abs(signal.signal) < self.config.get("min_signal_threshold", 0.2):
            return {"action": "hold", "size": 0, "price": market_data["price"]}
            
        action = "buy" if signal.signal > 0 else "sell"
        executed_price = market_data["price"] * (1 + slippage if action == "buy" else 1 - slippage)
        
        return {
            "action": action,
            "size": trade_size,
            "price": executed_price,
            "slippage": slippage
        }

    def calculate_metrics(self) -> Dict[str, float]:
        """
        Calculate backtest performance metrics.
        
        Returns:
            Dictionary containing performance metrics
        """
        if not self.results:
            return {}
            
        total_trades = len([r for r in self.results if r["trade_result"]["action"] != "hold"])
        winning_trades = len([r for r in self.results if self._is_winning_trade(r)])
        
        return {
            "total_trades": total_trades,
            "win_rate": winning_trades / total_trades if total_trades > 0 else 0,
            "avg_return": self._calculate_average_return(),
            "sharpe_ratio": self._calculate_sharpe_ratio()
        }
        
    def _is_winning_trade(self, result: Dict[str, Any]) -> bool:
        """Helper method to determine if a trade was profitable"""
        trade = result["trade_result"]
        if trade["action"] == "hold":
            return False
        return (trade["action"] == "buy" and result["price"] > trade["price"]) or \
               (trade["action"] == "sell" and result["price"] < trade["price"])
               
    def _calculate_average_return(self) -> float:
        """Calculate average return across all trades"""
        if not self.results:
            return 0.0
        returns = [self._calculate_trade_return(r) for r in self.results]
        return sum(returns) / len(returns)
        
    def _calculate_sharpe_ratio(self) -> float:
        """Calculate Sharpe ratio of trading strategy"""
        if not self.results:
            return 0.0
        returns = [self._calculate_trade_return(r) for r in self.results]
        if not returns:
            return 0.0
        avg_return = sum(returns) / len(returns)
        std_dev = (sum((r - avg_return) ** 2 for r in returns) / len(returns)) ** 0.5
        return avg_return / std_dev if std_dev > 0 else 0.0
        
    def _calculate_trade_return(self, result: Dict[str, Any]) -> float:
        """Calculate return for a single trade"""
        trade = result["trade_result"]
        if trade["action"] == "hold":
            return 0.0
        return (result["price"] - trade["price"]) / trade["price"] * \
               (1 if trade["action"] == "buy" else -1)
