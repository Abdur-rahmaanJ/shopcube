import importlib
import os
import click

from shopyo.api.constants import SEP_CHAR, SEP_NUM


def autoload_models(verbose=False):
    """
    Auto imports models from modules/ in desired file. Used so that
    flask_migrate does not miss models when migrating

    Returns
    -------
    None
    """
    click.echo("Auto importing models...")
    click.echo(SEP_CHAR * SEP_NUM)

    for folder in os.listdir("modules"):
        if folder.startswith("__"):
            continue
        elif folder.startswith("box__"):
            for sub_folder in os.listdir(os.path.join("modules", folder)):
                if sub_folder.startswith("__"):  # ignore __pycache__
                    continue
                elif sub_folder.endswith(".json"):  # box_info.json
                    continue
                try:
                    to_load_submodel = "modules.{}.{}.models".format(
                        folder, sub_folder
                    )
                    importlib.import_module(to_load_submodel)
                    if verbose:
                        click.echo(f"[x] imported {to_load_submodel}")
                except Exception as e:
                    if verbose:
                        click.echo(f"[ ] {e}")
        else:
            try:
                to_load = "modules.{}.models".format(folder)
                importlib.import_module(to_load)
                if verbose:
                    click.echo(f"[x] imported {to_load}")
            except Exception as e:
                if verbose:
                    click.echo(f"[ ] {e}")

    click.echo("")