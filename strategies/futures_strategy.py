import logging
from typing import Dict, Any
from datetime import datetime
from strategies.base_strategy import BaseStrategy, StrategyResult
from models.sentiment_analysis import SentimentAnalyzer
from models.chatgpt_integration import ChatGPTIntegration
from data.weather_data_fetcher import WeatherDataFetcher
from data.news_data_fetcher import NewsDataFetcher

class FuturesStrategy(BaseStrategy):
    """
    Strategy for trading futures contracts using sentiment analysis, technical indicators, weather data, and news data.
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
        self.weather_fetcher = WeatherDataFetcher(
            api_key=config["api"]["weather_api_key"],
            api_endpoint=config["api"]["weather_api_endpoint"]
        )
        self.news_fetcher = NewsDataFetcher(
            api_key=config["api"]["news_api_key"],
            api_endpoint=config["api"]["news_api_endpoint"]
        )
        
    async def generate_signal(self, market_data: Dict[str, Any]) -> StrategyResult:
        """
        Generate trading signal for futures based on market data, sentiment, weather data, and news data.
        
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
        
        # Fetch and process weather data
        weather_data = await self.weather_fetcher.fetch_weather_data("New York")  # Example location
        weather_score = self._analyze_weather_data(weather_data)
        
        # Fetch and process news data
        news_data = await self.news_fetcher.fetch_news_data("market")
        news_score = self._analyze_news_data(news_data)
        
        # Combine signals
        signals = {
            "sentiment": sentiment.score,
            "chatgpt": chatgpt_score,
            "technical": self._analyze_technical_indicators(market_data),
            "weather": weather_score,
            "news": news_score
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

    def _analyze_weather_data(self, weather_data: Dict[str, Any]) -> float:
        """
        Analyze weather data for trading signals.
        
        Args:
            weather_data: Dictionary containing weather data
            
        Returns:
            Weather analysis score between -1 and 1
        """
        score = 0.0
        temperature = weather_data.get("main", {}).get("temp")
        weather_description = weather_data.get("weather", [{}])[0].get("description")
        
        if temperature and temperature < 0:  # Example condition for cold weather
            score -= 0.2
        if weather_description and "rain" in weather_description.lower():
            score -= 0.3  # Example condition for rainy weather
        
        return max(min(score, 1.0), -1.0)  # Clamp between -1 and 1

    def _analyze_news_data(self, news_data: Dict[str, Any]) -> float:
        """
        Analyze news data for trading signals.
        
        Args:
            news_data: Dictionary containing news data
            
        Returns:
            News analysis score between -1 and 1
        """
        score = 0.0
        articles = news_data.get("articles", [])
        
        for article in articles:
            sentiment = article.get("sentiment", 0)
            score += sentiment
        
        if articles:
            score /= len(articles)  # Average sentiment score
        
        return max(min(score, 1.0), -1.0)  # Clamp between -1 and 1
