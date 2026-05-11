"""
Hotels tool: searches for hotels via Serper api.
"""

import httpx
from app.config import settings
from app.schemas.hotels import Hotel, HotelList


def fetch_hotels(city: str, budget: str = "moderate") -> HotelList:
    """Search for top-rated hotels in a city."""

    query = f"best {budget} hotels in {city} with prices and ratings"

    response = httpx.post(
        "https://google.serper.dev/search",
        headers={
            "X-API-KEY": settings.SERPER_API_KEY,
            "Content-Type": "application/json",
        },
        json={"q": query, "num": 10},
        timeout=15,
    )
    response.raise_for_status()
    data = response.json()

    hotels: list[Hotel] = []
    seen_names: set[str] = set()

    for place in data.get("places", []):
        name = place.get("title", "").strip()
        if name and name not in seen_names:
            seen_names.add(name)
            hotels.append(
                Hotel(
                    name=name,
                    rating=place.get("rating"),
                    price_per_night=place.get("price"),
                    location=place.get("address", city),
                    link=place.get("link", ""),
                )
            )

    # Fill remaining from organic results
    JUNK_WORDS = ["BEST", "TOP", "RANKING", "CHEAPEST", "MOST", "GUIDE", "REVIEW"]
    for item in data.get("organic", []):
        name = item.get("title", "").split(" - ")[0].split(" | ")[0].strip()
        if any(word in name.upper() for word in JUNK_WORDS):
            continue
        if name and name not in seen_names and len(name) < 80:
            seen_names.add(name)
            hotels.append(
                Hotel(
                    name=name,
                    location=city,
                    link=item.get("link", ""),
                )
            )

    return HotelList(hotels=hotels[:10])
