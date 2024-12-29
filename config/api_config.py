# config/api_config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class APIConfig:
    """
    Configuration class for managing API keys and endpoint URLs.
    """

    def __init__(self):
        # Dhan API configurations
        self.dhan_api_key = os.getenv("DHAN_API_KEY")
        self.dhan_secret_key = os.getenv("DHAN_SECRET_KEY")
        self.dhan_base_url = "https://api.dhan.co"  # Base URL for Dhan API
        self.dhan_ws_url = os.getenv("DHAN_WEBSOCKET_URL", "wss://api.dhan.co/ws/marketData")

        # ChatGPT API configurations
        self.chatgpt_api_key = os.getenv("CHATGPT_API_KEY")
        self.chatgpt_endpoint = "https://api.openai.com/v1/chat/completions"  # Endpoint for ChatGPT API

        # Weather API configurations
        self.weather_api_key = os.getenv("WEATHER_API_KEY")
        self.weather_api_endpoint = os.getenv("WEATHER_API_ENDPOINT")

        # News API configurations
        self.news_api_key = os.getenv("NEWS_API_KEY")
        self.news_api_endpoint = os.getenv("NEWS_API_ENDPOINT")

        # Mutual Funds API configurations
        self.mutual_funds_api_key = os.getenv("MUTUAL_FUNDS_API_KEY")
        self.mutual_funds_api_endpoint = os.getenv("MUTUAL_FUNDS_API_ENDPOINT")

        # Denodo API configurations
        self.denodo_host = os.getenv("DENODO_HOST")
        self.denodo_port = os.getenv("DENODO_PORT")
        self.denodo_database = os.getenv("DENODO_DATABASE")
        self.denodo_username = os.getenv("DENODO_USERNAME")
        self.denodo_password = os.getenv("DENODO_PASSWORD")
        self.denodo_jdbc_driver = os.getenv("DENODO_JDBC_DRIVER")

        # Additional API configurations can be added here
        # Example for other market data or sentiment analysis APIs:
        # self.other_api_key = os.getenv("OTHER_API_KEY")
        # self.other_api_endpoint = "https://api.otherprovider.com/endpoint"

    def dhan_headers(self):
        """
        Returns headers required for making authenticated requests to the Dhan API.
        """
        return {
            "Authorization": f"Bearer {self.dhan_api_key}",
            "Content-Type": "application/json",
        }

    def chatgpt_headers(self):
        """
        Returns headers required for making requests to the ChatGPT API.
        """
        return {
            "Authorization": f"Bearer {self.chatgpt_api_key}",
            "Content-Type": "application/json",
        }

    def weather_headers(self):
        """
        Returns headers required for making requests to the Weather API.
        """
        return {
            "Authorization": f"Bearer {self.weather_api_key}",
            "Content-Type": "application/json",
        }

    def news_headers(self):
        """
        Returns headers required for making requests to the News API.
        """
        return {
            "Authorization": f"Bearer {self.news_api_key}",
            "Content-Type": "application/json",
        }

    def mutual_funds_headers(self):
        """
        Returns headers required for making requests to the Mutual Funds API.
        """
        return {
            "Authorization": f"Bearer {self.mutual_funds_api_key}",
            "Content-Type": "application/json",
        }

    def denodo_headers(self):
        """
        Returns headers required for making requests to the Denodo API.
        """
        return {
            "Authorization": f"Bearer {self.denodo_username}:{self.denodo_password}",
            "Content-Type": "application/json",
        }

    def get_dhan_endpoint(self, path):
        """
        Constructs and returns a full Dhan API endpoint for a given path.
        """
        return f"{self.dhan_base_url}{path}"

    def get_chatgpt_endpoint(self):
        """
        Returns the ChatGPT API endpoint.
        """
        return self.chatgpt_endpoint

    def get_weather_endpoint(self):
        """
        Returns the Weather API endpoint.
        """
        return self.weather_api_endpoint

    def get_news_endpoint(self):
        """
        Returns the News API endpoint.
        """
        return self.news_api_endpoint

    def get_mutual_funds_endpoint(self):
        """
        Returns the Mutual Funds API endpoint.
        """
        return self.mutual_funds_api_endpoint

    def get_denodo_endpoint(self):
        """
        Returns the Denodo API endpoint.
        """
        return f"jdbc:denodo://{self.denodo_host}:{self.denodo_port}/{self.denodo_database}"
