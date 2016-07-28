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

import time

from overkill.sinks import Sink
from .base import SimpleWidget, Widget
from .. import colors

class MemWidget(SimpleWidget):
    prefix = colors.FADED("")
    width = 3
    subscription = "memperc"

    def handle_update(self, update):
        color = colors.FADED
        try:
            if int(update) >= 80:
                color = colors.WARNING
        except:
            pass

        self.prefix = color("")
        self.text = str(update)

class CPUWidget(SimpleWidget):
    width = 3
    subscription = "cpu"
    prefix = colors.FADED("")

    def __init__(self, *args, **kwargs):
        self.pegging = None
        super().__init__(*args, **kwargs)

    def handle_update(self, update):
        color = colors.FADED
        try:
            if int(update) >= 24:
                if self.pegging is None:
                    self.pegging = time.monotonic()
                elif self.pegging is True or (time.monotonic() - self.pegging) > 10:
                    self.pegging = True
                    color = colors.WARNING
            else:
                self.pegging = None
        except:
            pass

        self.prefix = color("")
        self.text = str(update)


class TempWidget(SimpleWidget):
    width = 2
    subscription = "acpitemp"
    prefix = colors.FADED(" ")

    def handle_update(self, update):
        color = colors.FADED
        try:
            if int(update) >= 90:
                color = colors.WARNING
        except:
            pass
        self.prefix = color(" ")
        self.text = str(update)


class BatteryWidget(SimpleWidget):
    width = 3
    subscription = "battery_short"
    prefix = colors.FADED("")

    def handle_update(self, update):
        if update[:1] in ("C", "U", "D"):
            (prefix, perc) = update.split(' ')
            perc = perc.strip('%')
            if prefix == "D":
                if int(perc) < 10:
                    self.prefix = colors.WARNING("")
                else:
                    self.prefix = colors.FADED("")
            else:
                self.prefix = colors.FADED("")
            self.text = perc
        elif update == "F":
            self.prefix = colors.FADED("")
            self.text = "99" # Fits better... 🙈
        else:
            self.prefix = colors.FADED("")
            self.text = update

class NetWidget(Sink, Widget):
    prefix = colors.FADED(" ")

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
        self.text = r"{upspeed:>5.1f}{grey}u{reset} {downspeed:>5.1f}{grey}d{reset}".format(
            reset=colors.RESET.fg,
            grey=colors.FADED.fg,
            **self.data
        )
