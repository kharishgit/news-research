News Research Assistant
A web application to scrape, store, and query news articles using Streamlit, LangChain, Pinecone, and OpenAI. The app scrapes news from BBC and CNN, stores articles in a Pinecone vector store, and allows users to ask questions about current events.
Features

News Scraping: Automatically fetches articles from BBC and CNN via cron jobs.
Vector Storage: Stores articles in Pinecone for efficient retrieval.
Query System: Uses LangChain and OpenAI to answer user questions about news events.
Streamlit UI: Interactive web app with pages for querying, viewing top-rated articles, and more.

Prerequisites

Python 3.10+
Anaconda or virtualenv
API keys for:
OpenAI (for embeddings and LLM)
Pinecone (for vector storage)



Setup Instructions

Clone the Repository:
git clone https://github.com/your-username/news-research-assistant.git
cd news-research-assistant


Create and Activate a Virtual Environment:Using Anaconda:
conda create -n newsresearch python=3.10
conda activate newsresearch

Or using virtualenv:
python -m venv newsresearch
source newsresearch/bin/activate  # On Windows: newsresearch\Scripts\activate


Install Dependencies:
pip install -r requirements.txt


Set Up Environment Variables:Create a .env file or export the following:
export OPENAI_API_KEY="your-openai-api-key"
export PINECONE_API_KEY="your-pinecone-api-key"
export PINECONE_ENVIRONMENT="us-east1-gcp"  # Replace with your Pinecone environment


Download NLTK Data:
python -c "import nltk; nltk.download('punkt')"


Set Up Pinecone Index:

Log in to Pinecone.
Create an index named news-research-assistant (dimension: 1536, metric: cosine).


Run the App Locally:
streamlit run Home.py

Access the app at http://localhost:8501.


Usage

Scrape News:

Run refresh_news.py manually or set up a cron job to scrape BBC and CNN articles:python refresh_news.py


Articles are saved to bbc_news.json, cnn_news.json, and all_news.json.


Query News:

Open the Streamlit app.
On the home page, enter a question (e.g., "What’s happening with the Pehalgam attack?").
View results and top-rated articles on the respective pages.



Deployment on Streamlit Community Cloud

Push to GitHub:

Ensure all files (Home.py, pages/, requirements.txt, etc.) are in your repo.
Push to a public GitHub repository.


Deploy:

Sign up at streamlit.io/cloud.
Link your GitHub repo and select Home.py as the main file.
Set environment variables in Streamlit Cloud (under "Advanced Settings"):OPENAI_API_KEY=your-openai-api-key
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_ENVIRONMENT=us-east1-gcp


Deploy the app. Access it at yourappname.streamlit.app.



Project Structure

Home.py: Main Streamlit app for querying news.
pages/: Additional Streamlit pages (e.g., 3_Top_Rated.py for top-rated articles).
refresh_news.py: Script to scrape news and update Pinecone.
scrape_bbc.py, scrape_cnn.py: Scripts for scraping specific sites.
vector_store.py: Handles Pinecone vector storage.
cron.log: Logs for cron job runs.

Known Issues

LangChain deprecation warnings: Plan to migrate to LangGraph for agent functionality.
API costs: Monitor OpenAI/Pinecone usage to avoid unexpected charges.

Future Improvements

Add caching to reduce API calls.
Expand news sources (e.g., Reuters, AP).
Improve UI with better layout and error handling.

License
MIT License
