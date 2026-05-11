"""
Places Agent:
  1. Serper 'places' results → parse directly (structured, no LLM)
  2. Serper 'organic' results → filter junk, batch remaining to LLM for extraction
"""

import json
from app.schemas.trip_state import TripState
from app.schemas.places import Place, PlacesList
from app.tools.search_tool import web_search
from app.llm.ollama_client import get_llm

EXTRACT_PROMPT = """Extract real tourist attraction names from these search snippets about {city}.
{snippets}
Return JSON array: [{{"name":"...","description":"...","category":"beach|temple|fort|museum|nature|market|attraction"}}]
Only real place names. No website names. JSON only, no markdown."""

JUNK_PATTERNS = ["THE BEST", "TOP 10", "TOP 15", "TOP 20", "THINGS TO DO", "VISIT IN", "RANKING", "GUIDE TO", "TRIP TO"]


def places_agent(state: TripState) -> dict:
    """Hybrid: parse places directly, LLM-extract from organic snippets."""

    city = state["request"].destination
    print(f"\n Places Agent: searching attractions in {city}...")

    try:
        results = web_search(f"tourist attractions in {city}", num_results=10)

        places: list[Place] = []
        seen: set[str] = set()
        organic_snippets: list[str] = []

        for r in results:
            if r.get("_source") == "places":
                name = r["title"].strip()
                if name and name not in seen:
                    seen.add(name)
                    places.append(
                        Place(
                            name=name,
                            description=r.get("snippet") or "",
                            rating=r.get("rating"),
                            category="attraction",
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
        if organic_snippets and len(places) < 8:
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
                        places.append(
                            Place(
                                name=name,
                                description=item.get("description", ""),
                                category=item.get("category", "attraction"),
                            )
                        )
            except json.JSONDecodeError:
                print(" LLM extraction failed, using places-only results")

        print(f" Found {len(places)} attractions")
        return {"places": PlacesList(places=places[:10])}

    except Exception as e:
        print(f" Places agent error: {e}")
        return {"places": PlacesList()}
