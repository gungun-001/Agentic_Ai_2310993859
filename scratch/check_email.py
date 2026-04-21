import requests
import os
import json

def search_email(company_name):
    api_key = "b4f5a2895f3a0d7169e0608a83a3b44ea8bd92c1ac622a5f75ed9ed775654b85"
    query = f"{company_name} contact email"
    resp = requests.get(
        "https://serpapi.com/search.json",
        params={"q": query, "api_key": api_key, "num": 5},
        timeout=10,
    )
    data = resp.json()
    results = data.get("organic_results", [])
    for r in results:
        print(f"Title: {r.get('title')}")
        print(f"Snippet: {r.get('snippet')}")
        print("-" * 20)

search_email("Glassdoor")
