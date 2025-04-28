import streamlit as st
import json
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk
import os
# import matplotlib.pyplot as plt

nltk.download('punkt')

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

st.title("Latest News")

try:
    with open("all_news.json", "r", encoding="utf-8") as f:
        articles = json.load(f)
    sources = list(set(article["source"] for article in articles))
    source_filter = st.selectbox("Filter by source", ["All"] + sources, key="source_filter")
    if source_filter != "All":
        articles = [a for a in articles if a["source"] == source_filter]

    categories = list(set(article.get("category", "Uncategorized") for article in articles))
    category_filter = st.selectbox("Filter by category", ["All"] + categories, key="category_filter")
    if category_filter != "All":
        articles = [a for a in articles if a.get("category", "Uncategorized") == category_filter]

    page_size = 5
    page = st.number_input("Page", min_value=1, value=1, key="page_input")
    start = (page - 1) * page_size
    end = start + page_size
    articles = articles[start:end]


    
    # category_counts = {}
    # for article in articles:
    #     category = article.get("category", "Uncategorized")
    #     category_counts[category] = category_counts.get(category, 0) + 1
    # plt.figure(figsize=(6, 6))
    # plt.pie(category_counts.values(), labels=category_counts.keys(), autopct="%1.1f%%", colors=["#00ffcc", "#ff6666", "#66ccff"])
    # plt.title("Articles by Category")
    # st.pyplot(plt)

    def summarize(text, sentences=2):
        parser = PlaintextParser(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, sentences)
        return " ".join(str(s) for s in summary)

    for article in articles:
        st.markdown(f"**{article['title']}** ({article['source']})")
        summary = summarize(article["content"]) if len(article["content"].split()) > 20 else article["content"]
        st.write(summary)

        if st.button("Bookmark", key=f"bookmark_{article['title']}"):
            with open("bookmarks.json", "r+", encoding="utf-8") as f:
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