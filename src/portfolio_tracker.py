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