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
        # vertically centre in DATE_BAR_H=60 at size 2
        fb.text(date_str, y=DATE_BAR_Y + 18, size=2, centered=True)

    def _draw_widgets(self):
        # vertical dividers between widgets
        fb.vline(WIDGET_W,     WIDGET_ROW_Y, WIDGET_ROW_Y + WIDGET_ROW_H)
        fb.vline(WIDGET_W * 2, WIDGET_ROW_Y, WIDGET_ROW_Y + WIDGET_ROW_H)

        self._draw_weather()
        self._draw_f1()
        self._draw_sailgp()

    def _draw_weather(self):
        d = self.state.data.get("weather", {})
        x = COL_WEATHER + WIDGET_PADDING
        y = WIDGET_ROW_Y + WIDGET_PADDING

        fb.text("London",              x=x, y=y,      size=1)
        fb.text(d.get("temp", "--°"), x=x, y=y + 40,  size=3)
        fb.text(d.get("desc", "---"), x=x, y=y + 100, size=1)
        fb.text(d.get("rain", ""),    x=x, y=y + 125, size=1)

    def _draw_f1(self):
        d = self.state.data.get("f1", {})
        x = COL_F1 + WIDGET_PADDING
        y = WIDGET_ROW_Y + WIDGET_PADDING

        fb.text("Next Race",            x=x, y=y,       size=1)
        fb.text(d.get("name",  "---"), x=x, y=y + 35,  size=1)
        fb.text(d.get("date",  "---"), x=x, y=y + 70,  size=1)
        fb.text(d.get("time",  "---"), x=x, y=y + 100, size=2)

    def _draw_sailgp(self):
        d = self.state.data.get("sailgp", {})
        x = COL_SAILGP + WIDGET_PADDING
        y = WIDGET_ROW_Y + WIDGET_PADDING

        fb.text("SailGP",               x=x, y=y,       size=1)
        fb.text(d.get("event", "---"), x=x, y=y + 35,  size=1)
        fb.text(d.get("dates", "---"), x=x, y=y + 70,  size=1)
        fb.text(d.get("round", "---"), x=x, y=y + 105, size=1)

    def _draw_stocks(self):
        stocks = self.state.data.get("stocks", [])
        if not stocks:
            fb.text("---", x=WIDGET_PADDING, 
                    y=STOCK_BAR_Y + 25, size=1)
            return

        # spread tickers evenly across 600px
        slot_w = SCREEN_W // len(stocks)
        for i, s in enumerate(stocks):
            arrow = "▲" if s.get("change", 0) >= 0 else "▼"
            label = f"{s['ticker']}  {s['price']}  {arrow}{s['pct']}%"
            fb.text(label,
                    x=i * slot_w + WIDGET_PADDING,
                    y=STOCK_BAR_Y + 25,
                    size=1)

    def _draw_headlines(self):
        headlines = self.state.data.get("headlines", [])
        selected  = self.state.selected_index

        for i in range(min(4, len(headlines))):
            h   = headlines[i]
            y   = HEADLINES_Y + (i * HEADLINE_ITEM_H)
            is_selected = (i == selected)

            # source label
            fb.text(h.get("source", ""),
                    x=WIDGET_PADDING, y=y + 8, size=1)

            # headline text — inverted if selected
            fb.text(h.get("title", ""),
                    x=WIDGET_PADDING, y=y + 30,
                    size=2, inverted=is_selected)

            # divider between items (not after last)
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
            # flip to source view
            self.state.source_index   = 0
            self.state.selected_index = 0
            self.state.prev_screen    = SCREEN_HOME
            self.state.screen         = SCREEN_SOURCE