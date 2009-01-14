# Django settings for comics project.
from settings import *

# Debugging
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# URL and media
MEDIA_URL = '/media/comics/'
ADMIN_MEDIA_PREFIX = MEDIA_URL + 'admin/'

# Sessions
SESSION_COOKIE_PATH = '/comics/'

# Caching
CACHE_BACKEND = 'locmem:///'
CACHE_MIDDLEWARE_KEY_PREFIX = 'comics-dev'

if DEBUG:
    try:
        # Setup debug_toolbar
        import debug_toolbar
        MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
        INSTALLED_APPS += ('debug_toolbar',)
    except ImportError:
        pass
