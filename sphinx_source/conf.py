# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# sys.path.insert(0, os.path.abspath('../shopyo/'))


# -- Project information -----------------------------------------------------

project = 'Shopyo'
# copyright = '2020, Abdur-rahmaanJ'
author = 'Abdur-rahmaanJ & Shopyo Team'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc', 'sphinx.ext.viewcode'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------
html_context = {
    "project_links": [
        "Source Code", "https://github.com/Abdur-rahmaanJ/shopyo",
        "Issue Tracker", "https://github.com/Abdur-rahmaanJ/shopyo/issues",
    ]
}
html_logo = 'shopyo.ico'

html_sidebars = {'**': [
    'about.html',
    'relations.html',
    'navigation.html',
    'searchbox.html'
]}

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'
html_theme_options = {
    'github_repo': 'Abdur-rahmaanJ/shopyo',
    'fixed_sidebar': 'true',

}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []
