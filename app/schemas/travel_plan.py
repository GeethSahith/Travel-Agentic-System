"""Final travel plan: it is synthesiser merged output."""

from pydantic import BaseModel, Field
from typing import Optional

from .weather import WeatherResult
from .places import PlacesList
from .hotels import HotelList
from .restaurants import RestaurantList
from .images import ImageCollection


class DayPlan(BaseModel):
    day: int
    title: str
    activities: list[str] = Field(default_factory=list)


class FinalTravelPlan(BaseModel):
    destination: str
    summary: str = ""
    weather: Optional[WeatherResult] = None
    places: Optional[PlacesList] = None
    hotels: Optional[HotelList] = None
    restaurants: Optional[RestaurantList] = None
    images: Optional[ImageCollection] = None
    itinerary: list[DayPlan] = Field(default_factory=list)
