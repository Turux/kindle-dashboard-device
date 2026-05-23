# app/display/fbink_wrapper.py

import subprocess
import os

FBINK_BIN = "/mnt/us/fbink/bin/fbink"
FBINK_LIB = "/mnt/us/fbink/lib"

from app.display.layout import (UI_FONT_REG, UI_FONT_BOLD,
                                 ARTICLE_FONT_BODY_REG, ARTICLE_FONT_BODY_BOLD,
                                 ARTICLE_BODY_SIZE, ARTICLE_TITLE_SIZE)

# replace hardcoded paths
FONT_UI_REGULAR = UI_FONT_REG
FONT_UI_BOLD    = UI_FONT_BOLD
FONT_READ_REG   = ARTICLE_FONT_BODY_REG
FONT_READ_BOLD  = ARTICLE_FONT_BODY_BOLD


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

def refresh_region(top, left, width, height):
    """Force e-ink display refresh of a specific region"""
    _run(["-s", f"top={top},left={left},width={width},height={height}"])

def flash():
    """Full screen flash to clear e-ink ghosting"""
    _run(["-f", "-k"])

def ui_text(string, top, left=10, right=10, size=12,
            bold=False, inverted=False, centered=False):
    """Helvetica — for all dashboard UI elements"""
    regular  = FONT_UI_REGULAR
    bold_f   = FONT_UI_BOLD
    style    = "BOLD" if bold else "REGULAR"
    font_str = (f"regular={regular},bold={bold_f},"
                f"size={size},top={top},left={left},"
                f"right={right},style={style}")
    args = ["-t", font_str]
    if inverted:
        args += ["-h"]
    if centered:
        args += ["-m"]
    args += ["--", string]
    _run(args)

def read_text(string, top, left=10, right=10, size=16,
              bold=False, inverted=False):
    """Caecilia — for article reading"""
    regular  = FONT_READ_REG
    bold_f   = FONT_READ_BOLD
    style    = "BOLD" if bold else "REGULAR"
    font_str = (f"regular={regular},bold={bold_f},"
                f"size={size},top={top},left={left},"
                f"right={right},style={style}")
    args = ["-t", font_str, "--", string]
    if inverted:
        args = ["-h"] + args
    _run(args)

def ui_text_norefresh(string, top, left=10, right=10, size=12,
                      bold=False):
    """Helvetica — draw without triggering e-ink refresh"""
    style    = "BOLD" if bold else "REGULAR"
    font_str = (f"regular={FONT_UI_REGULAR},bold={FONT_UI_BOLD},"
                f"size={size},top={top},left={left},"
                f"right={right},style={style}")
    args = ["-b", "-t", font_str, "--", string]
    _run(args)

def read_text_norefresh(string, top, left=10, right=10, size=12):
    """Caecilia — draw without triggering e-ink refresh"""
    font_str = (f"regular={FONT_READ_REG},bold={FONT_READ_BOLD},"
                f"size={size},top={top},left={left},"
                f"right={right},style=REGULAR")
    args = ["-b", "-t", font_str, "--", string]
    _run(args)

def refresh_screen():
    """Single full screen refresh after batch drawing"""
    _run(["-s", "top=0,left=0,width=600,height=800"])

def truncate(text, max_chars, ellipsis="..."):
    """Truncate string to max_chars, adding ellipsis if needed"""
    if len(text) <= max_chars:
        return text
    return text[:max_chars - len(ellipsis)] + ellipsis

def hline(y, x_start=0, x_end=600, thickness=1):
    """Draw a horizontal line in black"""
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
          f"width=1,height={y_end - y_start}",
          "-B", "BLACK"])

def filled_rect(top, left, width, height, color="BLACK"):
    """Filled rectangle"""
    _run(["-k",
          f"top={top},left={left},"
          f"width={width},height={height}",
          "-B", color])