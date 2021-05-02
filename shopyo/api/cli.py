import click
import os
import sys
from pathlib import Path
from shutil import copytree, ignore_patterns

from flask.cli import FlaskGroup
from flask.cli import pass_script_info
from subprocess import run
from subprocess import PIPE
from shopyo.api.cmd_helper import _clean
from shopyo.api.cmd_helper import _collectstatic
from shopyo.api.cmd_helper import _upload_data
from shopyo.api.cmd_helper import _create_box
from shopyo.api.cmd_helper import _create_module
from shopyo.api.database import autoload_models
from shopyo.api.constants import SEP_CHAR, SEP_NUM
from shopyo.api.validators import get_module_path_if_exists
from shopyo.api.validators import is_alpha_num_underscore
from shopyo.api.info import printinfo


def _create_shopyo_app(info):
    sys.path.insert(0, os.getcwd())

    try:
        from app import create_app
    except Exception:
        return None

    config_name = info.data.get('config') or "development"

    return create_app(config_name=config_name)


@click.group(cls=FlaskGroup, create_app=_create_shopyo_app)
@click.option(
    '--config', default="development", help="Flask app configuration type"
)
@pass_script_info
def cli(info, **parmams):
    """CLI for shopyo"""
    printinfo()
    config_name = parmams["config"]
    info.data['config'] = config_name
    # os.environ["FLASK_APP"] = f"app:create_app('{config_name}')"
    # os.environ["FLASK_ENV"] = config_name


@cli.command("startbox", with_appcontext=False)
@click.argument("boxname")
@click.option('--verbose', "-v", is_flag=True, default=False)
def create_box(boxname, verbose):
    """creates ``box`` with ``box_info.json``.

    ``BOXNAME`` is the name of the ``box`` which holds modules
    """
    path = os.path.join("modules", boxname)

    if os.path.exists(os.path.join("modules", boxname)):
        click.echo(
            f"[ ] unable to create. Box {path} already exists!",
            err=True
        )
        sys.exit(1)

    _create_box(boxname, verbose=verbose)


@cli.command("createmodule", with_appcontext=False)
@click.argument("modulename")
@click.argument("boxname", required=False, default="")
@click.option('--verbose', "-v", is_flag=True, default=False)
def create_module(modulename, boxname, verbose):
    """
    create a module ``MODULENAME`` inside ``modules/``. If ``BOXNAME`` is
    provided, creates the module inside ``modules/BOXNAME.``

    \b
    If box ``BOXNAME`` does not exist, it is created.
    If ``MODULENAME`` already exists, an error is thrown and command is
    terminated.

    structure of modules created is as follows:

        <add module/box directory tree here>

    BOXNAME the name of box to create the MODULENAME in. Must start with
    ``box__``, otherwise error is thrown

    MODULENAME the name of module to be created. Must not start with
    ``box__``, otherwise error is thrown

    """
    if boxname != "" and not boxname.startswith("box__"):
        click.echo(
            f"[ ] Invalid BOXNAME '{boxname}'. "
            "BOXNAME should start with 'box__' prefix"
        )
        sys.exit(1)

    if modulename.startswith("box_"):
        click.echo(
            f"[ ] Invalid MODULENAME '{modulename}'. "
            "MODULENAME cannot start with box_ prefix"
        )
        sys.exit(1)

    if not is_alpha_num_underscore(modulename):
        click.echo(
            "[ ] Error: MODULENAME is not valid, please use alphanumeric "
            "and underscore only"
        )
        sys.exit(1)

    if boxname != "" and not is_alpha_num_underscore(boxname):
        click.echo(
            "[ ] Error: BOXNAME is not valid, please use alphanumeric "
            "and underscore only"
        )
        sys.exit(1)

    module_path = get_module_path_if_exists(modulename)

    if module_path is not None:
        click.echo(
            f"[ ] Unable to create module '{modulename}'. "
            f"MODULENAME already exists inside modules/ at {module_path}"
        )
        sys.exit(1)

    if boxname != "":
        box_path = get_module_path_if_exists(boxname)
        if box_path is None:
            _create_box(boxname, verbose=verbose)

    module_path = os.path.join("modules", boxname, modulename)
    _create_module(modulename, base_path=module_path, verbose=verbose)


@cli.command("collectstatic", with_appcontext=False)
@click.argument("src", required=False, type=click.Path(), default="modules")
@click.option('--verbose', "-v", is_flag=True, default=False)
def collectstatic(src, verbose):
    """Copies ``static/`` in ``modules/`` or ``modules/SRC`` into
    ``/static/modules/``

    ``SRC`` is the module path relative to ``modules/`` where ``static/``
    exists.

    Ex usage for::

        \b
        .
        └── modules/
            └── box__default/
                ├── auth/
                │   └── static
                └── appadmin/
                    └── static

    To collect static in only one module, run either of two commands::

        $ shopyo collectstatic box__default/auth

        $ shopyo collectstatic modules/box__default/auth

    To collect static in all modules inside a box, run either of two commands
    below::

        $ shopyo collectstatic box__default

        $ shopyo collectstatic modules/box__default

    To collect static in all modules run either of the two commands below::

        $ shopyo collectstatic

        $ shopyo collectstatic modules
    """
    _collectstatic(target_module=src, verbose=verbose)


@cli.command("clean")
@click.option('--verbose', "-v", is_flag=True, default=False)
def clean(verbose):
    """removes ``__pycache__``, ``migrations/``, ``shopyo.db`` files and drops
    ``db`` if present
    """
    _clean(verbose=verbose)


@cli.command("initialise")
@click.option('--verbose', "-v", is_flag=True, default=False)
def initialise(verbose):
    """
    Creates ``db``, ``migration/``, adds default users, add settings
    """
    click.echo("initializing...")

    # drop db, remove mirgration/ and shopyo.db
    _clean(verbose=verbose)

    # load all models available inside modules
    autoload_models(verbose=verbose)

    # add a migrations folder to your application.
    click.echo("Creating db...")
    click.echo(SEP_CHAR * SEP_NUM)
    if verbose:
        run(["flask", "db", "init"])
    else:
        run(["flask", "db", "init"], stdout=PIPE, stderr=PIPE)
    click.echo("")

    # generate an initial migration i.e autodetect changes in the
    # tables (table autodetection is limited. See
    # https://flask-migrate.readthedocs.io/en/latest/ for more details)
    click.echo("Migrating db...")
    click.echo(SEP_CHAR * SEP_NUM)
    if verbose:
        run(["flask", "db", "migrate"])
    else:
        run(["flask", "db", "migrate"], stdout=PIPE, stderr=PIPE)
    click.echo("")

    click.echo("Upgrading db...")
    click.echo(SEP_CHAR * SEP_NUM)
    if verbose:
        run(["flask", "db", "upgrade"])
    else:
        run(["flask", "db", "upgrade"], stdout=PIPE, stderr=PIPE)
    click.echo("")

    # collect all static folders inside modules/ and add it to global
    # static/
    _collectstatic(verbose=verbose)

    # Upload models data in upload.py files inside each module
    _upload_data(verbose=verbose)

    click.echo("All Done!")


@cli.command("new", with_appcontext=False)
@click.argument("projname", required=False, default="")
@click.option('--verbose', "-v", is_flag=True, default=False)
def new(projname, verbose):
    """Creates a new shopyo project.

    By default it will create the project(folder) of same name as the parent
    folder. If ``PROJNAME`` is provided, it will create ``PROJNAME/PROJNAME``
    under parent folder

    ``PROJNAME`` is the name of the project that you want to create.
    """

    from shopyo.__init__ import __version__
    from shopyo.api.file import trymkfile
    from shopyo.api.file import trymkdir
    from shopyo.api.file import trycopy
    from shopyo.api.cli_content import get_tox_ini_content
    from shopyo.api.cli_content import get_dev_req_content
    from shopyo.api.cli_content import get_gitignore_content
    from shopyo.api.cli_content import get_sphinx_conf_py
    from shopyo.api.cli_content import get_sphinx_makefile
    from shopyo.api.cli_content import get_index_rst_content
    from shopyo.api.cli_content import get_docs_rst_content
    from shopyo.api.cli_content import get_pytest_ini_content
    from shopyo.api.cli_content import get_manifest_ini_content
    from shopyo.api.cli_content import get_init_content
    from shopyo.api.cli_content import get_cli_content
    from shopyo.api.cli_content import get_setup_py_content

    here = os.getcwd()

    if projname == "":

        projname = os.path.basename(here)

        # the base/root project folder where files such as README, docs,
        # .gitignore etc. will be stored will be same as current working
        # directory i.e ./
        root_proj_path = here

        # the current project path in which we will create the project
        project_path = os.path.join(here, projname)

        if os.path.exists(project_path):
            click.echo(
                f"[ ] Error: Unable to create new project. Path {project_path}"
                " exits"
            )
            sys.exit(1)

    else:
        if not is_alpha_num_underscore(projname):
            click.echo(
                "[ ] Error: PROJNAME is not valid, please use alphanumeric "
                "and underscore only"
            )
            sys.exit(1)

        # the base/root project folder where files such as README, docs,
        # .gitignore etc. will be stored will be ./projname
        root_proj_path = os.path.join(here, projname)

        # the current project path in which we will create the project
        project_path = os.path.join(here, projname, projname)

        if os.path.exists(root_proj_path):
            click.echo(
                "[ ] Error: Unable to create new project. Path "
                f"{root_proj_path} exits"
            )
            sys.exit(1)

    click.echo(f"creating project {projname}...")
    click.echo(SEP_CHAR * SEP_NUM)

    # the shopyo src path that the new project will mimic
    src_shopyo_shopyo = Path(__file__).parent.parent.absolute()

    # copy the shopyo/shopyo content to the new project
    copytree(
        src_shopyo_shopyo, project_path,
        ignore=ignore_patterns(
            "__main__.py",
            "api",
            ".tox",
            ".coverage",
            "*.db",
            "coverage.xml",
            "setup.cfg",
            "instance",
            "migrations",
            "__pycache__",
            "*.pyc",
            "sphinx_source",
            "config.json",
            "pyproject.toml"
        )
    )

    # create requirements.txt in root
    trymkfile(
        os.path.join(root_proj_path, "requirements.txt"),
        f"shopyo=={__version__}\n",
        verbose=verbose
    )

    # copy the dev_requirement.txt in root
    trymkfile(
        os.path.join(root_proj_path, "dev_requirements.txt"),
        get_dev_req_content(),
        verbose=verbose
    )

    # copy the tox.ini in root
    trymkfile(
        os.path.join(root_proj_path, "tox.ini"),
        get_tox_ini_content(projname),
        verbose=verbose
    )

    # create MANIFEST.in needed for tox
    trymkfile(
        os.path.join(root_proj_path, "MANIFEST.in"),
        get_manifest_ini_content(projname),
        verbose=verbose
    )

    # create README.md in root
    trymkfile(
        os.path.join(root_proj_path, "README.md"),
        f"# Welcome to {projname}",
        verbose=verbose
    )

    # create .gitignore in root
    trymkfile(
        os.path.join(root_proj_path, ".gitignore"),
        get_gitignore_content(),
        verbose=verbose
    )

    # create pytest.ini
    trymkfile(
        os.path.join(root_proj_path, "pytest.ini"),
        get_pytest_ini_content(),
        verbose=verbose
    )

    # create setup.py
    trymkfile(
        os.path.join(root_proj_path, "setup.py"),
        get_setup_py_content(projname),
        verbose=verbose
    )

    # override the __init__.py file
    trymkfile(
        os.path.join(project_path, "__init__.py"),
        get_init_content(),
        verbose=verbose
    )

    # add cli.py for users to add their own cli
    trymkfile(
        os.path.join(project_path, "cli.py"),
        get_cli_content(projname),
        verbose=verbose
    )

    sphinx_src = os.path.join(root_proj_path, "docs")

    # create sphinx docs in project root
    trymkdir(sphinx_src, verbose=verbose)
    # create sphinx conf.py inside docs
    trymkfile(
        os.path.join(sphinx_src, "conf.py"),
        get_sphinx_conf_py(projname),
        verbose=verbose
    )
    # create _static sphinx folder
    trymkdir(os.path.join(sphinx_src, "_static"), verbose=verbose)
    trymkfile(
        os.path.join(sphinx_src, "_static", "custom.css"), "", verbose=verbose
    )
    # create sphinx Makefile inside docs
    trymkfile(
        os.path.join(sphinx_src, "Makefile"),
        get_sphinx_makefile(),
        verbose=verbose
    )
    # create index page
    trymkfile(
        os.path.join(sphinx_src, "index.rst"),
        get_index_rst_content(projname),
        verbose=verbose
    )
    # create docs page
    trymkfile(
        os.path.join(sphinx_src, "docs.rst"),
        get_docs_rst_content(projname),
        verbose=verbose
    )

    click.echo(f"[x] Project {projname} created successfully!\n")


def shopyo_cli():
    arguments = sys.argv[1:]
    if len(arguments) > 0:
        if arguments[0] in ['rundebug', 'runserver']:
            if arguments[0] == 'rundebug':
                printinfo()
                from app import app
                app.run(debug=True)
            elif arguments[0] == 'runserver':
                printinfo()
                from app import app
                app.run(debug=False)
    else:
        cli()


if __name__ == '__main__':
    shopyo_cli()
