# Portfolio Tracker & PnL Monitoring Bot

This repository contains a comprehensive Python-based automation system designed to track financial portfolios in real-time. It automates market data collection, calculates daily and total PnL metrics, manages a historical price database, and triggers automated alerts based on portfolio performance.

# 📌 Problem & Solution
Manually tracking multiple stock positions and calculating real-time P&L across different entry points is labor-intensive and prone to calculation errors. Investors need a centralized system that bridges the gap between live market data, historical records, and instant risk notifications.

This automation bot:

Eliminates manual price updates by fetching live market data via the Yahoo Finance API.

Enforces data persistence by storing daily price snapshots in a structured SQLite database using SQLAlchemy ORM.

Automates complex P&L calculations by merging live market prices with static portfolio positions (CSV).

Streamlines reporting and risk management through automated Excel generation and real-time Telegram alerts for PnL thresholds.

# 🛠 Tech Stack
**Python:** Core engine for data orchestration and automation.

**Pandas:** For high-performance data manipulation and PnL calculations.

**yFinance:** To retrieve intraday and historical market data.

**SQLAlchemy (ORM):** For database schema management and secure data persistence.

**SQLite:** Lightweight relational storage for historical price snapshots.

**Requests:** To facilitate real-time communication with the Telegram Bot API.

**Excel (openpyxl):** For generating structured portfolio performance reports.

# ⚙️ Core Automation Workflow
**Data Ingestion:** Fetches current and previous close prices for the target ticker list.

**Persistence:** Checks for existing records and commits new price snapshots to the SQLite database.

**Analytics:** Merges database records with portfolio CSV data to calculate Daily and Total PnL.

**Reporting & Alerts:** Generates a professional Excel report and triggers a Telegram notification if PnL thresholds are exceeded.

# 📊 Example Output
Upon execution, the bot provides a structured summary of the portfolio status and execution flow:

```
INFO:root:5 new stock records inserted.
INFO:root:Total Daily PnL: 105.35
INFO:root:Total PnL: 479.14
INFO:root:Excel report generated successfully.
INFO:root:PnL threshold not reached.

   Stock   Price   Close  Quantity  Entry Price  Daily PnL  Total PnL
0   AAPL  260.48  260.49         5       234.00      -0.05     132.40
1   TSLA  348.95  345.62        10       403.00      33.30    -540.50
2   AMZN  238.38  233.65         8       218.00      37.84     163.04
```

# 🚀 How to Run
1.Configure your .env file with BOT_TOKEN and CHAT_ID.



2.Install dependencies:

```
pip install -r requirements.txt
```

3.Run the automation:


```
python src/portfolio_tracker.py
```
