# app/input/dpad.py

import struct
import threading
import queue

# ── fiveway (event1) ──────────────────────────────
KEY_UP     = 103
KEY_DOWN   = 108
KEY_LEFT   = 105
KEY_RIGHT  = 106
KEY_SELECT = 194

# ── keyboard row (event0) ─────────────────────────
KEY_BACK     = 158
KEY_HOME     = 102
KEY_MENU     = 139
KEY_KEYBOARD = 29

# ── page turn buttons (event0) ────────────────────
# both sides behave identically
KEY_RIGHT_PREV = 109
KEY_RIGHT_NEXT = 191
KEY_LEFT_PREV  = 193
KEY_LEFT_NEXT  = 104

# ── logical aliases (use these in app code) ───────
PAGE_FORWARD  = {KEY_RIGHT_NEXT, KEY_LEFT_NEXT}
PAGE_BACKWARD = {KEY_RIGHT_PREV, KEY_LEFT_PREV}

# ── input loop ────────────────────────────────────
FMT      = "llHHi"
EVT_SIZE = struct.calcsize(FMT)

DEVICES = [
    "/dev/input/event0",
    "/dev/input/event1",
]

_queue = queue.Queue()

def _reader(path):
    with open(path, "rb") as f:
        while True:
            data = f.read(EVT_SIZE)
            if len(data) == EVT_SIZE:
                _, _, etype, code, value = struct.unpack(FMT, data)
                if etype == 1 and value == 1:  # KEY_PRESS only
                    _queue.put(code)

def start():
    """Start background threads for all input devices"""
    for path in DEVICES:
        t = threading.Thread(target=_reader, args=(path,), daemon=True)
        t.start()

def wait_for_key():
    """Blocking — returns next key code from any device"""
    return _queue.get()

def is_page_forward(key):
    return key in PAGE_FORWARD

def is_page_backward(key):
    return key in PAGE_BACKWARD