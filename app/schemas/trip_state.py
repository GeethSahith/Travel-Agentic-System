"""
TripState — the shared state object flowing through the LangGraph.
"""

from typing import TypedDict

from .trip_request import TripRequest
from .weather import WeatherResult
from .places import PlacesList
from .hotels import HotelList
from .restaurants import RestaurantList
from .images import ImageCollection
from .travel_plan import FinalTravelPlan


class TripState(TypedDict, total=False):
    # from run.py
    raw_input: str

    # set by the orchestrator
    request: TripRequest

    # set by individual agents
    weather: WeatherResult
    places: PlacesList
    hotels: HotelList
    restaurants: RestaurantList
    images: ImageCollection

    # set by the synthesizer
    plan: FinalTravelPlan
