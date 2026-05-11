"""Image schema: output of the Images Agent."""

from pydantic import BaseModel, Field
from typing import Optional


class ImageItem(BaseModel):
    url: str
    alt_text: str = ""
    source: str = ""
    width: Optional[int] = None
    height: Optional[int] = None


class ImageCollection(BaseModel):
    """Maps subject names (place/hotel/restaurant) to their images."""
    images: dict[str, list[ImageItem]] = Field(default_factory=dict)
