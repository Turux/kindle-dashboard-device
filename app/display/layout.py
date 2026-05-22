# app/display/layout.py

# ── screen ────────────────────────────────────────
SCREEN_W = 600
SCREEN_H = 800

# ── home screen zones ─────────────────────────────
DATE_BAR_Y      = 0
DATE_BAR_H      = 60

WIDGET_ROW_Y    = 60
WIDGET_ROW_H    = 180
WIDGET_W        = 200   # 600 / 3
WIDGET_PADDING = 8   # inner padding for all widgets

STOCK_BAR_Y     = 240
STOCK_BAR_H     = 80

HEADLINES_Y     = 320
HEADLINES_H     = 480   # to bottom of screen
HEADLINE_ITEM_H = 120   # 4 items × 120 = 480

# ── widget columns ────────────────────────────────
COL_WEATHER  = 0
COL_F1       = 200
COL_SAILGP   = 400

# ── source view ───────────────────────────────────
SOURCE_BAR_Y    = 0
SOURCE_BAR_H    = 50
SOURCE_ITEMS_Y  = 50
SOURCE_ITEM_H   = 125   # 6 items × 125 = 750px
SOURCE_UNDERLINE_OFFSET = 28  # px below title_top, tune if needed

# ── article screen ────────────────────────────────
ARTICLE_HEADER_H       = 60
ARTICLE_MARGIN_LEFT    = 15
ARTICLE_MARGIN_RIGHT   = 10
ARTICLE_MARGIN_TOP     = 75    # header height + breathing room
ARTICLE_LINE_HEIGHT    = 28
ARTICLE_CHARS_PER_LINE = 50
ARTICLE_LINES_PAGE_1   = 24
ARTICLE_LINES_OTHER    = 30
ARTICLE_TITLE_GAP      = 14   # gap between title block and body
ARTICLE_TITLE_CHARS    = 42 

# ── typography (fbink sizes) ──────────────────────
SIZE_SMALL  = "1"
SIZE_MEDIUM = "2"
SIZE_LARGE  = "3"
CHARS_SIZE_11 = 58   # small UI text
CHARS_SIZE_13 = 48   # headline text  
CHARS_SIZE_14 = 44   # medium UI text

# ── divider ───────────────────────────────────────
DIVIDER_CHAR = "─"