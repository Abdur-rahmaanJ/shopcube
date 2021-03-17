"""
Helper utility functions for commandline api
"""
import os
import sys
import click
import importlib

from init import root_path
from init import static_path
from init import modules_path
from shopyo.api.file import get_folders
from shopyo.api.file import trycopytree
from shopyo.api.file import tryrmcache
from shopyo.api.file import tryrmfile
from shopyo.api.file import tryrmtree
from shopyo.api.constants import SEP_CHAR, SEP_NUM


def _clean(db, verbose=False):
    """
    Deletes shopyo.db and migrations/ if present in current working directory.
    Deletes all __pycache__ folders starting from current working directory
    all the way to leaf directory.

    Parameters
    ----------
        - verbose: flag to indicate whether to print to result of clean to
            stdout or not.
        - db: db to be cleaned

    Returns
    -------
    None
        ...

    """

    click.echo("Cleaning...")
    click.echo(SEP_CHAR * SEP_NUM)

    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")

    if verbose:
        click.echo("[x] all tables dropped")

    tryrmcache(os.getcwd(), verbose=verbose)
    tryrmfile(os.path.join(os.getcwd(), "shopyo.db"), verbose=verbose)
    tryrmtree(os.path.join(os.getcwd(), "migrations"), verbose=verbose)

    click.echo("")


def _collectstatic(target_module=None, verbose=False):

    """
    Copies ``module/static`` into ``/static/modules/module``.
    In static it becomes like

    ::

       static/
            modules/
                box_something/
                    modulename
                modulename2


    Parameters
    ----------
    target_module: str
        name of module, in alphanumeric-underscore,
        supports ``module`` or ``box__name/module``

    Returns
    -------
    None

    """
    click.echo("Collecting static...")
    click.echo(SEP_CHAR * SEP_NUM)
    modules_path_in_static = os.path.join(static_path, "modules")

    if target_module is None:
        # clear modules dir if exists.
        tryrmtree(modules_path_in_static)
        # look for static folders in all project
        for folder in get_folders(modules_path):
            if folder.startswith("box__"):
                box_path = os.path.join(modules_path, folder)
                for subfolder in get_folders(box_path):
                    module_name = subfolder
                    module_static_folder = os.path.join(
                        box_path, subfolder, "static"
                    )
                    if not os.path.exists(module_static_folder):
                        continue
                    module_in_static_dir = os.path.join(
                        modules_path_in_static, folder, module_name
                    )
                    trycopytree(module_static_folder, module_in_static_dir)
            else:
                module_name = folder
                module_static_folder = os.path.join(
                    modules_path, folder, "static"
                )
                if not os.path.exists(module_static_folder):
                    continue
                module_in_static_dir = os.path.join(
                    modules_path_in_static, module_name
                )
                trycopytree(module_static_folder, module_in_static_dir)
    else:
        # copy only module's static folder
        module_static_folder = os.path.join(
            modules_path, target_module, "static"
        )
        if os.path.exists(module_static_folder):
            if target_module.startswith("box__"):
                if "/" in target_module:
                    module_name = target_module.split("/")[1]
                else:
                    print("Could not understand module name")
                    sys.exit()
            else:
                module_name = target_module
            module_in_static_dir = os.path.join(
                modules_path_in_static, module_name
            )
            tryrmtree(module_in_static_dir)
            trycopytree(module_static_folder, module_in_static_dir)
        else:
            print("Module does not exist")

    click.echo("")


def _upload_data(verbose=False):
    click.echo("Uploading initial data to db...")
    click.echo(SEP_CHAR * SEP_NUM)

    for folder in os.listdir(os.path.join(root_path, "modules")):
        if folder.startswith("__"):  # ignore __pycache__
            continue
        if folder.startswith("box__"):
            # boxes
            for sub_folder in os.listdir(
                os.path.join(root_path, "modules", folder)
            ):
                if sub_folder.startswith("__"):  # ignore __pycache__
                    continue
                elif sub_folder.endswith(".json"):  # box_info.json
                    continue

                try:
                    upload = importlib.import_module(
                        f"modules.{folder}.{sub_folder}.upload"
                    )
                    upload.upload(verbose=verbose)
                except ImportError as e:
                    if verbose:
                        click.echo(f"[ ] {e}")
        else:
            # apps
            try:
                upload = importlib.import_module(
                    f"modules.{folder}.upload"
                )
                upload.upload(verbose=verbose)
            except ImportError as e:
                if verbose:
                    click.echo(f"[ ] {e}")

    click.echo("")
