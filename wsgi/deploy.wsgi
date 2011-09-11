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

# Slip into the virtualenv if we have to...
from comics.utils.virtualenv import enter_virtualenv
enter_virtualenv()

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
