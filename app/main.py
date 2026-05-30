# app/main.py

import sys
import os
import threading
sys.path.insert(0, "/mnt/us/dashboard")

from app.input.dpad import start as start_input
from app.display import fbink_wrapper as fb
from app.state import AppState, SCREEN_HOME, SCREEN_SOURCE, SCREEN_ARTICLE
from app.screens.home import HomeScreen
from app.screens.source import SourceScreen
from app.screens.article import ArticleScreen
from app.data.cache import sync_if_online, load_home, is_wifi_on

def _sleep_watcher(state):
    import subprocess
    from app.input.dpad import inject_event, KEY_SLEEP, KEY_WAKE

    while True:
        result = subprocess.run(
            ["lipc-wait-event", "-s", "60",
             "com.lab126.powerd",
             "goingToScreenSaver,outOfScreenSaver"],
            capture_output=True, text=True
        )

        if "goingToScreenSaver" in result.stdout:
            state.resume_screen  = state.screen   # save position before going home
            state.sleeping       = True
            state.screen         = SCREEN_HOME
            state.selected_index = 0
            inject_event(KEY_SLEEP)
            # auto-sync in background if WiFi available
            if is_wifi_on():
                def bg_sync():
                    if sync_if_online():
                        state.data         = load_home()
                        state.needs_refresh = True
                threading.Thread(target=bg_sync, daemon=True).start()

        elif "outOfScreenSaver" in result.stdout:
            state.sleeping = False
            if state.resume_screen:
                state.screen        = state.resume_screen
                state.resume_screen = None
            state.needs_refresh = True
            inject_event(KEY_WAKE)

def main():
    start_input()
    state = AppState()

    # start sleep watcher thread
    t = threading.Thread(target=_sleep_watcher, args=(state,), daemon=True)
    t.start()

    fb.clear()
    fb.ui_text("Loading...", top=380, size=14, centered=True)
    sync_if_online()
    state.data = load_home()

    screens = {
        SCREEN_HOME:    HomeScreen(state),
        SCREEN_SOURCE:  SourceScreen(state),
        SCREEN_ARTICLE: ArticleScreen(state),
    }

    while True:
        current = screens[state.screen]

        if state.needs_refresh:
            state.needs_refresh = False
            current.full_render_needed = True

        if current.full_render_needed:
            current.render()
            current.full_render_needed = False
        else:
            current.partial_render()

        current.handle_input()

if __name__ == "__main__":
    main()