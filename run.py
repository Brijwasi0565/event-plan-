"""
Convenience launcher for CelebrateAI planning assistant server.
"""
import sys
import uvicorn

# Ensure UTF-8 output on Windows consoles
try:
    if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

if __name__ == "__main__":
    print("=" * 65)
    print("CelebrateAI - GenAI Event Planning Assistant")
    print("Weddings, Birthdays, Community Events with Budgets & Timelines")
    print("Opening server at http://127.0.0.1:8000")
    print("=" * 65)
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
