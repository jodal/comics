# noqa: INP001

import pathlib
import tomllib

project = "Comics"
author = "Stein Magnus Jodal and contributors"
copyright = f"2009-2024, {author}"  # noqa: A001

with pathlib.Path("../pyproject.toml").open("rb") as fh:
    release = tomllib.load(fh)["project"]["version"]
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
