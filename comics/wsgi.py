import os
import sys

import environ
import importlib


root = environ.Path(os.path.dirname(os.path.dirname(__file__)))

env = environ.Env()
env.read_env(root(".env"))


sys.path.insert(0, root())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "comics.settings")


VIRTUALENV_ROOT = env.str("VIRTUALENV_ROOT", default="")

if VIRTUALENV_ROOT:
    # Activate virtualenv
    venv = environ.Path(VIRTUALENV_ROOT)
    activate_this = venv("bin/activate_this.py")
    exec(
        compile(open(activate_this, "rb").read(), activate_this, "exec"),
        {"__file__": activate_this},
    )

    # Import Django and reload it in case it was loaded outside the virtualenv
    import django

    django = importlib.reload(django)


from django.core.wsgi import get_wsgi_application  # noqa

application = get_wsgi_application()
