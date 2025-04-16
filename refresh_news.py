import os
import subprocess

def refresh_news():
    scripts = ["scrape_bbc.py", "scrape_cnn.py", "fetch_google_news.py", "combine_news.py"]
    for script in scripts:
        subprocess.run(["/Users/harishk/anaconda3/envs/newsresearch/bin/python", script], check=True)
    subprocess.run(["/Users/harishk/anaconda3/envs/newsresearch/bin/python", "vector_store.py"], check=True)
    print("✅ News refreshed successfully!")
if __name__ == "__main__":
    refresh_news()