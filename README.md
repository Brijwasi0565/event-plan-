# ✨ CelebrateAI — GenAI-Powered Event Planning Assistant

CelebrateAI is a full-featured, intelligent event planning assistant engineered to help organizers plan **Weddings**, **Birthdays**, and **Community Events** with structured budgets, chronological timelines, vendor interview checklists, and personalized theme ideas.

---

## 🌟 Key Features

### 1. 💍 Weddings, 🎂 Birthdays & 🌳 Community Events
Tailored domain architectures for distinct event types:
- **Weddings**: Rehearsal timelines, ceremony arches, photographer coverage, multi-course catering, floral preservation, and day-of minute-by-minute run of show.
- **Birthdays**: Milestone themes (e.g. 90s Throwback, Luxury Lounge, Kid's Adventures), interactive games, bespoke cakes, custom neon backdrops, and mixology stations.
- **Community Events**: Municipal street & park closure permits, stage & AV rental safety, food truck coordination, zero-waste hydration, volunteer shifts, and neighborhood engagement activities.

### 2. 💰 Dynamic Budget Allocation & Auto-Rebalancing
- Itemized allocations across Venue, Catering, Media, Decor, Music, Logistics, and Contingency buffers.
- Live calculations of **Total Ceiling**, **Allocated Plan**, **Actual Spent**, and **Remaining Buffer**.
- **Auto-Rebalance Engine**: Proportionally scales item budgets to strictly honor the user's spending ceiling without broken math.

### 3. 📅 Interactive Milestones & Run-of-Show
- Chronological phased roadmap (e.g., *Phase 1: Foundation (9-12 Months Out)* through *Day-Of Run of Show*).
- Interactive completion tracking with real-time percentage progress indicators.
- Filter by All, Pending, or Completed.
- Priority tagging (High, Medium, Low) and assigned-to roles.

### 4. 🤝 Vendor Checklist with AI Interview Guides
- End-to-end vendor CRM: Status tracking (`To Contact`, `Proposal Received`, `Negotiating`, `Booked`, `Paid in Full`), contract signing toggles, and deposit vs. balance tracking.
- **🧠 Expert AI Interview Questions**: Expandable questions for each vendor to uncover hidden fees, noise curfews, load-in constraints, and overtime charges.

### 5. 💡 Personalized GenAI Ideas & Brainstormer
- Bespoke aesthetic color palettes (Primary, Secondary, Accent, Neutral) with one-click hex copying.
- Signature drink concepts, interactive icebreakers, budget hacks, and grand exit surprises.
- Real-time custom brainstorming bar with preset chips for signature cocktails, photo booths, and DIY decor.

---

## 🚀 Quickstart Guide

### 1. Requirements
- Python 3.10+
- Installed packages: `fastapi`, `uvicorn`, `pydantic`

```bash
pip install -r requirements.txt
```

### 2. Start the Server
```bash
python run.py
```
Open your browser to:
👉 **http://127.0.0.1:8000**

### 3. Dual-Mode GenAI Execution
- **Zero-Setup Offline Mode**: Out-of-the-box, the application includes a rich domain-heuristic generative engine that generates complete, highly realistic plans instantly without needing any API key.
- **Live Google Gemini Mode**: Click the ⚙️ Settings icon in the top navigation and input your Google Gemini API key to unlock unbounded, live LLM reasoning and custom generation!

---

## 📂 Architecture

```
event-planner-ai/
├── app/
│   ├── main.py              # FastAPI application, REST endpoints, static mounting
│   ├── models.py            # Pydantic schemas for EventPlan, Budget, Timeline, Vendor, Ideas
│   ├── planner_engine.py    # GenAI Gemini API integration & domain-heuristic synthesis
│   ├── event_templates.py   # Specialized domain heuristics for Weddings, Birthdays, Community
│   └── storage.py           # Persistent JSON event store with pre-seeded demo showcases
├── static/
│   ├── index.html           # Modern responsive single-page web app with Tailwind CSS
│   ├── app.js               # Reactive state management, client-side math, interactive tabs
│   └── styles.css           # Custom styles, transitions, and printable dossier stylesheet
├── data/
│   └── events.json          # Persistent event store (auto-created on first run)
├── run.py                   # Convenience runner
└── requirements.txt         # Project dependencies
```
