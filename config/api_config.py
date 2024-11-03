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
