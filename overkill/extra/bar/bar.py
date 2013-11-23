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

