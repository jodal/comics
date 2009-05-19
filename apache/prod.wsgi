import os, sys
path = '/home/jodal/production/comics'
if path not in sys.path:
	sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'comics.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
