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

from .base import SimpleWidget, BaseWidget
from overkill.sinks import Sink
from .. import colors

def format_escape(string):
    return string.replace("{", "{{").replace("}", "}}")

class DesktopsWidget(SimpleWidget):
    emits = ["wm.desktop.focus"]
    ACTIVE_DESKTOP_FORMAT = format_escape(colors.SELECT.bg + colors.HIGHLIGHT.u + "%{+u}") + " {desktop.name} " + format_escape("%{-u}" + colors.RESET.bg)
    INACTIVE_DESKTOP_FORMAT = "%{{A:emit wm.desktop.focus {desktop.index}:}} {desktop.name} %{{A}}"
    subscription = "desktops"

    def __init__(self, monitor=None):
        if monitor:
            self.subscription = ("desktops", monitor)
        super().__init__()

    def handle_update(self, desktops):
        self.text = "".join(
            (self.ACTIVE_DESKTOP_FORMAT if desktop.focused else self.INACTIVE_DESKTOP_FORMAT).format(desktop=desktop)
            for desktop in desktops if desktop.occupied or desktop.focused
        )


class MultiMonitorWidget(Sink, BaseWidget):
    emits = ["wm.desktop.focus", "wm.desktop.layout"]
    def on_start(self):
        self.subscribe_to("monitors")
        self.monitors = []
        self.widgets = {}
        self.__widget_indices = {}

    def handle_updates(self, updates, source):
        if "text" in updates:
            try:
                self.text_pieces[self.__widget_indices[source]] = updates["text"]
            except KeyError:
                pass
            self.render()

        if "monitors" in updates:
            new_monitors = list(reversed(updates["monitors"]))
            new_names = [m.name for m in new_monitors]
            old_names = [m.name for m in self.monitors]
            if old_names != new_names:
                new_widgets = {}
                for monitor in new_monitors:
                    if monitor in self.widgets:
                        new_widgets[monitor] = self.widgets[monitor]
                    else:
                        widget = new_widgets[monitor] = DesktopsWidget(monitor.name)
                        self.subscribe_to("text", widget)

                for monitor in self.monitors:
                    if monitor not in new_widgets and monitor in self.widgets:
                        self.unsubscribe_from("text", self.widgets[monitor])

                self.widgets = new_widgets
                self.__widget_indices = {
                    self.widgets[m]:i for i, m in enumerate(new_monitors)
                }
                self.text_pieces = [""]*len(new_monitors)
            self.monitors = new_monitors
            self.render()

    def render(self):

        self.text = "".join(
            r"%%{S%i}%%{l}%%{A:emit wm.desktop.layout next:}%s%%{A}%s" % (i, (colors.HIGHLIGHT.fg if m.focused else colors.ICON.fg) + "  " + colors.RESET.fg, t)
            for i, (t, m) in enumerate(zip(self.text_pieces, self.monitors))
        )
