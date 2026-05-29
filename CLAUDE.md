# Kindle Dashboard — Device Repo Context

## What this is
A custom e-ink dashboard app for a jailbroken Kindle 4 Non-Touch (2011/2012), built as a replacement for the stock Amazon UI. Runs on the device's native Linux (ARMv7, Python 3.9) using direct framebuffer access via FBInk.

## Companion repo
The backend is at `https://github.com/Turux/kindle-dashboard-server` — a self-hosted Flask API + fetcher running on a Linux VPS via Docker Compose. The device syncs from it over HTTPS.
The server repo is cloned locally in the same parent folder as this repo.

## Hardware facts
- Screen: 600×800 e-ink, 167dpi, 16 grayscale levels
- Input: 5-way d-pad (event1), keyboard/buttons (event0)
- Fonts: Helvetica LT and Caecilia LT at `/usr/java/lib/fonts/`
- FBInk: installed at `/mnt/us/fbink/`, used for all drawing
- App lives at `/mnt/us/dashboard/`
- Cache at `/mnt/us/dashboard/cache/`
- Python 3.9.8

## Architecture
Three screens in a state machine:
- `home.py` — widgets (weather, F1, SailGP, stocks) + 4 headlines
- `source.py` — per-source headline list (6 sources, side buttons flip between them)
- `article.py` — article reader with pagination

Main loop in `main.py` — calls `render()` or `partial_render()` then `handle_input()` on the current screen. A background thread watches for lipc sleep/wake events.

## Key design decisions
- All drawing via FBInk subprocess calls (no Python bindings)
- Pixel coordinates throughout — all constants in `layout.py`
- UI font: Helvetica, body/reading font: Caecilia
- `-b` norefresh flag on all text draws, single `refresh_screen()` at end of page
- Partial render on navigation (erase/redraw underline only, not full screen)
- Cache is JSON files — never fetches data directly, only reads from cache
- SSL verification disabled (Kindle lacks modern CA certs)

## Input map (measured keycodes)
```
KEY_UP=103, KEY_DOWN=108, KEY_LEFT=105, KEY_RIGHT=106, KEY_SELECT=194
KEY_BACK=158, KEY_HOME=102, KEY_MENU=139, KEY_KEYBOARD=29
KEY_RIGHT_PREV=109, KEY_RIGHT_NEXT=191, KEY_LEFT_PREV=193, KEY_LEFT_NEXT=104
KEY_SLEEP=999 (synthetic), KEY_WAKE=998 (synthetic)
```

Page turn buttons (both sides): `PAGE_FORWARD = {191, 104}`, `PAGE_BACKWARD = {109, 193}`

## Typography (measured on device)
```
Caecilia size 11: 27px per line, 56 chars per line
Caecilia size 12: 29px per line, 47 chars per line  
Helvetica bold size 16: 37px per line, 35 chars per line
```

## Layout constants (layout.py)
Key zones:
- Date bar: y=0, h=60
- Widget row: y=60, h=180 (3 columns × 200px)
- Stock bar: y=240, h=95
- Headlines: y=335, h=465 (4 items)
- Source bar: h=50, items below at 125px each

## Sleep/wake
- Device uses lipc: `goingToScreenSaver` / `outOfScreenSaver`
- Background thread injects synthetic KEY_SLEEP/KEY_WAKE into input queue
- On sleep: navigate to home, show [lock] indicator, auto-sync if WiFi on
- Battery: `lipc-get-prop com.lab126.powerd battLevel`
- WiFi state: `lipc-get-prop com.lab126.wifid cmState`

## Deployment
No git on device yet — files deployed via scp:
```bash
scp -r app/ root@192.168.15.244:/mnt/us/dashboard/
```
SSH via USBNetworking (enable via KUAL first).
Device IP: 192.168.15.244, Mac IP: 192.168.15.201

## Launching
Via KUAL → Dashboard → Start Dashboard
This kills the framework and launches `python3 app/main.py`
Emergency exit: keyboard button → reboots device

## Open issues
Tracked on GitHub: https://github.com/Turux/kindle-dashboard-device/issues

Current open issues (as of May 2026):
- **#1 Ghost underline** — 1px underline persists on first headline. E-ink refresh timing. Low priority.
- **#4 WiFi toggle** — add on/off toggle via app using `lipc-set-prop com.lab126.wifid enable 0/1`
- **#5 Git on Kindle** — pre-compiled ARMv7 static binary for easier deployment

Not yet filed:
- **Paragraph spacing** — articles lack breathing room between paragraphs (single \n not treated as break)
- **Boot automation** — auto-launch via KUAL autostart
- **Symbol font** — no good symbol font available; [lock], stock arrows etc use ASCII fallbacks
- **America's Cup / Ocean Race widgets** — future addition, needs layout redesign for extra columns

## Recently fixed
- Sports widget event name wrapping — switched to size 12 bold, prevents overflow in 180px column
- KUAL launcher extension added to repo under `kual/` (config.xml, menu.json, start.sh, stop.sh, restart.sh)
- Article pagination now correct (measured actual line heights)
- Batch rendering — all text drawn with -b flag, single refresh at end
- Article cache stability — server keeps 150 articles, Kindle keeps 100 for 7 days
- Sleep detection and home-on-sleep navigation
- F1 live session fallback (shows last known session when API returns 401)
- SailGP Race Day 1/2 logic from ICS calendar
- Weather location configurable from device config.py
- City name configurable via WEATHER_CITY in config.py