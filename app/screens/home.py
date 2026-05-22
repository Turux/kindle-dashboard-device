# app/screens/home.py

from app.display import fbink_wrapper as fb
from app.display.layout import *
from app.input.dpad import (wait_for_key,
                             KEY_UP, KEY_DOWN, KEY_SELECT,
                             KEY_BACK, KEY_HOME, KEY_MENU, KEY_KEYBOARD,
                             is_page_forward, is_page_backward)
from app.state import SCREEN_SOURCE, SCREEN_ARTICLE, SCREEN_HOME
from app.data.cache import sync_if_online, load_home, is_wifi_on
from datetime import datetime


class HomeScreen:

    def __init__(self, state):
        self.state = state
        self.full_render_needed = True
        self._prev_selected = 0

    # ── main render ───────────────────────────────

    def render(self):
        fb.clear()
        fb.flash()
        self._draw_date_bar()
        fb.hline(DATE_BAR_H)
        self._draw_widgets()
        fb.hline(WIDGET_ROW_Y + WIDGET_ROW_H)
        self._draw_stocks()
        self._draw_headlines()
        self._prev_selected = self.state.selected_index

    def _item_title_top(self, i):
        """Single source of truth for title Y position of headline i"""
        y = HEADLINES_Y + (i * HEADLINE_ITEM_H)
        return y + 30

    def partial_render(self):
        prev = self._prev_selected
        cur  = self.state.selected_index

        if prev == cur:
            return

        # redraw both affected items cleanly
        for i in [prev, cur]:
            if i is None:
                continue
            headlines = self.state.data.get("headlines", [])
            if i >= len(headlines):
                continue
            h = headlines[i]
            y = HEADLINES_Y + (i * HEADLINE_ITEM_H)

            # clear the item's underline area only
            fb.cls_region(top=y + 28, left=0,
                        width=SCREEN_W, height=60)

            # redraw title
            title = fb.truncate(h.get("title", ""), CHARS_SIZE_13)
            fb.ui_text(title, top=y + 28, left=WIDGET_PADDING,
                    right=10, size=13)

            # redraw underline only if selected
            if i == cur:
                fb.hline(y + 28 + SOURCE_UNDERLINE_OFFSET,
                        x_start=10, x_end=150, thickness=3)

        self._prev_selected = cur

    # ── sections ──────────────────────────────────

    def _draw_date_bar(self):
        now = datetime.now()
        date_str = now.strftime("%A  %d %B %Y")
        fb.ui_text(date_str, top=15, left=10, right=10,
                   size=16, bold=True, centered=True)

    def _draw_widgets(self):
        fb.vline(WIDGET_W,     WIDGET_ROW_Y, WIDGET_ROW_Y + WIDGET_ROW_H)
        fb.vline(WIDGET_W * 2, WIDGET_ROW_Y, WIDGET_ROW_Y + WIDGET_ROW_H)
        self._draw_weather()
        self._draw_f1()
        self._draw_sailgp()

    def _draw_weather(self):
        d     = self.state.data.get("weather", {})
        left  = COL_WEATHER + 10
        right = SCREEN_W - WIDGET_W + 10   # clamp text to weather column

        fb.ui_text("London",
                   top=WIDGET_ROW_Y + 10, left=left, right=right, size=11)
        fb.ui_text(d.get("temp", "--°"),
                   top=WIDGET_ROW_Y + 35, left=left, right=right, size=28)
        fb.ui_text(d.get("desc", "---"),
                   top=WIDGET_ROW_Y + 110, left=left, right=right, size=11)
        fb.ui_text(d.get("rain", ""),
                   top=WIDGET_ROW_Y + 135, left=left, right=right, size=11)

    def _draw_f1(self):
        d    = self.state.data.get("f1", {})
        left = COL_F1 + 10
        right = SCREEN_W - COL_F1 - WIDGET_W + 10

        fb.ui_text("F1",
                top=WIDGET_ROW_Y + 10, left=left, right=right, size=11)
        fb.ui_text(d.get("label", "---"),
                top=WIDGET_ROW_Y + 35, left=left, right=right, size=11)
        fb.ui_text(fb.truncate(d.get("name", "---"), 16),
                top=WIDGET_ROW_Y + 60, left=left, right=right, size=14)
        fb.ui_text(d.get("date", "---"),
                top=WIDGET_ROW_Y + 100, left=left, right=right, size=11)

    def _draw_sailgp(self):
        d    = self.state.data.get("sailgp", {})
        left = COL_SAILGP + 10
        right = 10

        fb.ui_text("SailGP",
                top=WIDGET_ROW_Y + 10, left=left, right=right, size=11)
        fb.ui_text(d.get("label", "---"),
                top=WIDGET_ROW_Y + 35, left=left, right=right, size=11)
        fb.ui_text(fb.truncate(d.get("name", "---"), 16),
                top=WIDGET_ROW_Y + 60, left=left, right=right, size=14)
        fb.ui_text(d.get("date", "---"),
                top=WIDGET_ROW_Y + 100, left=left, right=right, size=11)

    def _draw_stocks(self):
        stocks = self.state.data.get("stocks", [])
        if not stocks:
            return

        slot_w = SCREEN_W // len(stocks)

        for i, s in enumerate(stocks):
            arrow      = "+" if s.get("change", 0) >= 0 else "-"
            slot_left  = i * slot_w
            slot_right = SCREEN_W - (i + 1) * slot_w

            fb.ui_text(s['ticker'],
                    top=STOCK_BAR_Y + STOCK_TICKER_Y,
                    left=slot_left + STOCK_PADDING,
                    right=slot_right + STOCK_PADDING,
                    size=10)

            fb.ui_text(s['price'],
                    top=STOCK_BAR_Y + STOCK_PRICE_Y,
                    left=slot_left + STOCK_PADDING,
                    right=slot_right + STOCK_PADDING,
                    size=11, bold=True)

            fb.ui_text(f"{arrow}{s['pct']}%",
                    top=STOCK_BAR_Y + STOCK_CHANGE_Y,
                    left=slot_left + STOCK_PADDING,
                    right=slot_right + STOCK_PADDING,
                    size=10)

    def _draw_headlines(self):
        headlines = self.state.data.get("headlines", [])
        selected  = self.state.selected_index

        for i in range(min(4, len(headlines))):
            h           = headlines[i]
            y           = HEADLINES_Y + (i * HEADLINE_ITEM_H)

            # source label
            fb.ui_text(h.get("source", ""),
                    top=y + 8, left=WIDGET_PADDING,
                    right=10, size=10)

            # title
            title = fb.truncate(h.get("title", ""), CHARS_SIZE_13)
            fb.ui_text(title,
                    top=y + 28, left=WIDGET_PADDING,
                    right=10, size=13)

            # selection underline
            if i == selected:
                fb.hline(y + 28 + SOURCE_UNDERLINE_OFFSET,
                        x_start=10, x_end=150, thickness=3)

            # summary — only if there's room
            summary = h.get("summary", "")
            if summary:
                fb.ui_text(fb.truncate(summary, 72),
                        top=y + 58, left=WIDGET_PADDING,
                        right=10, size=10)

    # ── input ─────────────────────────────────────

    def handle_input(self):
        headlines = self.state.data.get("headlines", [])
        max_idx   = min(4, len(headlines)) - 1

        key = wait_for_key()

        if key == KEY_UP:
            self.state.selected_index = max(0,
                self.state.selected_index - 1)
            self.full_render_needed = False   # partial only

        elif key == KEY_DOWN:
            self.state.selected_index = min(max_idx,
                self.state.selected_index + 1)
            self.full_render_needed = False   # partial only

        elif key == KEY_SELECT:
            h = headlines[self.state.selected_index]
            self.state.article      = h
            self.state.article_page = 0
            self.state.prev_screen  = SCREEN_HOME
            self.state.screen       = SCREEN_ARTICLE
            self.full_render_needed = True    # new screen, full render

        elif key == KEY_MENU:
            if is_wifi_on():
                # show syncing message in top right
                fb.cls_region(top=0, left=480, width=120, height=60)
                fb.ui_text("Syncing...", top=18, left=480, right=10, size=10)
                synced = sync_if_online()
                if synced:
                    self.state.data = load_home()
                self.full_render_needed = True
            else:
                # flash a "No WiFi" message briefly then restore
                fb.cls_region(top=0, left=460, width=140, height=60)
                fb.ui_text("No WiFi", top=18, left=460, right=10, size=10)
                import time
                time.sleep(2)
                self.full_render_needed = True

        elif key == KEY_KEYBOARD:
            import subprocess
            import time
            fb.clear()
            fb.ui_text("Rebooting...", top=380, size=14, centered=True)
            time.sleep(1)
            subprocess.run(["reboot"])

        elif is_page_forward(key) or is_page_backward(key):
            self.state.source_index   = 0
            self.state.selected_index = 0
            self.state.prev_screen    = SCREEN_HOME
            self.state.screen         = SCREEN_SOURCE
            self.full_render_needed = True    # new screen, full render