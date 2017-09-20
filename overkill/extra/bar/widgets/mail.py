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

from .base import SimpleWidget, Sink, Widget

from .. import colors

class MailCountWidget(SimpleWidget):
    prefix = colors.ICON.fg + " " + colors.RESET.fg
    width = 2
    subscription = "mailcount"

class ExtendedMailCountWidget(Sink, Widget):
    prefix = colors.ICON.fg + r" " + colors.RESET.fg
    def on_start(self):
        self.data = {
            "mailcount": 0,
            "mailqueue": 0
        }
        self.subscribe_to("mailcount")
        self.subscribe_to("mailqueue")
    
    def handle_updates(self, updates, source):
        self.data.update(updates)

        self.prefix = (colors.WARNING.fg if (self.data["mailqueue"] > 0) else colors.ICON.fg) + " " + colors.RESET.fg
        self.text = str(self.data["mailcount"])
