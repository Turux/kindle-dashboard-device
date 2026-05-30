# app/screens/source.py

from app.display import fbink_wrapper as fb
from app.display.layout import *
from app.input.dpad import (wait_for_key,
                             KEY_UP, KEY_DOWN, KEY_SELECT,
                             KEY_BACK, KEY_HOME,
                             KEY_SLEEP, KEY_WAKE,
                             is_page_forward, is_page_backward)
from app.state import SCREEN_HOME, SCREEN_ARTICLE
from app.data.cache import load_source
from app.config import SOURCES, SOURCE_NAMES, MAX_HEADLINES_SOURCE


class SourceScreen:

    def __init__(self, state):
        self.state = state
        self.full_render_needed = True
        self._headlines = []
        self._prev_selected = None

    # ── main render ───────────────────────────────

    def render(self):
        self._headlines = load_source(SOURCES[self.state.source_index])
        fb.clear()
        fb.flash()
        self._draw_header()
        fb.hline(SOURCE_BAR_H)
        self._draw_headlines()
        if self._headlines:
            fb.hline(self._item_title_top(self.state.selected_index) + SOURCE_UNDERLINE_OFFSET,
                    x_start=10, x_end=150, thickness=3)
        self._prev_selected = self.state.selected_index

    def partial_render(self):
        prev = self._prev_selected
        cur  = self.state.selected_index

        if prev is not None and prev != cur:
            # erase old underline — 3px tall to be safe
            title_top = self._item_title_top(prev)
            fb.cls_region(
                top=title_top + SOURCE_UNDERLINE_OFFSET,
                left=10, width=140, height=3)

        # draw new underline
        title_top = self._item_title_top(cur)
        fb.hline(title_top + SOURCE_UNDERLINE_OFFSET,
                x_start=10, x_end=150, thickness=3)

        self._prev_selected = cur

    # ── sections ──────────────────────────────────

    def _item_title_top(self, i):
        """Calculate title_top for item i — single source of truth"""
        h   = self._headlines[i] if i < len(self._headlines) else {}
        y   = SOURCE_ITEMS_Y + (i * SOURCE_ITEM_H)
        return y + 30 if h.get("date") else y + 10

    def _draw_header(self):
        source_id   = SOURCES[self.state.source_index]
        name        = SOURCE_NAMES.get(source_id, source_id.title())
        total       = len(SOURCES)
        position    = self.state.source_index + 1

        # source name on the left
        fb.ui_text(name,
                   top=SOURCE_BAR_H // 2 - 8,
                   left=10, right=120,
                   size=13, bold=True)

        # position indicator on the right  e.g. "2 of 6"
        fb.ui_text(f"{position} of {total}",
                   top=SOURCE_BAR_H // 2 - 8,
                   left=460, right=10,
                   size=11)

    def _draw_headlines(self):
        headlines = self._headlines
        count     = min(MAX_HEADLINES_SOURCE, len(headlines))

        if not headlines:
            fb.ui_text("No articles cached.",
                    top=SOURCE_BAR_H + 40,
                    left=10, right=10, size=12)
            fb.ui_text("Press Menu to sync.",
                    top=SOURCE_BAR_H + 70,
                    left=10, right=10, size=12)
            return

        for i in range(count):
            h         = headlines[i]
            y         = SOURCE_ITEMS_Y + (i * SOURCE_ITEM_H)
            title_top = self._item_title_top(i)

            # date
            date_str = h.get("date", "")
            if date_str:
                fb.ui_text(date_str,
                        top=y + 6,
                        left=10, right=10, size=10)

            # title
            title = fb.truncate(h.get("title", ""), 52)
            fb.ui_text(title,
                    top=title_top,
                    left=10, right=10, size=13)

            # summary
            summary = h.get("summary", "")
            if summary:
                fb.ui_text(fb.truncate(summary, 80),
                        top=y + 62,
                        left=10, right=10, size=10)

    # ── input ─────────────────────────────────────

    def handle_input(self):
        count   = min(MAX_HEADLINES_SOURCE, len(self._headlines))
        max_idx = max(0, count - 1)

        key = wait_for_key()

        if key == KEY_UP:
            self.state.selected_index = max(0,
                self.state.selected_index - 1)
            self.full_render_needed = False

        elif key == KEY_DOWN:
            self.state.selected_index = min(max_idx,
                self.state.selected_index + 1)
            self.full_render_needed = False

        elif key == KEY_SELECT:
            if self._headlines:
                h = self._headlines[self.state.selected_index]
                self.state.article      = h
                self.state.article_page = 0
                self.state.prev_screen  = self.state.screen
                self.state.screen       = SCREEN_ARTICLE
                self.full_render_needed = True

        elif is_page_forward(key):
            # next source
            self.state.source_index = (
                (self.state.source_index + 1) % len(SOURCES)
            )
            self.state.selected_index = 0
            self.full_render_needed   = True

        elif is_page_backward(key):
            # previous source
            self.state.source_index = (
                (self.state.source_index - 1) % len(SOURCES)
            )
            self.state.selected_index = 0
            self.full_render_needed   = True

        elif key in (KEY_BACK, KEY_HOME):
            self.state.selected_index = 0
            self.state.screen         = SCREEN_HOME
            self.full_render_needed   = True
        
        elif key in (KEY_SLEEP, KEY_WAKE):
            self.full_render_needed = True