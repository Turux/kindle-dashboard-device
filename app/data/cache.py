# app/data/cache.py

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