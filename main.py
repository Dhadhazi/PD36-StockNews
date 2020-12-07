from dotenv import DotEnv
from twilio.rest import Client
import requests

dotenv = DotEnv()

STOCK = "NIO"
client = Client(dotenv.get('TWILIO_SID'), dotenv.get('TWILIO_AUTH'))
TWILIO_NUMBER=""
VERIFIED_NUMBER = ""

def get_datily_stock_data(stock):
    stock_params = {
        "symbol":stock,
        "function":"TIME_SERIES_DAILY_ADJUSTED",
        "outputsize":"compact",
        "apikey":dotenv.get('ALPHAADCENTAGE_API_KEY')
    }
    res = requests.get(f"https://www.alphavantage.co/query", params=stock_params)
    res.raise_for_status()
    return res.json()["Time Series (Daily)"]


def stock_moved_by_5(stock):
    stock_data = get_datily_stock_data(stock)
    data_list = [value for (key, value) in stock_data.items()]
    yesterday_closing = float(data_list[0]["4. close"])
    day_before_yesterday_closing = float(data_list[1]["4. close"])
    stock_moved = (abs(yesterday_closing-day_before_yesterday_closing)/yesterday_closing)*100
    if stock_moved > 5:
        return True
    else:
        return False


def get_news(stock):
    news_params = {
        "q": stock,
        "apikey": dotenv.get('NEWSAPI_API_KEY')
    }
    res = requests.get(f"https://newsapi.org/v2/everything", params=news_params)
    res.raise_for_status()
    return res.json()["articles"][:3]


def get_formatted_stock_news(stock):
    return [f"Headline: {article['title']}.\nBrief: {article['description']}" for article in get_news(stock)]


def send_articles(stock):
    articles = get_formatted_stock_news(stock)
    for article in articles:
        message = client.messages.create(
            body=article,
            from_=TWILIO_NUMBER,
            to=VERIFIED_NUMBER
        )


if stock_moved_by_5(STOCK):
    send_articles(STOCK)