
import subprocess
import os

def refresh_news():
    base_dir = "/Users/harishk/Documents/Projects/ML/GenAI/NewsResearchAssistant"
    scripts = [
        "scrape_bbc.py",
        "scrape_cnn.py",
        "fetch_google_news.py",
        "combine_news.py"
    ]
    for script in scripts:
        full_path = os.path.join(base_dir, script)
        subprocess.run(["/Users/harishk/anaconda3/envs/newsresearch/bin/python", full_path], check=True)
    subprocess.run(["/Users/harishk/anaconda3/envs/newsresearch/bin/python", os.path.join(base_dir, "vector_store.py")], check=True)
    print("✅ News refreshed successfully!")

if __name__ == "__main__":
    refresh_news()