"""
Helper utility functions for commandline api
"""
import os
import sys
import click
import re
import importlib
from flask import current_app

from shopyo.api.file import get_folders
from shopyo.api.file import trycopytree
from shopyo.api.file import tryrmcache
from shopyo.api.file import tryrmfile
from shopyo.api.file import tryrmtree
from shopyo.api.constants import SEP_CHAR, SEP_NUM


def _clean(verbose=False):
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
    db = current_app.extensions['sqlalchemy'].db
    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")

    if verbose:
        click.echo("[x] all tables dropped")

    tryrmcache(os.getcwd(), verbose=verbose)
    tryrmfile(os.path.join(os.getcwd(), "shopyo.db"), verbose=verbose)
    tryrmtree(os.path.join(os.getcwd(), "migrations"), verbose=verbose)

    click.echo("")


def _collectstatic(target_module="modules", verbose=False):

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

    root_path = os.getcwd()
    static_path = os.path.join(root_path, "static")

    # if target_module path does not start with 'modules\' add it to as a
    # prefix to the target_module path
    if target_module != "modules":

        # normalize the target_module path to be same as that of OS
        target_module = re.split(r"[/|\\]+", target_module)
        target_module_start = target_module[0]
        target_module = os.path.join(*target_module)

        # add the modules folder to start of target_module incase it is not
        # already present in the path
        if target_module_start != "modules":
            target_module = (
                os.path.join("modules", target_module)
            )

    # get the full path for modules (the src). Defaults to ./modules
    modules_path = os.path.join(root_path, target_module)

    # get the full path of static folder to copy to (the dest).
    # always ./static/modules
    modules_path_in_static = os.path.join(static_path, "modules")

    # terminate if modules_path (i.e. src to copy static from) does not exist
    if not os.path.exists(modules_path):
        click.echo(f"[ ] path: {modules_path} does not exist")
        sys.exit(1)

    # clear ./static/modules before coping to it
    tryrmtree(modules_path_in_static, verbose=verbose)

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

                # copy from ./modules/<box__name>/<submodule> to
                # ./static/modules
                trycopytree(
                    module_static_folder,
                    module_in_static_dir,
                    verbose=verbose
                )
        else:
            path_split = ""

            # split the target module if default target_module path name is
            # not used
            if target_module != "modules":
                path_split = re.split(r"[/|\\]", target_module, maxsplit=1)
                path_split = path_split[1]

            if folder.lower() == "static":
                module_static_folder = os.path.join(
                    modules_path, folder
                )
                module_name = path_split
            else:
                module_static_folder = os.path.join(
                    modules_path, folder, "static"
                )
                module_name = os.path.join(path_split, folder)

            if not os.path.exists(module_static_folder):
                continue
            module_in_static_dir = os.path.join(
                modules_path_in_static, module_name
            )
            tryrmtree(module_in_static_dir, verbose=verbose)
            trycopytree(
                module_static_folder,
                module_in_static_dir,
                verbose=verbose
            )

    click.echo("")


def _upload_data(verbose=False):
    click.echo("Uploading initial data to db...")
    click.echo(SEP_CHAR * SEP_NUM)

    root_path = os.getcwd()

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
