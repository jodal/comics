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
    import debug_toolbar  # noqa
    MIDDLEWARE_CLASSES += (  # noqa
        'debug_toolbar.middleware.DebugToolbarMiddleware',)
    INSTALLED_APPS += ('debug_toolbar',)  # noqa
except ImportError:
    pass

try:
    import django_extensions  # noqa
    INSTALLED_APPS += ('django_extensions',)
except ImportError:
    pass
