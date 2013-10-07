from .base import Widget
from overkill.sinks import Sink
class AudioWidget(Sink, Widget):
    width = 3
    def on_start(self):
        self.data = {
            "volume": 0,
            "muted": False,
            "playing": False,
        }
        self.subscribe_to("volume")
        self.subscribe_to("muted")
        self.subscribe_to("playing")

    def handle_updates(self, updates, source):
        self.data.update(updates)
        self.prefix = (r"\f9" if self.data["playing"] else r"\f3") \
                    + (r"" if self.data["muted"] else r"") + r"\fr" 
        self.postfix = r"\ur"
        self.text = str(self.data["volume"])
