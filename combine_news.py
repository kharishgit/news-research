import json

# Load all JSON files
with open("bbc_news.json", "r", encoding="utf-8") as f:
    bbc_news = json.load(f)
with open("cnn_news.json", "r", encoding="utf-8") as f:
    cnn_news = json.load(f)
with open("google_news.json", "r", encoding="utf-8") as f:
    google_news = json.load(f)

# Combine into one list with source labels
all_news = []
for article in bbc_news:
    all_news.append({"title": article["title"], "link": article["link"], "source": "BBC"})
for article in cnn_news:
    all_news.append({"title": article["title"], "link": article["link"], "source": "CNN"})
for article in google_news:
    all_news.append({"title": article["title"], "link": article["link"], "source": "Google News"})

# Save combined data (optional)
with open("all_news.json", "w", encoding="utf-8") as f:
    json.dump(all_news, f, indent=4)
print(f"Combined {len(all_news)} articles from BBC, CNN, and Google News")