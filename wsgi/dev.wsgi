import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'comics.settings.dev'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
