"""
file: cli.py
description: Add your custom cli commands here
documentation: https://click.palletsprojects.com/en/7.x/

You will need to run ``python -m pip install -e .`` to load the setup.py
which contains the entry point to this file before being able to run your
custom commands

Usage ``testapp [OPTIONS] COMMAND [ARGS]...``

Example command 'welcome' has been added.
- To get your project version, run ``testapp --version``
- Run the sample command as ``testapp welcome [OPTIONS] NAME``
"""

try:
    from __init__ import __version__
except ImportError:
    __version__ = "1.0.0"
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
    click.secho(f"Hi {name}. Welcome to testapp", fg="cyan")

    if verbose:
        click.echo("See you soon")
