# app/data/cache.py

import json, os, time, hashlib

CACHE_DIR   = "/mnt/us/dashboard/cache"
HOME_CACHE  = f"{CACHE_DIR}/home.json"
META_FILE   = f"{CACHE_DIR}/meta.json"

VM_ENDPOINT = "http://your-oracle-vm/api/full-sync"

def sync_if_online():
    """Call on wake — syncs everything if wifi is up"""
    if not is_wifi_on():
        return False
    try:
        import urllib.request
        with urllib.request.urlopen(VM_ENDPOINT, timeout=15) as r:
            payload = json.loads(r.read())
        _write_cache(payload)
        return True
    except Exception as e:
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

    # pre-cached articles
    for url_hash, text in payload.get("articles", {}).items():
        path = f"{CACHE_DIR}/articles/{url_hash}.txt"
        with open(path, "w") as f:
            f.write(text)

    # metadata — when we last synced
    with open(META_FILE, "w") as f:
        json.dump({"synced_at": time.time()}, f)

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
        return []
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

def load_cache():
    return {
        "weather": {
            "temp": "13°",
            "desc": "Cloudy",
            "rain": "Rain 70%"
        },
        "f1": {
            "name": "Monaco GP",
            "date": "Sun 25 May",
            "time": "14:00"
        },
        "sailgp": {
            "event": "Taranto, Italy",
            "dates": "12-13 June",
            "round": "Round 7"
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
             "title": "Scientists discover new approach to solar energy storage"},
            {"source": "Guardian", 
             "title": "UK inflation falls to lowest level in three years"},
            {"source": "Reuters",  
             "title": "F1: Verstappen takes pole in Monaco qualifying"},
            {"source": "Semafor",  
             "title": "AI regulation talks stall ahead of Geneva summit"},
        ]
    }