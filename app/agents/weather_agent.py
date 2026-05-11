"""
Weather Agent: fetches forecast from OpenWeatherMap.
"""

from app.schemas.trip_state import TripState
from app.schemas.weather import WeatherResult
from app.tools.weather_tool import fetch_weather


def weather_agent(state: TripState) -> dict:
    """Fetch weather forecast for the destination."""

    city = state["request"].destination
    print(f"\n  Weather Agent: fetching forecast for {city}...")

    try:
        result = fetch_weather(city)
        print(f"  Got {len(result.forecast)} day(s), {len(result.warnings)} warning(s)")
        return {"weather": result}
    except Exception as e:
        print(f" Weather API error: {e}")
        return {
            "weather": WeatherResult(
                city=city,
                country="",
                warnings=[f"Could not fetch weather: {str(e)}"],
            )
        }
