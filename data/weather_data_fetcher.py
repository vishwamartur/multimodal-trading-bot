import requests
import logging

class WeatherDataFetcher:
    """
    Fetches weather data from the Weather API.
    """

    def __init__(self, api_key: str, api_endpoint: str):
        """
        Initialize the WeatherDataFetcher with API key and endpoint.
        
        Args:
            api_key: API key for the Weather API
            api_endpoint: Endpoint URL for the Weather API
        """
        self.api_key = api_key
        self.api_endpoint = api_endpoint
        self.logger = logging.getLogger(__name__)

    def fetch_weather_data(self, location: str) -> dict:
        """
        Fetch weather data for a given location.
        
        Args:
            location: Location for which to fetch weather data
            
        Returns:
            Dictionary containing weather data
        """
        try:
            self.logger.info(f"Fetching weather data for location: {location}")
            response = requests.get(
                self.api_endpoint,
                params={"q": location, "appid": self.api_key}
            )
            response.raise_for_status()
            weather_data = response.json()
            self.logger.info(f"Weather data fetched successfully for location: {location}")
            return weather_data
        except requests.RequestException as e:
            self.logger.error(f"Error fetching weather data: {str(e)}")
            return {}
