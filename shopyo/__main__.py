import sys

from . import shopyoapi

def main(args):
    if args[1] == "new" and len(args) == 4:
        shopyoapi.cmd.new_project(args[2], args[3])


if __name__ == "__main__":
    main(sys.argv)