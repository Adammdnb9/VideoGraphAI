"""
Optional: use SerpAPI for web search and then summarize results via OpenAI.
"""
import os
from serpapi import GoogleSearch
from dotenv import load_dotenv
from .openai_client import chat_completion

load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_API_KEY")

def serp_search(query, num=5):
    if not SERPAPI_KEY:
        raise RuntimeError("SERPAPI_API_KEY not set in environment")
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_KEY,
        "num": num
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    hits = []
    for r in results.get("organic_results", [])[:num]:
        hits.append({
            "title": r.get("title"),
            "snippet": r.get("snippet"),
            "link": r.get("link")
        })
    return hits

def summarize_search_results(results):
    system = {"role":"system","content":"You are an assistant that summarizes web search results into a short research summary for script generation."}
    content = "Summarize these search results into bullet points and key facts:\n\n"
    for r in results:
        content += f"- {r.get('title')}\n  {r.get('snippet')}\n  {r.get('link')}\n\n"
    user = {"role":"user","content":content}
    return chat_completion([system, user], max_tokens=400)
