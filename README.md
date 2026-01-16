# Portfolio Tracker & PnL Monitoring Bot

## Project Objective

This project is a Python-based portfolio tracking and profit & loss (PnL) monitoring system designed to automate the collection of market prices, store historical price data, calculate portfolio performance metrics, and generate automated reports and alerts.

The system retrieves near real-time (intraday) and historical stock prices using the yfinance API, stores daily price snapshots in a SQLite database, calculates daily and total PnL based on portfolio positions, generates Excel reports, and sends Telegram alerts when predefined PnL thresholds are exceeded.

The project aims to simulate a lightweight portfolio monitoring tool similar to those used in professional trading and risk management environments and is intended as a simplified prototype and learning-oriented system rather than a production trading platform.

## Technologies Used

Python: Core language for data processing, automation, and orchestration.

Pandas: Used for data manipulation, portfolio calculations, and report generation.

Yfinance: Retrieves intraday and historical stock market prices from Yahoo Finance.

SQLAlchemy: ORM-based interaction with the SQLite database.

SQLite: Lightweight relational database for storing daily stock price snapshots.

Logging: Tracks execution flow, database operations, and alert conditions.

Requests: Sends HTTP requests to the Telegram Bot API for automated PnL alerts.

Excel (openpyxl): Generates structured portfolio performance reports.

Dotenv: Manages sensitive configuration values such as API tokens.

## How to Run

1. Install the required dependencies:

pip install -r requirements.txt


2. Configure environment variables in a .env file:

BOT_TOKEN=your_telegram_bot_token 
CHAT_ID=your_chat_id


3. Run the portfolio tracker script:

python src/portfolio_tracker.py


4. After execution, check the SQLite database (financial_data.db) for stored stock prices, review the terminal output for portfolio PnL calculations, verify the generated portfolio_report.xlsx file, and confirm that a Telegram alert is sent if the defined PnL threshold is exceeded.

## Why This Is Valuable for a Hedge Fund

- Automates portfolio monitoring and reduces manual tracking effort

- Demonstrates end-to-end data flow: API → database → analytics → reporting → alerts

- Simulates real-world portfolio PnL calculation logic

- Provides a foundation for:

   - Risk monitoring

   - Strategy performance tracking

   - Alert-driven decision-making

- Easily extensible to larger portfolios, additional asset classes, or scheduled execution
