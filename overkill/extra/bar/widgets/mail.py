from .base import SimpleWidget, Sink, Widget

class MailCountWidget(SimpleWidget):
    prefix = r"\f3\fr "
    width = 2
    subscription = "mailcount"

class ExtendedMailCountWidget(Sink, Widget):
    prefix = r"\f3\fr "
    def on_start(self):
        self.data = {
            "mailcount": 0,
            "mailqueue": 0
        }
        self.subscribe_to("mailcount")
        self.subscribe_to("mailqueue")
    
    def handle_updates(self, updates, source):
        self.data.update(updates)

        self.prefix = r"\f6\fr " if self.data["mailqueue"] > 0 else r"\f3\fr "
        self.text = str(self.data["mailcount"])
