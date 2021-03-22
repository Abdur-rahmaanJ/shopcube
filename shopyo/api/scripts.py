import click
import os
import sys
from pathlib import Path
from shutil import copytree, ignore_patterns

from flask.cli import FlaskGroup, pass_script_info
from subprocess import run, PIPE
from shopyo.api.cmd_helper import _clean
from shopyo.api.cmd_helper import _collectstatic
from shopyo.api.cmd_helper import _upload_data
from shopyo.api.cmd_helper import _create_box
from shopyo.api.cmd_helper import _create_module
from shopyo.api.database import autoload_models
from shopyo.api.constants import SEP_CHAR, SEP_NUM
from shopyo.api.validators import get_module_path_if_exists
from shopyo.api.validators import is_alpha_num_underscore


def create_shopyo_app(info):
    sys.path.insert(0, os.getcwd())
    try:
        from app import create_app
    except Exception:
        return None

    config_name = info.data.get('config')

    if config_name is None:
        return None

    return create_app(config_name=config_name)


@click.group(cls=FlaskGroup, create_app=create_shopyo_app)
@click.option('--config', default="development")
@pass_script_info
def cli(info, **parmams):
    """CLI for shopyo"""
    info.data['config'] = parmams["config"]


@cli.command("startbox2", with_appcontext=False)
@click.argument("boxname")
@click.option('--verbose', "-v", is_flag=True, default=False)
def create_box(boxname, verbose):
    """creates box with box_info.json.

    BOXNAME is the name of the box which holds modules
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
    create a module MODULENAME inside modules/. If BOXNAME is provided,
    creates the module inside modules/BOXNAME.

    \b
    If box BOXNAME does not exist, it is created.
    If MODULENAME already exists (either inside BOXNAME for the case BOXNAME is
    provided or inside modules/ when BOXNAME is not provided), an error
    is thrown and command is terminated.

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


@cli.command("collectstatic2", with_appcontext=False)
@click.argument("src", required=False, type=click.Path(), default="modules")
@click.option('--verbose', "-v", is_flag=True, default=False)
def collectstatic(src, verbose):
    """Copies ``static/`` in ``modules/`` or modules/SRC into
    ``/static/modules/``

    SRC is the module path relative to ``modules/`` where static/ exists.

    \b
    Ex usage for
        modules\\
            box_default\\
                auth\\
                    static\\
                appadmin\\
                    static\\

    To collect static in only one module, run either of two commands

    \b
    ``$ shopyo collectstatic2 box__default/auth``
    ``$ shopyo collectstatic2 modules/box__default/auth``

    To collect static in all modules inside a box, run either of two commands
    below

    \b
    ``$ shopyo collectstatic2 box__default``
    ``$ shopyo collectstatic2 modules/box__default``

    To collect static in all modules run either of the two commands below

    \b
    ``$ shopyo collectstatic2``
    ``$ shopyo collectstatic2 modules``
    """
    _collectstatic(target_module=src, verbose=verbose)


@cli.command("clean2")
@click.option('--verbose', "-v", is_flag=True, default=False)
def clean(verbose):
    """remove __pycache__, migrations/, shopyo.db files and drops db
    if present
    """
    _clean(verbose=verbose)


@cli.command("initialise2")
@click.option('--verbose', "-v", is_flag=True, default=False)
def initialise(verbose):
    """
    Create db, migrate, adds default users, add settings
    """
    click.echo("initializing...")

    # drop db, remove mirgration/ and shopyo.db
    _clean(verbose=verbose)

    # load all models available inside modules
    autoload_models()

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


@cli.command("new2", with_appcontext=False)
@click.argument("projname")
@click.option('--verbose', "-v", is_flag=True, default=False)
def new(projname, verbose):

    if not is_alpha_num_underscore(projname):
        click.echo(
            "[ ] Error: PROJNAME is not valid, please use alphanumeric "
            "and underscore only"
        )
        sys.exit(1)

    # get the shopyo src path that the new project will mimic
    src_shopyo_shopyo = Path(__file__).parent.parent.absolute()

    # the current project path in which we will create the project
    project_path = os.path.join(".", projname, projname)

    # copy the shopyo/shopyo content to a new shopyo project
    copytree(
        src_shopyo_shopyo, project_path,
        ignore=ignore_patterns(
            "__main__.py", "api", ".tox", ".coverage", "*.db",
            "coverage.xml", "setup.cfg", "instance", "migrations",
            "__pycache__", "*.pyc"

        )
    )

    # create requirements.txt in root

    # copy the dev_requirement.txt in root

    # copy the tox.ini in root

    # create README in root

    # create .gitignore in root

    # create docs in root

    # create sphinx_source in ./PROJNAME/PROJNAME

    # create sphinx_source in ./PROJNAME/PROJNAME


if __name__ == '__main__':
    cli()
