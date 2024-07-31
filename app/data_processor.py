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

if __name__ == '__main__':
    raw_data = {
        'general_news': {
            'status': 'ok',
            'totalResults': 46,
            'articles': [
                {
                    'source': {'id': 'associated-press', 'name': 'Associated Press'},
                    'author': 'JOSHUA GOODMAN, REGINA GARCIA CANO',
                    'title': 'Venezuelan opposition says it has proof its candidate defeated President Maduro in disputed election - The Associated Press',
                    'description': 'As thousands of people demonstrate across Venezuela, opposition candidate Edmundo González has announced that his campaign has the proof it needs to show he won the country’s disputed election whose victory electoral authorities handed to President Nicolás Ma…',
                    'url': 'https://apnews.com/article/venezuela-presidential-election-maduro-machado-edmundo-results-acee6c8cd3a8fc88086c2dd71963b759',
                    'urlToImage': 'https://dims.apnews.com/dims4/default/ea733c3/2147483647/strip/true/crop/6229x3504+0+325/resize/1440x810!/quality/90/?url=https%3A%2F%2Fassets.apnews.com%2F%5B1%2F03%2F%2C%20-71%2C%2060%2C%20-52%2C%20-128%2C%20-97%2C%20-126%2C%20-73%2C%20-30%2C%20-27%2C%20-86%2C%20-69%2C%20-26%2C%20-121%2C%20-72%2C%2056%2C%20-39%2C%2017%2C%20111%2C%20-85%2C%20-84%2C%20-60%2C%2084%2C%208%2C%20-11%2C%20-68%2C%20-64%2C%2024%5D%2F561f4d6070534385b616a744f98a31c4',
                    'publishedAt': '2024-07-30T02:28:00Z',
                    'content': 'CARACAS, Venezuela (AP) As thousands of people demonstrated across Venezuela, opposition candidate Edmundo González on Monday announced that his campaign has the proof it needs to show he won the cou… [+10597 chars]'
                },
            ]
        },
        'personal_news': {
            'russia': {
                'status': 'ok',
                'totalResults': 2,
                'articles': [
                    {
                        'source': {'id': 'bbc-news', 'name': 'BBC News'},
                        'author': 'BBC News',
                        'title': 'Mali rebels thwart Russian mercenaries in sandstorm ambush',
                        'description': 'Mercenaries formerly of the Wagner group say they suffered "losses" at the hands of 1,000 rebels.',
                        'url': 'https://www.bbc.co.uk/news/articles/c4ng5zkn7dro',
                        'urlToImage': 'https://ichef.bbci.co.uk/news/1024/branded_news/0d32/live/8facd760-4dc5-11ef-aebc-6de4d31bf5cd.jpg',
                        'publishedAt': '2024-07-29T18:07:13.5494864Z',
                        'content': 'Similarly, several Russian military bloggers reported that at least 20 were killed in the ambush near the north-eastern town of Tinzaouaten.\r\nIn an official statement posted to Telegram, the Russian … [+2039 chars]'
                    },
                ]
            },
            'israel': {
                'status': 'ok',
                'totalResults': 4,
                'articles': [
                    {
                        'source': {'id': 'bbc-news', 'name': 'BBC News'},
                        'author': 'BBC News',
                        'title': 'Israeli protesters enter Sde Teiman army base after soldiers held over Gaza detainee abuse',
                        'description': 'The Sde Teiman base has been at the centre of reports of serious abuses against Palestinians from Gaza.',
                        'url': 'https://www.bbc.co.uk/news/articles/c2q07kd3ld6o',
                        'urlToImage': 'https://ichef.bbci.co.uk/news/1024/branded_news/ad96/live/80dc8de0-4dd7-11ef-8f0f-0577398c3339.jpg',
                        'publishedAt': '2024-07-29T23:52:13.2047765Z',
                        'content': 'Some soldiers at the base reportedly used pepper spray against the military police personnel who arrived to detain the reservists. \r\nDemonstrators also entered the Beit Lid military base in central I… [+1034 chars]'
                    },
                ]
            },
        }
    }

    email_content = generate_email_content(raw_data)
    print(email_content)
