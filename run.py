"""
Run:  This is the starting point of the graph and getting the request from the user"
"""

import sys
import json
from app.graph.builder import build_trip_graph


def pretty_print_plan(state: dict) -> None:
    """Print the final travel plan in a readable format."""

    plan = state.get("plan")
    if not plan:
        print("\n No plan was generated.")
        return

    print(f" TRAVEL PLAN: {plan.destination}")

    # Summary
    if plan.summary:
        print(f"\n {plan.summary}")

    # Weather
    if plan.weather and plan.weather.forecast:
        print(f"\n  WEATHER FORECAST ({plan.weather.city}, {plan.weather.country})")
        print("-" * 50)
        for day in plan.weather.forecast:
            print(f"  {day.date}  |  {day.temp_min}°–{day.temp_max}°C  |  {day.description}")
        if plan.weather.warnings:
            print(f"\n  Warnings:")
            for w in plan.weather.warnings:
                print(f"     {w}")

    # Places
    if plan.places and plan.places.places:
        print(f"\n TOP ATTRACTIONS")
        print("-" * 50)
        for i, p in enumerate(plan.places.places, 1):
            rating = f" (★{p.rating})" if p.rating else ""
            print(f"  {i}. {p.name}{rating}")
            if p.description:
                print(f"     {p.description[:120]}")

    # Hotels
    if plan.hotels and plan.hotels.hotels:
        print(f"\n RECOMMENDED HOTELS")
        print("-" * 50)
        for i, h in enumerate(plan.hotels.hotels, 1):
            price = f" — {h.price_per_night}/night" if h.price_per_night else ""
            rating = f" (★{h.rating})" if h.rating else ""
            print(f"  {i}. {h.name}{rating}{price}")
            if h.location:
                print(f" {h.location}")

    # Restaurants
    if plan.restaurants and plan.restaurants.restaurants:
        print(f"\n RECOMMENDED RESTAURANTS")
        print("-" * 50)
        for i, r in enumerate(plan.restaurants.restaurants, 1):
            cuisine = f" [{r.cuisine}]" if r.cuisine else ""
            rating = f" (★{r.rating})" if r.rating else ""
            print(f"  {i}. {r.name}{cuisine}{rating}")
            if r.address:
                print(f"      {r.address}")

    # Images
    if plan.images and plan.images.images:
        print(f"\n IMAGES ({len(plan.images.images)} subjects)")
        print("-" * 50)
        for subject, imgs in plan.images.images.items():
            print(f"  {subject}: {len(imgs)} photo(s)")

    # Itinerary
    if plan.itinerary:
        print(f"\n DAY-BY-DAY ITINERARY")
        print("-" * 50)
        for day in plan.itinerary:
            print(f"\n  Day {day.day}: {day.title}")
            for activity in day.activities:
                print(f"    • {activity}")


def main():
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        user_input = input("\n Where do you want to travel? → ")

    if not user_input.strip():
        print("Please provide a destination!")
        sys.exit(1)

    print(f"\n Starting Travel Agent for: '{user_input}'")
    print("   This may take 30-60 seconds as agents work in parallel...\n")

    graph = build_trip_graph()
    result = graph.invoke({"raw_input": user_input})

    pretty_print_plan(result)

    plan = result.get("plan")
    if plan:
        output_file = "travel_plan.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(plan.model_dump(), f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
