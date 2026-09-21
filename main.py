"""
FastAPI entry point for the Travel Agent system.
Run with:  uvicorn main:app --reload
Docs at:   http://localhost:8000/docs
"""

from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Travel Agent API",
    description="Multi-agent travel planning system powered by LangGraph",
    version="1.0.0",
)

app.include_router(router)


@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "message": "Travel Agent API is running"}
