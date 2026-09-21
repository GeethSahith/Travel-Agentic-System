"""
POST /api/travel-plan — accepts a TripRequest and runs the full LangGraph workflow.
"""

from fastapi import APIRouter, HTTPException
from app.schemas.trip_request import TripRequest
from app.graph.builder import build_trip_graph

router = APIRouter(prefix="/api", tags=["Travel Plan"])

# Build the graph once at module level so it's reused across requests
trip_graph = build_trip_graph()


@router.post("/travel-plan")
async def create_travel_plan(request: TripRequest):
    """
    Accept a structured TripRequest, run the multi-agent travel planning
    workflow, and return the final travel plan as JSON.
    """
    # Build a raw_input string from the TripRequest fields so the
    # orchestrator (which expects raw_input) can process it normally.
    parts = [request.destination]
    if request.country:
        parts.append(request.country)
    if request.dates:
        parts.append(f"dates: {request.dates}")
    if request.budget:
        parts.append(f"budget: {request.budget}")
    if request.preferences:
        parts.append(f"preferences: {', '.join(request.preferences)}")
    raw_input = ", ".join(parts)

    try:
        result = trip_graph.invoke({"raw_input": raw_input})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Workflow failed: {e}")

    plan = result.get("plan")
    if not plan:
        raise HTTPException(status_code=500, detail="No travel plan was generated.")

    return plan.model_dump()
