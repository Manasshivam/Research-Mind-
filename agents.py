from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_website
import os
from dotenv import load_dotenv

load_dotenv()

# Read API key safely from Streamlit Secrets or Environment
google_key = os.environ.get("GOOGLE_API_KEY")
groq_key = os.environ.get("GROQ_API_KEY")
try:
    import streamlit as st
    if hasattr(st, "secrets"):
        try:
            google_key = google_key or st.secrets.get("GOOGLE_API_KEY")
            groq_key = groq_key or st.secrets.get("GROQ_API_KEY")
        except Exception:
            # st.secrets throws an error locally if .streamlit/secrets.toml doesn't exist
            pass
except ImportError:
    pass

if groq_key:
    llm = ChatOpenAI(
        model="llama3-8b-8192",
        api_key=groq_key,
        base_url="https://api.groq.com/openai/v1",
        temperature=0
    )
elif google_key and google_key.startswith("AIza"):
    llm = ChatOpenAI(
        model="gemini-1.5-flash",
        api_key=google_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        temperature=0
    )
elif google_key and google_key.startswith("AQ."):
    raise ValueError("ERROR: The GOOGLE_API_KEY you provided (starts with 'AQ.') is a Google Cloud Vertex AI key! Vertex AI requires setting up a Google Cloud Project ID, Region, and Billing. Please get a standard AI Studio key (starts with 'AIza') or use a Groq API key instead.")
else:
    raise ValueError("Missing API Key! Please add either a GROQ_API_KEY or a standard GOOGLE_API_KEY (must start with 'AIza') to your Streamlit Secrets.")

def build_search_agent():
    """Returns an agent equipped with web search capabilities."""
    return create_react_agent(llm, tools=[web_search])

def build_scrape_agent():
    """Returns an agent equipped with website scraping capabilities."""
    return create_react_agent(llm, tools=[scrape_website])

# Writer Chain
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert technical writer. Write a detailed and comprehensive research report based on the provided search results and scraped content. Use markdown formatting, headers, and bullet points to structure the report clearly."),
    ("user", "Topic: {topic}\n\nResearch Materials:\n{research}\n\nPlease write the report now.")
])

writer_chain = writer_prompt | llm | StrOutputParser()

# Critic Chain
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a senior editor. Review the following research report for clarity, completeness, structure, and accuracy. Provide constructive feedback on how it can be improved. Focus on what is missing or what could be formatted better."),
    ("user", "Report to review:\n\n{report}\n\nPlease provide your feedback.")
])

critic_chain = critic_prompt | llm | StrOutputParser()
