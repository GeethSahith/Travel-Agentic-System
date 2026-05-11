"""
Uses the LLM to parse raw user input into a structured TripRequest.
"""

import json
from app.schemas.trip_state import TripState
from app.schemas.trip_request import TripRequest
from app.llm.ollama_client import get_llm

ORCHESTRATOR_PROMPT = """You are a travel planning assistant. Extract structured information from the user's travel request.

User input: {raw_input}

Return a JSON object with EXACTLY these fields:
- "destination": the city or place name (required)
- "country": the country (if mentioned or can be inferred, otherwise null)
- "dates": travel dates as a string (if mentioned, otherwise null)
- "budget": one of "budget", "moderate", "luxury" (infer from context, default "moderate")
- "preferences": list of preferences like ["beaches", "nightlife", "culture", "food"] (infer from context)

Return ONLY the raw JSON object. No markdown, no explanation, no code fences."""


def orchestrator(state: TripState) -> dict:
    """Parse raw user input into a structured TripRequest using the LLM."""

    raw_input = state["raw_input"]
    print(f"\n Orchestrator: parsing '{raw_input}'...")

    llm = get_llm()
    response = llm.invoke(ORCHESTRATOR_PROMPT.format(raw_input=raw_input))

    try:
        content = response.content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]

        parsed = json.loads(content.strip())

        request = TripRequest(
            destination=parsed.get("destination", raw_input),
            country=parsed.get("country"),
            dates=parsed.get("dates"),
            budget=parsed.get("budget", "moderate"),
            preferences=parsed.get("preferences", []),
        )
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        print(f" LLM parse failed ({e}), falling back to raw input as destination")
        request = TripRequest(destination=raw_input)

    print(f" Parsed: {request.destination} ({request.country}), budget={request.budget}")
    return {"request": request}
