# app/config.py

# ── sources ───────────────────────────────────────
SOURCES = [
    "guardian",
    "the_nerve",
    "ft",
    "semafor",
    "the_dial",
    "bellingcat",
]

# ── display names ─────────────────────────────────
SOURCE_NAMES = {
    "guardian":   "The Guardian",
    "the_nerve":  "The Nerve",
    "ft":         "Financial Times",
    "semafor":    "Semafor",
    "the_dial":   "The Dial",
    "bellingcat": "Bellingcat",
}

# ── cache settings ────────────────────────────────
STALE_THRESHOLD_MINS = 30
MAX_HEADLINES_HOME   = 4
MAX_HEADLINES_SOURCE = 6

# ── location ──────────────────────────────────────
# Used for weather — update to your actual coordinates
WEATHER_LAT = 51.5074   # London default
WEATHER_LON = -0.1278

# ── VM endpoint ───────────────────────────────────
VM_ENDPOINT = "https://kindle.turux.co.uk/api/full-sync"