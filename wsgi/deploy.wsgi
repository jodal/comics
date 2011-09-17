import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.insert(0, root_path)

try:
    from wsgi.local import *
except ImportError as e:
    raise EnvironmentError('Unable to import WSGI local settings: did you '
        'copy wsgi/local.py.template to wsgi/local.py and modify?')

os.environ['DJANGO_SETTINGS_MODULE'] = DJANGO_SETTINGS_MODULE

# Slip into the virtualenv if we have to
if VIRTUALENV_ROOT is not None:
    VIRTUALENV_ROOT = os.path.join(
        root_path, 'wsgi', VIRTUALENV_ROOT
    )
    virtualenv_bin = os.path.join(VIRTUALENV_ROOT, 'bin')
    activate_this = os.path.join(virtualenv_bin, 'activate_this.py')
    execfile(activate_this, dict(__file__=activate_this))

    # Import Django and reload from the virtualenv in case it was loaded
    # elsewhere
    import django
    django = reload(django)

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
