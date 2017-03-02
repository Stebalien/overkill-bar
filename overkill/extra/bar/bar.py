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

from overkill.sources import Source
from overkill.sinks import Sink
from overkill.sinks import PipeSink
from overkill.extra.writers import PipeWriter
from . import colors

__all__ = ("Bar",)

class Bar(PipeSink, PipeWriter, Sink, Source):
    cmd = ["lemonbar",
           "-B", colors.BACKGROUND,
           "-F", colors.DEFAULT,
           '-g', 'x18',
           '-u', '2',
           '-f', '-*-fixed-medium-r-normal-*-10-*-*-*-*-*-*-*',
           '-f', '-*-montecarlo-bold-r-normal-*-11-*-*-*-*-*-*-*',
           '-f', '-*-siji-medium-r-*-*-10-100-*-*-*-*-*-*'
          ]

    def __init__(self):
        super().__init__()

    def set_widget(self, widget):
        self.widget = widget
        self.num_monitors = None
        self.publishes = widget.emits[:]

    def handle_updates(self, updates, source):
        super().handle_updates(updates, source)
        if source == self.widget:
            self.write(updates["text"])
        elif "monitors" in updates:
            new_num_monitors = len(updates["monitors"])
            if self.num_monitors is not None and new_num_monitors != self.num_monitors:
                self.restart()
            self.num_monitors = new_num_monitors

    def on_start(self):
        self.subscribe_to("text", self.widget)
        if self.is_publishing("monitors"):
            self.subscribe_to("monitors")

    def handle_input(self, line):
        words = line.split(' ', 2)
        if words[0] == 'emit':
            self.push_updates({words[1]: words[2]})
