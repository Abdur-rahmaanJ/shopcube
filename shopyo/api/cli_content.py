import textwrap


def get_module_view_content():
    content = textwrap.dedent(
        """\
        from shopyo.api.module import ModuleHelp
        # from flask import render_template
        # from flask import url_for
        # from flask import redirect
        # from flask import flash
        # from flask import request

        # from shopyo.api.html import notify_success
        # from shopyo.api.forms import flash_errors

        mhelp = ModuleHelp(__file__, __name__)
        globals()[mhelp.blueprint_str] = mhelp.blueprint
        module_blueprint = globals()[mhelp.blueprint_str]


        @module_blueprint.route("/")
        def index():
            return mhelp.info['display_string']

        # If "dashboard": "/dashboard" is set in info.json
        #
        # @module_blueprint.route("/dashboard", methods=["GET"])
        # def dashboard():

        #     context = mhelp.context()

        #     context.update({

        #         })
        #     return mhelp.render('dashboard.html', **context)
        """
    )

    return content


def get_dashboard_html_content():
    content = textwrap.dedent(
        """\
        {% extends "base/module_base.html" %}
        {% set active_page = info['display_string']+' dashboard' %}
        {% block pagehead %}
        <title></title>
        <style>
        </style>
        {% endblock %}
        {% block sidebar %}
        {% include info['module_name']+'/blocks/sidebar.html' %}
        {% endblock %}
        {% block content %}
        <br>

        <div class="card">
            <div class="card-body">

            </div>
        </div>
        {% endblock %}
        """
    )

    return content


def get_global_py_content():
    content = textwrap.dedent(
        """\
        available_everywhere = {

        }
        """
    )

    return content


def get_cli_content(projname):
    content = textwrap.dedent(
        f'''\
        """
        file: cli.py
        description: Add your custom cli commands here
        documentation: https://click.palletsprojects.com/en/7.x/

        You will need to run ``python -m pip install -e .`` to load the setup.py
        which contains the entry point to this file before being able to run your
        custom commands

        Usage ``{projname} [OPTIONS] COMMAND [ARGS]...``

        Example command 'welcome' has been added.
        - To get your project version, run ``{projname} --version``
        - Run the sample command as ``{projname} welcome [OPTIONS] NAME``
        """

        from {projname} import __version__
        import click


        @click.group()
        @click.version_option(__version__)
        @click.pass_context
        def cli(ctx):
            """CLI entry point"""
            pass


        @cli.command("welcome")
        @click.argument("name")
        @click.option('--verbose', "-v", is_flag=True, default=False)
        def welcome(name, verbose):
            """Sample command to welcome users.

            NAME will be printed along with the welcome message
            """
            click.secho(f"Hi {{name}}. Welcome to {projname}", fg="cyan")

            if verbose:
                click.echo("See you soon")
        '''
    )

    return content


def get_init_content():
    content = textwrap.dedent(
        """\
        version_info = (1, 0, 0)
        __version__ = ".".join([str(v) for v in version_info])
        """
    )

    return content


def get_setup_py_content(projname):
    content = textwrap.dedent(
        f'''\
        """
        A setuptools based setup module.
        See:
        https://packaging.python.org/guides/distributing-packages-using-setuptools/
        https://github.com/pypa/sampleproject

        python setup.py publish to publish

        """

        # Always prefer setuptools over distutils
        from setuptools import setup

        # from setuptools import find_packages

        import os
        import sys
        from {projname} import __version__  # thanks gunicorn

        here = os.path.abspath(os.path.dirname(__file__))

        if sys.argv[-1] == "publish":  # requests
            os.system("python setup.py sdist")  # bdist_wheel
            os.system("twine upload dist/* --skip-existing")
            sys.exit()

        # Get the long description from the README file
        with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
            long_description = f.read()
        setup(
            name="{projname}",  # Required
            version=__version__,  # Required
            description="",  # Optional
            long_description=long_description,  # Optional
            long_description_content_type="text/markdown",  # Optional (see note above)
            url="",  # Optional
            author="",  # Optional
            author_email="",  # Optional
            # Classifiers help users find your project by categorizing it.
            #
            # For a list of valid classifiers, see https://pypi.org/classifiers/
            classifiers=[  # Optional
                # How mature is this project? Common values are
                #   3 - Alpha
                #   4 - Beta
                #   5 - Production/Stable
                "Development Status :: 4 - Beta",
                # Indicate who your project is intended for
                "Intended Audience :: Developers",
                # 'Topic :: Weather',
                # Pick your license as you wish
                "License :: OSI Approved :: MIT License",
                # Specify the Python versions you support here. In particular, ensure
                # that you indicate whether you support Python 2, Python 3 or both.
                # These classifiers are *not* checked by 'pip install'. See instead
                # 'python_requires' below.
                "Programming Language :: Python :: 3.6",
                "Programming Language :: Python :: 3.7",
                "Programming Language :: Python :: 3.8",
                "Programming Language :: Python :: 3.9",
            ],
            keywords="",  # Optional
            # You can just specify package directories manually here if your project is
            # simple. Or you can use find_packages().
            #
            # Alternatively, if you just want to distribute a single Python file, use
            # the `py_modules` argument instead as follows, which will expect a file
            # called `my_module.py` to exist:
            #
            #   py_modules=["my_module"],
            #
            # packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
            packages=["{projname}"],
            include_package_data=True,
            python_requires=">=3.6",
            install_requires=open(
                os.path.join(here, "requirements.txt"), encoding="utf-8"
            )
            .read()
            .split("\\n"),  # Optional
            project_urls={{  # Optional
                "Bug Reports": "",
                "Source": "",
            }},
            entry_points={{
                "console_scripts": [
                    "{projname}={projname}.cli:cli"
                ]
            }},
        )
        '''
    )

    return content


def get_manifest_ini_content(projname):
    content = textwrap.dedent(
        """\
        include requirements.txt
        include dev_requirements.txt
        exclude config.json
        recursive-include {projname} *
        recursive-exclude {projname}/instance *
        recursive-exclude {projname}/static/modules *
        recursive-exclude {projname}/.tox *
        recursive-exclude __pycache__ *
        """
    )

    return content


def get_pytest_ini_content():
    content = textwrap.dedent(
        """\
        [pytest]
        env_files =
            .test.prod.env
        """
    )

    return content


def get_tox_ini_content(projname):
    content = textwrap.dedent(
        f"""\
        [tox]
        envlist =
            py39
            py38
            py37
            py36
        skip_missing_interpreters=true

        [testenv]
        changedir = {projname}
        deps =
            -rrequirements.txt
            -rdev_requirements.txt
        commands = python -m pytest {{posargs}}
        """
    )

    return content


def get_dev_req_content():
    content = textwrap.dedent(
        """\
        flake8==3.8.4
        black==20.8b1
        isort==5.6.4
        Sphinx==3.2.1
        pytest==6.1.1
        pytest-order==0.9.5
        tox==3.21.0
        pytest-cov==2.11.1
        codecov==2.1.11
        factory-boy==3.2.0
        freezegun==1.1.0
        pytest-dotenv
        """
    )

    return content


def get_gitignore_content():
    content = textwrap.dedent(
        """\
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

        # vscode
        .vscode
        workspace.code-workspace

        # modules in static since present in modules
        shopyo/static/modules/

        # ignore secrets
        config.json
        """
    )

    return content


def get_index_rst_content(projname):
    content = textwrap.dedent(
        f"""\
        Welcome to {projname} docs!
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
    )

    return content


def get_docs_rst_content(projname):
    content = textwrap.dedent(
        """\
        .. :tocdepth:: 5

        Documentation
        =============

        Sphinx is included in dev_requirements.txt

        .. code:: bash

            cd docs
            sphinx-build . _build

        to generate html pages in docs
        """
    )

    return content


def get_sphinx_conf_py(projname):
    content = textwrap.dedent(
        f"""\
        # Configuration file for the Sphinx documentation builder.
        #
        # This file only contains a selection of the most common options. For a full
        # list see the documentation:
        # https://www.sphinx-doc.org/en/master/usage/configuration.html

        # -- Path setup --------------------------------------------------------------
        #
        # If extensions (or modules to document with autodoc) are in another directory,
        # add these directories to sys.path here. If the directory is relative to the
        # documentation root, use os.path.abspath to make it absolute, like shown here.
        #
        # import os
        # import sys
        # sys.path.insert(0, os.path.abspath('.'))
        #
        # -- Project information -----------------------------------------------------

        project = "{projname}"
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
        """
    )

    return content


def get_sphinx_makefile():
    content = textwrap.dedent(
        """\
        # Minimal makefile for Sphinx documentation
        #

        # You can set these variables from the command line, and also
        # from the environment for the first two.
        SPHINXOPTS    ?=
        SPHINXBUILD   ?= sphinx-build
        SOURCEDIR     = .
        BUILDDIR      = _build

        # Put it first so that "make" without argument is like "make help".
        help:
            @$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

        .PHONY: help Makefile

        # Catch-all target: route all unknown targets to Sphinx using the new
        # "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
        %: Makefile
            @$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

        """
    )

    return content
