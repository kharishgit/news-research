import streamlit as st
import json

st.markdown(
    """
    <style>
    .stApp {background-color: #1a1a1a; color: white;}
    .stMarkdown {color: #d3d3d3;}
    h1 {color: #00ffcc; text-align: center;}
    a {color: #00ccff; text-decoration: underline;}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Saved Bookmarks")
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