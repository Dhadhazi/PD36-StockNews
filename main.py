from dotenv import DotEnv
import requests

dotenv = DotEnv()

STOCK = "NIO"
COMPANY_NAME = "Tesla Inc"


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


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
def get_news(stock):
    news_params = {
        "q": stock,
        "apikey": dotenv.get('NEWSAPI_API_KEY')
    }
    res = requests.get(f"https://newsapi.org/v2/everything", params=news_params)
    res.raise_for_status()
    return res.json()["articles"][:3]


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 





print(get_news(STOCK))

#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

