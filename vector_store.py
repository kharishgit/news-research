import json
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone as PineconeClient, ServerlessSpec
from dotenv import load_dotenv
import os

# Load environment
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
if not OPENAI_API_KEY or not PINECONE_API_KEY:
    print("Error: Missing API keys in .env")
    exit()

# Initialize Pinecone
try:
    pc = PineconeClient(api_key=PINECONE_API_KEY)
except Exception as e:
    print(f"Failed to connect to Pinecone: {e}")
    exit()

# Create or clear index
index_name = "news-research-assistant"
if index_name in pc.list_indexes().names():
    pc.delete_index(index_name)  # Clear old data
try:
    pc.create_index(
        name=index_name,
        dimension=1536,  # text-embedding-ada-002
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
    print(f"Created index: {index_name}")
except Exception as e:
    print(f"Failed to create index: {e}")
    exit()

# Load embedding model
try:
    embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=OPENAI_API_KEY)
except Exception as e:
    print(f"Failed to load embedding model: {e}")
    exit()

# Load all_news.json
try:
    with open("all_news.json", "r", encoding="utf-8") as f:
        articles = json.load(f)
except FileNotFoundError:
    print("Error: all_news.json not found")
    exit()
except json.JSONDecodeError:
    print("Error: Invalid JSON in all_news.json")
    exit()

if not articles:
    print("Error: No articles found")
    exit()

# Prepare data
texts = [f"{article['title']} {article['content']}" for article in articles]
metadatas = [
    {
        "title": article["title"],
        "link": article["link"],
        "content": article["content"],
        "source": article["source"]
    }
    for article in articles
]
ids = [f"article_{i}" for i in range(len(articles))]

# Upload
try:
    vectorstore = PineconeVectorStore.from_texts(
        texts=texts,
        embedding=embedding_model,
        metadatas=metadatas,
        ids=ids,
        index_name=index_name
    )
    print(f"✅ Uploaded {len(articles)} articles to Pinecone")
except Exception as e:
    print(f"Failed to upload: {e}")
    exit()