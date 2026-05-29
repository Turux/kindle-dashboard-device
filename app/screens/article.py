# app/screens/article.py

from app.display import fbink_wrapper as fb
from app.display.layout import *
from app.input.dpad import (wait_for_key,
                             KEY_BACK, KEY_HOME,
                             KEY_SLEEP, KEY_WAKE,
                             is_page_forward, is_page_backward)
from app.state import SCREEN_HOME
from app.data.cache import load_article
import textwrap

from app.display.layout import ARTICLE_BODY_SIZE, ARTICLE_TITLE_SIZE

class ArticleScreen:

    def __init__(self, state):
        self.state = state
        self.full_render_needed = True
        self._pages  = []
        self._source = ""
        self._title  = ""

    # ── main render ───────────────────────────────

    def render(self, flash=True):
        self._prepare()
        fb.clear()
        if flash:
            fb.flash()
        self._draw_header()
        fb.hline(ARTICLE_HEADER_H)
        self._draw_page()

    def partial_render(self):
        self.render(flash=False)

    # ── preparation ───────────────────────────────

    def _prepare(self):
        h            = self.state.article or {}
        self._title  = h.get("title", "")
        self._source = h.get("source", "")

        url_hash = h.get("url_hash", "")
        text     = load_article(url_hash) if url_hash else None

        if not text:
            text = h.get("summary", "")
        if not text:
            text = "Article not available offline.\n\nPress Menu on the home screen to sync."

        self._pages = self._paginate(text)

        max_page = max(0, len(self._pages) - 1)
        self.state.article_page = min(self.state.article_page, max_page)

    def _paginate(self, text):
        paragraphs = text.split("\n")
        lines = []
        for para in paragraphs:
            if para.strip() == "":
                lines.append("")
            else:
                wrapped = textwrap.wrap(para, width=ARTICLE_CHARS_PER_LINE)
                lines.extend(wrapped)

        title_lines  = len(textwrap.wrap(self._title, width=ARTICLE_TITLE_CHARS))
        title_px     = (title_lines * ARTICLE_TITLE_LINE_H) + ARTICLE_TITLE_GAP
        available_px = SCREEN_H - ARTICLE_MARGIN_TOP - title_px
        page_1_lines = available_px // ARTICLE_LINE_HEIGHT

        pages  = []
        i      = 0
        page_n = 0

        while i < len(lines):
            capacity   = page_1_lines if page_n == 0 else ARTICLE_LINES_OTHER
            page       = []
            body_count = 0   # only count non-blank lines

            while i < len(lines) and body_count < capacity:
                line = lines[i]
                page.append(line)
                if line.strip():
                    body_count += 1   # only increment for real content
                else:
                    # blank line costs half
                    body_count += 0.5
                i += 1

            pages.append(page)
            page_n += 1

        return pages if pages else [[]]

    # ── sections ──────────────────────────────────

    def _draw_header(self):
        page  = self.state.article_page
        total = len(self._pages)
        h     = self.state.article or {}
        date  = h.get("date", "")

        # source + date on the left
        source_str = self._source
        if date:
            source_str += f"  {date}"

        fb.ui_text(source_str,
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

        if page_idx == 0:
            y = ARTICLE_MARGIN_TOP
            title_lines = textwrap.wrap(self._title,
                                        width=ARTICLE_TITLE_CHARS)
            for line in title_lines:
                fb.ui_text_norefresh(line, top=y,
                     left=ARTICLE_MARGIN_LEFT,
                     right=ARTICLE_MARGIN_RIGHT,
                     size=ARTICLE_TITLE_SIZE, bold=True)
                y += ARTICLE_TITLE_LINE_H
            y += ARTICLE_TITLE_GAP
        else:
            y = ARTICLE_MARGIN_TOP

        for line in lines:
            if line == "":
                y += ARTICLE_LINE_HEIGHT
                continue
            fb.read_text_norefresh(line, top=y,
                       left=ARTICLE_MARGIN_LEFT,
                       right=ARTICLE_MARGIN_RIGHT,
                       size=ARTICLE_BODY_SIZE)
            y += ARTICLE_LINE_HEIGHT

        # single refresh after everything is drawn
        fb.refresh_screen()

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
        
        elif key in (KEY_SLEEP, KEY_WAKE):
            self.full_render_needed = True