import os
import subprocess
import sys
import re
from .__init__ import __version__
from pathlib import Path

from .api.file import trycopy
from .api.file import trycopytree
from .api.file import trymkdir
from .api.file import trymkfile
from .api.info import printinfo
from .api.file import tryrmtree
from .api.file import tryrmfile

dirpath = Path(__file__).parent.absolute()
dirpathparent = Path(__file__).parent.parent.absolute()


def is_venv():
    return hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )


def conf_py_content(project_name):
    return """
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
import sys
import os

current_dir = os.path.dirname(__file__)
target_dir = os.path.abspath(os.path.join(current_dir, "../"))
sys.path.insert(0, os.path.abspath(target_dir))


# -- Project information -----------------------------------------------------

project = "{project_name}"
# copyright = ''
author = ""


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.napoleon",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
html_context = {{
    "project_links": [
        "Source Code",
        "https://github.com/<name>/<project>",
        "Issue Tracker",
        "https://github.com/<name>/<project>/issues",
    ]
}}
html_logo = "shopyo.ico"

html_sidebars = {{
    "**": ["about.html", "relations.html", "navigation.html", "searchbox.html"]
}}

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"
html_theme_options = {{
    "github_repo": "<name>/<project>",
    "fixed_sidebar": "true",
}}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
""".format(
        project_name=project_name
    )


def index_rst_content():
    return """
Welcome to ProjectName docs!
============================

Write project description here

.. toctree::
   :maxdepth: 9

   Docs <docs>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


def docs_rst_content():
    return """
.. :tocdepth:: 5

Documentation
=============

Sphinx is included in dev_requirements.txt .
Run in main folder:

.. code:: bash

    sphinx-build -b html sphinx_source docs

to generate html pages in docs
"""


def gitignore_content():
    return """
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# celery beat schedule file
celerybeat-schedule

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/

# shopyo
test.db
testing.db
shopyo.db

# pycharm
.idea/

# win
*.exe
*.cs
*.bat
*.vbs

#migrations
migrations/

#vscode
.vscode
workspace.code-workspace

#uploads
shopyo/static/uploads/products/
shopyo/static/uploads/images/
shopyo/static/uploads/thumbs/
shopyo/static/uploads/category/
shopyo/static/uploads/subcategory/

# modules in static since present in modules
shopyo/static/modules/

# ignore secrets
config.json

"""


def readme_md_content(project_name):
    return """
# {0}
""".format(project_name)


def tox_ini_content():
    return """
[tox]
envlist =
    py39
    py38
    py37
    py36
skip_missing_interpreters=true

[testenv]
# test setup according to https://www.appinv.science/shopyo/testing.html
changedir = shopyo
deps = 
    pytest 
    pytest-order
commands = python -m pytest  {posargs}
"""


def requirements_txt_content():
    return """
shopyo=={version}
""".format(version=__version__)


def dev_requirements_txt_content():
    return """
flake8==3.8.4
black==20.8b1
isort==5.6.4
Sphinx==3.2.1
pytest==6.1.1
pytest-order==0.9.2
tox==3.21.0
pytest-cov==2.11.1
codecov==2.1.11
factory-boy==3.2.0
freezegun==1.1.0
pytest-dotenv
"""


def new_project(newfoldername):
    """
    $ shopyo new blog

    creates:
        blog/
            docs/
                conf.py
                index.rst
            blog/
    """
    path = "."
    newfoldername = newfoldername.strip("/").strip("\\")
    print("creating new project {}".format(newfoldername))

    base_path = path + "/" + newfoldername
    trymkdir(base_path)
    print("created dir {} in {}".format(newfoldername, path))

    trycopytree(
        os.path.join(dirpathparent, "shopyo"),
        os.path.join(base_path, newfoldername),
    )
    tryrmfile(os.path.join(base_path, newfoldername, "__init__.py"))
    tryrmfile(os.path.join(base_path, newfoldername, "__main__.py"))
    tryrmtree(os.path.join(base_path, newfoldername, "api"))

    # trycopy(
    #     os.path.join(dirpathparent, "requirements.txt"),
    #     os.path.join(base_path, "requirements.txt"),
    # )
    # with open(os.path.join(base_path, "requirements.txt"), "a") as f:
    #     f.write("\nshopyo")
    trymkfile(
        os.path.join(base_path, "requirements.txt"), requirements_txt_content()
    )
    trymkfile(
        os.path.join(base_path, "dev_requirements.txt"),
        dev_requirements_txt_content(),
    )
    trymkfile(
        os.path.join(base_path, ".gitignore"),
        gitignore_content(),
    )
    trymkfile(
        os.path.join(base_path, ".nojekyll"),
        "",
    )
    trymkfile(
        os.path.join(base_path, "tox.ini"),
        tox_ini_content(),
    )

    trymkfile(
        os.path.join(base_path, "README.md"), readme_md_content(newfoldername)
    )

    # docs
    trymkdir(os.path.join(base_path, "docs"))
    sphinx_src = os.path.join(base_path, newfoldername, "sphinx_source")
    tryrmtree(sphinx_src)
    trymkdir(sphinx_src)
    trymkfile(
        os.path.join(sphinx_src, "conf.py"),
        conf_py_content(newfoldername),
    )
    trymkdir(os.path.join(sphinx_src, "_static"))
    trymkfile(os.path.join(sphinx_src, "_static", "custom.css"), "")
    trycopy(
        os.path.join(dirpathparent, "shopyo", "sphinx_source", "Makefile"),
        os.path.join(sphinx_src, "Makefile"),
    )
    trymkfile(
        os.path.join(sphinx_src, "index.rst"),
        index_rst_content(),
    )
    trymkfile(
        os.path.join(sphinx_src, "docs.rst"),
        docs_rst_content(),
    )
    trycopy(
        os.path.join(dirpathparent, "shopyo", "sphinx_source", "shopyo.ico"),
        os.path.join(sphinx_src, "shopyo.ico"),
    )

    print("Project", newfoldername, "created successfully!")


def is_valid_name(name):
    notallowedpattern = r'[_\.]+'
    allowedpattern = r'^[\w+\.]+$'
    isallowed = re.match(allowedpattern, name)
    isnotallowed = re.match(notallowedpattern, name)

    if not isnotallowed and isallowed:
        return True
    else:
        return False


def main():
    args = sys.argv
    if len(args) == 1:
        printinfo()
        print("No arguments supplied")
    elif len(args) == 2 and args[1] == "new":
        printinfo()
        print("""Please enter an alphanumeric name.
A combination of character, number and underscore is allowed""")
    elif len(args) == 3 and args[1] == "new":
        printinfo()
        if args[2] and is_valid_name(args[2]):
            new_project(args[2])
        else:
            print("""Please enter an alphanumeric name.
A combination of character, number and underscore is allowed""")
    else:
        if not is_venv():
            print("Please use Shopyo in a virtual environment for this command")
            sys.exit()
        torun = [sys.executable, "manage.py"] + args[1:]
        subprocess.run(torun)


if __name__ == "__main__":
    main()
