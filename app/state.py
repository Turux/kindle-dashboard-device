# app/state.py

SCREEN_HOME    = "home"
SCREEN_SOURCE  = "source"
SCREEN_ARTICLE = "article"

class AppState:
    def __init__(self):
        self.screen         = SCREEN_HOME
        self.selected_index = 0      # headline index on current screen
        self.source_index   = 0      # which source we're viewing
        self.article_page   = 0      # current page in article view
        self.article        = None   # full article text, paginated
        self.prev_screen    = None   # for back navigation
        self.data           = {}     # loaded from cache