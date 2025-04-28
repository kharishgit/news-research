import streamlit as st
import json
import matplotlib.pyplot as plt

st.markdown(
    """
    <style>
    .stApp {background-color: #1a1a1a; color: white;}
    .stMarkdown {color: #d3d3d3;}
    h1 {color: #00ffcc; text-align: center;}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Top-Rated Articles")
try:
    with open("ratings.json", "r", encoding="utf-8") as f:
        ratings = json.load(f)
    if ratings:
        sorted_ratings = sorted(ratings.items(), key=lambda x: x[1], reverse=True)[:3]
        for title, rating in sorted_ratings:
            st.write(f"{title}: {rating} stars")
    else:
        st.write("No ratings yet.")
except FileNotFoundError:
    st.write("No ratings yet.")
except json.JSONDecodeError:
    st.error("Error reading ratings.")



if ratings:
    titles, scores = zip(*sorted_ratings)
    plt.figure(figsize=(8, 4))
    plt.bar(titles, scores, color="teal")
    plt.xlabel("Article")
    plt.ylabel("Rating (Stars)")
    plt.title("Top-Rated Articles")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    st.pyplot(plt)