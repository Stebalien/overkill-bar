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

from .base import Widget
from .. import colors
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
        self.prefix = (colors.ACTIVE.fg if self.data["playing"] else colors.ICON.fg) \
                    + (r"" if self.data["muted"] else r"") + colors.RESET.fg
        self.postfix = colors.RESET.u
        self.text = str(self.data["volume"])

class RecordingWidget(Sink, Widget):
    width = 3
    def on_start(self):
        self.data = {
            "recording": False,
            "mic_muted": False,
        }
        self.subscribe_to("recording")
        self.subscribe_to("mic_muted")

    def handle_updates(self, updates, source):
        self.data.update(updates)
        if self.data["recording"]:
            if self.data["mic_muted"]:
                self.text = colors.ACTIVE("")
            else:
                self.text = colors.ACTIVE("")
        else:
            self.text = " "

