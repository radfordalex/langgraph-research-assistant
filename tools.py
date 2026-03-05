from langchain_community.tools.tavily_search import TavilySearchResults
import os
from dotenv import load_dotenv

load_dotenv()

search_tool = TavilySearchResults(max_results=5)