import importlib.resources as resources
import os
import shutil

import click
from flask import current_app
from flask.cli import with_appcontext


def _theme_src(name):
    """Return (Traversable, Path-context-manager) for a theme in this package."""
    anchor = resources.files("shopyo_ecommerce")
    return anchor / "templates" / name


def _css_src():
    """Return Traversable for the package's styles.css."""
    return resources.files("shopyo_ecommerce") / "static" / "css" / "styles.css"


@click.group("shopyo-ecommerce")
def cli():
    """Shopyo Ecommerce management commands."""


@cli.command("copy")
@click.argument("kind")
@click.argument("name")
@with_appcontext
def copy_theme(kind, name):
    """Copy a theme from the package to the project's static/themes/."""

    src = _theme_src(name)
    if not src.is_dir():
        click.echo(f"Error: theme '{name}' not found in package templates/")
        raise SystemExit(1)

    base_dir = current_app.config.get("BASE_DIR", os.getcwd())
    dst = os.path.join(base_dir, "static", "themes", kind, name)

    if os.path.exists(dst):
        click.echo(f"Error: {dst} already exists. Use 'update' to overwrite.")
        raise SystemExit(1)

    with resources.as_file(src) as src_path:
        shutil.copytree(src_path, dst, dirs_exist_ok=False)

    css = _css_src()
    if css.is_file():
        with resources.as_file(css) as css_path:
            shutil.copy2(css_path, os.path.join(dst, "styles.css"))

    click.echo(f"Copied theme '{name}' to {dst}")


@cli.command("update")
@click.argument("kind")
@click.argument("name")
@with_appcontext
def update_theme(kind, name):
    """Erase and re-copy a theme to the project's static/themes/."""

    src = _theme_src(name)
    if not src.is_dir():
        click.echo(f"Error: theme '{name}' not found in package templates/")
        raise SystemExit(1)

    base_dir = current_app.config.get("BASE_DIR", os.getcwd())
    dst = os.path.join(base_dir, "static", "themes", kind, name)

    if os.path.exists(dst):
        shutil.rmtree(dst)
        click.echo(f"Removed existing {dst}")

    with resources.as_file(src) as src_path:
        shutil.copytree(src_path, dst, dirs_exist_ok=False)

    css = _css_src()
    if css.is_file():
        with resources.as_file(css) as css_path:
            shutil.copy2(css_path, os.path.join(dst, "styles.css"))

    click.echo(f"Updated theme '{name}' at {dst}")
