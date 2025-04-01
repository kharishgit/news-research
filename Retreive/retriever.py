import os
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone as PineconeClient

# Load API keys
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone
pc = PineconeClient(api_key=PINECONE_API_KEY)
index_name = "news-research-assistant"

# Connect to the index
index = pc.Index(index_name)

# Verify data directly from Pinecone
sample = index.fetch(ids=["chunk_0"])
print("Raw Pinecone fetch for chunk_0:", sample)

# Initialize OpenAI embeddings
embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=OPENAI_API_KEY)

# Connect to Pinecone with LangChain
vectorstore = PineconeVectorStore(index, embedding_model, text_key="text")

# Define a retriever function
def retrieve_similar_news(query, top_k=5):
    """Retrieve top-k most similar news articles based on query"""
    results = vectorstore.similarity_search_with_score(query, k=top_k)
    return results

# Example query
query = "Latest updates on AI regulations in Europe"
retrieved_articles = retrieve_similar_news(query)

# Display results
for i, (article, score) in enumerate(retrieved_articles):
    print(f"Result {i + 1}:")
    text = article.page_content  # Use page_content instead of metadata['text']
    source = article.metadata.get("source", "Unknown Source")
    print(f"Source: {source}")
    print(f"Article: {text}")
    print(f"Score: {score}\n")