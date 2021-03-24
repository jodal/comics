import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "comics.settings")

from django.core.wsgi import get_wsgi_application  # noqa

application = get_wsgi_application()
