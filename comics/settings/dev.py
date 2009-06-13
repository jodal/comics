from comics.settings.base import *
from comics.settings.local import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

try:
    import debug_toolbar
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INSTALLED_APPS += ('debug_toolbar',)
except ImportError:
    pass
