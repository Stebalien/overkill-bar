from .base import SimpleWidget, Widget
from overkill.sinks import Sink

class MemWidget(SimpleWidget):
    prefix = r"\f3\fr"
    width = 3
    subscription = "memperc"

class CPUWidget(SimpleWidget):
    width = 3
    subscription = "cpu"
    prefix = r"\f3\fr"

class TempWidget(SimpleWidget):
    width = 2
    subscription = "acpitemp"
    prefix = r"\f3\fr "

class BatteryWidget(SimpleWidget):
    width = 4
    subscription = "battery_short"
    prefix = r"\f3\fr"

class NetWidget(Sink, Widget):
    prefix = r"\f3\fr "

    def __init__(self, interfaces=None, **kwargs):
        super().__init__(**kwargs)
        self.interfaces = interfaces
        self.data = {
            "upspeed": 0,
            "downspeed": 0
        }

    def on_start(self):
        if self.interfaces:
            for interface in self.interfaces:
                self.subscribe_to("downspeedf " + interface)
                self.subscribe_to("upspeedf " + interface)
        else:
            self.subscribe_to("downspeedf")
            self.subscribe_to("upspeedf")

    def handle_updates(self, updates, source):
        self.data["upspeed"] = 0
        self.data["downspeed"] = 0
        for key, value in updates.items():
            if key.startswith("upspeedf"):
                self.data["upspeed"] += float(value)
            elif key.startswith("downspeedf"):
                self.data["downspeed"] += float(value)
        self.text = r"{upspeed:>5.1f}\f3u\fr {downspeed:>5.1f}\f3d\fr".format_map(self.data)

