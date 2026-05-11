"""Trip request: the parsed user intent from orchestrator agent."""

from pydantic import BaseModel, Field
from typing import Optional


class TripRequest(BaseModel):
    destination: str = Field(..., description="City or place name")
    country: Optional[str] = Field(None, description="Country name")
    dates: Optional[str] = Field(None, description="Travel dates as free text")
    budget: Optional[str] = Field(
        "moderate", description="Budget tier: budget | moderate | luxury"
    )
    preferences: list[str] = Field(
        default_factory=list, description="E.g. ['beaches', 'nightlife', 'culture']"
    )
