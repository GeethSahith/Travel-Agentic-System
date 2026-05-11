"""
Hotels Agent:
  1. Serper 'places' results → parse directly (name, rating, price, address)
  2. Serper 'organic' results → filter junk, batch remaining to LLM for extraction
"""

import json
from app.schemas.trip_state import TripState
from app.schemas.hotels import Hotel, HotelList
from app.tools.search_tool import web_search
from app.llm.ollama_client import get_llm

EXTRACT_PROMPT = """Extract real hotel names and details from these search snippets about {city}.
{snippets}
Return JSON array: [{{"name":"...","price_per_night":"...or null","rating":"number or null","location":"...","amenities":["pool","spa",...]}}]
Only real hotel names. No website names. JSON only, no markdown."""

JUNK_PATTERNS = ["THE BEST", "TOP 10", "TOP 15", "TOP 20", "RANKING", "GUIDE TO", "TRIP TO"]


def hotels_agent(state: TripState) -> dict:
    """parse places directly, LLM extract from organic snippets."""

    request = state["request"]
    city = request.destination
    budget = request.budget or "moderate"
    print(f"\n Hotels Agent: searching {budget} hotels in {city}...")

    try:
        results = web_search(
            f"best {budget} hotels in {city} with prices", num_results=10
        )

        hotels: list[Hotel] = []
        seen: set[str] = set()
        organic_snippets: list[str] = []

        for r in results:
            if r.get("_source") == "places":
                name = r["title"].strip()
                if name and name not in seen:
                    seen.add(name)
                    hotels.append(
                        Hotel(
                            name=name,
                            rating=r.get("rating"),
                            price_per_night=r.get("price"),
                            location=r.get("snippet") or city,
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

        if organic_snippets and len(hotels) < 8:
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
                        hotels.append(
                            Hotel(
                                name=name,
                                price_per_night=item.get("price_per_night"),
                                rating=item.get("rating"),
                                location=item.get("location", city),
                                amenities=item.get("amenities", []),
                            )
                        )
            except json.JSONDecodeError:
                print(" LLM extraction failed, using places-only results")

        print(f" Found {len(hotels)} hotels")
        return {"hotels": HotelList(hotels=hotels[:10])}

    except Exception as e:
        print(f" Hotels agent error: {e}")
        return {"hotels": HotelList()}
