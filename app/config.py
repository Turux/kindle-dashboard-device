# app/config.py

# ── sources ───────────────────────────────────────
SOURCES = [
    "guardian",
    "the_nerve",
    "semafor",
    "the_dial",
    "bellingcat",
    "the_conversation"
]

# ── display names ─────────────────────────────────
SOURCE_NAMES = {
    "guardian":   "The Guardian",
    "the_nerve":  "The Nerve",
    "ft":         "Financial Times",
    "semafor":    "Semafor",
    "the_dial":   "The Dial",
    "bellingcat": "Bellingcat",
    "the_conversation": "The Conversation",
}

# ── cache settings ────────────────────────────────
STALE_THRESHOLD_MINS = 30
MAX_HEADLINES_HOME   = 4
MAX_HEADLINES_SOURCE = 6

# ── location ──────────────────────────────────────
# Used for weather — update to your actual coordinates
WEATHER_CITY = "Leicester"
WEATHER_LAT = 52.61457
WEATHER_LON = -1.12390

# ── VM endpoint ───────────────────────────────────
VM_ENDPOINT = "https://kindle.turux.co.uk/api/full-sync"