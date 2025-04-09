import streamlit as st
import os
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pinecone import Pinecone as PineconeClient

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

def init_vectorstore():
    pc = PineconeClient(api_key=PINECONE_API_KEY)
    index_name = "news-research-assistant"
    index = pc.Index(index_name)
    embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=OPENAI_API_KEY)
    return PineconeVectorStore(index, embedding_model, text_key="text")

vectorstore = init_vectorstore()  # Initialize once

# Define retrieval function
def retrieve_similar_news(query, top_k=5):
    results = vectorstore.similarity_search_with_score(query, k=top_k)
    return results

# Set up chatbot and prompt
llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)
prompt = ChatPromptTemplate.from_template(
    "Summarize these articles in 2-3 simple sentences:\n{context}\nAnswer this question clearly: {query}\nThen suggest 2 relevant follow-up questions."
)

# Define answer function
def get_answer(query):
    articles = retrieve_similar_news(query)
    context = "\n".join([article.page_content for article, _ in articles])
    response = llm.invoke(prompt.format(context=context, query=query))
    return response.content

# Streamlit UI
st.title("News Research Assistant")
query = st.text_input("Ask me anything about news!")
if query:
    answer = get_answer(query)
    st.write("Answer:", answer)