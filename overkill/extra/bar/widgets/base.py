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
from overkill.sinks import Sink, SimpleSink

class BaseWidget(Source):
    publishes = ["text"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__buffer = ""

    @property
    def text(self):
        return self.__buffer

    @text.setter
    def text(self, value):
        self.__buffer = value
        self.push_updates({"text": value})

    def handle_unsubscribe(self, subscription, source):
        self.text = "-"


class TextWidget(BaseWidget):
    def __init__(self, text):
        self.text = text

class Widget(BaseWidget):
    width=0
    align=">"
    postfix=""
    prefix=""
    def __init__(self, prefix=None, postfix=None, align=None, width=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if prefix is not None:
            self.prefix = prefix
        if postfix is not None:
            self.postfix = postfix
        if width is not None:
            self.width = width
        if align is not None:
            self.align = align
        self.text = "-"

    @BaseWidget.text.setter
    def text(self, value):
        BaseWidget.text.fset(self, "{prefix}{value:{align}{width}s}{postfix}".format(
            prefix=self.prefix,
            postfix=self.postfix,
            align=self.align,
            width=self.width, value=value
        ))

class SimpleWidget(SimpleSink, Widget):

    def start(self):
        try:
            if not super().start():
                return False
        except:
            self.text = "No Source"
        return True

    def handle_update(self, update):
        self.text = str(update)

from threading import Thread, Event
import time

def debounce(timeout, max_delay=None):
    def wrapper(fn):
        interrupt = Event();
        called = False
        thread = None
        last_args = ()
        last_kwargs = {}
        call_by = None

        def run():
            nonlocal called, call_by
            while True:
                if called:
                    if not call_by:
                        call_by = time.time() + max_delay
                        next_timeout = timeout
                    else:
                        next_timeout = min(timeout, call_by - time.time())

                    if next_timeout > 0:
                        interrupt.wait(next_timeout)
                    
                    if not interrupt.is_set():
                        call_by = False
                        called = False
                        fn(*last_args, **last_kwargs)
                else:
                    interrupt.wait()
                interrupt.clear()


        def do(*args, **kwargs):
            nonlocal called, thread, last_args, last_kwargs
            last_args = args
            last_kwargs = kwargs
            called = True
            if not thread:
                thread = Thread(target=run)
                thread.start()
            else:
                interrupt.set()

        return do
    return wrapper


class Layout(Sink, Widget):
    def __init__(self, widgets, separator="", debounce_params=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if debounce_params:
            self.render = debounce(*debounce_params)(self.render)
        self.separator = separator
        self.widgets = {w:i for i, w in enumerate(widgets)}
        self.text_pieces = [""]*len(widgets)

    def start(self):
        if super().start():
            for widget in self.widgets:
                self.subscribe_to("text", widget)
            return True
        return False

    def render(self):
        self.text = self.separator.join(self.text_pieces)

    def handle_updates(self, update, source):
        self.text_pieces[self.widgets[source]] = update["text"]
        self.render()
