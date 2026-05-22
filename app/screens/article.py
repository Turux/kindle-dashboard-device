# app/screens/article.py

from app.display import fbink_wrapper as fb
from app.display.layout import *
from app.input.dpad import (wait_for_key,
                             KEY_BACK, KEY_HOME,
                             is_page_forward, is_page_backward)
from app.state import SCREEN_HOME
from app.data.cache import load_article
import textwrap

# ── reading typography constants ─────────────────
ARTICLE_MARGIN_LEFT  = 15
ARTICLE_MARGIN_RIGHT = 15
ARTICLE_MARGIN_TOP   = 60   # below header
ARTICLE_LINE_HEIGHT  = 24   # px between lines at size 15
ARTICLE_CHARS_PER_LINE = 48 # approx at size 15, tune after seeing on screen
ARTICLE_LINES_PAGE_1 = 22   # less on page 1 — title takes space
ARTICLE_LINES_OTHER  = 30   # more on subsequent pages
ARTICLE_TITLE_GAP    = 16


class ArticleScreen:

    def __init__(self, state):
        self.state = state
        self.full_render_needed = True
        self._pages  = []
        self._source = ""
        self._title  = ""

    # ── main render ───────────────────────────────

    def render(self):
        self._prepare()
        fb.clear()
        fb.flash()
        self._draw_header()
        fb.hline(ARTICLE_HEADER_H)
        self._draw_page()

    def partial_render(self):
        # page turns always do a full render — content changes completely
        self.render()

    # ── preparation ───────────────────────────────

    def _prepare(self):
        """Load article text and paginate it"""
        h = self.state.article or {}
        self._title  = h.get("title", "")
        self._source = h.get("source", "")

        # try cache first, fall back to summary, then placeholder
        url_hash = h.get("url_hash", "")
        text     = load_article(url_hash) if url_hash else None

        if not text:
            text = h.get("summary", "")
        if not text:
            text = "Article not available offline.\n\nPress Menu on the home screen to sync."

        self._pages = self._paginate(text)

        # clamp page index in case article changed
        max_page = max(0, len(self._pages) - 1)
        self.state.article_page = min(self.state.article_page, max_page)

    def _paginate(self, text):
        """Split text into pages that fit the screen"""
        # wrap all text to our line width first
        paragraphs = text.split("\n")
        lines = []
        for para in paragraphs:
            if para.strip() == "":
                lines.append("")   # blank line between paragraphs
            else:
                wrapped = textwrap.wrap(para, width=ARTICLE_CHARS_PER_LINE)
                lines.extend(wrapped)

        pages  = []
        i      = 0
        page_n = 0

        while i < len(lines):
            capacity = ARTICLE_LINES_PAGE_1 if page_n == 0 else ARTICLE_LINES_OTHER
            page     = lines[i:i + capacity]
            pages.append(page)
            i      += capacity
            page_n += 1

        return pages if pages else [[]]

    # ── sections ──────────────────────────────────

    def _draw_header(self):
        page     = self.state.article_page
        total    = len(self._pages)
        source   = self._source

        fb.ui_text(source,
                   top=ARTICLE_HEADER_H // 2 - 8,
                   left=10, right=120,
                   size=12, bold=True)

        fb.ui_text(f"{page + 1} of {total}",
                   top=ARTICLE_HEADER_H // 2 - 8,
                   left=460, right=10, size=11)

    def _draw_page(self):
        page_idx = self.state.article_page
        if not self._pages:
            return

        lines = self._pages[page_idx]
        y     = ARTICLE_MARGIN_TOP

        # page 1 — draw title first in bold
        if page_idx == 0:
            title_lines = textwrap.wrap(self._title,
                                        width=ARTICLE_CHARS_PER_LINE)
            for line in title_lines:
                fb.ui_text(line,
                           top=y,
                           left=ARTICLE_MARGIN_LEFT,
                           right=ARTICLE_MARGIN_RIGHT,
                           size=16, bold=True)
                y += 28   # title line height — slightly more than body

            y += ARTICLE_TITLE_GAP   # gap between title and body

        # body text
        for line in lines:
            if line == "":
                y += ARTICLE_LINE_HEIGHT // 2   # paragraph gap
                continue
            fb.ui_text(line,
                top=y,
                left=ARTICLE_MARGIN_LEFT,
                right=ARTICLE_MARGIN_RIGHT,
                size=12)
            y += ARTICLE_LINE_HEIGHT

    # ── input ─────────────────────────────────────

    def handle_input(self):
        key      = wait_for_key()
        max_page = max(0, len(self._pages) - 1)

        if is_page_forward(key):
            if self.state.article_page < max_page:
                self.state.article_page += 1
                self.full_render_needed  = True

        elif is_page_backward(key):
            if self.state.article_page > 0:
                self.state.article_page -= 1
                self.full_render_needed  = True

        elif key in (KEY_BACK, KEY_HOME):
            self.state.article_page = 0
            self.state.screen       = self.state.prev_screen or SCREEN_HOME
            self.full_render_needed = True