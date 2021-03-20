import click
import os
import sys

from flask.cli import FlaskGroup, pass_script_info
from subprocess import run, PIPE
from shopyo.api.cmd_helper import _clean
from shopyo.api.cmd_helper import _collectstatic
from shopyo.api.cmd_helper import _upload_data
from shopyo.api.cmd_helper import _create_box
from shopyo.api.cmd_helper import _create_module
from shopyo.api.database import autoload_models
from shopyo.api.constants import SEP_CHAR, SEP_NUM


def create_shopyo_app(info):
    sys.path.insert(0, os.getcwd())
    from app import create_app

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


@cli.command("startbox2")
@click.option('--verbose', "-v", is_flag=True, default=False)
@click.argument("boxname")
def create_box(boxname, verbose):
    """creates box with box_info.json.

    BOXNAME is the name of the box
    """
    _create_box(boxname, verbose=verbose)


@cli.command("createmodule")
@click.option('--verbose', "-v", is_flag=True, default=False)
@click.argument("modulename")
@click.argument("boxname", required=False, default="")
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
            "Boxes should start with box__"
        )
        sys.exit(1)

    if modulename.startswith("box__"):
        click.echo(
            f"[ ] Invalid MODULENAME '{modulename}'. "
            "MODULENAME cannot start with box__"
        )
        sys.exit(1)

    module_path = os.path.join("modules", boxname, modulename)

    if os.path.exists(module_path):
        if boxname == "":
            click.echo(
                f"[ ] Unable to create module '{modulename}'. "
                f"Path '{module_path}' exists"
            )
        else:
            click.echo(
                f"[ ] Unable to create module '{modulename}' in box"
                f"'{boxname}. Path '{module_path}' exists"
            )
        sys.exit(1)

    if boxname != "":
        _create_box(boxname, verbose=verbose)

    _create_module(modulename, base_path=module_path, verbose=verbose)


@cli.command("collectstatic2")
@click.option('--verbose', "-v", is_flag=True, default=False)
@click.argument("src", required=False, type=click.Path(), default="modules")
def collectstatic(verbose, src):
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
    print("initializing...")
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
    # proc = run(["flask", "db", "upgrade"], stdout=PIPE, stderr=PIPE)
    click.echo("")

    # collect all static folders inside modules/ and add it to global
    # static
    _collectstatic(verbose=verbose)

    # Upload models data in upload.py files inside each module
    _upload_data(verbose=verbose)

    click.echo("All Done!")


if __name__ == '__main__':
    cli()
