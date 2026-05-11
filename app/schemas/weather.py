"""Weather schema: output of the Weather Agent."""

from pydantic import BaseModel, Field
from typing import Optional


class DayForecast(BaseModel):
    date: str
    temp_min: float
    temp_max: float
    humidity: int
    description: str
    icon: str
    wind_speed: float


class WeatherResult(BaseModel):
    city: str
    country: str = ""
    forecast: list[DayForecast] = Field(default_factory=list)
    best_time_to_visit: Optional[str] = None
    warnings: list[str] = Field(default_factory=list)
