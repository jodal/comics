import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# -- General configuration ----------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinxcontrib.httpdomain",
]

templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"

project = "Comics"
copyright = "2009-2021, Stein Magnus Jodal and contributors"

version = "3.0"
release = "3.0.0"

exclude_trees = ["_build"]

pygments_style = "sphinx"


# -- Options for HTML output --------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

html_use_modindex = True
html_use_index = True
html_split_index = False
html_show_sourcelink = True

htmlhelp_basename = "comics"


# -- Options for LaTeX output -------------------------------------------------

latex_documents = [
    (
        "index",
        "comics.tex",
        "Comics Documentation",
        "Stein Magnus Jodal and contributors",
        "manual",
    ),
]


# -- Options for extlink extension --------------------------------------------

extlinks = {
    "issue": ("https://github.com/jodal/comics/issues/%s", "#"),
}
