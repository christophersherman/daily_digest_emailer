import json
from datetime import datetime

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def process_weather_data(city, weather_data):
    forecast_list = weather_data['list'][:3]  # Get only the first 3 forecasts for brevity
    weather_html = f'''
    <div style="background-color: #f0f8ff; border-radius: 10px; padding: 20px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
        <h2 style="color: #2e6da4; text-align: center; margin-bottom: 20px;">Weather Forecast for {city}</h2>
        <div style="display: flex; justify-content: space-around; align-items: center;">
    '''

    for forecast in forecast_list:
        dt_txt = forecast['dt_txt']
        date, time = dt_txt.split()
        temp = kelvin_to_celsius(forecast['main']['temp'])
        temp_min = kelvin_to_celsius(forecast['main']['temp_min'])
        temp_max = kelvin_to_celsius(forecast['main']['temp_max'])
        description = forecast['weather'][0]['description'].capitalize()
        icon = forecast['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon}.png"

        weather_html += f'''
        <div style="text-align: center; padding: 10px; border-radius: 10px; background-color: #ffffff; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin: 10px;">
            <div style="font-weight: bold; font-size: 1.2em; margin-bottom: 10px;">{date}</div>
            <div style="color: #555; font-size: 1em; margin-bottom: 10px;">{time}</div>
            <img src="{icon_url}" alt="Weather Icon" style="width: 50px; height: 50px; margin-bottom: 10px;">
            <div style="font-size: 1.5em; font-weight: bold; color: #333;">{temp:.1f}°C</div>
            <div style="color: #555; font-size: 1em; margin-bottom: 10px;">{temp_min:.1f}°C / {temp_max:.1f}°C</div>
            <div style="font-size: 1em; color: #2e6da4;">{description}</div>
        </div>
        '''
    
    weather_html += '''
        </div>
    </div>
    '''
    return weather_html


def process_articles(section_name, articles):
    html_content = f'<h2 style="color: #2e6da4;">{section_name.replace("_", " ").title()}</h2>'

    for article in articles:
        source = article.get('source', {}).get('name', 'Unknown Source')
        author = article.get('author', 'Unknown Author')
        title = article.get('title', 'No Title')
        description = article.get('description', 'No Description')
        url = article.get('url', '#')
        url_to_image = article.get('urlToImage', '')

        html_content += f'''
        <div style="margin-bottom: 20px; padding: 10px; border-bottom: 1px solid #ddd; overflow: hidden;">
            <h3 style="margin: 0 0 10px 0; color: #333;">{title}</h3>
            <p style="margin: 0 0 5px 0;"><strong>Source:</strong> {source}</p>
            <p style="margin: 0 0 5px 0;"><strong>Author:</strong> {author}</p>
            <p style="margin: 0 0 5px 0;">{description}</p>
            <p style="margin: 0 0 10px 0;"><a href="{url}" style="color: #1e70bf; text-decoration: none;">Read more</a></p>
        '''
        if url_to_image:
            html_content += f'''
            <div style="text-align: center; overflow: hidden;">
                <img src="{url_to_image}" alt="{title}" style="max-width: 100%; height: auto; display: block; margin: 0 auto;">
            </div>
            '''
        
        html_content += '</div>'

    return html_content

def generate_email_content(data):
    html_content = '''
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="width: 100%; max-width: 600px; margin: auto; border: 1px solid #ddd; padding: 20px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
            <h1 style="color: #2e6da4; text-align: center;">Daily Digest</h1>
    '''
    
    # Process Weather Forecast
    forecast_data = data.get('forecast')
    if forecast_data:
        for city, forecast_response in forecast_data.items():
            if forecast_response.status_code == 200:
                weather_data = forecast_response.json()
                html_content += process_weather_data(city, weather_data)

    # Process General News
    general_news = data.get('general_news', {})
    if general_news.get('status') == 'ok':
        html_content += '<div style="background-color: #f5f5f5; padding: 20px; margin-bottom: 20px;">'
        html_content += process_articles('General News', general_news.get('articles', []))
        html_content += '</div>'
    
    # Process Personal News
    personal_news = data.get('personal_news', {})
    for section_name, section_data in personal_news.items():
        if section_data.get('status') == 'ok' and int(section_data.get('totalResults')) > 0 :
            html_content += '<div style="background-color: #eef5ff; padding: 20px; margin-bottom: 20px;">'
            html_content += process_articles(section_name, section_data.get('articles', []))
            html_content += '</div>'
    
    html_content += '''
        </div>
    </body>
    </html>
    '''
    return html_content
