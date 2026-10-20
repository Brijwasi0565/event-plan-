"""
GenAI Planner Engine for Event Planning.
Integrates with Google Gemini API for dynamic AI generation and includes
a robust fallback domain-heuristic generator for guaranteed offline/zero-setup reliability.
"""
from __future__ import annotations
import os
import json
import uuid
import datetime
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional

from app.models import (
    EventPlan, EventGenerationRequest, CustomIdeaRequest,
    IdeaItem, BudgetItem, TimelineItem, VendorItem, ColorPalette
)
from app.event_templates import (
    build_wedding_heuristic_plan,
    build_birthday_heuristic_plan,
    build_community_heuristic_plan,
    get_palette_for_vibe
)

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

def call_gemini_api(prompt: str, api_key: str, system_instruction: str = "") -> Optional[str]:
    """Call Google Gemini API using native urllib to avoid heavy external dependencies."""
    url = f"{GEMINI_API_URL}?key={api_key}"
    
    payload: Dict[str, Any] = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.7,
            "maxOutputTokens": 4096
        }
    }
    
    if system_instruction:
        payload["systemInstruction"] = {
            "parts": [{"text": system_instruction}]
        }
        
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            resp_data = json.loads(response.read().decode("utf-8"))
            candidates = resp_data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "")
    except Exception as e:
        print(f"[Gemini API Warning] Request failed or timed out: {e}")
        return None
    return None

def generate_plan_with_ai(req: EventGenerationRequest) -> EventPlan:
    """
    Generate a full structured event plan using Gemini if API key is supplied,
    or using our expert heuristic engine.
    """
    api_key = req.api_key or os.environ.get("GEMINI_API_KEY", "").strip()

    if api_key:
        system_prompt = (
            "You are an elite, world-class professional event planner specializing in Weddings, Birthdays, and Community events. "
            "Generate an exhaustive, realistic, structured JSON event plan adhering strictly to the requested schema. "
            "The budget items must logically total approximately the user's target budget. "
            "Timelines must have distinct, chronological milestones leading up to day-of run-of-show. "
            "Vendor checklist items must include smart, practical questions to ask each vendor. "
            "Personalized ideas should be creative, distinct, and tailored specifically to the theme and vibe."
        )

        user_prompt = f"""
Plan a {req.event_type.upper()} event with the following parameters:
- Title: {req.title}
- Location: {req.location}
- Target Date: {req.date or 'Flexible'} (approx {req.days_until_event or 90} days away)
- Guest Count: {req.guest_count}
- Total Target Budget: {req.currency}{req.total_budget:,.2f}
- Desired Theme & Vibe: {req.theme_vibe or 'Modern, joyful, memorable'}
- Special Requirements/Notes: {req.special_notes or 'None'}

Return a single JSON object with this exact shape:
{{
  "tagline": "A short, evocative one-line theme tagline",
  "theme_vibe": "{req.theme_vibe or 'Chic & Memorable'}",
  "color_palette": {{
    "primary": "#hex",
    "secondary": "#hex",
    "accent": "#hex",
    "neutral": "#hex",
    "description": "Name and feeling of color scheme"
  }},
  "budget_items": [
    {{
      "id": "bgt-1",
      "category": "Venue / Catering / Decor / Media / Music / etc.",
      "name": "Item or service name",
      "allocated_amount": 1500.0,
      "actual_amount": 0.0,
      "status": "estimated",
      "notes": "Cost rationale and percentage breakdown"
    }}
  ],
  "timeline_items": [
    {{
      "id": "tml-1",
      "phase": "Phase description with timeframe",
      "timeframe": "e.g. 6 Months Out or 02:00 PM",
      "title": "Milestone action item",
      "description": "Clear step-by-step guidance",
      "is_completed": false,
      "priority": "high",
      "assigned_to": "Role or person"
    }}
  ],
  "vendor_checklist": [
    {{
      "id": "vnd-1",
      "category": "Catering / Photography / Florals / Rentals / etc.",
      "name": "Vendor role or company",
      "status": "to_contact",
      "estimated_cost": 2500.0,
      "contract_signed": false,
      "deposit_paid": 0.0,
      "balance_due": 2500.0,
      "contact_email": "example@vendor.com",
      "contact_phone": "+1 555-0199",
      "key_questions_to_ask": [
        "Insightful question 1",
        "Insightful question 2",
        "Insightful question 3"
      ],
      "notes": "Advice and requirements"
    }}
  ],
  "personalized_ideas": [
    {{
      "id": "idea-1",
      "category": "Theme & Decor / Food & Beverage / Guest Engagement / Budget Hacks",
      "title": "Memorable idea title",
      "description": "Detailed explanation of why it will wow guests",
      "cost_level": "$$ (or $, $$$, Free / DIY)",
      "impact_level": "High (or Medium, Memorable)"
    }}
  ],
  "ai_summary_and_tips": "Comprehensive 2-3 sentence strategic advice on maximizing value, saving budget, and avoiding common pitfalls."
}}
"""
        raw_json = call_gemini_api(user_prompt, api_key, system_prompt)
        if raw_json:
            try:
                # Strip markdown code blocks if returned
                cleaned = raw_json.strip()
                if cleaned.startswith("```json"):
                    cleaned = cleaned[7:]
                if cleaned.startswith("```"):
                    cleaned = cleaned[3:]
                if cleaned.endswith("```"):
                    cleaned = cleaned[:-3]
                parsed = json.loads(cleaned.strip())
                
                # Assign unique IDs if missing
                for b in parsed.get("budget_items", []):
                    if not b.get("id"):
                        b["id"] = f"bgt-{uuid.uuid4().hex[:6]}"
                for t in parsed.get("timeline_items", []):
                    if not t.get("id"):
                        t["id"] = f"tml-{uuid.uuid4().hex[:6]}"
                for v in parsed.get("vendor_checklist", []):
                    if not v.get("id"):
                        v["id"] = f"vnd-{uuid.uuid4().hex[:6]}"
                for i in parsed.get("personalized_ideas", []):
                    if not i.get("id"):
                        i["id"] = f"idea-{uuid.uuid4().hex[:6]}"

                now_iso = datetime.datetime.now().isoformat()
                return EventPlan(
                    id=f"evt-{uuid.uuid4().hex[:8]}",
                    event_type=req.event_type,
                    title=req.title,
                    tagline=parsed.get("tagline", f"An extraordinary {req.event_type} celebration"),
                    date=req.date or (datetime.date.today() + datetime.timedelta(days=req.days_until_event or 90)).isoformat(),
                    location=req.location,
                    guest_count=req.guest_count,
                    total_budget=req.total_budget,
                    currency=req.currency,
                    theme_vibe=req.theme_vibe or parsed.get("theme_vibe", "Joyful & Inspiring"),
                    color_palette=ColorPalette(**parsed.get("color_palette", {})),
                    budget_items=[BudgetItem(**item) for item in parsed.get("budget_items", [])],
                    timeline_items=[TimelineItem(**item) for item in parsed.get("timeline_items", [])],
                    vendor_checklist=[VendorItem(**item) for item in parsed.get("vendor_checklist", [])],
                    personalized_ideas=[IdeaItem(**item) for item in parsed.get("personalized_ideas", [])],
                    ai_summary_and_tips=parsed.get("ai_summary_and_tips", ""),
                    created_at=now_iso,
                    updated_at=now_iso
                )
            except Exception as parse_err:
                print(f"[Parser Warning] Failed to parse LLM structured output: {parse_err}. Falling back to domain heuristic.")

    # High-fidelity domain fallback engine
    req_dict = req.model_dump()
    if req.event_type == "wedding":
        plan_dict = build_wedding_heuristic_plan(req_dict)
    elif req.event_type == "birthday":
        plan_dict = build_birthday_heuristic_plan(req_dict)
    elif req.event_type == "community":
        plan_dict = build_community_heuristic_plan(req_dict)
    else:
        # Default custom
        plan_dict = build_wedding_heuristic_plan(req_dict)
        plan_dict["event_type"] = req.event_type

    return EventPlan.model_validate(plan_dict)


def generate_custom_ideas_ai(req: CustomIdeaRequest) -> List[IdeaItem]:
    """Generate dynamic personalized ideas based on a specific prompt."""
    api_key = req.api_key or os.environ.get("GEMINI_API_KEY", "").strip()
    
    if api_key:
        prompt = f"""
For a {req.event_type.upper()} titled '{req.title}' with theme/vibe '{req.theme_vibe}',
generate 3 fresh, innovative, unexpected ideas for:
Prompt: {req.prompt}

Return a JSON array of objects with:
[
  {{
    "category": "Theme & Decor / Food & Beverage / Guest Fun / Budget Hack",
    "title": "Creative Title",
    "description": "Engaging description with actionable details",
    "cost_level": "$ / $$ / $$$ / Free / DIY",
    "impact_level": "High / Medium / Memorable"
  }}
]
"""
        raw = call_gemini_api(prompt, api_key)
        if raw:
            try:
                cleaned = raw.strip()
                if cleaned.startswith("```json"):
                    cleaned = cleaned[7:]
                if cleaned.startswith("```"):
                    cleaned = cleaned[3:]
                if cleaned.endswith("```"):
                    cleaned = cleaned[:-3]
                parsed = json.loads(cleaned.strip())
                results = []
                for item in parsed:
                    results.append(IdeaItem(
                        id=f"idea-{uuid.uuid4().hex[:6]}",
                        category=item.get("category", "Personalized Idea"),
                        title=item.get("title", "Fresh Event Concept"),
                        description=item.get("description", ""),
                        cost_level=item.get("cost_level", "$$"),
                        impact_level=item.get("impact_level", "High")
                    ))
                if results:
                    return results
            except Exception as e:
                print(f"[Custom Ideas Error] {e}")

    # Fallback creative ideas tailored to query
    p_lower = req.prompt.lower()
    items = []
    if "drink" in p_lower or "cocktail" in p_lower or "food" in p_lower:
        items = [
            IdeaItem(
                id=f"idea-{uuid.uuid4().hex[:6]}",
                category="Food & Beverage",
                title="Bespoke Herb-Infused Smoked Mocktail Bar",
                description="Offer a live smoking gun station where bartenders infuse zero-proof botanicals and ciders with smoked cinnamon and applewood.",
                cost_level="$$",
                impact_level="High"
            ),
            IdeaItem(
                id=f"idea-{uuid.uuid4().hex[:6]}",
                category="Food & Beverage",
                title="Miniature Gourmet Comfort Food Passed Bites",
                description="Tiny grilled cheese triangles paired with shot glasses of creamy tomato bisque, served on rustic wooden trays.",
                cost_level="$",
                impact_level="Memorable"
            )
        ]
    elif "photo" in p_lower or "booth" in p_lower or "selfie" in p_lower:
        items = [
            IdeaItem(
                id=f"idea-{uuid.uuid4().hex[:6]}",
                category="Guest Engagement",
                title="Vintage Magazine Cover Pop-Up Studio",
                description="Guests step inside a framed physical magazine cut-out styled with event headlines and their names on the glossy masthead.",
                cost_level="$$",
                impact_level="Memorable"
            ),
            IdeaItem(
                id=f"idea-{uuid.uuid4().hex[:6]}",
                category="Guest Engagement",
                title="Live Digital Graffiti Wall",
                description="An infrared digital spray can allows guests to spray art onto a massive rear-projection screen and email themselves instant digital stickers.",
                cost_level="$$$",
                impact_level="High"
            )
        ]
    else:
        items = [
            IdeaItem(
                id=f"idea-{uuid.uuid4().hex[:6]}",
                category="Guest Experience",
                title="Curated Audio Memory Station",
                description="A dedicated quiet lounge where guests can record short audio stories, advice, and celebratory wishes.",
                cost_level="$",
                impact_level="Memorable"
            ),
            IdeaItem(
                id=f"idea-{uuid.uuid4().hex[:6]}",
                category="Budget Hacks & DIY",
                title="Community / Friend Talent Barter",
                description="Exchange custom event invitations or thank-you gifts with talented friends who can MC, DJ, or bake desserts.",
                cost_level="Free / DIY",
                impact_level="High"
            )
        ]
    return items
