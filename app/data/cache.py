# app/data/cache.py

import json, os, time, hashlib, ssl, urllib.request
from app.config import VM_ENDPOINT
import subprocess

def get_battery():
    try:
        result = subprocess.run(
            ["lipc-get-prop", "com.lab126.powerd", "battLevel"],
            capture_output=True, text=True, timeout=3
        )
        val = result.stdout.strip()
        return int(val) if val.isdigit() else None
    except:
        return None

def get_wifi_state():
    try:
        result = subprocess.run(
            ["lipc-get-prop", "com.lab126.wifid", "cmState"],
            capture_output=True, text=True, timeout=3
        )
        return result.stdout.strip() == "CONNECTED"
    except:
        return is_wifi_on()   # fallback to sysfs check

def is_sleeping():
    """Listen for sleep event non-blocking — returns True if going to sleep"""
    try:
        result = subprocess.run(
            ["lipc-wait-event", "-s", "1",
             "com.lab126.powerd", "goingToScreenSaver"],
            capture_output=True, text=True, timeout=2
        )
        return "goingToScreenSaver" in result.stdout
    except:
        return False

CACHE_DIR   = "/mnt/us/dashboard/cache"
HOME_CACHE  = f"{CACHE_DIR}/home.json"
META_FILE   = f"{CACHE_DIR}/meta.json"


def sync_if_online():
    if not is_wifi_on():
        return False
    try:
        # create unverified context — Kindle lacks modern CA certs
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        with urllib.request.urlopen(VM_ENDPOINT, timeout=15, 
                                    context=ctx) as r:
            payload = json.loads(r.read())
        _write_cache(payload)
        return True
    except Exception as e:
        print(f"sync failed: {e}")
        return False

def _write_cache(payload):
    os.makedirs(CACHE_DIR, exist_ok=True)
    os.makedirs(f"{CACHE_DIR}/articles", exist_ok=True)
    os.makedirs(f"{CACHE_DIR}/sources", exist_ok=True)

    # home data
    with open(HOME_CACHE, "w") as f:
        json.dump(payload["home"], f)

    # per-source headlines
    for source, items in payload.get("sources", {}).items():
        path = f"{CACHE_DIR}/sources/{source}.json"
        with open(path, "w") as f:
            json.dump(items, f)

    # pre-cached articles — only add, never delete
    for url_hash, text in payload.get("articles", {}).items():
        path = f"{CACHE_DIR}/articles/{url_hash}.txt"
        if not os.path.exists(path):   # don't overwrite existing
            with open(path, "w") as f:
                f.write(text)

    # metadata — when we last synced
    with open(META_FILE, "w") as f:
        json.dump({"synced_at": time.time()}, f)

    # clean after yourself
    cleanup_cache()

def load_home():
    if not os.path.exists(HOME_CACHE):
        return load_cache()   # fall back to dummy data during development
    with open(HOME_CACHE) as f:
        data = json.load(f)
    if os.path.exists(META_FILE):
        with open(META_FILE) as f:
            meta = json.load(f)
        data["synced_at"] = meta.get("synced_at", 0)
    return data

def load_source(source_id):
    path = f"{CACHE_DIR}/sources/{source_id}.json"
    if not os.path.exists(path):
        # dummy data for development
        return [
            {"title": "Test headline one", "date": "22 May", "summary": "Brief summary of the article goes here."},
            {"title": "Test headline two", "date": "21 May", "summary": "Another brief summary here."},
            {"title": "Test headline three", "date": "21 May", "summary": ""},
        ]
    with open(path) as f:
        return json.load(f)

def load_article(url_hash):
    path = f"{CACHE_DIR}/articles/{url_hash}.txt"
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return f.read()

def is_wifi_on():
    try:
        with open("/sys/class/net/wlan0/operstate") as f:
            return f.read().strip() == "up"
    except:
        return False

def cache_age_mins():
    if not os.path.exists(META_FILE):
        return 9999
    with open(META_FILE) as f:
        meta = json.load(f)
    return (time.time() - meta.get("synced_at", 0)) / 60

def cleanup_cache():
    if not os.path.exists(f"{CACHE_DIR}/articles"):
        return
    files = [
        (f, os.path.getmtime(f"{CACHE_DIR}/articles/{f}"))
        for f in os.listdir(f"{CACHE_DIR}/articles")
        if f.endswith(".txt")
    ]
    files.sort(key=lambda x: x[1], reverse=True)
    now = time.time()
    for i, (fname, mtime) in enumerate(files):
        path = f"{CACHE_DIR}/articles/{fname}"
        age_days = (now - mtime) / 86400
        if i >= 100 or age_days > 7:   # keep 100, max 7 days
            os.remove(path)

def load_cache():
    return {
        "weather": {
            "temp": "13°",
            "desc": "Cloudy",
            "rain": "Rain 70%"
        },
        "f1": {
            "label":   "Next Session",
            "name":    "Canada FP1",
            "date":    "22 May 17:30",
        },
        "sailgp": {
            "label":   "Next Event",
            "name":    "New York Race 1",
            "date":    "30 May 15:30",
        },
        "stocks": [
            {"ticker": "AAPL", "price": "213.4", 
             "change": 1.2,    "pct": "1.2"},
            {"ticker": "TSLA", "price": "190.1", 
             "change": -0.8,   "pct": "0.8"},
            {"ticker": "VOD",  "price": "1.24",  
             "change": 0.3,    "pct": "0.3"},
        ],
        "headlines": [
            {"source": "BBC",      
             "title": "Scientists discover new approach to solar energy storage",
             "url_hash": "test001"},
            {"source": "Guardian", 
             "title": "UK inflation falls to lowest level in three years"},
            {"source": "Reuters",  
             "title": "F1: Verstappen takes pole in Monaco qualifying"},
            {"source": "Semafor",  
             "title": "AI regulation talks stall ahead of Geneva summit"},
        ]
    }