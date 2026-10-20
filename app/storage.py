"""
Storage layer for Event Plans with JSON file persistence and pre-loaded showcase events.
"""
from __future__ import annotations
import os
import json
from typing import Dict, List, Optional
from app.models import EventPlan
from app.event_templates import (
    build_wedding_heuristic_plan,
    build_birthday_heuristic_plan,
    build_community_heuristic_plan
)

STORAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
STORAGE_FILE = os.path.join(STORAGE_DIR, "events.json")

def _ensure_storage():
    os.makedirs(STORAGE_DIR, exist_ok=True)
    if not os.path.exists(STORAGE_FILE):
        # Seed initial showcase plans
        wedding_seed = build_wedding_heuristic_plan({
            "title": "Maya & Julian's Romantic Garden Wedding",
            "location": "Willowbrook Botanical Gardens, Austin TX",
            "total_budget": 28000.0,
            "guest_count": 120,
            "theme_vibe": "Boho Floral Garden, Acoustic Sunset & Golden Lights",
            "currency": "$"
        })
        birthday_seed = build_birthday_heuristic_plan({
            "title": "Leo's Epic 90s Throwback 30th Birthday",
            "location": "Skyline Loft & Terrace, Downtown",
            "total_budget": 4500.0,
            "guest_count": 45,
            "theme_vibe": "Neon 90s Nostalgia, Arcade Cocktails & Vinyl DJ",
            "currency": "$"
        })
        community_seed = build_community_heuristic_plan({
            "title": "Riverside Community Earth Day Fair & 5K",
            "location": "Oakwood Memorial Park & Riverside Trail",
            "total_budget": 8500.0,
            "guest_count": 400,
            "theme_vibe": "Eco-Friendly Festival, Local Artisans, Live Brass Band",
            "currency": "$"
        })
        seeds = {
            wedding_seed["id"]: wedding_seed,
            birthday_seed["id"]: birthday_seed,
            community_seed["id"]: community_seed
        }
        with open(STORAGE_FILE, "w", encoding="utf-8") as f:
            json.dump(seeds, f, indent=2)

def get_all_events() -> List[EventPlan]:
    _ensure_storage()
    try:
        with open(STORAGE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [EventPlan.model_validate(val) for val in data.values()]
    except Exception as e:
        print(f"[Storage Error] {e}")
        return []

def get_event_by_id(event_id: str) -> Optional[EventPlan]:
    _ensure_storage()
    try:
        with open(STORAGE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if event_id in data:
                return EventPlan.model_validate(data[event_id])
    except Exception as e:
        print(f"[Storage Error] {e}")
    return None

def save_event(plan: EventPlan) -> EventPlan:
    _ensure_storage()
    try:
        with open(STORAGE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = {}
    data[plan.id] = plan.model_dump()
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return plan

def delete_event(event_id: str) -> bool:
    _ensure_storage()
    try:
        with open(STORAGE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if event_id in data:
            del data[event_id]
            with open(STORAGE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            return True
    except Exception as e:
        print(f"[Storage Error] {e}")
    return False
