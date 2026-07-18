# noqa: INP001

from importlib.metadata import version as get_version

project = "Comics"
author = "Stein Magnus Jodal and contributors"
copyright = f"2009-2026, {author}"  # noqa: A001

release = get_version("comics")
version = ".".join(release.split(".")[:2])

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinxcontrib.httpdomain",
]

html_theme = "sphinx_rtd_theme"
html_use_modindex = True
html_use_index = True
html_split_index = False
html_show_sourcelink = True
html_static_path = ["_static"]

autodoc_member_order = "bysource"

extlinks = {"issue": ("https://github.com/jodal/comics/issues/%s", "#")}
