import os
from dotenv import load_dotenv
from pinecone import Pinecone

# Load API keys
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# Your index name
index_name = "news-research-assistant"

# Fetch the index
index = pc.Index(index_name)

# Fetch 5 stored documents
query_results = index.query(
    vector=[0] * 1536,  # Dummy vector (replace with real query)
    top_k=5,
    include_metadata=True
)

# Display metadata
for match in query_results["matches"]:
    print(f"ID: {match['id']}")
    print(f"Metadata: {match['metadata']}\n")
