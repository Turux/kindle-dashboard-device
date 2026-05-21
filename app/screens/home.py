# app/screens/home.py

from app.display import fbink_wrapper as fb
from app.display.layout import *
from app.input.dpad import (wait_for_key,
                             KEY_UP, KEY_DOWN, KEY_SELECT,
                             KEY_BACK, KEY_HOME,
                             is_page_forward, is_page_backward)
from app.state import SCREEN_SOURCE, SCREEN_ARTICLE
from datetime import datetime


class HomeScreen:

    def __init__(self, state):
        self.state = state

    # ── main render ───────────────────────────────

    def render(self):
        fb.clear()
        self._draw_date_bar()
        fb.hline(DATE_BAR_H)
        self._draw_widgets()
        fb.hline(WIDGET_ROW_Y + WIDGET_ROW_H)
        self._draw_stocks()
        fb.hline(STOCK_BAR_Y + STOCK_BAR_H)
        self._draw_headlines()

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
        d     = self.state.data.get("f1", {})
        left  = COL_F1 + 10
        right = SCREEN_W - WIDGET_W - COL_F1 + 10

        fb.ui_text("Next Race",
                   top=WIDGET_ROW_Y + 10, left=left, right=right, size=11)
        fb.ui_text(fb.truncate(d.get("name", "---"), 16),
                   top=WIDGET_ROW_Y + 35, left=left, right=right, size=14)
        fb.ui_text(d.get("date", "---"),
                   top=WIDGET_ROW_Y + 75, left=left, right=right, size=11)
        fb.ui_text(d.get("time", "---"),
                   top=WIDGET_ROW_Y + 100, left=left, right=right, size=22)

    def _draw_sailgp(self):
        d     = self.state.data.get("sailgp", {})
        left  = COL_SAILGP + 10
        right = 10

        fb.ui_text("SailGP",
                   top=WIDGET_ROW_Y + 10, left=left, right=right, size=11)
        fb.ui_text(fb.truncate(d.get("event", "---"), 16),
                   top=WIDGET_ROW_Y + 35, left=left, right=right, size=13)
        fb.ui_text(d.get("dates", "---"),
                   top=WIDGET_ROW_Y + 75, left=left, right=right, size=11)
        fb.ui_text(d.get("round", "---"),
                   top=WIDGET_ROW_Y + 100, left=left, right=right, size=11)

    def _draw_stocks(self):
        stocks = self.state.data.get("stocks", [])
        if not stocks:
            return
        slot_w = SCREEN_W // len(stocks)
        for i, s in enumerate(stocks):
            arrow = "▲" if s.get("change", 0) >= 0 else "▼"
            label = f"{s['ticker']}  {s['price']}  {arrow}{s['pct']}%"
            left  = i * slot_w + 10
            right = SCREEN_W - (i + 1) * slot_w + 10
            fb.ui_text(label,
                       top=STOCK_BAR_Y + 22,
                       left=left, right=right, size=11)

    def _draw_headlines(self):
        headlines = self.state.data.get("headlines", [])
        selected  = self.state.selected_index

        for i in range(min(4, len(headlines))):
            h           = headlines[i]
            y           = HEADLINES_Y + (i * HEADLINE_ITEM_H)
            is_selected = (i == selected)

            # source label — small, grey feel via size 10
            fb.ui_text(h.get("source", ""),
                       top=y + 8, left=WIDGET_PADDING,
                       right=10, size=10)

            # headline text — inverted bar if selected
            title = fb.truncate(h.get("title", ""), CHARS_SIZE_13)
            if is_selected:
                fb.filled_rect(y + 28, 0, SCREEN_W, 48)
                fb.ui_text(title,
                           top=y + 30, left=WIDGET_PADDING,
                           right=10, size=13, inverted=True)
            else:
                fb.ui_text(title,
                           top=y + 30, left=WIDGET_PADDING,
                           right=10, size=13)

            # divider between items, not after last
            if i < 3:
                fb.hline(y + HEADLINE_ITEM_H)

    # ── input ─────────────────────────────────────

    def handle_input(self):
        headlines = self.state.data.get("headlines", [])
        max_idx   = min(4, len(headlines)) - 1

        key = wait_for_key()

        if key == KEY_UP:
            self.state.selected_index = max(0,
                self.state.selected_index - 1)

        elif key == KEY_DOWN:
            self.state.selected_index = min(max_idx,
                self.state.selected_index + 1)

        elif key == KEY_SELECT:
            h = headlines[self.state.selected_index]
            self.state.article      = h
            self.state.article_page = 0
            self.state.prev_screen  = SCREEN_HOME
            self.state.screen       = SCREEN_ARTICLE

        elif is_page_forward(key) or is_page_backward(key):
            self.state.source_index   = 0
            self.state.selected_index = 0
            self.state.prev_screen    = SCREEN_HOME
            self.state.screen         = SCREEN_SOURCE