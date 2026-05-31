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
- Symbol font: Font Awesome 7 Free Solid at `/mnt/us/dashboard/fonts/fa-solid.ttf`
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
- UI font: Helvetica, body/reading font: Caecilia, symbol font: Font Awesome 7 Solid
- **Batch rendering**: every draw uses `-b` (norefresh), single `refresh_screen()` at end of render. `flash()` at start of full render to clear e-ink ghosting.
- Partial render on navigation (erase/redraw underline only, not full screen). Underline always drawn last in `render()` to prevent e-ink washout.
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

## Symbol icons (Font Awesome 7 Free Solid)
Font file lives at `/mnt/us/dashboard/fonts/fa-solid.ttf` on device, and in `fonts/fa-solid.ttf` in this repo (gitignored — SIL OFL licence, not redistributed).
Constants defined in `layout.py`, rendered via `fb.symbol_norefresh()` in `fbink_wrapper.py`.

| Constant | Icon | Codepoint |
|----------|------|-----------|
| ICON_LOCK | lock | U+F023 |
| ICON_WIFI | wifi | U+F1EB |
| ICON_WIFI_SLASH | ban (no-wifi indicator) | U+F05E |
| ICON_SYNC | arrows-rotate (syncing indicator) | U+F021 |
| ICON_STOCK_UP | arrow-up | U+F062 |
| ICON_STOCK_DOWN | arrow-down | U+F063 |
| ICON_BATT_FULL | battery-full | U+F240 |
| ICON_BATT_3Q | battery-three-quarters | U+F241 |
| ICON_BATT_HALF | battery-half | U+F242 |
| ICON_BATT_1Q | battery-quarter | U+F243 |
| ICON_BATT_EMPTY | battery-empty | U+F244 |

## Sleep/wake
- Device uses lipc: `goingToScreenSaver` / `outOfScreenSaver`
- Background thread injects synthetic KEY_SLEEP/KEY_WAKE into input queue
- On sleep: navigate to home, show lock icon, auto-sync if WiFi on, save resume_screen
- On wake: restore resume_screen (returns to article/source if that's where user was)
- Battery: `lipc-get-prop com.lab126.powerd battLevel`
- WiFi state: `lipc-get-prop com.lab126.wifid cmState`

## Deployment
No git on device yet — files deployed via scp:
```bash
scp -r app/ root@192.168.15.244:/mnt/us/dashboard/
```
Font (first time only):
```bash
ssh root@192.168.15.244 "mkdir -p /mnt/us/dashboard/fonts"
scp fonts/fa-solid.ttf root@192.168.15.244:/mnt/us/dashboard/fonts/
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
- **#1 Ghost underline** — ghost line appears on the Rebooting screen when pressing keyboard button. flash() in reboot handler helps but doesn't fully clear on Kindle 4 NT hardware. Low priority.
- **#4 WiFi toggle** — add on/off toggle via app. Use ownership state machine (save state before enabling, only disable if app enabled it). See issue comment for full design.
- **#5 Git on Kindle** — pre-compiled ARMv7 static binary for easier deployment
- **#18 Squircle widget borders** — rounded rectangle borders via PNG overlay + FBInk `-i` flag. Back burner.
- **#19 Sync message overwrites status bar** — sync notification clobbers status bar display.
- **#20 Pull quotes render as plain text** — publishers style pull quotes visually on web; trafilatura flattens them to plain paragraphs, indistinguishable from body text. Fix likely requires per-source HTML preprocessing or trafilatura XML output mode. Low priority.

Not yet filed:
- **Boot automation** — auto-launch via KUAL autostart
- **America's Cup / Ocean Race widgets** — future addition, needs layout redesign for extra columns

## Recently fixed
- **Symbol icons** — Font Awesome 7 Free Solid for lock, WiFi, 5-level battery, stock up/down arrows
- **Batch rendering on all screens** — all draw calls use norefresh variants; single refresh_screen() at end. Eliminates intermediate flashes on every screen transition.
- **Page rendering transition** — article page turns now smooth (was 5 intermediate refreshes, now 1)
- **Separator line between stocks and headlines** — missing hline added at HEADLINES_Y
- **Ghost underline root cause fixed** — underline drawn last in render() to prevent e-ink washout from subsequent draws
- **Resume after sleep** — app returns to article/source screen after wake if that's where the user was
- **Article summary display** — shown in Helvetica (vs Caecilia for body) on page 1 of article
- **Paragraph spacing** — blank line inserted after each paragraph in article paginator
- **Article pagination** — pixel-budget tracking replaces fractional line counting
- **Reboot handler** — uses flash() instead of clear() to reduce ghost line on Rebooting screen
- **Paragraph spacing in article reader** — each paragraph now gets breathing room via blank line insertion in paginator
- **Sports widget event name wrapping** — switched to size 12 bold, prevents overflow in 180px column
- **KUAL launcher extension** — added to repo under `kual/` (config.xml, menu.json, start.sh, stop.sh, restart.sh)
- **Article cache stability** — server keeps 150 articles, Kindle keeps 100 for 7 days
- **Sleep detection** — home-on-sleep navigation
- **F1 live session fallback** — shows last known session when API returns 401
- **SailGP Race Day 1/2 logic** — from ICS calendar
- **Weather location** — configurable via WEATHER_CITY in config.py
