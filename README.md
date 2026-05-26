# kindle-dashboard-device

A custom e-ink dashboard application for the jailbroken Kindle 4 Non-Touch (2011/2012), built as a replacement for the stock Amazon UI. Displays real-time weather, motorsport and sailing schedules, stock prices and news headlines from curated RSS sources — all fetched from a self-hosted backend and cached for offline reading.

## Background

Amazon end-of-lifed the Kindle 4 in May 2026. Rather than retire the device, this project repurposes it as a personal e-ink news and information dashboard, running entirely on the device's native Linux environment via a jailbreak.

## Hardware

- **Device:** Kindle 4 Non-Touch (Tequila/Yoshi, ARMv7)
- **Screen:** 600×800 e-ink, 167dpi, 16 grayscale levels
- **Input:** 5-way d-pad, page turn buttons (×4), back, home, menu, keyboard buttons
- **OS:** Linux 2.6.31

## Prerequisites

### Jailbreak
The device must be jailbroken. Follow the guide at:
`https://longplaytech.com/posts/jailbreak-kindle-4th-gen/`

After jailbreak, install:
- **MKK** — allows community packages
- **KUAL** — custom launcher (required to launch the dashboard)
- **USBNetworking** — SSH access over USB

### Python 3
Install the ARMv7 Python 3.9 package from NiLuJe's MobileRead thread (Kindle Developer's Corner).

### FBInk
Install the FBInk package (K3 build) from NiLuJe's MobileRead thread via the standard side-load process.

## Installation

> ⚠️ Installation is currently a work in progress. A future release will include a KUAL extension installer and may require Git on the device. For now, SSH access is required — either via diagnostic mode or USBNetworking.

```bash
# SSH into the Kindle (requires USBNetworking enabled via KUAL)
ssh root@192.168.15.244

# Create the app directory
mkdir -p /mnt/us/dashboard

# Copy the app from your computer
scp -r app/ root@192.168.15.244:/mnt/us/dashboard/
```

### KUAL Extension

The KUAL launcher extension (start/stop dashboard) is installed on the device but not yet tracked in this repository. This is a known gap — see open issues.

## Configuration

Edit `app/config.py` to set your backend endpoint and news sources:

```python
VM_ENDPOINT = "https://your-backend-domain/api/full-sync"

SOURCES = [
    "source_one",
    "source_two",
    # add your sources here — must match backend config
]
```

Source display names and home screen headline counts are also configured here.

## File Structure

```
app/
├── main.py              # entry point, main loop, sleep watcher thread
├── state.py             # AppState — shared state between screens
├── config.py            # sources list, VM endpoint
├── screens/
│   ├── home.py          # home screen — widgets + headlines
│   ├── source.py        # per-source headline list
│   └── article.py       # article reader with pagination
├── display/
│   ├── fbink_wrapper.py # FBInk drawing primitives
│   └── layout.py        # all pixel constants and typography settings
├── input/
│   └── dpad.py          # d-pad + button input, threading, event injection
└── data/
    └── cache.py         # sync, read/write cache, battery/WiFi helpers
cache/
└── articles/
    └── test001.txt      # sample article for development/testing
```

## Screen Flow

```
HOME ──select──► ARTICLE
  │                 │
  ├──page fwd/back──► SOURCE VIEW ──select──► ARTICLE
  │                                               │
  └──────────────────back/home────────────────────┘
```

## Input Map

| Button | Action |
|--------|--------|
| D-pad up/down | Navigate headlines |
| D-pad select | Open article |
| Side buttons | Flip sources / page turn in article |
| Back | Return to previous screen |
| Home | Return to home screen |
| Menu | Sync with backend (if WiFi on) |
| Keyboard | Reboot device |
| Power | Lock screen (screensaver) |

## Cache

Data is cached at `/mnt/us/dashboard/cache/`:

```
cache/
├── home.json          # home screen data
├── meta.json          # last sync timestamp
├── sources/           # per-source headline JSON files
└── articles/          # pre-fetched article text files
```

Cache survives power cycles. The app works fully offline when WiFi is unavailable.

## Display

- **UI font:** Helvetica LT (from the Kindle's own font library at `/usr/java/lib/fonts/`)
- **Reading font:** Caecilia LT (Kindle's native book font)
- **Rendering:** FBInk, direct framebuffer access
- **Coordinates:** pixel-based, origin top-left

All pixel positions, font sizes and line heights are measured constants in `layout.py`.

## SSH Access

SSH access is needed for installation and troubleshooting. Two methods:

- **USBNetworking** — install via KUAL, enable before connecting USB
- **Diagnostic mode** — available on some firmware versions without USBNetworking

## Known Issues

- **Ghost underline** — a 1px underline can persist on the first headline after navigation. E-ink refresh timing issue. Low priority.
- **Paragraph spacing** — articles lack visual separation between paragraphs when the source uses single `\n` line breaks.
- **Sleep handling** — sleep detection works but auto-sync on wake and navigate-home-on-sleep are not yet fully implemented.
- **Boot automation** — app must be launched manually via KUAL after each boot.
- **KUAL extension not in repo** — the launcher extension files are on the device but not tracked in version control. See open issues.