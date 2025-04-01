import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Your NewsAPI key (replace with your own)
api_key = os.getenv('NEWS_API_KEY')

# URL to get top headlines (we’ll use 'google-news' as a source)
url = f"https://newsapi.org/v2/top-headlines?sources=google-news&apiKey={api_key}"

# Send a request to NewsAPI
response = requests.get(url)

# Check if it worked
if response.status_code == 200:
    # Get the news data
    data = response.json()
    articles = data["articles"]

    # Create a list to store our news (like before)
    news_list = []
    for article in articles:
        news_item = {
            "title": article["title"],
            "link": article["url"]
        }
        news_list.append(news_item)

    # Save to google_news.json
    with open("google_news.json", "w", encoding="utf-8") as file:
        json.dump(news_list, file, indent=4)
    
    print(f"✅ Found {len(news_list)} news articles, saved to 'google_news.json'")
else:
    print(f"Failed to get news: {response.status_code} - {response.text}")