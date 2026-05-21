# app/screens/source.py

from app.input.dpad import wait_for_key, KEY_BACK, is_page_forward, is_page_backward
from app.state import SCREEN_HOME

class SourceScreen:
    def __init__(self, state):
        self.state = state

    def render(self):
        pass  # TODO

    def partial_render(self):
        self.render()

    def handle_input(self):
        key = wait_for_key()
        if key == KEY_BACK:
            self.state.screen = SCREEN_HOME