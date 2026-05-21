# app/input/dpad.py

KEY_UP     = 103
KEY_DOWN   = 108
KEY_LEFT   = 105
KEY_RIGHT  = 106
KEY_SELECT = 194

KEY_PRESS   = 1
KEY_RELEASE = 0

import struct

DEVICE    = "/dev/input/event1"
FMT       = "llHHi"
EVT_SIZE  = struct.calcsize(FMT)

def read_event():
    """blocking read, returns (code, value) or None"""
    with open(DEVICE, "rb") as f:
        while True:
            data = f.read(EVT_SIZE)
            if len(data) == EVT_SIZE:
                _, _, etype, code, value = struct.unpack(FMT, data)
                if etype == 1 and value == KEY_PRESS:
                    return code

def wait_for_key():
    """returns the next key code pressed"""
    return read_event()