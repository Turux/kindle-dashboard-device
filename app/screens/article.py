# app/screens/article.py

from app.input.dpad import wait_for_key, KEY_BACK
from app.state import SCREEN_HOME

class ArticleScreen:
    def __init__(self, state):
        self.state = state
        self.full_render_needed = True

    def render(self):
        pass  # TODO

    def partial_render(self):
        self.render()

    def handle_input(self):
        key = wait_for_key()
        if key == KEY_BACK:
            self.state.screen = self.state.prev_screen or SCREEN_HOME