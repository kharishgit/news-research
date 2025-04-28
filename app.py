



import streamlit as st
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os
import json
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk
from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

# Download NLTK data
nltk.download('punkt')


st.set_page_config(page_title="News Research Assistant", page_icon="📰")
# Custom styling
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

# Load environment
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
if not OPENAI_API_KEY or not PINECONE_API_KEY:
    st.error("Missing OPENAI_API_KEY or PINECONE_API_KEY in .env")
    st.stop()

# Initialize vector store
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

web_search = DuckDuckGoSearchRun()

@tool
def summarize_article(text: str) -> str:
    """Summarize a given article text."""
    parser = PlaintextParser(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 2)
    return " ".join(str(s) for s in summary)

# Initialize the agent
llm = OpenAI(api_key=OPENAI_API_KEY, temperature=0.7)
agent = initialize_agent(
    tools=[pinecone_search, web_search,summarize_article],
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)


# Streamlit UI
st.title("Personalized News Research Assistant")

st.subheader("Ask a Question")
question = st.text_input("Ask about the news (e.g., 'What’s happening in Ukraine?')", "")
if question:
    response = agent.run(question)
    st.write(response)

# Search bar
query = st.text_input("Search news (e.g., 'Ukraine', 'tariffs')", "")
if query:
    st.subheader("Search Results")
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
else:
    # Show all articles with filter and pagination
    st.subheader("Latest News")
    try:
        with open("all_news.json", "r", encoding="utf-8") as f:
            articles = json.load(f)
        sources = list(set(article["source"] for article in articles))
        source_filter = st.selectbox("Filter by source", ["All"] + sources, key="source_filter")
        if source_filter != "All":
            articles = [a for a in articles if a["source"] == source_filter]
        page_size = 5
        page = st.number_input("Page", min_value=1, value=1, key="page_input")
        start = (page - 1) * page_size
        end = start + page_size
        articles = articles[start:end]

        # Summarization function
        def summarize(text, sentences=2):
            parser = PlaintextParser(text, Tokenizer("english"))
            summarizer = LsaSummarizer()
            summary = summarizer(parser.document, sentences)
            return " ".join(str(s) for s in summary)

        # Display articles with summaries
        for article in articles:
            st.markdown(f"**{article['title']}** ({article['source']})")
            summary = summarize(article["content"]) if len(article["content"].split()) > 20 else article["content"]
            st.write(summary)
            
            if st.button("Bookmark", key=f"bookmark_{article['title']}"):
                with open("bookmarks.json", "r+", encoding="utf-8") as f:
                    import json
                    try:
                        bookmarks = json.load(f) if os.path.getsize("bookmarks.json") > 0 else []
                    except json.JSONDecodeError:
                        bookmarks = []
                    bookmarks.append(article)
                    f.seek(0)
                    json.dump(bookmarks, f)
                    f.truncate()
                st.success("Article bookmarked!")

            rating = st.slider("Rate this article (1-5)", 1, 5, 3, key=f"rating_{article['title']}")
            if st.button("Submit Rating", key=f"submit_{article['title']}"):
                with open("ratings.json", "r+", encoding="utf-8") as f:
                    try:
                        ratings = json.load(f) if os.path.getsize("ratings.json") > 0 else {}
                    except json.JSONDecodeError:
                        ratings = {}
                    ratings[article['title']] = rating
                    f.seek(0)
                    json.dump(ratings, f)
                    f.truncate()
                st.success("Rating submitted!")
            st.markdown(f"[Read more]({article['link']})")
            st.markdown("---")

    except FileNotFoundError:
        st.error("all_news.json not found.")
    except json.JSONDecodeError:
        st.error("Invalid JSON in all_news.json.")
    
    st.subheader("Saved Bookmarks")
    try:
        with open("bookmarks.json", "r", encoding="utf-8") as f:
            bookmarks = json.load(f)
        if bookmarks:
            for article in bookmarks:
                st.markdown(f"**{article['title']}** ({article['source']})")
                st.write(article["content"])
                st.markdown(f"[Read more]({article['link']})")
                st.markdown("---")
        else:
            st.write("No bookmarks yet.")
    except FileNotFoundError:
        st.write("No bookmarks yet.")
    except json.JSONDecodeError:
        st.error("Error reading bookmarks.")