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
try:
    import streamlit as st
    if not google_key and hasattr(st, "secrets"):
        google_key = st.secrets.get("GOOGLE_API_KEY")
except ImportError:
    pass

if not google_key:
    raise ValueError("GOOGLE_API_KEY is completely missing! Please check Streamlit Secrets.")

llm = ChatOpenAI(
    model="gemini-1.5-flash",
    api_key=google_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    temperature=0
)

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
