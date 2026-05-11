"""
Web search tool: uses Serper api for Google Search results.
"""

import httpx
from app.config import settings


def web_search(query: str, num_results: int = 10) -> list[dict]:
    """
    Run a Google web search via Serper api.
    Returns a list of dicts with keys: title, snippet, link, position.
    """

    response = httpx.post(
        "https://google.serper.dev/search",
        headers={
            "X-API-KEY": settings.SERPER_API_KEY,
            "Content-Type": "application/json",
        },
        json={"q": query, "num": num_results},
        timeout=15,
    )
    response.raise_for_status()
    data = response.json()

    results = []

    for item in data.get("organic", []):
        results.append(
            {
                "title": item.get("title", ""),
                "snippet": item.get("snippet", ""),
                "link": item.get("link", ""),
                "position": item.get("position", 0),
            }
        )
    for place in data.get("places", []):
        results.append(
            {
                "title": place.get("title") or "",
                "snippet": place.get("address") or "",
                "link": place.get("link") or "",
                "rating": place.get("rating"),
                "price": place.get("price"),
                "position": 0,
                "_source": "places",
            }
        )

    return results
