# main.py

import asyncio
import logging
import os
from typing import Dict, List
from dotenv import load_dotenv # type: ignore
from config.config import load_config
from config.logging_config import setup_logging
from websocket.websocket_client import WebSocketClient
from data.data_fetcher import DataFetcher
from strategies.futures_strategy import FuturesStrategy
from strategies.options_strategy import OptionsStrategy
from models.chatgpt_integration import ChatGPTIntegration
from utils.notifier import Notifier
from utils.logger import setup_logger
from websocket.order_execution import OrderExecution
from utils.backtest import Backtester
from data.investment_banking_tracker import InvestmentBankingTracker
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from data.weather_data_fetcher import WeatherDataFetcher
from data.news_data_fetcher import NewsDataFetcher
from data.mutual_funds_tracker import MutualFundsTracker

# Load environment variables and validate required keys
load_dotenv()
required_env_vars = [
    "DHAN_API_KEY",
    "DHAN_SECRET_KEY",
    "CHATGPT_API_KEY",
    "TELEGRAM_BOT_API_KEY",
    "TELEGRAM_CHAT_ID",
    "WEATHER_API_KEY",
    "WEATHER_API_ENDPOINT",
    "NEWS_API_KEY",
    "NEWS_API_ENDPOINT"
]
for var in required_env_vars:
    if not os.getenv(var):
        raise ValueError(f"Missing required environment variable: {var}")

# Set up logging with enhanced configuration
logger = setup_logging()
logger.info("Starting trading bot...")

# Load and validate configuration settings
config = load_config()

# Initialize Telegram bot
telegram_bot = telegram.Bot(token=os.getenv("TELEGRAM_BOT_API_KEY"))

async def process_market_data(
    data: Dict,
    data_fetcher: DataFetcher,
    futures_strategy: FuturesStrategy,
    options_strategy: OptionsStrategy,
    chatgpt_integration: ChatGPTIntegration,
    order_executor: OrderExecution,
    notifier: Notifier,
    investment_banking_tracker: InvestmentBankingTracker,
    weather_fetcher: WeatherDataFetcher,
    news_fetcher: NewsDataFetcher,
    mutual_funds_tracker: MutualFundsTracker
) -> None:
    """
    Process incoming market data asynchronously and execute trading strategies
    """
    try:
        logger.info("Processing new market data")
        processed_data = await data_fetcher.process_data_async(data)

        # Run strategies concurrently
        futures_task = asyncio.create_task(futures_strategy.evaluate_async(processed_data))
        options_task = asyncio.create_task(options_strategy.evaluate_async(processed_data))
        sentiment_task = asyncio.create_task(chatgpt_integration.analyze_sentiment_async(processed_data))
        investment_banking_task = asyncio.create_task(investment_banking_tracker.process_investment_banking_trades(data))
        weather_task = asyncio.create_task(weather_fetcher.fetch_and_process_weather_data("New York"))
        news_task = asyncio.create_task(news_fetcher.fetch_news_data("market"))
        mutual_funds_task = asyncio.create_task(mutual_funds_tracker.process_mutual_funds_trades(data))

        futures_signal, options_signal, sentiment, _, weather_data, news_data, _ = await asyncio.gather(
            futures_task, options_task, sentiment_task, investment_banking_task, weather_task, news_task, mutual_funds_task
        )

        # Handle futures signals
        if futures_signal:
            logger.info(f"Futures Strategy Signal: {futures_signal}")
            await order_executor.execute_order_async(futures_signal)
            await notifier.send_async(f"Futures trade executed: {futures_signal}")

        # Handle options signals  
        if options_signal:
            logger.info(f"Options Strategy Signal: {options_signal}")
            await order_executor.execute_order_async(options_signal)
            await notifier.send_async(f"Options trade executed: {options_signal}")

        # Process sentiment analysis
        if sentiment:
            logger.info(f"AI Sentiment Analysis: {sentiment}")
            await notifier.send_async(f"Market sentiment update: {sentiment}")

        # Process weather data
        if weather_data:
            logger.info(f"Weather Data: {weather_data}")
            await notifier.send_async(f"Weather update: {weather_data}")

        # Process news data
        if news_data:
            logger.info(f"News Data: {news_data}")
            await notifier.send_async(f"News update: {news_data}")

        # Calculate profit and loss
        executed_price = futures_signal.get("price") if futures_signal else options_signal.get("price")
        current_price = processed_data.get("price")
        profit_loss = current_price - executed_price
        logger.info(f"Profit/Loss: {profit_loss}")
        await notifier.send_async(f"Profit/Loss update: {profit_loss}")

    except Exception as e:
        logger.error(f"Error processing market data: {str(e)}")
        await notifier.send_async(f"Error in market data processing: {str(e)}")

async def main():
    """
    Main async function to run the trading bot
    """
    logger.info("Starting the Multimodal Trading Bot...")

    try:
        # Initialize core components
        websocket_client = WebSocketClient(
            url=config["websocket"]["url"],
            api_key=os.getenv("DHAN_API_KEY"),
            secret_key=os.getenv("DHAN_SECRET_KEY")
        )
        data_fetcher = DataFetcher(api_key=os.getenv("DHAN_API_KEY"))
        
        # Load and validate historical data
        historical_data = await data_fetcher.load_historical_data_async()
        if not historical_data:
            raise ValueError("Failed to load historical data")
        logger.info("Historical data loaded successfully")

        # Initialize strategy components
        futures_strategy = FuturesStrategy(config["strategy"]["futures"])
        options_strategy = OptionsStrategy(config["strategy"]["options"])
        chatgpt_integration = ChatGPTIntegration(api_key=os.getenv("CHATGPT_API_KEY"))
        notifier = Notifier(config["notifications"], telegram_bot)
        order_executor = OrderExecution(api_key=os.getenv("DHAN_API_KEY"))
        investment_banking_tracker = InvestmentBankingTracker(config["investment_banking"])
        weather_fetcher = WeatherDataFetcher(
            api_key=config["api"]["weather_api_key"],
            api_endpoint=config["api"]["weather_api_endpoint"]
        )
        news_fetcher = NewsDataFetcher(
            api_key=config["api"]["news_api_key"],
            api_endpoint=config["api"]["news_api_endpoint"]
        )
        mutual_funds_tracker = MutualFundsTracker(config["investment_banking"])

        # Run backtesting with performance metrics
        backtester = Backtester()
        logger.info("Starting backtesting on historical data...")
        backtest_results = await backtester.run_backtest_async(
            historical_data, 
            [futures_strategy, options_strategy]
        )
        logger.info(f"Backtesting completed. Results: {backtest_results}")

        # Define WebSocket callback
        async def on_message(data: Dict) -> None:
            await process_market_data(
                data,
                data_fetcher,
                futures_strategy,
                options_strategy,
                chatgpt_integration,
                order_executor,
                notifier,
                investment_banking_tracker,
                weather_fetcher,
                news_fetcher,
                mutual_funds_tracker
            )

        # Start WebSocket connection
        await websocket_client.start_async(on_message=on_message)
        logger.info("WebSocket connection established")

        # Keep the bot running
        while True:
            await asyncio.sleep(1)

    except Exception as e:
        logger.error(f"Critical error in trading bot: {str(e)}")
        await notifier.send_async(f"Trading bot error: {str(e)}")
        raise
    finally:
        await websocket_client.close_async()
        logger.info("Trading bot shutdown complete")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Received shutdown signal, closing trading bot...")
    except Exception as e:
        logger.critical(f"Fatal error: {str(e)}")
