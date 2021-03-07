import click
import os
from flask.cli import with_appcontext
from shopyo.api.cmd_helper import tryrmcache
from shopyo.api.cmd_helper import tryrmfile
from shopyo.api.cmd_helper import tryrmtree
from shopyo.api.file import trymkdir
from flask.cli import FlaskGroup
import sys

sys.path.append(os.getcwd())

from app import create_app
from init import db


SEP_CHAR = "#"
SEP_NUM = 23


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    """CLI for shopyo"""
    pass


@cli.command("startbox2")
@click.option('--verbose', "-v", is_flag=True, default=False)
@click.argument("boxname")
@with_appcontext
def create_box2(boxname, verbose):
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


@cli.command("clean2")
@click.option('--verbose', "-v", is_flag=True, default=False)
@with_appcontext
def clean2(verbose):
    """tries to removes __pycache__, migrations/, shopyo.db files and drops all
    tables
    """

    click.echo(SEP_CHAR * SEP_NUM + "\n")
    click.echo("Cleaning...")

    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")

    if verbose:
        click.echo("[x] all tables dropped")

    tryrmcache(os.getcwd(), verbose=verbose)
    tryrmfile(os.path.join(os.getcwd(), "shopyo.db"), verbose=verbose)
    tryrmtree(os.path.join(os.getcwd(), "migrations"), verbose=verbose)
