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
from overkill import manager

class BaseWidget(Source):
    publishes = ["text"]
    emits = []
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

class Layout(Sink, Widget):
    def __init__(self, widgets, separator="", min_delay=None, max_delay=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.separator = separator
        self.__do_render = Event()
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.widgets = {w:i for i, w in enumerate(widgets)}
        self.emits = sum((w.emits for w in widgets), [])
        self.text_pieces = [""]*len(widgets)

    def on_start(self):
        for widget in self.widgets:
            self.subscribe_to("text", widget)

        if self.min_delay:
            self.__render_thread = Thread(target=self.__render_loop)
            self.__render_thread.start()
        else:
            self.render = self.__render
            self.__render_thread = None

    def on_stop(self):
        if self.render_thread:
            self.__do_render.set()
            self.__render_thread.join()

    def render(self):
        self.__do_render.set()

    def __render_loop(self):
        call_by = None
        called = False
        while self.running:
            if called:
                if not call_by:
                    call_by = time.time() + self.max_delay
                    next_timeout = self.min_delay
                else:
                    next_timeout = min(self.min_delay, call_by - time.time())

                if next_timeout > 0:
                    self.__do_render.wait(next_timeout)
                
                if not self.__do_render.is_set():
                    call_by = None
                    called = False
                    self.__render()
            else:
                self.__do_render.wait()
                called = True
            self.__do_render.clear()

    def __render(self):
        self.text = self.separator.join(self.text_pieces)

    def handle_updates(self, update, source):
        self.text_pieces[self.widgets[source]] = update["text"]
        self.render()

    def unsubscribe(self, *args, **kwargs):
        super().unsubscribe(*args, **kwargs)

