# import requests
# import json
# import os
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()


# # Your NewsAPI key (replace with your own)
# api_key = os.getenv('NEWS_API_KEY')

# # URL to get top headlines (we’ll use 'google-news' as a source)
# url = f"https://newsapi.org/v2/top-headlines?sources=google-news&apiKey={api_key}"

# # Send a request to NewsAPI
# response = requests.get(url)

# # Check if it worked
# if response.status_code == 200:
#     # Get the news data
#     data = response.json()
#     articles = data["articles"]

#     # Create a list to store our news (like before)
#     news_list = []
#     for article in articles:
#         news_item = {
#             "title": article["title"],
#             "link": article["url"]
#         }
#         news_list.append(news_item)

#     # Save to google_news.json
#     with open("google_news.json", "w", encoding="utf-8") as file:
#         json.dump(news_list, file, indent=4)
    
#     print(f"✅ Found {len(news_list)} news articles, saved to 'google_news.json'")
# else:
#     print(f"Failed to get news: {response.status_code} - {response.text}")

import requests
import json
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()

# Your NewsAPI key
api_key = os.getenv('NEWS_API_KEY')
if not api_key:
    print("Error: NEWS_API_KEY not found in .env file")
    exit()

# Use 'everything' endpoint for recent news
url = f"https://newsapi.org/v2/everything?q=news&sortBy=publishedAt&apiKey={api_key}"

# Send request
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
except requests.RequestException as e:
    print(f"Failed to get news: {e}")
    exit()

# Parse data
data = response.json()
if data["status"] != "ok":
    print(f"NewsAPI error: {data.get('message', 'Unknown error')}")
    exit()

articles = data.get("articles", [])
print(f"Found {len(articles)} articles from NewsAPI")

# Collect news
news_list = []
for article in articles[:10]:
    try:
        title = article.get("title", "").strip()
        link = article.get("url", "").strip()
        description = article.get("description", "").strip()
        
        # Get source
        source = article.get("source", {}).get("name", "Unknown").strip()
        if source.lower() in ["google news", "unknown"]:
            source = urlparse(link).netloc.replace("www.", "").split(".")[0].capitalize()
        
        # Content: prefer description, fallback to page
        content = description[:500] if description else ""
        if not content and "news.google.com" not in link:
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
                }
                response = requests.get(link, headers=headers, timeout=5)
                soup = BeautifulSoup(response.text, "html.parser")
                paragraphs = soup.select("article p, div[class*='content'] p, p")
                content = " ".join([p.text.strip() for p in paragraphs if p.text.strip()])[:500]
                if not content:
                    meta_desc = soup.find("meta", {"name": "description"})
                    content = meta_desc["content"].strip()[:500] if meta_desc and meta_desc.get("content") else ""
            except Exception as e:
                print(f"Failed to fetch content for {link}: {e}")
                content = ""
        
        # Save article
        if title and link and "javascript:" not in link and title.lower() != "google news":
            news_item = {
                "title": title,
                "link": link,
                "content": content,
                "source": source
            }
            news_list.append(news_item)
            print(f"Saved article: {title} | {source}")
        
        if len(news_list) >= 10:
            break
    except Exception as e:
        print(f"Skipped article: {e}")
        continue

# Save to JSON
with open("google_news.json", "w", encoding="utf-8") as file:
    json.dump(news_list, file, indent=4)

print(f"✅ Saved {len(news_list)} news articles to 'google_news.json'")