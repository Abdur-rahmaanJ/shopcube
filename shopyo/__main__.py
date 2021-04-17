import subprocess
import sys
import re
from pathlib import Path

from .api.info import printinfo

dirpath = Path(__file__).parent.absolute()
dirpathparent = Path(__file__).parent.parent.absolute()


def is_venv():
    return hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )


def is_valid_name(name):
    notallowedpattern = r'[_\.]+'
    allowedpattern = r'^[\w+\.]+$'
    isallowed = re.match(allowedpattern, name)
    isnotallowed = re.match(notallowedpattern, name)

    if not isnotallowed and isallowed:
        return True
    else:
        return False


def main():
    args = sys.argv
    if len(args) == 1:
        printinfo()
        print("No arguments supplied")
    else:
        if not is_venv():
            print("Please use Shopyo in a virtual environment for this command")
            sys.exit()
        torun = [sys.executable, "manage.py"] + args[1:]
        subprocess.run(torun)


if __name__ == "__main__":
    main()
