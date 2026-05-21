# app/display/fbink_wrapper.py

import subprocess
import os

FBINK_BIN = "/mnt/us/fbink/bin/fbink"
FBINK_LIB = "/mnt/us/fbink/lib"

env = os.environ.copy()
env["LD_LIBRARY_PATH"] = FBINK_LIB

def _run(args):
    cmd = [FBINK_BIN] + args
    subprocess.run(cmd, env=env, stdout=subprocess.DEVNULL, 
                   stderr=subprocess.DEVNULL)

def clear():
    """Clear the screen to white"""
    _run(["-c", "-f"])

def text(string, x=0, y=0, size=1, inverted=False, centered=False):
    """
    Draw text at pixel position (x, y)
    size: 1=small 2=medium 3=large
    inverted: white text on black background
    centered: ignore x, centre horizontally
    """
    args = ["-S", str(size)]
    if inverted:
        args += ["-h"]
    if centered:
        args += ["-m"]
    else:
        # use pixel offsets, not character grid
        args += ["-x", "0", "-y", "0",
                 "-X", str(x), "-Y", str(y)]
    args += ["--", string]
    _run(args)

def hline(y, x_start=0, x_end=600):
    """Draw a horizontal rule"""
    # fbink can draw rectangles - a 1px tall rectangle is a line
    args = [
        "-x", str(x_start),
        "-y", str(y),
        "--size-w", str(x_end - x_start),
        "--size-h", "1",
        "-B", "BLACK"
    ]
    _run(args)

def vline(x, y_start=0, y_end=800):
    """Draw a vertical rule"""
    args = [
        "-x", str(x),
        "-y", str(y_start),
        "--size-w", "1",
        "--size-h", str(y_end - y_start),
        "-B", "BLACK"
    ]
    _run(args)

def refresh():
    """Force a full screen refresh to clear ghosting"""
    _run(["-f", "-m", "--", " "])