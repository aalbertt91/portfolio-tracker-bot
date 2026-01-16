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

