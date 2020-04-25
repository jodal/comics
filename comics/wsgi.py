import os
import sys

import dotenv


PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "comics.settings")


# Load environment variables from .env if it exists
dotenv_path = os.path.join(PROJECT_ROOT, ".env")
if os.path.exists(dotenv_path):
    dotenv.load_dotenv(dotenv_path)


VIRTUALENV_ROOT = os.environ.get("VIRTUALENV_ROOT")

if VIRTUALENV_ROOT:
    # Activate virtualenv
    activate_this = os.path.join(VIRTUALENV_ROOT, "bin", "activate_this.py")
    execfile(activate_this, {"__file__": activate_this})

    # Import Django and reload it in case it was loaded outside the virtualenv
    import django

    django = reload(django)


from django.core.wsgi import get_wsgi_application  # noqa

application = get_wsgi_application()
