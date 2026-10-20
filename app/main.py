"""
FastAPI application for GenAI Event Planning Assistant.
"""
from __future__ import annotations
import os
import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.models import (
    EventPlan, EventGenerationRequest, CustomIdeaRequest,
    IdeaItem, BudgetItem, TimelineItem, VendorItem
)
from app.planner_engine import generate_plan_with_ai, generate_custom_ideas_ai
from app.storage import get_all_events, get_event_by_id, save_event, delete_event

app = FastAPI(
    title="CelebrateAI - GenAI Event Planning Assistant",
    description="Intelligent planning assistant for Weddings, Birthdays, and Community Events with Budgets, Timelines, Vendor Checklists & Ideas.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")

@app.get("/api/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.datetime.now().isoformat()}

@app.get("/api/events", response_model=List[EventPlan])
def list_events():
    return get_all_events()

@app.get("/api/events/{event_id}", response_model=EventPlan)
def get_event(event_id: str):
    plan = get_event_by_id(event_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Event plan not found")
    return plan

@app.post("/api/events/generate", response_model=EventPlan)
def create_event(req: EventGenerationRequest):
    plan = generate_plan_with_ai(req)
    saved = save_event(plan)
    return saved

@app.put("/api/events/{event_id}", response_model=EventPlan)
def update_event(event_id: str, updated: EventPlan):
    existing = get_event_by_id(event_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Event plan not found")
    updated.id = event_id
    updated.updated_at = datetime.datetime.now().isoformat()
    return save_event(updated)

@app.delete("/api/events/{event_id}")
def remove_event(event_id: str):
    success = delete_event(event_id)
    if not success:
        raise HTTPException(status_code=404, detail="Event plan not found")
    return {"status": "deleted", "id": event_id}

@app.post("/api/events/{event_id}/ideas/generate", response_model=List[IdeaItem])
def generate_ideas(event_id: str, req: CustomIdeaRequest):
    plan = get_event_by_id(event_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Event plan not found")
    new_ideas = generate_custom_ideas_ai(req)
    # Append to existing plan and save
    plan.personalized_ideas.extend(new_ideas)
    plan.updated_at = datetime.datetime.now().isoformat()
    save_event(plan)
    return new_ideas

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def serve_index():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "CelebrateAI API running. Static frontend not found."}
