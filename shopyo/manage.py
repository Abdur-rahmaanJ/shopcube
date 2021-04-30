"""
file: manage.py
description: allows using cli commands similar to Django.
Example all ``shopyo <cmd> [OPTIONS] [ARGS]...`` commands can also be run as
``python manage.py <cmd> [OPTIONS] [ARGS]...``
"""

from shopyo.api.cli import shopyo_cli

if __name__ == '__main__':
    shopyo_cli()
