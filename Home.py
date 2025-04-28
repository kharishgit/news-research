import streamlit as st
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings, OpenAI
from dotenv import load_dotenv
import os
from langchain.agents import initialize_agent, AgentType
from langchain.tools import tool
import logging
logging.basicConfig(filename="app.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

st.set_page_config(page_title="News Research Assistant", page_icon="📰")
st.markdown(
    """
    <style>
    .stApp {background-color: #1a1a1a; color: white;}
    .stTextInput > div > div > input {background-color: #333; color: white; border: 1px solid #555;}
    .stMarkdown {color: #d3d3d3;}
    h1 {color: #00ffcc; text-align: center;}
    a {color: #00ccff; text-decoration: underline;}
    </style>
    """,
    unsafe_allow_html=True
)

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
if not OPENAI_API_KEY or not PINECONE_API_KEY:
    st.error("Missing OPENAI_API_KEY or PINECONE_API_KEY in .env")
    st.stop()

try:
    embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=OPENAI_API_KEY)
    vectorstore = PineconeVectorStore(
        index_name="news-research-assistant",
        embedding=embedding_model,
        pinecone_api_key=PINECONE_API_KEY
    )
except Exception as e:
    st.error(f"Failed to connect to Pinecone: {e}")
    st.stop()

@tool
def pinecone_search(query: str) -> str:
    """Search news articles in Pinecone."""
    results = vectorstore.similarity_search(query, k=5)
    return "\n".join([f"{doc.metadata['title']} ({doc.metadata['source']}): {doc.metadata['content'][:100]}..." for doc in results])

from langchain_community.tools import DuckDuckGoSearchRun
web_search = DuckDuckGoSearchRun()

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk
nltk.download('punkt')

@tool
def summarize_article(text: str) -> str:
    """Summarize a given article text."""
    parser = PlaintextParser(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 2)
    return " ".join(str(s) for s in summary)

llm = OpenAI(api_key=OPENAI_API_KEY, temperature=0.7)
agent = initialize_agent(
    tools=[pinecone_search, web_search, summarize_article],
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

st.title("Personalized News Research Assistant")
st.subheader("Ask a Question")
question = st.text_input("Ask about the news (e.g., 'What’s happening in Ukraine?')", "")
if question:
    response = agent.run(question)
    st.write(response)

st.subheader("Search News")
query = st.text_input("Search news (e.g., 'Ukraine', 'tariffs')", "")
if query:
    try:
        results = vectorstore.similarity_search(query, k=5)
        if results:
            for doc in results:
                meta = doc.metadata
                st.markdown(f"**{meta['title']}** ({meta['source']})")
                st.write(meta["content"])
                st.markdown(f"[Read more]({meta['link']})")
                st.markdown("---")
        else:
            st.write("No results found.")
    except Exception as e:
        st.error(f"Search failed: {e}")