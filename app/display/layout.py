# app/display/layout.py

# ── screen ────────────────────────────────────────
SCREEN_W = 600
SCREEN_H = 800

# ── home screen zones ─────────────────────────────
DATE_BAR_Y      = 0
DATE_BAR_H      = 60

WIDGET_ROW_Y    = DATE_BAR_H
WIDGET_ROW_H    = 180
WIDGET_W        = SCREEN_W // 3
WIDGET_PADDING = 8   # inner padding for all widgets

STOCK_BAR_Y        = WIDGET_ROW_Y + WIDGET_ROW_H
STOCK_BAR_H     = 95
STOCK_PADDING      = 8
STOCK_TICKER_Y     = 10   # relative to STOCK_BAR_Y
STOCK_PRICE_Y      = 30   # relative to STOCK_BAR_Y
STOCK_CHANGE_Y     = 54   # relative to STOCK_BAR_Y — more space after price


HEADLINES_Y        = STOCK_BAR_Y + STOCK_BAR_H
HEADLINES_H        = SCREEN_H - HEADLINES_Y
HEADLINE_ITEM_H    = HEADLINES_H // 4

# ── widget columns ────────────────────────────────
COL_WEATHER  = 0
COL_F1       = 200
COL_SAILGP   = 400

# ── ui typography ─────────────────────────────────
UI_FONT_REG  = "/usr/java/lib/fonts/Helvetica_LT_65_Medium.ttf"
UI_FONT_BOLD = "/usr/java/lib/fonts/Helvetica_LT_75_Bold.ttf"

# ── symbol font (Font Awesome 7 Free Solid) ────────
SYMBOL_FONT     = "/mnt/us/dashboard/fonts/fa-solid.ttf"
ICON_LOCK       = ""  # fa-lock
ICON_WIFI       = ""  # fa-wifi
ICON_SYNC       = ""  # fa-arrows-rotate U+F021
ICON_WIFI_SLASH = ""  # fa-ban           U+F05E
ICON_PLANE      = ""  # fa-plane          U+F072
ICON_STOCK_UP   = ""  # fa-caret-up   U+F0D8
ICON_STOCK_DOWN = ""  # fa-caret-down U+F0D7
ICON_BATT_FULL  = ""  # fa-battery-full
ICON_BATT_3Q    = ""  # fa-battery-three-quarters
ICON_BATT_HALF  = ""  # fa-battery-half
ICON_BATT_1Q    = ""  # fa-battery-quarter
ICON_BATT_EMPTY = ""  # fa-battery-empty

# ── source view ───────────────────────────────────
SOURCE_BAR_Y    = 0
SOURCE_BAR_H    = 50
SOURCE_ITEMS_Y  = 50
SOURCE_ITEM_H   = 125   # 6 items × 125 = 750px
SOURCE_UNDERLINE_OFFSET = 28  # px below title_top, tune if needed

# ── article typography ────────────────────────────
ARTICLE_BODY_SIZE      = 11
ARTICLE_TITLE_SIZE     = 16
ARTICLE_FONT_BODY_REG  = "/usr/java/lib/fonts/Caecilia_LT_65_Medium.ttf"
ARTICLE_FONT_BODY_BOLD = "/usr/java/lib/fonts/Caecilia_LT_75_Bold.ttf"
ARTICLE_FONT_UI_REG    = "/usr/java/lib/fonts/Helvetica_LT_65_Medium.ttf"
ARTICLE_FONT_UI_BOLD   = "/usr/java/lib/fonts/Helvetica_LT_75_Bold.ttf"

# ── article screen ────────────────────────────────
ARTICLE_HEADER_H       = 60
ARTICLE_MARGIN_LEFT    = 15
ARTICLE_MARGIN_RIGHT   = 10
ARTICLE_MARGIN_TOP     = ARTICLE_HEADER_H + 15    # header height + breathing room
ARTICLE_LINE_HEIGHT    = 27
ARTICLE_CHARS_PER_LINE = 56
ARTICLE_LINES_PAGE_1   = 18
ARTICLE_LINES_OTHER    = (SCREEN_H - ARTICLE_MARGIN_TOP) // ARTICLE_LINE_HEIGHT
ARTICLE_TITLE_GAP      = 14   # gap between title block and body
ARTICLE_PARAGRAPH_GAP  = 13   # blank line height between paragraphs (~half a body line)
ARTICLE_TITLE_CHARS    = 35
ARTICLE_TITLE_LINE_H   = 37

# ── typography (fbink sizes) ──────────────────────
SIZE_SMALL  = "1"
SIZE_MEDIUM = "2"
SIZE_LARGE  = "3"
CHARS_SIZE_11 = 58   # small UI text
CHARS_SIZE_13 = 48   # headline text
CHARS_SIZE_14 = 44   # medium UI text

# ── divider ───────────────────────────────────────
DIVIDER_CHAR = "─"
