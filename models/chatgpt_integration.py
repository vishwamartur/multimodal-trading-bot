import logging
import aiohttp # type: ignore
from typing import Dict, Any
from datetime import datetime

class ChatGPTIntegration:
    """
    Handles integration with ChatGPT API for market sentiment analysis.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize ChatGPT integration with configuration settings.
        
        Args:
            config: Dictionary containing configuration parameters including API key
        """
        self.api_key = config["api"]["chatgpt_api_key"]
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing ChatGPT Integration")
        
    async def analyze_sentiment_async(self, market_data: Dict[str, Any]) -> float:
        """
        Analyze market sentiment using ChatGPT API asynchronously.
        
        Args:
            market_data: Dictionary containing processed market data
            
        Returns:
            Float between -1 and 1 representing sentiment (negative to positive)
        """
        try:
            # Format market data for prompt
            prompt = self._format_prompt(market_data)
            
            # Call ChatGPT API
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "gpt-3.5-turbo",
                        "messages": [
                            {"role": "system", "content": "You are a market sentiment analyzer."},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.3
                    }
                ) as response:
                    result = await response.json()
                    
            # Parse response and extract sentiment score
            sentiment = self._parse_sentiment(result)
            self.logger.info(f"Sentiment analysis complete: {sentiment}")
            return sentiment
            
        except Exception as e:
            self.logger.error(f"Error analyzing sentiment: {str(e)}")
            return 0.0  # Neutral sentiment on error
            
    def _format_prompt(self, market_data: Dict[str, Any]) -> str:
        """
        Format market data into a prompt for ChatGPT.
        
        Args:
            market_data: Dictionary containing market data
            
        Returns:
            Formatted prompt string
        """
        return f"""Analyze the market sentiment for {market_data.get('symbol', 'unknown')}:
        Price: {market_data.get('price')}
        Volume: {market_data.get('volume')}
        High: {market_data.get('high')}
        Low: {market_data.get('low')}
        Time: {market_data.get('timestamp', datetime.now().isoformat())}
        
        Provide a sentiment score between -1 (extremely bearish) and 1 (extremely bullish).
        """
        
    def _parse_sentiment(self, api_response: Dict[str, Any]) -> float:
        """
        Parse ChatGPT API response to extract sentiment score.
        
        Args:
            api_response: Dictionary containing API response
            
        Returns:
            Sentiment score between -1 and 1
        """
        try:
            content = api_response["choices"][0]["message"]["content"]
            # Extract numerical score from response
            # This is a simple implementation - could be enhanced with more sophisticated parsing
            for line in content.split('\n'):
                if any(word in line.lower() for word in ['score', 'sentiment']):
                    numbers = [float(s) for s in line.split() if s.replace('-', '').replace('.', '').isdigit()]
                    if numbers:
                        return max(min(numbers[0], 1.0), -1.0)  # Clamp between -1 and 1
            
            return 0.0  # Default to neutral if no clear sentiment found
            
        except Exception as e:
            self.logger.error(f"Error parsing sentiment response: {str(e)}")
            return 0.0
