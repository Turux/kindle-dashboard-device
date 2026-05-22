# app/display/fbink_wrapper.py

import subprocess
import os

FBINK_BIN = "/mnt/us/fbink/bin/fbink"
FBINK_LIB = "/mnt/us/fbink/lib"

# fonts
FONT_UI_REGULAR = "/usr/java/lib/fonts/Helvetica_LT_65_Medium.ttf"
FONT_UI_BOLD    = "/usr/java/lib/fonts/Helvetica_LT_75_Bold.ttf"
FONT_READ_REG   = "/usr/java/lib/fonts/Caecilia_LT_65_Medium.ttf"
FONT_READ_BOLD  = "/usr/java/lib/fonts/Caecilia_LT_75_Bold.ttf"

env = os.environ.copy()
env["LD_LIBRARY_PATH"] = FBINK_LIB

def _run(args):
    cmd = [FBINK_BIN] + args
    subprocess.run(cmd, env=env,
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)

def clear():
    _run(["-k"])

def cls_region(top, left, width, height, flash=False):
    """Clear a region to white"""
    args = ["-k",
            f"top={top},left={left},width={width},height={height}",
            "-B", "WHITE"]
    if flash:
        args += ["-f"]
    _run(args)

def flash():
    """Full screen flash to clear e-ink ghosting"""
    _run(["-f", "-k"])

def ui_text(string, top, left=10, right=10, size=12,
            bold=False, inverted=False, centered=False):
    """Helvetica — for all dashboard UI elements"""
    regular = FONT_UI_REGULAR
    bold_f  = FONT_UI_BOLD
    font_str = (f"regular={regular},bold={bold_f},"
                f"size={size},top={top},left={left},right={right}","padding=HORIZONTAL")
    args = ["-t", font_str]
    if inverted:
        args += ["-h"]
    if centered:
        args += ["-m"]
    if bold:
        args += []   # use **text** markdown, or pass style=BOLD
        font_str = (f"regular={regular},bold={bold_f},"
                    f"size={size},top={top},left={left},"
                    f"right={right},style=BOLD")
        args = ["-t", font_str]
        if inverted:
            args += ["-h"]
        if centered:
            args += ["-m"]
    args += ["--", string]
    _run(args)

def truncate(text, max_chars, ellipsis="..."):
    """Truncate string to max_chars, adding ellipsis if needed"""
    if len(text) <= max_chars:
        return text
    return text[:max_chars - len(ellipsis)] + ellipsis

def read_text(string, top, left=10, right=10, size=16,
              bold=False, inverted=False):
    """Caecilia — for article reading"""
    regular = FONT_READ_REG
    bold_f  = FONT_READ_BOLD
    style   = "BOLD" if bold else "REGULAR"
    font_str = (f"regular={regular},bold={bold_f},"
                f"size={size},top={top},left={left},"
                f"right={right},style={style}",
                f"padding=HORIZONTAL")
    args = ["-t", font_str, "--", string]
    if inverted:
        args = ["-h"] + args
    _run(args)

def hline(y, x_start=0, x_end=600, thickness=1):
    _run([
        "-k",
        f"top={y},left={x_start},"
        f"width={x_end - x_start},height={thickness}",
        "-B", "BLACK"
    ])

def vline(x, y_start=0, y_end=800):
    """1px vertical rule"""
    _run(["-k",
          f"top={y_start},left={x},"
          f"width=1,height={y_end - y_start}"])
    _run(["-s",
          f"top={y_start},left={x},"
          f"width=1,height={y_end - y_start}"])

def filled_rect(top, left, width, height, color="BLACK"):
    """Filled rectangle — useful for inverted headers"""
    _run(["-k",
          f"top={top},left={left},"
          f"width={width},height={height}",
          "-B", color])