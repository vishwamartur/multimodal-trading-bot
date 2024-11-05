import requests
import logging

class NewsDataFetcher:
    """
    Fetches news data from the News API.
    """

    def __init__(self, api_key: str, api_endpoint: str):
        """
        Initialize the NewsDataFetcher with API key and endpoint.
        
        Args:
            api_key: API key for the News API
            api_endpoint: Endpoint URL for the News API
        """
        self.api_key = api_key
        self.api_endpoint = api_endpoint
        self.logger = logging.getLogger(__name__)

    def fetch_news_data(self, topic: str) -> dict:
        """
        Fetch news data for a given topic.
        
        Args:
            topic: Topic for which to fetch news data
            
        Returns:
            Dictionary containing news data
        """
        try:
            self.logger.info(f"Fetching news data for topic: {topic}")
            response = requests.get(
                self.api_endpoint,
                params={"q": topic, "apiKey": self.api_key}
            )
            response.raise_for_status()
            news_data = response.json()
            self.logger.info(f"News data fetched successfully for topic: {topic}")
            return news_data
        except requests.RequestException as e:
            self.logger.error(f"Error fetching news data: {str(e)}")
            return {}
