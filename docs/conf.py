"""Sphinx configuration."""

from datetime import datetime

project = "iterage"
author = "Richard Liebscher"
copyright = f"{datetime.now().year}, {author}"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx_autodoc_typehints",
]
