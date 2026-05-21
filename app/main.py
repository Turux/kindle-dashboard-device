# app/main.py

import sys
import os
sys.path.insert(0, "/mnt/us/dashboard")

from app.input.dpad import start as start_input
from app.display.fbink_wrapper import clear
from app.state import AppState, SCREEN_HOME, SCREEN_SOURCE, SCREEN_ARTICLE
from app.screens.home import HomeScreen
from app.screens.source import SourceScreen
from app.screens.article import ArticleScreen
from app.data.cache import load_cache

def main():
    start_input()
    state = AppState()
    state.data = load_cache()

    screens = {
        SCREEN_HOME:    HomeScreen(state),
        SCREEN_SOURCE:  SourceScreen(state),
        SCREEN_ARTICLE: ArticleScreen(state),
    }

    clear()

    while True:
        current = screens[state.screen]
        current.render()
        current.handle_input()

if __name__ == "__main__":
    main()