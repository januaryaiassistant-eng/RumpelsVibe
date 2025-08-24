from flask import Flask, render_template, request, jsonify, abort
from datetime import datetime, date
from pathlib import Path
import json
import threading
import re

app = Flask(__name__)

# ---------- Storage setup ----------
DATA_DIR = Path(app.instance_path)
DATA_DIR.mkdir(parents=True, exist_ok=True)
BOOKINGS_FILE = DATA_DIR / "bookings.json"
_lock = threading.Lock()

TIME_SLOTS = [
    "09:00", "10:00", "11:00",
    "13:00", "14:00", "15:00", "16:00"
]

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def _load_bookings():
    if not BOOKINGS_FILE.exists():
        return []
    with BOOKINGS_FILE.open("r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []
    return data

def _save_bookings(bookings):
    tmp = BOOKINGS_FILE.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(bookings, f, ensure_ascii=False, indent=2)
    tmp.replace(BOOKINGS_FILE)

# ---------- Pages ----------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/promposal")
def promposal():
    return render_template("promposal.html")

@app.route("/dateinvite")
def dateinvite():
    return render_template("dateinvite.html")

@app.route("/fake1")
def fake1():
    return render_template("fake1.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# Booking page
@app.route("/booking")
def booking():
    return render_template("booking.html")

# ---------- Booking API ----------
@app.route("/api/availability")
def api_availability():
    """
    Returns JSON:
    {
      "booked": [{"date":"YYYY-MM-DD","time":"HH:MM"}, ...],
      "timeSlots": ["HH:MM", ...],
      "today": "YYYY-MM-DD"
    }
    """
    with _lock:
        bookings = _load_bookings()
    out = {
        "booked": bookings,
        "timeSlots": TIME_SLOTS,
        "today": date.today().isoformat()
    }
    return jsonify(out)

@app.route("/api/book", methods=["POST"])
def api_book():
    """
    Accepts JSON: {"date":"YYYY-MM-DD","time":"HH:MM","email":"...","message":"...","agree":true}
    Validates and saves if slot is free.
    """
    data = request.get_json(silent=True) or {}
    d = data.get("date", "").strip()
    t = data.get("time", "").strip()
    email = (data.get("email") or "").strip()
    message = (data.get("message") or "").strip()
    agree = bool(data.get("agree"))

    # Basic validation
    if not d or not t or not email:
        return abort(400, description="Missing required fields.")
    if not EMAIL_RE.match(email):
        return abort(400, description="Invalid email format.")
    if t not in TIME_SLOTS:
        return abort(400, description="Invalid time slot.")
    try:
        chosen = datetime.strptime(d, "%Y-%m-%d").date()
    except ValueError:
        return abort(400, description="Invalid date.")

    if chosen < date.today():
        return abort(400, description="Cannot book a past date.")
    if not agree:
        return abort(400, description="You must agree to the meeting rules.")

    with _lock:
        bookings = _load_bookings()
        # conflict check
        for b in bookings:
            if b.get("date") == d and b.get("time") == t:
                return abort(409, description="That slot is already booked. Please choose another.")
        # save
        bookings.append({
            "date": d,
            "time": t,
            "email": email,
            "message": message[:1000],
            "created_at": datetime.utcnow().isoformat() + "Z"
        })
        _save_bookings(bookings)

    return jsonify({"ok": True, "message": "Booked successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
