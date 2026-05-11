"""
Restaurants tool: searches for restaurants via Serper api.
"""

import httpx
from app.config import settings
from app.schemas.restaurants import Restaurant, RestaurantList


def fetch_restaurants(city: str, cuisine: str = "") -> RestaurantList:
    """Search for top-rated restaurants in a city, optionally filtered by cuisine."""

    cuisine_part = f"{cuisine} " if cuisine else ""
    query = f"best {cuisine_part}restaurants in {city} with ratings"

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

    restaurants: list[Restaurant] = []
    seen_names: set[str] = set()

    for place in data.get("places", []):
        name = place.get("title", "").strip()
        if name and name not in seen_names:
            seen_names.add(name)
            restaurants.append(
                Restaurant(
                    name=name,
                    cuisine=cuisine,
                    rating=place.get("rating"),
                    price_range=place.get("price", ""),
                    address=place.get("address", ""),
                    link=place.get("link", ""),
                )
            )

    # Fill from organic results
    JUNK_WORDS = ["BEST", "TOP", "RANKING", "CHEAPEST", "MOST", "GUIDE", "REVIEW"]
    for item in data.get("organic", []):
        name = item.get("title", "").split(" - ")[0].split(" | ")[0].strip()
        if any(word in name.upper() for word in JUNK_WORDS):
            continue
        if name and name not in seen_names and len(name) < 80:
            seen_names.add(name)
            restaurants.append(
                Restaurant(
                    name=name,
                    cuisine=cuisine,
                    address=city,
                    link=item.get("link", ""),
                )
            )

    return RestaurantList(restaurants=restaurants[:10])
