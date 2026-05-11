"""Hotels schema: output of the Hotels Agent."""

from pydantic import BaseModel, Field
from typing import Optional


class Hotel(BaseModel):
    name: str
    price_per_night: Optional[str] = None
    rating: Optional[float] = None
    location: str = ""
    amenities: list[str] = Field(default_factory=list)
    link: Optional[str] = None


class HotelList(BaseModel):
    hotels: list[Hotel] = Field(default_factory=list)
