import click
import os
import sys

from flask.cli import FlaskGroup, pass_script_info
from flask.cli import with_appcontext
from subprocess import run, PIPE
from shopyo.api.cmd_helper import _clean
from shopyo.api.cmd_helper import _collectstatic
from shopyo.api.cmd_helper import _upload_data
from shopyo.api.file import trymkdir
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
@with_appcontext
def create_box(boxname, verbose):
    """creates box with box_info.json.

    BOXNAME is the name of the box
    """
    import json

    base_path = f"modules/box__{boxname}"
    if os.path.exists(base_path):

        if verbose:
            click.echo(
                f"[ ] unable to create. Box {base_path} already exists!",
                err=True
            )
    else:
        trymkdir(base_path, verbose=verbose)

        info_json = {
            "display_string": boxname.capitalize(),
            "box_name": boxname,
            "author": {
                "name": "",
                "website": "",
                "mail": ""
            }
        }

        with open(f"{base_path}/box_info.json", 'w', encoding='utf-8') as f:
            json.dump(info_json, f, indent=4)

        if verbose:
            click.echo("'box_info.json' content:")
            click.echo(json.dumps(info_json, indent=4, sort_keys=True))


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
