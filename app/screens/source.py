# app/screens/source.py

from app.display import fbink_wrapper as fb
from app.display.layout import *
from app.input.dpad import (wait_for_key,
                             KEY_UP, KEY_DOWN, KEY_SELECT,
                             KEY_BACK, KEY_HOME,
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
        self._headlines   = load_source(SOURCES[self.state.source_index])
        self._prev_selected = None    # reset on full render
        fb.clear()
        self._draw_header()
        fb.hline(SOURCE_BAR_H)
        self._draw_headlines()

    def partial_render(self):
        """Erase old underline, draw new one — no region clear needed"""
        # erase previous underline
        prev = self._prev_selected
        if prev is not None:
            y_prev       = SOURCE_ITEMS_Y + (prev * SOURCE_ITEM_H)
            h_prev       = self._headlines[prev] if prev < len(self._headlines) else {}
            title_top    = y_prev + 30 if h_prev.get("date") else y_prev + 10
            underline_y  = title_top + 20
            # paint it white to erase
            fb.cls_region(top=underline_y, left=10,
                        width=580, height=2)

        # draw new underline
        cur        = self.state.selected_index
        y_cur      = SOURCE_ITEMS_Y + (cur * SOURCE_ITEM_H)
        h_cur      = self._headlines[cur] if cur < len(self._headlines) else {}
        title_top  = y_cur + 30 if h_cur.get("date") else y_cur + 10
        fb.hline(title_top + 20, x_start=10, x_end=590)

        self._prev_selected = cur

    # ── sections ──────────────────────────────────

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
        selected  = self.state.selected_index
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
            h    = headlines[i]
            y    = SOURCE_ITEMS_Y + (i * SOURCE_ITEM_H)

            # date
            date_str = h.get("date", "")
            if date_str:
                fb.ui_text(date_str,
                        top=y + 6,
                        left=10, right=10, size=10)

            # title — no inversion, always plain
            title     = fb.truncate(h.get("title", ""), 52)
            title_top = y + 30 if date_str else y + 10
            fb.ui_text(title,
                    top=title_top,
                    left=10, right=10, size=13)

            # selection indicator — underline only
            if i == selected:
                fb.hline(title_top + 20, x_start=10, x_end=590)

            # summary
            summary = h.get("summary", "")
            if summary:
                fb.ui_text(fb.truncate(summary, 80),
                        top=y + 62,
                        left=10, right=10, size=10)

            # item divider
            if i < count - 1:
                fb.hline(y + SOURCE_ITEM_H)
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