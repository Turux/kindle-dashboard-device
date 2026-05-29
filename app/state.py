# app/state.py

SCREEN_HOME    = "home"
SCREEN_SOURCE  = "source"
SCREEN_ARTICLE = "article"

class AppState:
    def __init__(self):
        self.screen         = SCREEN_HOME
        self.selected_index = 0
        self.source_index   = 0
        self.article_page   = 0
        self.article        = None
        self.prev_screen    = None
        self.data           = {}
        self.sleeping       = False
        self.needs_refresh  = False