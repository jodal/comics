from comics.settings.dev import *

# Use in-memory Sqlite3 database for testing to reduce startup time
DATABASES = {
    'default': {
        'NAME': None,
        'ENGINE': 'django.db.backends.sqlite3',
    }
}
