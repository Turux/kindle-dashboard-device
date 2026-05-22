# app/config.py
# ── sources ───────────────────────────────────────
# Edit this list to add, remove, or reorder sources.
# IDs must match the RSS feed keys in the backend config.
# Order determines the side-button navigation sequence.

SOURCES = [
    "guardian",
    "the_nerve",
    "ft",
    "semafor",
    "the_dial",
    "bellingcat",
]

# ── display names ─────────────────────────────────
# Human-readable names for the source header bar.
SOURCE_NAMES = {
    "guardian":  "The Guardian",
    "the_nerve": "The Nerve",
    "ft":        "Financial Times",
    "semafor":   "Semafor",
    "the_dial":  "The Dial",
    "bellingcat": "Bellingcat",
}

# ── cache settings ────────────────────────────────
STALE_THRESHOLD_MINS = 30   # show stale indicator after this
MAX_HEADLINES_HOME   = 4    # headlines shown on home screen
MAX_HEADLINES_SOURCE = 6    # headlines shown in source view

# ── VM endpoint ───────────────────────────────────
VM_ENDPOINT = "http://your-oracle-vm/api/full-sync"