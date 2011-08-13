import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.insert(0, root_path)

# If you use a virtualenv located at ../venv relative to this wsgi file,
# uncomment the following:
#activate_this = os.path.join(root_path, 'venv/bin/activate_this.py')
#execfile(activate_this, dict(__file__=activate_this))
#os.environ['PATH'] = os.path.join(root_path, 'venv/bin/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'comics.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
