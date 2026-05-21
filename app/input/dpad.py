# app/input/dpad.py - updated

import struct
import threading
import queue

# fiveway - event1
KEY_UP     = 103
KEY_DOWN   = 108
KEY_LEFT   = 105
KEY_RIGHT  = 106
KEY_SELECT = 194

# keyboard row - event0
KEY_BACK     = 158
KEY_HOME     = 102
KEY_MENU     = 139
KEY_KEYBOARD = 29

KEY_PRESS   = 1
KEY_RELEASE = 0

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
                if etype == 1 and value == KEY_PRESS:
                    _queue.put(code)

def start():
    """Start background threads for all input devices"""
    for path in DEVICES:
        t = threading.Thread(target=_reader, args=(path,), daemon=True)
        t.start()

def wait_for_key():
    """Blocking — returns next key code pressed from any device"""
    return _queue.get()