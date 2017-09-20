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

from .base import SimpleWidget
from .. import colors
import time

class ClockWidget(SimpleWidget):
    subscription = "time"
    prefix = colors.ICON(" ")

    def __init__(self, fmt="%Y.%m.%d", *args, **kwargs):
        self.fmt = fmt
        super().__init__(*args, **kwargs)

    def handle_update(self, localtime):
        self.text = time.strftime(self.fmt, localtime)

