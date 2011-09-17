import os
import sys

__doc__ = """
Controls all interactions with any configured virtualenv
"""

def enter_virtualenv():
    """Enters a virtualenv setup based on comics.settings.local's settings.
    Try to call this as early as you can so you don't pollute the namespace
    with all sorts of things that should be in the virtualenv but are
    instead using the global instances."""

    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 
        '../../'))
    sys.path.insert(0, root_path)

    try:
        # Loading comics.settings imports Django through __init__.py in that
        # directory; keep in mind that we therefore have to reload it if we're
        # using a virtualenv'd Django.
        from comics.settings.local import VIRTUALENV_ROOT
    except ImportError as e:
        VIRTUALENV_ROOT = None

    if VIRTUALENV_ROOT is not None:
        VIRTUALENV_ROOT = os.path.join(
            root_path, 'comics/settings', VIRTUALENV_ROOT
        )
        virtualenv_bin = os.path.join(VIRTUALENV_ROOT, 'bin')
        activate_this = os.path.join(virtualenv_bin, 'activate_this.py')
        execfile(activate_this, dict(__file__=activate_this))

        # Import Django and reload from the virtualenv
        import django
        django = reload(django)
