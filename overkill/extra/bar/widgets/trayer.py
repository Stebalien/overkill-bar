from .base import BaseWidget
from .. import colors
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
        "--tint", "0x" + colors.BACKGROUND[-6:].lower(),
        "--transparent", "true",
        "--expand", "true",
        "--SetDockType", "true",
        "--alpha", "0"
    ]

    def __init__(self):
        super().__init__()
        self.width = 0
        self.panel = None

    def on_start(self):
        # Yes there is a race condition...
        # That's why we restart xprop and pray...
        self.panel = subprocess.Popen(self.panel_cmd)

    def on_stop(self):
        if self.panel:
            try:
                self.panel.terminate()
                self.panel.wait()
            except:
                pass

    def handle_input(self, line):
        try:
            _, width = line.split(' ')
            self.width = int(width)
            self.render()
        except:
            # TODO: Something else?
            self.stop()

    def render(self):
        self.text = "%%{O%d}" % self.width
