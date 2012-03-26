from comics.settings.base import *  # NOQA

try:
    from comics.settings.local import *  # NOQA
except ImportError:
    pass
