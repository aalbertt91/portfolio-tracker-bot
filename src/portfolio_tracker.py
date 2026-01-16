# Core
import pandas as pd
import yfinance as yf
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, DateTime, func
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Excel & Reporting
import openpyxl

# Config & Utilities
from dotenv import load_dotenv
import os
import logging
from pathlib import Path

# Requests (for Telegram alerts)
import requests

logging.basicConfig(level=logging.INFO)

load_dotenv()
bottoken = os.getenv("BOT_TOKEN")
chatid = os.getenv("CHAT_ID")

# Create ticker objects
apple = yf.Ticker("AAPL")
tesla = yf.Ticker("TSLA")
amazon = yf.Ticker("AMZN")
nvidia = yf.Ticker("NVDA")
intel = yf.Ticker("INTC")

# Fetch current market prices
appleprice = apple.info.get("regularMarketPrice")
teslaprice = tesla.info.get("regularMarketPrice")
amazonprice = amazon.info.get("regularMarketPrice")
nvidiaprice = nvidia.info.get("regularMarketPrice")
intelprice = intel.info.get("regularMarketPrice")


# Fetch previous trading day's close prices
def get_previous_close(ticker):
    history = ticker.history(period="7d")["Close"].dropna()
    return history.iloc[-2]


apple_close = get_previous_close(apple)
tesla_close = get_previous_close(tesla)
amazon_close = get_previous_close(amazon)
nvidia_close = get_previous_close(nvidia)
intel_close = get_previous_close(intel)

# Create DataFrame for today's prices
data = {
    "Stock": ["AAPL", "TSLA", "AMZN", "NVDA", "INTC"],
    "Price": [appleprice, teslaprice, amazonprice, nvidiaprice, intelprice],
    "Close":
    [apple_close, tesla_close, amazon_close, nvidia_close, intel_close],
    "Date": [datetime.now()] * 5
}

df_today = pd.DataFrame(data)

# Initialize SQLite database
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
db_path = DATA_DIR / "financial_data.db"

engine = create_engine(f"sqlite:///{db_path}", echo=False)
Base = declarative_base()


class StockPrice(Base):
    __tablename__ = "stock_prices"
    id = Column(Integer, primary_key=True)
    stock = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

today = datetime.now().date()
existing_stocks = session.query(
    StockPrice.stock).filter(func.date(StockPrice.date) == today).all()
existing_stocks = [s[0] for s in existing_stocks]

objects = [
    StockPrice(stock=row["Stock"],
               price=row["Price"],
               close=row["Close"],
               date=row["Date"]) for _, row in df_today.iterrows()
    if row["Stock"] not in existing_stocks
]

if objects:
    session.add_all(objects)
    try:
        session.commit()
        logging.info(f"{len(objects)} new stock records inserted.")
    except Exception as e:
        logging.error(
            f"Database commit failed while inserting stock data: {e}")
        session.rollback()
else:
    logging.info("All today's stock data already exists in DB.")

session.close()

Session = sessionmaker(bind=engine)
session = Session()

subquery = session.query(StockPrice.stock,
                         func.max(StockPrice.date).label("max_date")).group_by(
                             StockPrice.stock).subquery()

latest_data = session.query(StockPrice).join(
    subquery, (StockPrice.stock == subquery.c.stock) &
    (StockPrice.date == subquery.c.max_date)).all()

df_prices = pd.DataFrame([(s.stock, s.price, s.close, s.date)
                          for s in latest_data],
                         columns=["Stock", "Price", "Close", "Date"])

print(df_prices)
session.close()

dfcsv = pd.read_csv(DATA_DIR / "portfolio.csv", sep=';')

quantities = dfcsv["quantity"]
print(quantities)

dfcsv = dfcsv.rename(columns={"symbol": "Stock"})

df = pd.merge(df_prices, dfcsv, on="Stock", how="inner")
print(df)

# DAILY PnL
df["daily_price_diff"] = df["Price"] - df["Close"]
df["daily_pnl"] = df["daily_price_diff"] * df["quantity"]
total_daily_pnl = df["daily_pnl"].sum()

# TOTAL PnL
df["total_price_diff"] = df["Price"] - df["entry_price"]
df["total_pnl"] = df["total_price_diff"] * df["quantity"]
total_pnl = df["total_pnl"].sum()

logging.info(f"Total Daily PnL: {total_daily_pnl}")
logging.info(f"Total PnL: {total_pnl}")

dfreport = pd.DataFrame({
    "Stock": df["Stock"],
    "Quantity": df["quantity"],
    "Entry Price": df["entry_price"],
    "Current Price": df["Price"],
    "Daily PnL": df["daily_pnl"],
    "Total PnL": df["total_pnl"]
})

REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Generate Excel report
dfreport.to_excel(REPORTS_DIR / "portfolio_report.xlsx", index=False)

logging.info("Excel report generated successfully.")

hreshold = 1000

# Trigger Telegram alert if PnL exceeds threshold
if total_pnl > threshold:
    message = f"Total PnL is above {threshold}! Current PnL: {total_pnl:.2f}"
    requests.post(f"https://api.telegram.org/bot{bottoken}/sendMessage",
                  data={
                      "chat_id": chatid,
                      "text": message
                  })
    logging.info("Telegram alert sent!")
else:
    logging.info("PnL threshold not reached.")
