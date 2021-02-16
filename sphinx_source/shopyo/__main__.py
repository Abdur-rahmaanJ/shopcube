import os
import subprocess
import sys
from pathlib import Path

# from .shopyoapi.file import trycopy
from .shopyoapi.file import trycopytree
from .shopyoapi.file import trymkdir
from .shopyoapi.info import printinfo

dirpath = Path(__file__).parent.absolute()
dirpathparent = Path(__file__).parent.parent.absolute()


def is_venv():
    return hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )


def new_project(path, newfoldername):
    newfoldername = newfoldername.strip("/").strip("\\")
    print("creating new project {}".format(newfoldername))

    base_path = path + "/" + newfoldername
    trymkdir(base_path)
    print("created dir {} in {}".format(newfoldername, path))

    trycopytree(os.path.join(dirpathparent, "shopyo"), base_path + "/shopyo")


def main():
    if not is_venv():
        print("Please use Shopyo in a virtual environment")
        sys.exit()
    args = sys.argv
    if len(args) == 1:
        printinfo()
        print("No arguments supplied")
    if args[1] == "new" and len(args) == 4:
        printinfo()
        new_project(args[2], args[3])
    else:
        torun = [sys.executable, "manage.py"] + args[1:]
        subprocess.run(torun, stdout=subprocess.PIPE)


if __name__ == "__main__":
    main()
