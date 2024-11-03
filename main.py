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

# Load environment variables and validate required keys
load_dotenv()
required_env_vars = [
    "DHAN_API_KEY",
    "DHAN_SECRET_KEY",
    "CHATGPT_API_KEY"
]
for var in required_env_vars:
    if not os.getenv(var):
        raise ValueError(f"Missing required environment variable: {var}")

# Set up logging with enhanced configuration
logger = setup_logging()
logger.info("Starting trading bot...")

# Load and validate configuration settings
config = load_config()

async def process_market_data(
    data: Dict,
    data_fetcher: DataFetcher,
    futures_strategy: FuturesStrategy,
    options_strategy: OptionsStrategy,
    chatgpt_integration: ChatGPTIntegration,
    order_executor: OrderExecution,
    notifier: Notifier,
    investment_banking_tracker: InvestmentBankingTracker
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

        futures_signal, options_signal, sentiment, _ = await asyncio.gather(
            futures_task, options_task, sentiment_task, investment_banking_task
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
        notifier = Notifier(config["notifications"])
        order_executor = OrderExecution(api_key=os.getenv("DHAN_API_KEY"))
        investment_banking_tracker = InvestmentBankingTracker(config["investment_banking"])

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
                investment_banking_tracker
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
