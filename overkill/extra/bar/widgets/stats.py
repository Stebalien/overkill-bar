##
#    This file is part of Overkill-bar.
#
#    Overkill-bar is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Overkill-bar is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Overkill-bar.  If not, see <http://www.gnu.org/licenses/>.
##

from .base import SimpleWidget, Widget
from overkill.sinks import Sink
from .. import colors

class MemWidget(SimpleWidget):
    prefix = colors.GREY("")
    width = 3
    subscription = "memperc"

class CPUWidget(SimpleWidget):
    width = 3
    subscription = "cpu"
    prefix = colors.GREY("")

class TempWidget(SimpleWidget):
    width = 2
    subscription = "acpitemp"
    prefix = colors.GREY(" ")

class BatteryWidget(SimpleWidget):
    width = 4
    subscription = "battery_short"
    prefix = colors.GREY(" ")

class NetWidget(Sink, Widget):
    prefix = colors.GREY(" ")

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
        self.text = r"{upspeed:>5.1f}{grey}u{reset} {downspeed:>5.1f}{grey}d{reset}".format(reset=colors.RESET.fg, grey=colors.GREY.fg, **self.data)

