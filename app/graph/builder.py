"""
LangGraph StateGraph builder.
Execution flow:
  START → Orchestrator → [Weather | Places | Hotels | Restaurants] → Images → Synthesizer → END
"""

from langgraph.graph import StateGraph, START, END
import os
from app.schemas.trip_state import TripState
from app.agents.orchestrator import orchestrator
from app.agents.weather_agent import weather_agent
from app.agents.places_agent import places_agent
from app.agents.hotels_agent import hotels_agent
from app.agents.restaurants_agent import restaurants_agent
from app.agents.images_agent import images_agent
from app.agents.synthesizer import synthesizer


def build_trip_graph():
    """Build and compile the multi-agent travel planning graph."""

    graph = StateGraph(TripState)

    graph.add_node("orchestrator", orchestrator)
    graph.add_node("weather", weather_agent)
    graph.add_node("places", places_agent)
    graph.add_node("hotels", hotels_agent)
    graph.add_node("restaurants", restaurants_agent)
    graph.add_node("images", images_agent)
    graph.add_node("synthesizer", synthesizer)

    graph.add_edge(START, "orchestrator")
    graph.add_edge("orchestrator", "weather")
    graph.add_edge("orchestrator", "places")
    graph.add_edge("orchestrator", "hotels")
    graph.add_edge("orchestrator", "restaurants")
    graph.add_edge("weather", "images")
    graph.add_edge("places", "images")
    graph.add_edge("hotels", "images")
    graph.add_edge("restaurants", "images")
    graph.add_edge("images", "synthesizer")
    graph.add_edge("synthesizer", END)
    
    app = graph.compile()
  
    # png_data = app.get_graph().draw_mermaid_png()
    # with open("visualize.png", "wb") as f:
    #     f.write(png_data)
    # print("Graph saved to visualize.png")
    # os.startfile("visualize.png") 
    return app
