import os
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pinecone import Pinecone as PineconeClient

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

pc = PineconeClient(api_key=PINECONE_API_KEY)
index_name = "news-research-assistant"
index = pc.Index(index_name)

embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=OPENAI_API_KEY)
vectorstore = PineconeVectorStore(index, embedding_model, text_key="text")

def retrieve_similar_news(query, top_k=5):
    results = vectorstore.similarity_search_with_score(query, k=top_k)
    return results

llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)
prompt = ChatPromptTemplate.from_template(
    "Summarize these articles in simple terms:\n{context}\nThen answer this question: {query}"
)

def get_answer(query):
    articles = retrieve_similar_news(query)
    context = "\n".join([article.page_content for article, _ in articles])
    response = llm.invoke(prompt.format(context=context, query=query))
    print("Articles Used:")
    for i, (article, score) in enumerate(articles):
        print(f"{i+1}. {article.page_content} (Score: {score})")
    return response.content

query = "Are there new tech laws in Europe?"
answer = get_answer(query)
print("Answer:", answer)