from comics.settings.base import *  # NOQA

try:
    from comics.settings.local import *  # NOQA
except ImportError:
    pass

DEBUG = True
TEMPLATE_DEBUG = DEBUG

TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
)

try:
    import debug_toolbar  # NOQA
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INSTALLED_APPS += ('debug_toolbar',)
except ImportError:
    pass

try:
    import django_extensions  # NOQA
    INSTALLED_APPS += ('django_extensions',)
except ImportError:
    pass
