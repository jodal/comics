import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.insert(0, root_path)

try:
    from comics.settings.local import DEBUG
except ImportError as e:
    DEBUG=False

if DEBUG:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'comics.settings.dev'
else:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'comics.settings'

try:
    from comics.settings.local import VIRTUALENV_ROOT
except ImportError as e:
    VIRTUALENV_ROOT = None

# If we need to activate virtualenv, do that here
if VIRTUALENV_ROOT is not None:
    VIRTUALENV_ROOT = os.path.join(
        root_path, 'comics/settings', VIRTUALENV_ROOT
    )
    virtualenv_bin = os.path.join(VIRTUALENV_ROOT, 'bin')
    activate_this = os.path.join(virtualenv_bin, 'activate_this.py')

    execfile(activate_this, dict(__file__=activate_this))
    import django
    django = reload(django)

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
