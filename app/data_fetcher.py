from newsapi import NewsApiClient
import os
import requests

NEWS_API_KEY = os.getenv('NEWS_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
BASE_WEATHER_URL = 'http://api.openweathermap.org/data/2.5/forecast'

newsapi = NewsApiClient(NEWS_API_KEY)

#do i even need this anymore 
news_sources = {
    'general' : ['bbc-news', 'reuters', 'the-new-york-times']
}

#do i even need this anymore 
def get_sources(category):
    return ','.join(news_sources.get(category, []))

queries_of_interest = (
    'russia',
    'israel', 
    'cyber',
)


def fetch_general_news():
    top_headlines = newsapi.get_top_headlines(language="en", page_size=5)
    return top_headlines
 
def fetch_news(query="", language="en", sources="bbc-news, reuters, the-new-york-times", page_size=3):
    top_headlines = newsapi.get_top_headlines(q=query, language=language, sources=sources, page_size=page_size)
    return top_headlines 
    
def fetch_weather_forecast(city_name):
    params = {
        'q': city_name,   
        'appid': WEATHER_API_KEY 
    }
    response = requests.get(BASE_WEATHER_URL, params=params)
    return response

def fetch_data(cities):
    raw_data = {}
    raw_data["forecast"] = {}
    for city in cities:
        raw_data["forecast"][city] = fetch_weather_forecast(city)

    raw_data["general_news"] = fetch_general_news()
    raw_data["personal_news"] = {}
    for q in queries_of_interest:
        raw_data["personal_news"][q] = fetch_news(query=q, page_size=2)
        
    return raw_data

    
if __name__ == '__main__':
    print(fetch_data())