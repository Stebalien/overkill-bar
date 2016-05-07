from os import getenv

class Color(str):
    def __init__(self, initial):
        self.fg = "%{F"+self+"}"
        self.bg = "%{B"+self+"}"
        self.u = "%{U"+self+"}"

    def __call__(self, string):
        return self.fg + string + RESET.fg

def get_color(name, default):
    color = getenv("COLOR_{}".format(name))
    if color is None:
        return default
    return "#ff{}".format(color[1:])

DEFAULT     = Color(get_color("DEFAULT", "#ffaaaaaa"))
BACKGROUND  = Color(get_color("BACKGROUND", "#ff151515"))
ACTIVE      = Color(get_color("ACTIVE", "#ffafd700"))
SELECT      = Color(get_color("SELECT", "#ff2a2a2a"))
FADED       = Color(get_color("FADED", "#ff555555"))
RESET       = Color("-")
BRIGHT      = Color(get_color("BRIGHT", "#ffeeeeee"))
WARNING     = Color(get_color("WARNING", "#ffff7e00"))
HIGHLIGHT   = Color(get_color("HIGHLIGHT", '#ff589CC5'))

del get_color
