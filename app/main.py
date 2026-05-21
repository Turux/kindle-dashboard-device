# app/main.py

import sys
import os
sys.path.insert(0, "/mnt/us/dashboard")

from app.input.dpad import start as start_input
from app.display import fbink_wrapper as fb
from app.state import AppState, SCREEN_HOME, SCREEN_SOURCE, SCREEN_ARTICLE
from app.screens.home import HomeScreen
from app.screens.source import SourceScreen
from app.screens.article import ArticleScreen
from app.data.cache import sync_if_online, load_home

def main():
    start_input()
    state = AppState()

    fb.clear()
    fb.ui_text("Loading...", top=380, size=14, centered=True)
    sync_if_online()          # tries wifi, silently skips if offline
    state.data = load_home()  # falls back to dummy data if no cache yet

    screens = {
        SCREEN_HOME:    HomeScreen(state),
        SCREEN_SOURCE:  SourceScreen(state),
        SCREEN_ARTICLE: ArticleScreen(state),
    }

    while True:
        current = screens[state.screen]
        if current.full_render_needed:
            current.render()
            current.full_render_needed = False
        else: 
            current.partial_render()
        current.handle_input()

if __name__ == "__main__":
    main()