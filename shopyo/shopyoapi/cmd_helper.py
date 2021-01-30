"""
Helper utility functions for commandline api
"""
import sys
import os
from shutil import rmtree


def remove_pycache(dir_name):
    """removes all __pycache__ starting from directory dir_name
       all the way to leaf directory

    Args:
        dir_name(string) : path from where to start removing pycache
    """
    directory_list = list()
    is_removed = False
    for root, dirs, files in os.walk(dir_name, topdown=False):
        for name in dirs:
            directory_list.append(os.path.join(root, name))
            if name == "__pycache__":
                rmtree(os.path.join(root, name))
                is_removed = True

    if is_removed:
        print("[x] __pycache__ successfully deleted")
    else:
        print("[ ] __pycache__ doesn't exist", file=sys.stderr)


def remove_file(path, filename):
    try:
        os.remove(os.path.join(path, filename))
        print(f"[x] file '{filename}' successfully deleted")
    except OSError as e:
        print(
            "[ ] unable to delete %s: %s." % (e.filename, e.strerror),
            file=sys.stderr
        )


def remove_directory(path, directory):
    try:
        rmtree(os.path.join(path, directory))
        print(f"[x] folder '{directory}' successfully deleted")
    except OSError as e:
        print(
            "[ ] unable to delete %s: %s." % (e.filename, e.strerror),
            file=sys.stderr
        )
