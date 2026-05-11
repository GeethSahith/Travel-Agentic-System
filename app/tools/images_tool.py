"""
Images tool: uses Serper api image search to find photos
of attractions, hotels, and restaurants.
"""

import httpx
from app.config import settings
from app.schemas.images import ImageItem


def fetch_images(query: str, num_results: int = 5) -> list[ImageItem]:
    """Search for images via Serper.dev Google Images endpoint."""

    response = httpx.post(
        "https://google.serper.dev/images",
        headers={
            "X-API-KEY": settings.SERPER_API_KEY,
            "Content-Type": "application/json",
        },
        json={"q": query, "num": num_results},
        timeout=15,
    )
    response.raise_for_status()
    data = response.json()

    images: list[ImageItem] = []
    for item in data.get("images", []):
        url = item.get("imageUrl", "")
        if url:
            images.append(
                ImageItem(
                    url=url,
                    alt_text=item.get("title", ""),
                    source=item.get("link", ""),
                    width=item.get("imageWidth"),
                    height=item.get("imageHeight"),
                )
            )

    return images
