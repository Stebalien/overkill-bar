from .base import SimpleWidget
import time

class ClockWidget(SimpleWidget):
    subscription = "time"

    def __init__(self, fmt="%Y.%m.%d", *args, **kwargs):
        self.fmt = fmt
        super().__init__(*args, **kwargs)

    def handle_update(self, localtime):
        self.text = time.strftime(self.fmt, localtime)

