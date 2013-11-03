from overkill.sinks import Sink
from overkill.extra.writers import PipeWriter

__all__ = ("Bar", "manager")

class Bar(Sink, PipeWriter):
    cmd = ["bar-aint-recursive"]
    def __init__(self):
        super().__init__()

    def set_widget(self, widget):
        self.widget = widget
        self.num_monitors = None

    def handle_updates(self, updates, source):
        if source == self.widget:
            self.write(updates["text"])
        elif "monitors" in updates:
            new_num_monitors = len(updates["monitors"])
            if self.num_monitors is not None and new_num_monitors != self.num_monitors:
                self.restart()
            self.num_monitors = new_num_monitors

    def on_start(self):
        self.subscribe_to("text", self.widget)
        self.subscribe_to("monitors")

