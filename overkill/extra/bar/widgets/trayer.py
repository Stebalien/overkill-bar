from .base import BaseWidget
from overkill.sinks import PipeSink
import subprocess

class TrayerWidget(PipeSink, BaseWidget):
    restart = True
    cmd = [
        "xprop", 
        '-name', "panel",
        "-f", "WM_SIZE_HINTS", "32i", " $5\n",
        "-spy", "WM_NORMAL_HINTS"
    ]

    panel_cmd = [
        "trayer",
        "--edge", "top",
        "--align", "right",
        "--widthtype", "request",
        "--height", "18",
        "--tint", "0x151515",
        "--transparent", "true",
        "--expand", "true",
        "--SetDockType", "true",
        "--alpha", "0"
    ]

    def on_start(self):
        # Yes there is a race condition...
        # That's why we restart xprop and pray...
        self.panel = subprocess.Popen(self.panel_cmd)

    def handle_input(self, line):
        try:
            _, width = line.split(' ')
            self.width = int(width)
            self.render()
        except:
            # TODO: Somethign else?
            self.stop()

    def render(self):
        self.text = "%%{O%d}" % self.width
