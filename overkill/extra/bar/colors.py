
class Color(str):
    def __init__(self, initial):
        self.fg = "%{F"+self+"}"
        self.bg = "%{B"+self+"}"
        self.u = "%{U"+self+"}"

    def __call__(self, string):
        return self.fg + string + RESET.fg

GREEN = Color("#afd700")
DARK = Color("#2a2a2a")
GREY = Color("#555555")
RED = Color("#a6000a")
GREEN = Color("#afd700")
RESET = Color("-")
BRIGHT = Color("#eeeeee")
