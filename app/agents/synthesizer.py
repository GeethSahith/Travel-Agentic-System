"""
Synthesizer Agent: merges all agent outputs into a coherent travel plan.
Uses the LLM to generate a readable summary and day by day itinerary.
"""

import json
from app.schemas.trip_state import TripState
from app.schemas.travel_plan import FinalTravelPlan, DayPlan
from app.llm.ollama_client import get_llm

SYNTHESIZER_PROMPT = """
You are a travel planning expert. Create a comprehensive travel plan based on the following data collected by specialized agents.

DESTINATION: {destination}
BUDGET: {budget}

WEATHER FORECAST:
{weather_summary}

TOP ATTRACTIONS:
{places_summary}

RECOMMENDED HOTELS:
{hotels_summary}

RECOMMENDED RESTAURANTS:
{restaurants_summary}

Create a JSON response with:
- "summary": A 3-4 sentence engaging overview of the trip
- "itinerary": A list of day plans, each with:
  - "day": day number (integer)
  - "title": catchy title for the day (e.g. "Beach Day & Local Cuisine")
  - "activities": list of 3-5 specific activities with times (e.g. "9:00 AM - Visit Fort Aguada")

Base the itinerary on the actual attractions, restaurants, and weather data provided.
If weather warnings exist, adjust activities accordingly (suggest indoor alternatives on rainy days).

Return ONLY the raw JSON object. No markdown, no explanation."""


def _summarize_weather(state: TripState) -> str:
    weather = state.get("weather")
    if not weather or not weather.forecast:
        return "No weather data available."
    lines = []
    for day in weather.forecast:
        lines.append(f"  {day.date}: {day.temp_min}°-{day.temp_max}°C, {day.description}")
    if weather.warnings:
        lines.append(f"  Warnings: {', '.join(weather.warnings)}")
    return "\n".join(lines)


def _summarize_places(state: TripState) -> str:
    places = state.get("places")
    if not places or not places.places:
        return "No attractions found."
    return "\n".join(f"  - {p.name}: {p.description[:100]}" for p in places.places[:8])


def _summarize_hotels(state: TripState) -> str:
    hotels = state.get("hotels")
    if not hotels or not hotels.hotels:
        return "No hotels found."
    lines = []
    for h in hotels.hotels[:5]:
        price = f", {h.price_per_night}/night" if h.price_per_night else ""
        rating = f", ★{h.rating}" if h.rating else ""
        lines.append(f"  - {h.name}{price}{rating}")
    return "\n".join(lines)


def _summarize_restaurants(state: TripState) -> str:
    restaurants = state.get("restaurants")
    if not restaurants or not restaurants.restaurants:
        return "No restaurants found."
    lines = []
    for r in restaurants.restaurants[:5]:
        rating = f", ★{r.rating}" if r.rating else ""
        lines.append(f"  - {r.name} ({r.cuisine}){rating}")
    return "\n".join(lines)


def synthesizer(state: TripState) -> dict:
    """Merge all agent results into a final structured travel plan."""

    request = state.get("request")
    destination = request.destination if request else "Unknown"
    budget = request.budget if request else "moderate"

    print(f"\n Synthesizer: generating travel plan for {destination}...")

    prompt = SYNTHESIZER_PROMPT.format(
        destination=destination,
        budget=budget,
        weather_summary=_summarize_weather(state),
        places_summary=_summarize_places(state),
        hotels_summary=_summarize_hotels(state),
        restaurants_summary=_summarize_restaurants(state),
    )

    llm = get_llm()
    response = llm.invoke(prompt)

    try:
        content = response.content.strip()

        # Strip markdown code fences
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]

        parsed = json.loads(content.strip())

        itinerary = [
            DayPlan(
                day=d.get("day", i + 1),
                title=d.get("title", f"Day {i + 1}"),
                activities=d.get("activities", []),
            )
            for i, d in enumerate(parsed.get("itinerary", []))
        ]

        plan = FinalTravelPlan(
            destination=destination,
            summary=parsed.get("summary", ""),
            weather=state.get("weather"),
            places=state.get("places"),
            hotels=state.get("hotels"),
            restaurants=state.get("restaurants"),
            images=state.get("images"),
            itinerary=itinerary,
        )
    except (json.JSONDecodeError, KeyError) as e:
        print(f"  Synthesizer parse error ({e}), building plan without LLM summary")
        plan = FinalTravelPlan(
            destination=destination,
            summary=f"Travel plan for {destination}",
            weather=state.get("weather"),
            places=state.get("places"),
            hotels=state.get("hotels"),
            restaurants=state.get("restaurants"),
            images=state.get("images"),
        )

    print(f" Plan ready: {len(plan.itinerary)} days in itinerary")
    return {"plan": plan}
