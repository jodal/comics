import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comics.settings')

root_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, root_path)

VIRTUALENV_ROOT = None

try:
    from comics.wsgi.local import *  # NOQA
except ImportError:
    pass

if VIRTUALENV_ROOT:
    # Activate virtualenv
    VIRTUALENV_ROOT = os.path.abspath(os.path.join(
        os.path.dirname(__file__), VIRTUALENV_ROOT))
    activate_this = os.path.join(VIRTUALENV_ROOT, 'bin', 'activate_this.py')
    execfile(activate_this, dict(__file__=activate_this))

    # Import Django and reload from the virtualenv in case it was loaded
    # elsewhere
    import django
    django = reload(django)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
