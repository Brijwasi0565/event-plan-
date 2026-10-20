from __future__ import annotations
from typing import List, Optional, Literal, Dict
from pydantic import BaseModel, Field

EventType = Literal["wedding", "birthday", "community", "other"]

class ColorPalette(BaseModel):
    primary: str = "#4F46E5"
    secondary: str = "#EC4899"
    accent: str = "#F59E0B"
    neutral: str = "#F3F4F6"
    description: str = "Modern Vibrant Palette"

class BudgetItem(BaseModel):
    id: str
    category: str
    name: str
    allocated_amount: float
    actual_amount: float = 0.0
    status: Literal["estimated", "quoted", "booked", "paid"] = "estimated"
    notes: str = ""

class TimelineItem(BaseModel):
    id: str
    phase: str
    timeframe: str
    title: str
    description: str
    is_completed: bool = False
    priority: Literal["high", "medium", "low"] = "medium"
    assigned_to: Optional[str] = "Organizer"

class VendorItem(BaseModel):
    id: str
    category: str
    name: str
    status: Literal["to_contact", "proposal_received", "negotiating", "booked", "paid_in_full"] = "to_contact"
    estimated_cost: float = 0.0
    contract_signed: bool = False
    deposit_paid: float = 0.0
    balance_due: float = 0.0
    contact_email: Optional[str] = ""
    contact_phone: Optional[str] = ""
    key_questions_to_ask: List[str] = Field(default_factory=list)
    notes: str = ""

class IdeaItem(BaseModel):
    id: str
    category: str
    title: str
    description: str
    cost_level: Literal["$", "$$", "$$$", "Free / DIY"] = "$$"
    impact_level: Literal["High", "Medium", "Memorable"] = "High"

class EventPlan(BaseModel):
    id: str
    event_type: EventType
    title: str
    tagline: str
    date: Optional[str] = ""
    location: str = ""
    guest_count: int = 50
    total_budget: float = 5000.0
    currency: str = "$"
    theme_vibe: str = ""
    color_palette: ColorPalette = Field(default_factory=ColorPalette)
    budget_items: List[BudgetItem] = Field(default_factory=list)
    timeline_items: List[TimelineItem] = Field(default_factory=list)
    vendor_checklist: List[VendorItem] = Field(default_factory=list)
    personalized_ideas: List[IdeaItem] = Field(default_factory=list)
    ai_summary_and_tips: str = ""
    created_at: str = ""
    updated_at: str = ""

class EventGenerationRequest(BaseModel):
    event_type: EventType
    title: str
    date: Optional[str] = None
    days_until_event: Optional[int] = 120
    location: str = "Local Venue"
    guest_count: int = 50
    total_budget: float = 5000.0
    currency: str = "$"
    theme_vibe: Optional[str] = ""
    special_notes: Optional[str] = ""
    api_key: Optional[str] = None

class CustomIdeaRequest(BaseModel):
    event_type: EventType
    title: str
    theme_vibe: str
    prompt: str
    api_key: Optional[str] = None
