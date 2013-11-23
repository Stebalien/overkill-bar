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

__all__ = []


# I like clean scopes and I cannot lie...

def wrapper():
    import pkgutil, sys
    import inspect
    from . import base
    self = sys.modules[__name__]

    for imp, name, ispkg in pkgutil.iter_modules(__path__, prefix=__name__+"."):
        if ispkg:
            continue
        mod = imp.find_module(name).load_module(name)
        if mod in sys.modules:
            continue
        for cname in dir(mod):
            klass = getattr(mod, cname)
            if inspect.isclass(klass) and issubclass(klass, base.BaseWidget):
                setattr(self, cname, klass)
                __all__.append(cname)
    delattr(self, "base")

wrapper()
del wrapper
