# config/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_config():
    """
    Loads the configuration settings for the trading bot.
    Returns a dictionary containing configuration parameters.
    """
    config = {
        "websocket": {
            "url": os.getenv("DHAN_WEBSOCKET_URL", "wss://api.dhan.co/ws/marketData"),
        },
        "api": {
            "api_key": os.getenv("DHAN_API_KEY"),
            "secret_key": os.getenv("DHAN_SECRET_KEY"),
            "chatgpt_api_key": os.getenv("CHATGPT_API_KEY"),
            "weather_api_key": os.getenv("WEATHER_API_KEY"),
            "weather_api_endpoint": os.getenv("WEATHER_API_ENDPOINT"),
            "denodo_host": os.getenv("DENODO_HOST"),
            "denodo_port": os.getenv("DENODO_PORT"),
            "denodo_database": os.getenv("DENODO_DATABASE"),
            "denodo_username": os.getenv("DENODO_USERNAME"),
            "denodo_password": os.getenv("DENODO_PASSWORD"),
            "denodo_jdbc_driver": os.getenv("DENODO_JDBC_DRIVER"),
        },
        "strategy": {
            "futures": {
                "entry_threshold": 0.7,           # Threshold for triggering an entry signal
                "exit_threshold": 0.3,            # Threshold for triggering an exit signal
                "risk_management": {
                    "stop_loss": 0.02,            # Stop-loss as a percentage of entry price
                    "take_profit": 0.05,          # Take-profit as a percentage of entry price
                },
            },
            "options": {
                "entry_threshold": 0.6,
                "exit_threshold": 0.4,
                "risk_management": {
                    "stop_loss": 0.03,
                    "take_profit": 0.06,
                },
            },
        },
        "investment_banking": {
            "tracking_enabled": os.getenv("INVESTMENT_BANKING_TRACKING_ENABLED", "false") == "true",
            "data_source": os.getenv("INVESTMENT_BANKING_DATA_SOURCE", "default_source"),
            "mutual_funds_tracking_enabled": os.getenv("MUTUAL_FUNDS_TRACKING_ENABLED", "false") == "true",
            "mutual_funds_data_source": os.getenv("MUTUAL_FUNDS_DATA_SOURCE", "default_source"),
        },
        "logging": {
            "log_level": os.getenv("LOG_LEVEL", "INFO"),
            "log_file": "logs/trading_bot.log"
        },
        "notifications": {
            "email": {
                "enabled": os.getenv("NOTIFY_EMAIL", "true") == "true",
                "smtp_server": os.getenv("SMTP_SERVER", "smtp.example.com"),
                "smtp_port": int(os.getenv("SMTP_PORT", "587")),
                "email_address": os.getenv("EMAIL_ADDRESS"),
                "email_password": os.getenv("EMAIL_PASSWORD"),
                "recipient_list": os.getenv("RECIPIENT_LIST", "").split(",")
            },
            "sms": {
                "enabled": os.getenv("NOTIFY_SMS", "false") == "true",
                "sms_api_key": os.getenv("SMS_API_KEY"),
                "sms_api_secret": os.getenv("SMS_API_SECRET"),
                "recipient_number": os.getenv("RECIPIENT_NUMBER")
            }
        }
    }

    return config
