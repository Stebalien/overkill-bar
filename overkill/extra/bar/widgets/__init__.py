
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
