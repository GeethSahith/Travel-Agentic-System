"""Tourist attractions schema: output of the Places Agent."""

from pydantic import BaseModel, Field
from typing import Optional


class Place(BaseModel):
    name: str
    description: str = ""
    rating: Optional[float] = None
    category: str = "attraction"
    link: Optional[str] = None


class PlacesList(BaseModel):
    places: list[Place] = Field(default_factory=list)
