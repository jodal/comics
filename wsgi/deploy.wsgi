import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.insert(0, root_path)

VIRTUALENV_ROOT = None
DJANGO_SETTINGS_MODULE = 'comics.settings'

try:
    from wsgi.local import *
except ImportError:
    pass

os.environ['DJANGO_SETTINGS_MODULE'] = DJANGO_SETTINGS_MODULE

if VIRTUALENV_ROOT:
    VIRTUALENV_ROOT = os.path.join(root_path, 'wsgi', VIRTUALENV_ROOT)
    activate_this = os.path.join(VIRTUALENV_ROOT, 'bin', 'activate_this.py')
    execfile(activate_this, dict(__file__=activate_this))

    # Import Django and reload from the virtualenv in case it was loaded
    # elsewhere
    import django
    django = reload(django)

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
