"""
Domain knowledge templates and generative heuristics for Weddings, Birthdays, and Community Events.
Provides realistic budget allocations, chronological planning phases, vendor checklists, and custom ideas.
"""
from typing import Dict, Any, List
import uuid
import datetime

WEDDING_BUDGET_RATIOS = [
    ("Venue & Rentals", "Main Ceremony & Reception Venue Booking", 0.28, "Venue"),
    ("Catering & Bar", "Full Dinner Catering, Hors D'oeuvres & Open Bar", 0.32, "Catering"),
    ("Photo & Video", "Full-day Photographer + Highlight Reel Videographer", 0.12, "Media"),
    ("Decor & Florals", "Bridal Bouquet, Centerpieces, Arch & Ambient Lighting", 0.08, "Decor"),
    ("Music & Entertainment", "Live Ceremony Musician & Reception DJ / MC", 0.07, "Entertainment"),
    ("Attire & Beauty", "Wedding Attire, Tailoring, Hair & Makeup Styling", 0.04, "Attire"),
    ("Stationery & Favors", "Save-the-Dates, Formal Invitations & Guest Keepsakes", 0.02, "Stationery"),
    ("Contingency & Tips", "Buffer for unexpected overtime, tips & weather logistics", 0.07, "Contingency"),
]

BIRTHDAY_BUDGET_RATIOS = [
    ("Venue & Space Rental", "Private Room, Backyard Tent or Event Hall", 0.25, "Venue"),
    ("Food & Beverages", "Catering, Specialty Finger Foods, Signature Cocktails & Drinks", 0.35, "Catering"),
    ("Custom Cake & Desserts", "Multi-tier Designer Theme Cake & Dessert Grazing Board", 0.08, "Dessert"),
    ("Entertainment & Games", "DJ / Host / Interactive Entertainer or Photo Booth", 0.14, "Entertainment"),
    ("Theme Decor & Balloons", "Custom Balloon Arch, Backdrops, Table Settings & Lighting", 0.10, "Decor"),
    ("Photography", "Event Photographer for Candid Memories & Group Portraits", 0.04, "Media"),
    ("Party Favors & Prizes", "Personalized Swag Bags & Game Winner Prizes", 0.04, "Favors"),
]

COMMUNITY_BUDGET_RATIOS = [
    ("Permits & City Fees", "Park/Street Closure Permits, Sound Variance & Insurance", 0.12, "Logistics"),
    ("Equipment & Stage Rentals", "Tents, Folding Tables/Chairs, PA Sound System & Stage", 0.28, "Equipment"),
    ("Community Refreshments", "Food Trucks, Hydration Stations & Volunteer Snacks", 0.22, "Food"),
    ("Entertainment & Activities", "Local Bands, Kid's Bounce Zone, Face Painters & Demonstrations", 0.18, "Entertainment"),
    ("Signage & Promotion", "Directional Banners, Flyers, Social Ads & Program Guides", 0.08, "Marketing"),
    ("Sanitation & Waste Mgmt", "Portable Restrooms, Trash/Recycling Stations & Clean-up", 0.07, "Sanitation"),
    ("First Aid & Safety Supplies", "Medical Station Supplies & Volunteer High-vis Vests", 0.05, "Safety"),
]

def get_palette_for_vibe(event_type: str, vibe: str) -> Dict[str, str]:
    vibe_lower = (vibe or "").lower()
    if "rustic" in vibe_lower or "boho" in vibe_lower or "earth" in vibe_lower:
        return {
            "primary": "#854D0E",      # Warm Ochre
            "secondary": "#15803D",    # Sage Green
            "accent": "#D97706",       # Terracotta
            "neutral": "#FEF3C7",      # Cream
            "description": "Boho Woodland & Terracotta Sunset"
        }
    elif "luxury" in vibe_lower or "black tie" in vibe_lower or "elegant" in vibe_lower:
        return {
            "primary": "#1E1B4B",      # Midnight Indigo
            "secondary": "#D97706",    # Warm Gold
            "accent": "#7C3AED",       # Royal Violet
            "neutral": "#F8FAFC",      # Pure Slate
            "description": "Midnight Velvet & Champagne Gold"
        }
    elif "neon" in vibe_lower or "retro" in vibe_lower or "festival" in vibe_lower:
        return {
            "primary": "#EC4899",      # Electric Pink
            "secondary": "#06B6D4",    # Cyan Neon
            "accent": "#FACC15",       # Bright Amber
            "neutral": "#0F172A",      # Deep Midnight
            "description": "Electric Festival & Neon Glow"
        }
    elif event_type == "wedding":
        return {
            "primary": "#4F46E5",      # Royal Amethyst
            "secondary": "#FB7185",    # Blush Rose
            "accent": "#F59E0B",       # Golden Champagne
            "neutral": "#FDF2F8",      # Soft Whisper
            "description": "Romantic Blush & Golden Starlight"
        }
    elif event_type == "birthday":
        return {
            "primary": "#8B5CF6",      # Purple Violet
            "secondary": "#EC4899",    # Party Magenta
            "accent": "#10B981",       # Emerald Sparkle
            "neutral": "#F3F4F6",      # Bright Cloud
            "description": "Celebration Confetti & Vibrant Violet"
        }
    else: # Community
        return {
            "primary": "#059669",      # Fresh Evergreen
            "secondary": "#2563EB",    # Civic Blue
            "accent": "#D97706",       # Sunbeam Gold
            "neutral": "#F0FDF4",      # Morning Grass
            "description": "Community Green & Neighborhood Blue"
        }

def build_wedding_heuristic_plan(req_data: Dict[str, Any]) -> Dict[str, Any]:
    budget = float(req_data.get("total_budget", 20000.0))
    guests = int(req_data.get("guest_count", 100))
    currency = req_data.get("currency", "$")
    vibe = req_data.get("theme_vibe") or "Romantic Garden with Modern Elegance"
    title = req_data.get("title") or "Our Unforgettable Wedding Celebration"
    location = req_data.get("location") or "Enchanted Garden Estate"

    palette = get_palette_for_vibe("wedding", vibe)

    # Budget items
    budget_items = []
    for cat_name, desc, ratio, key in WEDDING_BUDGET_RATIOS:
        allocated = round(budget * ratio, 2)
        budget_items.append({
            "id": f"bgt-{uuid.uuid4().hex[:6]}",
            "category": key,
            "name": cat_name,
            "allocated_amount": allocated,
            "actual_amount": 0.0,
            "status": "estimated",
            "notes": f"{desc} (Targeting ~{int(ratio*100)}% of total)"
        })

    # Timeline milestones
    timeline_items = [
        {
            "id": f"tml-{uuid.uuid4().hex[:6]}",
            "phase": "Phase 1: Foundation (9-12 Months Out)",
            "timeframe": "12 Months Out",
            "title": "Establish Budget & Finalize Guest List Target",
            "description": f"Lock in overall target cap of {currency}{budget:,.0f} and estimate {guests} guests with both families.",
            "is_completed": False,
            "priority": "high",
            "assigned_to": "Couple"
        },
        {
            "id": f"tml-{uuid.uuid4().hex[:6]}",
            "phase": "Phase 1: Foundation (9-12 Months Out)",
            "timeframe": "10 Months Out",
            "title": "Secure Ceremony & Reception Venue",
            "description": f"Tour and sign contract for {location}. Verify weather rain plans and catering exclusivity policies.",
            "is_completed": False,
            "priority": "high",
            "assigned_to": "Couple"
        },
        {
            "id": f"tml-{uuid.uuid4().hex[:6]}",
            "phase": "Phase 2: Core Vendors (6-9 Months Out)",
            "timeframe": "8 Months Out",
            "title": "Book Priority Vendors (Photographer & Caterer)",
            "description": "High-demand wedding photographers and caterers book up to a year in advance. Conduct tastings.",
            "is_completed": False,
            "priority": "high",
            "assigned_to": "Planner / Couple"
        },
        {
            "id": f"tml-{uuid.uuid4().hex[:6]}",
            "phase": "Phase 2: Core Vendors (6-9 Months Out)",
            "timeframe": "6 Months Out",
            "title": "Send Save-the-Dates & Launch Wedding Website",
            "description": "Provide travel accommodations, hotel room blocks, and RSVP links for out-of-town guests.",
            "is_completed": False,
            "priority": "medium",
            "assigned_to": "Couple"
        },
        {
            "id": f"tml-{uuid.uuid4().hex[:6]}",
            "phase": "Phase 3: Design & Details (3-6 Months Out)",
            "timeframe": "4 Months Out",
            "title": "Florals, Decor Mockup & Attire Fittings",
            "description": f"Collaborate with florist on {palette['description']} color scheme and table centerpiece prototypes.",
            "is_completed": False,
            "priority": "medium",
            "assigned_to": "Couple"
        },
        {
            "id": f"tml-{uuid.uuid4().hex[:6]}",
            "phase": "Phase 4: Countdown (1-2 Months Out)",
            "timeframe": "6 Weeks Out",
            "title": "Formal Invitations & Dietary RSVPs",
            "description": "Collect finalized meal selections, food allergies, and build initial seating charts.",
            "is_completed": False,
            "priority": "high",
            "assigned_to": "Couple"
        },
        {
            "id": f"tml-{uuid.uuid4().hex[:6]}",
            "phase": "Phase 5: Final Week & Day-Of",
            "timeframe": "Week of Event",
            "title": "Ceremony Rehearsal & Vendor Run-of-Show Distribution",
            "description": "Walk through procession with bridal party and distribute minute-by-minute timeline to all vendors.",
            "is_completed": False,
            "priority": "high",
            "assigned_to": "Day-of Coordinator"
        },
        {
            "id": f"tml-{uuid.uuid4().hex[:6]}",
            "phase": "Day-Of Execution",
            "timeframe": "Day-Of: 02:00 PM - 11:00 PM",
            "title": "Live Run-of-Show & Celebration",
            "description": "02:00 PM First Look, 04:00 PM Ceremony, 05:00 PM Cocktail Hour, 06:30 PM Grand Entrance & Dinner, 08:30 PM Dancing & Cake.",
            "is_completed": False,
            "priority": "high",
            "assigned_to": "Event Lead"
        }
    ]

    # Vendor checklist with expert interview questions
    vendor_checklist = [
        {
            "id": f"vnd-{uuid.uuid4().hex[:6]}",
            "category": "Venue Coordinator",
            "name": f"{location} Management",
            "status": "proposal_received",
            "estimated_cost": round(budget * 0.28, 2),
            "contract_signed": False,
            "deposit_paid": 0.0,
            "balance_due": round(budget * 0.28, 2),
            "contact_email": "events@venue-example.com",
            "contact_phone": "+1 (555) 234-5678",
            "key_questions_to_ask": [
                "What is the noise curfew for outdoor music amplification?",
                "Are we required to use your preferred vendor list, or can we bring outside vendors?",
                "What is the exact load-in and load-out time window for decor setup?",
                "What is the backup inclement weather plan for outdoor ceremonies?"
            ],
            "notes": "Includes tables, chairs, and dedicated bridal suite."
        },
        {
            "id": f"vnd-{uuid.uuid4().hex[:6]}",
            "category": "Catering & Bar",
            "name": "Artisan Harvest Catering",
            "status": "to_contact",
            "estimated_cost": round(budget * 0.32, 2),
            "contract_signed": False,
            "deposit_paid": 0.0,
            "balance_due": round(budget * 0.32, 2),
            "contact_email": "hello@artisancatering.com",
            "contact_phone": "+1 (555) 345-6789",
            "key_questions_to_ask": [
                "Does the per-person quote include service staff, bartenders, and cleanup?",
                "How do you handle dietary restrictions (vegan, gluten-free, nut allergies)?",
                "Can we supply our own alcohol with a corkage fee, or must it be purchased through you?",
                "Do you provide cake-cutting service and late-night snack options?"
            ],
            "notes": f"Estimated at ~{currency}{round((budget * 0.32) / max(guests, 1), 0):,.0f} per guest all-inclusive."
        },
        {
            "id": f"vnd-{uuid.uuid4().hex[:6]}",
            "category": "Photography & Video",
            "name": "Lumière Wedding Studios",
            "status": "to_contact",
            "estimated_cost": round(budget * 0.12, 2),
            "contract_signed": False,
            "deposit_paid": 0.0,
            "balance_due": round(budget * 0.12, 2),
            "contact_email": "contact@lumierephoto.com",
            "contact_phone": "+1 (555) 456-7890",
            "key_questions_to_ask": [
                "Do you include a second shooter for dual-angle coverage?",
                "What is the turnaround time for receiving the sneak peek gallery vs full high-res album?",
                "Do we receive full printing rights to all edited digital photos?",
                "Have you shot at our venue before, and what are your favorite portrait spots?"
            ],
            "notes": "Request 8-10 hours coverage including prep and golden hour portraits."
        },
        {
            "id": f"vnd-{uuid.uuid4().hex[:6]}",
            "category": "DJ & Master of Ceremonies",
            "name": "SoundWave Entertainment",
            "status": "to_contact",
            "estimated_cost": round(budget * 0.07, 2),
            "contract_signed": False,
            "deposit_paid": 0.0,
            "balance_due": round(budget * 0.07, 2),
            "contact_email": "booking@soundwave-djs.com",
            "contact_phone": "+1 (555) 567-8901",
            "key_questions_to_ask": [
                "Do you provide separate audio setups for ceremony, cocktail hour, and dance floor?",
                "How do you accommodate a 'Do Not Play' list and crowd song requests?",
                "Do you bring wireless lapel microphones for the officiant and vows?"
            ],
            "notes": "Ask about intelligent dance floor wash lighting package."
        },
        {
            "id": f"vnd-{uuid.uuid4().hex[:6]}",
            "category": "Floral & Botanical Design",
            "name": "Botanica Floral Art",
            "status": "to_contact",
            "estimated_cost": round(budget * 0.08, 2),
            "contract_signed": False,
            "deposit_paid": 0.0,
            "balance_due": round(budget * 0.08, 2),
            "contact_email": "design@botanicadesign.com",
            "contact_phone": "+1 (555) 678-9012",
            "key_questions_to_ask": [
                "Which blooms are in season locally to maximize lushness within budget?",
                "Can ceremony floral installations (e.g. arch) be repurposed for the sweetheart table?",
                "Do you handle breakdown and vessel collection at the end of the night?"
            ],
            "notes": f"Theme palette: {palette['description']}."
        }
    ]

    # Personalized GenAI ideas
    personalized_ideas = [
        {
            "id": f"idea-{uuid.uuid4().hex[:6]}",
            "category": "Theme & Decor",
            "title": "Interactive Audio Guestbook with Vintage Rotary Phone",
            "description": "Set up a classic vintage rotary telephone where guests pick up the receiver, hear a recorded welcome from you, and leave heartfelt audio messages and toasts that you can keep as an audio vinyl record forever.",
            "cost_level": "$",
            "impact_level": "Memorable"
        },
        {
            "id": f"idea-{uuid.uuid4().hex[:6]}",
            "category": "Food & Beverage",
            "title": "His, Hers & Ours Signature Cocktail Trio + Mocktail Flight",
            "description": f"Feature tailored drinks like 'The Botanical Sparkler' (elderflower, prosecco, rosemary sprig) and an alcohol-free 'Spiced Orchard Spritz' using locally sourced fruits matching {palette['description']}.",
            "cost_level": "$$",
            "impact_level": "High"
        },
        {
            "id": f"idea-{uuid.uuid4().hex[:6]}",
            "category": "Budget Hacks & DIY",
            "title": "High-Impact Ceremony Arch Repurposing",
            "description": "Have your day-of coordinator or florist move the ceremony flower arch behind the sweetheart table during cocktail hour, doubling its visual impact without paying for two expensive statement pieces.",
            "cost_level": "Free / DIY",
            "impact_level": "High"
        },
        {
            "id": f"idea-{uuid.uuid4().hex[:6]}",
            "category": "Guest Engagement & Fun",
            "title": "Disposable Camera Scavenger Hunt / QR Live Gallery",
            "description": "Place instant cameras or a personalized QR code on every table with a playful prompt card: 'Snap the biggest smile', 'Catch the best dance floor spin', 'Capture a table clinking glasses'.",
            "cost_level": "$",
            "impact_level": "Memorable"
        },
        {
            "id": f"idea-{uuid.uuid4().hex[:6]}",
            "category": "Late Night Surprise",
            "title": "Midnight Gourmet Pretzel & Mini Milkshake Cart",
            "description": "Right when dancing hits its peak at 10 PM, wheel out warm Bavarian soft pretzels with artisan mustard dips and miniature dessert milkshakes to recharge the crowd.",
            "cost_level": "$$",
            "impact_level": "High"
        }
    ]

    ai_tips = (
        f"Planner Pro Tip: With a guest count of {guests} and a {currency}{budget:,.0f} budget "
        f"(~{currency}{round(budget/max(guests,1), 0):,.0f}/guest), your highest leverage area is the venue and catering "
        f"package. Booking an all-inclusive or BYO-beverage venue can save up to 18% in administrative and corkage fees. "
        f"Always safeguard your 7% contingency reserve ({currency}{round(budget*0.07, 0):,.0f}) for final-week headcount adjustments."
    )

    return {
        "id": f"evt-{uuid.uuid4().hex[:8]}",
        "event_type": "wedding",
        "title": title,
        "tagline": f"A breathtaking celebration styled in {palette['description']}",
        "date": req_data.get("date") or (datetime.date.today() + datetime.timedelta(days=240)).isoformat(),
        "location": location,
        "guest_count": guests,
        "total_budget": budget,
        "currency": currency,
        "theme_vibe": vibe,
        "color_palette": palette,
        "budget_items": budget_items,
        "timeline_items": timeline_items,
        "vendor_checklist": vendor_checklist,
        "personalized_ideas": personalized_ideas,
        "ai_summary_and_tips": ai_tips,
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }


def build_birthday_heuristic_plan(req_data: Dict[str, Any]) -> Dict[str, Any]:
    budget = float(req_data.get("total_budget", 3500.0))
    guests = int(req_data.get("guest_count", 35))
    currency = req_data.get("currency", "$")
    vibe = req_data.get("theme_vibe") or "Epic Retro Throwback Lounge Party"
    title = req_data.get("title") or "Milestone Birthday Extravaganza"
    location = req_data.get("location") or "Rooftop Lounge / Private Garden"

    palette = get_palette_for_vibe("birthday", vibe)

    budget_items = []
    for cat_name, desc, ratio, key in BIRTHDAY_BUDGET_RATIOS:
        allocated = round(budget * ratio, 2)
        budget_items.append({
            "id": f"bgt-{uuid.uuid4().hex[:6]}",
            "category": key,
            "name": cat_name,
            "allocated_amount": allocated,
            "actual_amount": 0.0,
            "status": "estimated",
            "notes": f"{desc} (~{int(ratio*100)}% budget)"
        })

    timeline_items = [
        {
            "id": f"tml-{uuid.uuid4().hex[:6]}",
            "phase": "Phase 1: Concept & Venue (6-8 Weeks Out)",
            "timeframe": "8 Weeks Out",
            "title": "Choose Theme & Lock in the Date & Venue",
            "description": f"Reserve {location} and confirm capacity for {guests} guests with appropriate sound setup.",
            "is_completed": False,
            "priority": "high",
            "assigned_to": "Host"
        },
        {
            "id": f"tml-{uuid.uuid4().hex[:6]}",
            "phase": "Phase 2: Invitations & Entertainment (4-6 Weeks Out)",
            "timeframe": "5 Weeks Out",
            "title": "Send Digital Video Invites & Book DJ/Entertainer",
            "description": "Send engaging animated invitations with themed dress code instructions and RSVP deadlines.",
            "is_completed": False,
            "priority": "high",
            "assigned_to": "Host"
        },
        {
            "id": f"tml-{uuid.uuid4().hex[:6]}",
            "phase": "Phase 3: Food, Custom Cake & Decor (2-4 Weeks Out)",
            "timeframe": "3 Weeks Out",
            "title": "Order Showstopper Cake & Finalize Menu",
            "description": f"Order bespoke multi-tier cake matching {palette['description']} and arrange cocktail finger food catering.",
            "is_completed": False,
            "priority": "medium",
            "assigned_to": "Host"
        },
        {
            "id": f"tml-{uuid.uuid4().hex[:6]}",
            "phase": "Phase 4: Final Preparations (1 Week Out)",
            "timeframe": "1 Week Out",
            "title": "Final Headcount & Playlist Curations",
            "description": "Confirm attendance count, assemble party favor bags, and review crowd-pleaser playlist with DJ.",
            "is_completed": False,
            "priority": "medium",
            "assigned_to": "Host"
        },
        {
            "id": f"tml-{uuid.uuid4().hex[:6]}",
            "phase": "Day-Of Party Timeline",
            "timeframe": "Party Day: 06:00 PM - 12:00 AM",
            "title": "Run of Show & Milestone Toast",
            "description": "04:30 PM Setup, 06:00 PM Doors Open & Welcome Drinks, 07:30 PM Bites & Entertainment, 09:00 PM Cake Cutting & Birthday Roast/Toast, 09:30 PM Dancing.",
            "is_completed": False,
            "priority": "high",
            "assigned_to": "Co-host / Emcee"
        }
    ]

    vendor_checklist = [
        {
            "id": f"vnd-{uuid.uuid4().hex[:6]}",
            "category": "Venue / Lounge",
            "name": f"{location} Booking",
            "status": "proposal_received",
            "estimated_cost": round(budget * 0.25, 2),
            "contract_signed": False,
            "deposit_paid": 0.0,
            "balance_due": round(budget * 0.25, 2),
            "contact_email": "private-events@lounge-example.com",
            "contact_phone": "+1 (555) 789-0123",
            "key_questions_to_ask": [
                "Is there an auxiliary input or Bluetooth connectivity for custom playlists?",
                "Can we bring our own specialty birthday cake without an exorbitant plating charge?",
                "What is the policy for hanging banners, neon signs, and balloon garlands?"
            ],
            "notes": "Confirm private bartender inclusion."
        },
        {
            "id": f"vnd-{uuid.uuid4().hex[:6]}",
            "category": "Catering & Finger Foods",
            "name": "BiteSize Gourmet Grazing Co.",
            "status": "to_contact",
            "estimated_cost": round(budget * 0.35, 2),
            "contract_signed": False,
            "deposit_paid": 0.0,
            "balance_due": round(budget * 0.35, 2),
            "contact_email": "orders@bitesizegourmet.com",
            "contact_phone": "+1 (555) 890-1234",
            "key_questions_to_ask": [
                "Do you provide grazing table presentation boards, warming trays, and stylish disposable utensils?",
                "Can you craft 3 vegetarian and gluten-free savory options?",
                "What is the shelf life/replenishment schedule during a 4-hour party?"
            ],
            "notes": "Plan for 6-8 heavy appetizers per guest."
        },
        {
            "id": f"vnd-{uuid.uuid4().hex[:6]}",
            "category": "Custom Cake Baker",
            "name": "Sweet Sculptures Bakery",
            "status": "to_contact",
            "estimated_cost": round(budget * 0.08, 2),
            "contract_signed": False,
            "deposit_paid": 0.0,
            "balance_due": round(budget * 0.08, 2),
            "contact_email": "cakes@sweetsculptures.com",
            "contact_phone": "+1 (555) 901-2345",
            "key_questions_to_ask": [
                "Can you create a custom topper or edible photo print relating to the theme?",
                "What flavor pairings do you recommend (e.g., Salted Caramel Dulce de Leche or Raspberry Lemon)?",
                "Do you offer refrigerated delivery directly to the venue?"
            ],
            "notes": f"Color accents: {palette['secondary']} and {palette['accent']}."
        },
        {
            "id": f"vnd-{uuid.uuid4().hex[:6]}",
            "category": "Entertainment / Photo Booth",
            "name": "FlashPop 360 & Glitz Booths",
            "status": "to_contact",
            "estimated_cost": round(budget * 0.14, 2),
            "contract_signed": False,
            "deposit_paid": 0.0,
            "balance_due": round(budget * 0.14, 2),
            "contact_email": "party@flashpopbooths.com",
            "contact_phone": "+1 (555) 012-3456",
            "key_questions_to_ask": [
                "Does the booth include instant SMS/AirDrop video sharing for social media?",
                "Can the physical printouts be branded with the guest-of-honor's name and celebration logo?",
                "Does an attendant stay with the booth throughout the active hours?"
            ],
            "notes": "Ask for glam filter and custom video boomerang option."
        }
    ]

    personalized_ideas = [
        {
            "id": f"idea-{uuid.uuid4().hex[:6]}",
            "category": "Theme & Decor",
            "title": "Custom LED Neon Name Sign Backdrop",
            "description": "Commission an illuminated neon sign of the birthday person's nickname or catchphrase, mounted over a lush balloon installation. After the party, they take it home to hang in their living room or office!",
            "cost_level": "$$",
            "impact_level": "Memorable"
        },
        {
            "id": f"idea-{uuid.uuid4().hex[:6]}",
            "category": "Guest Engagement & Fun",
            "title": "Hilarious 'Roast & Toast' Video Trivia Game",
            "description": "Before the party, crowdsource 5 funny questions about the birthday honoree. Run a rapid-fire smartphone trivia round (Kahoot style) with silly prizes for whoever knows them best.",
            "cost_level": "Free / DIY",
            "impact_level": "High"
        },
        {
            "id": f"idea-{uuid.uuid4().hex[:6]}",
            "category": "Food & Beverage",
            "title": "Mixology Cocktail Lab Station",
            "description": "Set up an interactive DIY garnish bar with dehydrated citrus wheels, smoked rosemary, edible glitter, and flavored syrups next to pre-batched craft spirits.",
            "cost_level": "$",
            "impact_level": "High"
        },
        {
            "id": f"idea-{uuid.uuid4().hex[:6]}",
            "category": "Memories & Keepsake",
            "title": "Giant Polarized 'Year of You' Memory Board",
            "description": "Collect photos from childhood, teenage years, and college up to present day, pinning them chronologically with blank speech bubbles for guests to write hilarious memories.",
            "cost_level": "$",
            "impact_level": "Memorable"
        }
    ]

    ai_tips = (
        f"Party Planner Tip: For an unforgettable birthday with {guests} guests, focus spending where guests dwell most: "
        f"great music, uninterrupted drinks, and an energetic centerpiece (like the photo booth or neon lounge). "
        f"Finger foods beat a formal sit-down meal for keeping conversation flowing and guests mingling freely!"
    )

    return {
        "id": f"evt-{uuid.uuid4().hex[:8]}",
        "event_type": "birthday",
        "title": title,
        "tagline": f"An electrifying birthday bash themed in {palette['description']}",
        "date": req_data.get("date") or (datetime.date.today() + datetime.timedelta(days=45)).isoformat(),
        "location": location,
        "guest_count": guests,
        "total_budget": budget,
        "currency": currency,
        "theme_vibe": vibe,
        "color_palette": palette,
        "budget_items": budget_items,
        "timeline_items": timeline_items,
        "vendor_checklist": vendor_checklist,
        "personalized_ideas": personalized_ideas,
        "ai_summary_and_tips": ai_tips,
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }


def build_community_heuristic_plan(req_data: Dict[str, Any]) -> Dict[str, Any]:
    budget = float(req_data.get("total_budget", 7500.0))
    guests = int(req_data.get("guest_count", 300))
    currency = req_data.get("currency", "$")
    vibe = req_data.get("theme_vibe") or "Inclusive Neighborhood Block Festival & Artisan Fair"
    title = req_data.get("title") or "Annual Community Block Fair & Unity Festival"
    location = req_data.get("location") or "Civic Community Park & Main Street"

    palette = get_palette_for_vibe("community", vibe)

    budget_items = []
    for cat_name, desc, ratio, key in COMMUNITY_BUDGET_RATIOS:
        allocated = round(budget * ratio, 2)
        budget_items.append({
            "id": f"bgt-{uuid.uuid4().hex[:6]}",
            "category": key,
            "name": cat_name,
            "allocated_amount": allocated,
            "actual_amount": 0.0,
            "status": "estimated",
            "notes": f"{desc} (~{int(ratio*100)}% allocation)"
        })

    timeline_items = [
        {
            "id": f"tml-{uuid.uuid4().hex[:6]}",
            "phase": "Phase 1: Permits & Community Coalition (12-16 Weeks Out)",
            "timeframe": "14 Weeks Out",
            "title": "Submit Municipal Permits & Park Reservation",
            "description": f"File municipal street closure permits, noise variance, and public liability insurance for {location}.",
            "is_completed": False,
            "priority": "high",
            "assigned_to": "Committee Lead"
        },
        {
            "id": f"tml-{uuid.uuid4().hex[:6]}",
            "phase": "Phase 2: Local Partner & Sponsor Outreach (8-12 Weeks Out)",
            "timeframe": "10 Weeks Out",
            "title": "Recruit Food Trucks, Local Artists & Sponsors",
            "description": "Send open call for community food vendors and local non-profits to host interactive booths.",
            "is_completed": False,
            "priority": "high",
            "assigned_to": "Partnerships Team"
        },
        {
            "id": f"tml-{uuid.uuid4().hex[:6]}",
            "phase": "Phase 3: Logistics & Volunteer Recruitment (4-8 Weeks Out)",
            "timeframe": "6 Weeks Out",
            "title": "Lock In Stage, Audio Equipment & Volunteer Roles",
            "description": "Schedule shifts for setup, gate greeters, waste recycling ambassadors, and safety liaisons.",
            "is_completed": False,
            "priority": "medium",
            "assigned_to": "Volunteer Coordinator"
        },
        {
            "id": f"tml-{uuid.uuid4().hex[:6]}",
            "phase": "Phase 4: Promotion & Safety Drill (1-3 Weeks Out)",
            "timeframe": "2 Weeks Out",
            "title": "Community Flyering, Social Blasts & Emergency Plan",
            "description": "Distribute banners across neighborhood businesses and establish emergency first-aid protocols.",
            "is_completed": False,
            "priority": "high",
            "assigned_to": "Marketing & Safety"
        },
        {
            "id": f"tml-{uuid.uuid4().hex[:6]}",
            "phase": "Day-Of Community Run-of-Show",
            "timeframe": "Festival Day: 08:00 AM - 06:00 PM",
            "title": "Festival Operations & Clean-Up",
            "description": "08:00 AM Street Closed & Vendor Load-in, 10:00 AM Gates Open & Welcome Address, 12:00 PM Live Youth Dance & Bands, 03:00 PM Community Raffle, 05:00 PM Festival Closes, 06:00 PM Street Cleaned & Reopened.",
            "is_completed": False,
            "priority": "high",
            "assigned_to": "Site Operations"
        }
    ]

    vendor_checklist = [
        {
            "id": f"vnd-{uuid.uuid4().hex[:6]}",
            "category": "Stage & AV Production",
            "name": "Community Sound & Stage Rentals",
            "status": "proposal_received",
            "estimated_cost": round(budget * 0.28, 2),
            "contract_signed": False,
            "deposit_paid": 0.0,
            "balance_due": round(budget * 0.28, 2),
            "contact_email": "info@communitystage.com",
            "contact_phone": "+1 (555) 123-4567",
            "key_questions_to_ask": [
                "Does the rental include generator power or do we hook into municipal power boxes?",
                "Is an experienced sound technician on-site all day to mic multiple performance groups?",
                "What is the wind load rating for the canopy stage cover in case of gusts?"
            ],
            "notes": "Includes 12x16 mobile stage, 4 PA speakers, and 6 wireless microphones."
        },
        {
            "id": f"vnd-{uuid.uuid4().hex[:6]}",
            "category": "City Permits & Public Works",
            "name": "City Parks & Recreation Department",
            "status": "to_contact",
            "estimated_cost": round(budget * 0.12, 2),
            "contract_signed": False,
            "deposit_paid": 0.0,
            "balance_due": round(budget * 0.12, 2),
            "contact_email": "permits@citygov.org",
            "contact_phone": "+1 (555) 234-8901",
            "key_questions_to_ask": [
                "Are police or traffic control officers required for pedestrian crosswalks?",
                "What is the deadline for submitting certificate of additional insured (COI)?",
                "Are food truck fire marshal inspections conducted prior to opening?"
            ],
            "notes": "Street closure approval requires neighbor signatures on file."
        },
        {
            "id": f"vnd-{uuid.uuid4().hex[:6]}",
            "category": "Sanitation & Eco-Waste",
            "name": "GreenEvent Clean & Restrooms",
            "status": "to_contact",
            "estimated_cost": round(budget * 0.07, 2),
            "contract_signed": False,
            "deposit_paid": 0.0,
            "balance_due": round(budget * 0.07, 2),
            "contact_email": "service@greeneventclean.com",
            "contact_phone": "+1 (555) 345-9012",
            "key_questions_to_ask": [
                "How many ADA-compliant accessible portable restrooms are recommended for 300+ guests?",
                "Do you provide clearly labeled triple-stream sorting bins (Compost, Recycling, Landfill)?",
                "What is the dispatch schedule for emptying bins during peak hours?"
            ],
            "notes": "Includes handwashing stations with foot-pump dispensers."
        },
        {
            "id": f"vnd-{uuid.uuid4().hex[:6]}",
            "category": "Community Kids Entertainment",
            "name": "WonderPlay Inflatables & Face Art",
            "status": "to_contact",
            "estimated_cost": round(budget * 0.18, 2),
            "contract_signed": False,
            "deposit_paid": 0.0,
            "balance_due": round(budget * 0.18, 2),
            "contact_email": "fun@wonderplaykids.com",
            "contact_phone": "+1 (555) 456-0123",
            "key_questions_to_ask": [
                "Are all operators certified and carry active commercial liability insurance?",
                "What are the age group restrictions for the obstacle course bounce house?",
                "What safety protocols are followed in case of sudden high winds or rain?"
            ],
            "notes": "Reserve 2 face painters and 1 interactive obstacle castle."
        }
    ]

    personalized_ideas = [
        {
            "id": f"idea-{uuid.uuid4().hex[:6]}",
            "category": "Community Art & Engagement",
            "title": "Collaborative 'Voices of Our Neighborhood' Canvas Mural",
            "description": "Erect an 8x16 foot freestanding wooden canvas where attendees of all ages paint what community means to them under the guidance of a local muralist. Once completed, donate it to the local library or community center.",
            "cost_level": "$",
            "impact_level": "Memorable"
        },
        {
            "id": f"idea-{uuid.uuid4().hex[:6]}",
            "category": "Eco & Sustainability",
            "title": "Zero-Waste Hydration Station & BYO Water Bottle Incentive",
            "description": "Partner with a local water filtration supplier to offer chilled fruit-infused water refill stations. Give out raffle tickets for local merchant gift baskets to anyone who brings a reusable bottle.",
            "cost_level": "Free / DIY",
            "impact_level": "High"
        },
        {
            "id": f"idea-{uuid.uuid4().hex[:6]}",
            "category": "Guest Engagement & Fun",
            "title": "Neighborhood 'Cook-Off / Bake-Off' Showdown",
            "description": "Host a friendly chili, pie, or salsa competition where community members can pay $5 for a tasting spoon to sample all entries and vote for the 'People's Choice Champion'. Proceeds offset permit fees!",
            "cost_level": "$",
            "impact_level": "High"
        },
        {
            "id": f"idea-{uuid.uuid4().hex[:6]}",
            "category": "Music & Culture",
            "title": "Cultural Storytelling & Youth Talent Showcase",
            "description": "Dedicate a 90-minute stage block to youth poetry, acoustic folk music, and senior community members sharing history and folklore about how the neighborhood was built.",
            "cost_level": "Free / DIY",
            "impact_level": "Memorable"
        }
    ]

    ai_tips = (
        f"Community Organizer Pro Tip: For public community events with {guests}+ projected attendees, "
        f"safety, sanitation, and municipal permissions are your absolute non-negotiables. "
        f"Engage local small businesses early to sponsor specific zones (e.g. 'Kid's Zone sponsored by Main St Bakery') "
        f"to offset equipment costs and multiply neighborhood turnout!"
    )

    return {
        "id": f"evt-{uuid.uuid4().hex[:8]}",
        "event_type": "community",
        "title": title,
        "tagline": f"An inspiring gathering celebrating community in {palette['description']}",
        "date": req_data.get("date") or (datetime.date.today() + datetime.timedelta(days=90)).isoformat(),
        "location": location,
        "guest_count": guests,
        "total_budget": budget,
        "currency": currency,
        "theme_vibe": vibe,
        "color_palette": palette,
        "budget_items": budget_items,
        "timeline_items": timeline_items,
        "vendor_checklist": vendor_checklist,
        "personalized_ideas": personalized_ideas,
        "ai_summary_and_tips": ai_tips,
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }
