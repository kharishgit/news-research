import json
import glob

all_news = []
for file in glob.glob("*_news.json"):
    with open(file, "r") as f:
        all_news.extend(json.load(f))

with open("all_news.json", "w") as f:
    json.dump(all_news, f, indent=4)

print(f"Saved {len(all_news)} articles to all_news.json")