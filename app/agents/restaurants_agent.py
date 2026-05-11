"""
Restaurants Agent:
  1. Serper 'places' results → parse directly (name, rating, price, address)
  2. Serper 'organic' results → filter junk, batch remaining to LLM for extraction
"""

import json
from app.schemas.trip_state import TripState
from app.schemas.restaurants import Restaurant, RestaurantList
from app.tools.search_tool import web_search
from app.llm.ollama_client import get_llm

EXTRACT_PROMPT = """Extract real restaurant names and details from these search snippets about {city}.
{snippets}
Return JSON array: [{{"name":"...","cuisine":"...","rating":"number or null","price_range":"$ or $$ or $$$","address":"..."}}]
Only real restaurant names. No website names. JSON only, no markdown."""

JUNK_PATTERNS = ["THE BEST", "TOP 10", "TOP 15", "TOP 20", "RANKING", "GUIDE TO", "TRIP TO"]


def restaurants_agent(state: TripState) -> dict:
    """Parse places directly, LLM extract from organic snippets."""

    request = state["request"]
    city = request.destination
    cuisine = request.preferences[0] if request.preferences else ""
    cuisine_part = f"{cuisine} " if cuisine else ""
    print(f"\n Restaurants Agent: searching {cuisine_part}restaurants in {city}...")

    try:
        results = web_search(
            f"best {cuisine_part}restaurants in {city} with ratings", num_results=10
        )

        restaurants: list[Restaurant] = []
        seen: set[str] = set()
        organic_snippets: list[str] = []

        for r in results:
            if r.get("_source") == "places":
                name = r["title"].strip()
                if name and name not in seen:
                    seen.add(name)
                    restaurants.append(
                        Restaurant(
                            name=name,
                            cuisine=cuisine,
                            rating=r.get("rating"),
                            price_range=r.get("price") or "",
                            address=r.get("snippet") or "",
                            link=r.get("link") or "",
                        )
                    )
            else:
                title = r.get("title") or ""
                title_upper = title.upper()
                if any(p in title_upper for p in JUNK_PATTERNS):
                    continue
                snippet = r.get("snippet") or ""
                if snippet:
                    organic_snippets.append(f"- {title}: {snippet[:200]}")

        if organic_snippets and len(restaurants) < 8:
            llm = get_llm()
            batch_text = "\n".join(organic_snippets)
            response = llm.invoke(
                EXTRACT_PROMPT.format(city=city, snippets=batch_text)
            )
            content = response.content.strip()
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]

            try:
                parsed = json.loads(content.strip())
                for item in parsed:
                    name = item.get("name", "").strip()
                    if name and name not in seen:
                        seen.add(name)
                        restaurants.append(
                            Restaurant(
                                name=name,
                                cuisine=item.get("cuisine", ""),
                                rating=item.get("rating"),
                                price_range=item.get("price_range", ""),
                                address=item.get("address", ""),
                            )
                        )
            except json.JSONDecodeError:
                print(" LLM extraction failed, using places-only results")

        print(f" Found {len(restaurants)} restaurants")
        return {"restaurants": RestaurantList(restaurants=restaurants[:10])}

    except Exception as e:
        print(f" Restaurants agent error: {e}")
        return {"restaurants": RestaurantList()}
