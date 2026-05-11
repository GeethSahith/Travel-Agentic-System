"""Restaurants schema: output of the Restaurants Agent."""

from pydantic import BaseModel, Field
from typing import Optional


class Restaurant(BaseModel):
    name: str
    cuisine: str = ""
    rating: Optional[float] = None
    price_range: str = ""
    address: str = ""
    link: Optional[str] = None


class RestaurantList(BaseModel):
    restaurants: list[Restaurant] = Field(default_factory=list)
