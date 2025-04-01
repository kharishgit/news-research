# import json
# from pinecone import Pinecone, ServerlessSpec
# from langchain_openai import OpenAIEmbeddings
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# # Load combined news
# with open("all_news.json", "r", encoding="utf-8") as f:
#     all_news = json.load(f)

# # Combine title, link, and source into text
# texts = [f"{a['title']} Source: {a['source']} Read more: {a['link']}" for a in all_news]

# # Chunk the text (optional, titles are short but good practice)
# splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
# chunks = splitter.split_text("\n".join(texts))

# # Set up embeddings
# embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

# # Connect to Pinecone
# pc = Pinecone()
# index_name = "news-research-assistant"

# # Create index if it doesn’t exist
# if index_name not in pc.list_indexes().names():
#     pc.create_index(
#         name=index_name,
#         dimension=1536,  # OpenAI embedding size
#         metric="cosine",
#         spec=ServerlessSpec(cloud="aws", region="us-east-1")
#     )

# # Connect to the index
# index = pc.Index(index_name)

# # Embed and store chunks
# vectors = []
# for i, chunk in enumerate(chunks):
#     vector = embeddings.embed_query(chunk)
#     metadata = {"text": chunk, "source": "Mixed"}  # Source is in text already
#     vectors.append({"id": f"chunk_{i}", "values": vector, "metadata": metadata})

# index.upsert(vectors)
# print(f"Stored {len(vectors)} chunks in Pinecone")

import json
import os
import time
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings

# Load environment variables
load_dotenv()
pinecone_api_key = os.getenv("PINECONE_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Load news data
with open("all_news.json", "r", encoding="utf-8") as f:
    all_news = json.load(f)
    print("Total articles:", len(all_news))
    print("Sample article:", all_news[0])

# Create chunks
chunks = [f"{a['title']} Source: {a['source']} Read more: {a['link']}" for a in all_news]
print("Total chunks:", len(chunks))
print("First chunk:", chunks[0])

# Set up embeddings
embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=openai_api_key)

# Connect to Pinecone
pc = Pinecone(api_key=pinecone_api_key)
index_name = "news-research-assistant"

# Delete and recreate index
if index_name in pc.list_indexes().names():
    pc.delete_index(index_name)
    print("Deleted old index")

pc.create_index(
    name=index_name,
    dimension=1536,
    metric="cosine",
    spec=ServerlessSpec(cloud="aws", region="us-east-1")
)

# Connect to the index
index = pc.Index(index_name)

# Embed and store chunks
vectors = []
for i, chunk in enumerate(chunks):
    vector = embedding_model.embed_query(chunk)
    metadata = {"text": chunk, "source": "Mixed"}
    vectors.append({"id": f"chunk_{i}", "values": vector, "metadata": metadata})
    if i == 0:
        print("First vector metadata:", metadata)

index.upsert(vectors)
print(f"Stored {len(vectors)} chunks in Pinecone")

# Wait longer and check index stats
time.sleep(5)  # Increase to 5 seconds
stats = index.describe_index_stats()
print("Index stats after upsert:", stats)
sample = index.fetch(ids=["chunk_0"])
print("Stored chunk_0 after upsert:", sample)