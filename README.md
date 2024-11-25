# NSE Trading Bot

A robust, high-performance cryptocurrency trading bot built in Python that leverages WebSocket connections for real-time market data and lightning-fast order execution.

## Key Features

- **Real-time Market Data**: Stream live market data via WebSocket connections with minimal latency
- **Advanced Order Management**: 
  - Automated order execution and tracking
  - Support for multiple order types (market, limit, stop)
  - Order validation and risk checks
- **Risk Management**:
  - Configurable position sizing and risk limits
  - Pre-trade risk validation
  - Maximum order size restrictions
- **Trading Strategy Framework**:
  - Easily implement and backtest custom strategies
  - Multiple built-in technical indicators
  - Strategy parameter optimization
- **Enterprise-grade Infrastructure**:
  - Comprehensive logging system
  - Real-time notifications via email, Slack and Telegram
  - Error handling and automatic reconnection
- **Multi-Exchange Support**:
  - Unified interface for multiple exchanges
  - Exchange-specific implementations
  - Easy addition of new exchanges

## Getting Started

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. Clone the repository:

```sh
git clone https://github.com/yourusername/nse-trading-bot.git
cd nse-trading-bot
```

2. Install dependencies:

```sh
pip install -r requirements.txt
```

3. Set up environment variables:

Create a `.env` file in the root directory of the project and add the following environment variables:

```sh
# API keys
DHAN_API_KEY=your_dhan_api_key
DHAN_SECRET_KEY=your_dhan_secret_key
CHATGPT_API_KEY=your_chatgpt_api_key

# WebSocket URL (Optional if the default URL is used)
DHAN_WEBSOCKET_URL=wss://api.dhan.co/ws/marketData

# Logging
LOG_LEVEL=INFO

# Email Notifications
NOTIFY_EMAIL=true
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
EMAIL_ADDRESS=your_email@example.com
EMAIL_PASSWORD=your_email_password
RECIPIENT_LIST=recipient1@example.com,recipient2@example.com

# SMS Notifications (Optional)
NOTIFY_SMS=false
SMS_API_KEY=your_sms_api_key
SMS_API_SECRET=your_sms_api_secret
RECIPIENT_NUMBER=1234567890

# Logging configurations
LOG_FILE_PATH=logs/trading_bot.log
LOG_LEVEL=INFO

# Telegram Notifications
TELEGRAM_BOT_API_KEY=your_telegram_bot_api_key
TELEGRAM_CHAT_ID=your_telegram_chat_id

# Weather API
WEATHER_API_KEY=your_weather_api_key
WEATHER_API_ENDPOINT=your_weather_api_endpoint

# News API
NEWS_API_KEY=your_news_api_key
NEWS_API_ENDPOINT=your_news_api_endpoint
```

## CI/CD Pipeline Configuration

### Setting Up CI/CD Pipeline

The CI/CD pipeline is configured using GitHub Actions. The workflow file is located at `.github/workflows/ci-cd.yml`.

### Environment Variables for Deployment

Ensure the following environment variables are set in your GitHub repository secrets:

- `DHAN_API_KEY`
- `DHAN_SECRET_KEY`
- `CHATGPT_API_KEY`
- `TELEGRAM_BOT_API_KEY`
- `TELEGRAM_CHAT_ID`
- `WEATHER_API_KEY`
- `WEATHER_API_ENDPOINT`
- `NEWS_API_KEY`
- `NEWS_API_ENDPOINT`

### Running the CI/CD Pipeline

The CI/CD pipeline is triggered on every push to the `main` branch and on pull requests targeting the `main` branch. It includes jobs for testing and deployment.

To manually trigger the pipeline, you can use the "Run workflow" button in the Actions tab of your GitHub repository.

### Deployment Commands

The deployment step in the CI/CD pipeline includes commands to deploy the application to a specified environment. Ensure you have the necessary deployment scripts and configurations in place.

