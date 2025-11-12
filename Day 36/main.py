import os
from datetime import timedelta

from dotenv import load_dotenv
import requests
import datetime as dt
import pytz
from bot import Bot

load_dotenv()
STOCK = "AAPL"
COMPANY_NAME = "Apple Inc."
STOCK_API_KEY = os.getenv("API_KEY")
URL = os.getenv("API_URL")
NEWS_KEY = os.getenv("API_KEY_NEWS")
NEWS_URL = os.getenv("API_NEWS_URL")

def get_percentage():

    today_date = str(dt.datetime.now(pytz.utc) - timedelta(days=1))[:10] + " 16:00:00"
    yesterday_date = str(dt.datetime.now(pytz.utc) - timedelta(days=2))[:10] + " 16:00:00"



    url_parameters = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": STOCK,
        "interval": "60min",
        "extended_hours": False,
        "apikey": STOCK_API_KEY
    }

    response = requests.get(url=URL, params=url_parameters)
    response.raise_for_status()

    data_today = float(response.json()["Time Series (60min)"][today_date]["4. close"])
    data_yesterday = float(response.json()["Time Series (60min)"][yesterday_date]["4. close"])
    return 100 * (data_today - data_yesterday) / data_yesterday

def get_news():
    url_parameters = {
        "q": COMPANY_NAME,
        "language" : "ru",
        "apiKey": NEWS_KEY
    }

    response_news = requests.get(url=NEWS_URL, params=url_parameters)
    response_news.raise_for_status()
    data = response_news.json()["articles"][:3]
    to_ret = []
    for article in data:
        to_ret.append(f"Заголовок: {article["title"]}\nОписание: {article["description"]}\n\n")
    return to_ret

def update(percentage)->str:
    news = get_news()
    sign = "🔺"
    if percentage<0:
        sign="🔻"
    to_send = f"Акции Apple за сутки {sign} {percentage}%\n\n"
    for new in news:
        to_send += new
    return to_send

#percentage = get_percentage()
percentage=-7
if not -5<percentage<5:
    bot = Bot(update(percentage))