"""
Weather tool: calls OpenWeatherMap 5 day/3 hour forecast API.
"""

import httpx
from collections import defaultdict

from app.config import settings
from app.schemas.weather import WeatherResult, DayForecast


def fetch_weather(city: str) -> WeatherResult:
    """Fetch and aggregate weather forecast for a city."""

    response = httpx.get(
        "https://api.openweathermap.org/data/2.5/forecast",
        params={
            "q": city,
            "appid": settings.OPENWEATHER_API_KEY,
            "units": "metric",
            "cnt": 40,  # max readings (5 days × 8 per day)
        },
        timeout=15,
    )
    response.raise_for_status()
    data = response.json()
    daily: dict[str, list] = defaultdict(list)
    for item in data["list"]:
        date = item["dt_txt"].split(" ")[0]
        daily[date].append(item)

    forecast: list[DayForecast] = []
    for date, readings in list(daily.items())[:7]:
        temps = [r["main"]["temp"] for r in readings]
        humidities = [r["main"]["humidity"] for r in readings]
        winds = [r["wind"]["speed"] for r in readings]
        descs = [r["weather"][0]["description"] for r in readings]
        icons = [r["weather"][0]["icon"] for r in readings]

        forecast.append(
            DayForecast(
                date=date,
                temp_min=round(min(temps), 1),
                temp_max=round(max(temps), 1),
                humidity=round(sum(humidities) / len(humidities)),
                description=max(set(descs), key=descs.count),  # most common
                icon=icons[len(icons) // 2],
                wind_speed=round(sum(winds) / len(winds), 1),
            )
        )

    warnings: list[str] = []
    for day in forecast:
        if day.temp_max > 38:
            warnings.append(f"Extreme heat on {day.date} ({day.temp_max}°C)")
        if day.temp_min < 2:
            warnings.append(f"Near freezing on {day.date} ({day.temp_min}°C)")
        if "rain" in day.description.lower() or "storm" in day.description.lower():
            warnings.append(f"Rain expected on {day.date}: {day.description}")

    city_info = data.get("city", {})
    return WeatherResult(
        city=city_info.get("name", city),
        country=city_info.get("country", ""),
        forecast=forecast,
        warnings=warnings,
    )
