from comics.settings.dev import *

# Remove cache middleware when running tests, as these cause problems in
# django.contrib.{admin,auth,session} unit tests.
MIDDLEWARE_CLASSES = [i for i in MIDDLEWARE_CLASSES
    if not i.startswith('django.middleware.cache')]

# Use a memory cache backend for django.contrib.sessions.tests tests
CACHE_BACKEND = 'locmem:///?timeout=300&max_entries=1000'
