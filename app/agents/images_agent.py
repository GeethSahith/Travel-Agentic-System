"""
Images Agent
  1. Search for attractions/landmarks
  2. Search for hotels/restaurants/food
  3. Local keyword matching to assign images to subjects
"""

from app.schemas.trip_state import TripState
from app.schemas.images import ImageItem, ImageCollection
from app.tools.images_tool import fetch_images


def _match_images(subject: str, all_images: list[ImageItem]) -> list[ImageItem]:
    """Match images to a subject using local keyword matching — no API call."""
    keywords = subject.lower().split()
    matched = []

    for img in all_images:
        alt = img.alt_text.lower()
        if any(kw in alt for kw in keywords if len(kw) > 2):
            matched.append(img)

    if not matched and all_images:
        matched = all_images[:2]

    return matched[:3] 


def images_agent(state: TripState) -> dict:
    """Fetch images with only 2 API calls."""

    request = state.get("request")
    city = request.destination if request else "travel"
    print(f"\n Images Agent: fetching photos for {city}...")

    attraction_names: list[str] = []
    hotel_names: list[str] = []
    restaurant_names: list[str] = []

    if state.get("places"):
        attraction_names = [p.name for p in state["places"].places[:5]]

    if state.get("hotels"):
        hotel_names = [h.name for h in state["hotels"].hotels[:3]]

    if state.get("restaurants"):
        restaurant_names = [r.name for r in state["restaurants"].restaurants[:3]]

    try:
        attractions_query = f"{city} tourist attractions landmarks beaches"
        hotels_food_query = f"{city} luxury hotels restaurants food"

        attractions_images = fetch_images(attractions_query, num_results=15)
        hotels_food_images = fetch_images(hotels_food_query, num_results=15)
        print(f" Fetched {len(attractions_images)} + {len(hotels_food_images)} images (2 API calls)")
    except Exception as e:
        print(f" Image search error: {e}")
        return {"images": ImageCollection()}

    all_images: dict[str, list[ImageItem]] = {}
    all_images[city] = attractions_images[:3] if attractions_images else []

    for name in attraction_names:
        matched = _match_images(name, attractions_images)
        if matched:
            all_images[name] = matched

    for name in hotel_names:
        matched = _match_images(name, hotels_food_images)
        if matched:
            all_images[name] = matched

    for name in restaurant_names:
        matched = _match_images(name, hotels_food_images)
        if matched:
            all_images[name] = matched

    print(f" Assigned images to {len(all_images)} subjects")
    return {"images": ImageCollection(images=all_images)}
