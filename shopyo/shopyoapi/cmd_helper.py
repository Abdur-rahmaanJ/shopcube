"""
Helper utility functions for commandline api
"""
import sys
import os
from shutil import rmtree


def tryrmcache(dir_name):
    """
    removes all __pycache__ starting from directory dir_name
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

    return is_removed


def tryrmfile(path):
    """
    tries to remove file path and output message to stdin or stderr.
    Path must point to a file

    Args:
        path (string): path of the file to remove

    Returns:
        bool: returns true upon successful removal false otherwise
    """
    try:
        os.remove(path)
        print(f"[x] file '{path}' successfully deleted")
        return True
    except OSError as e:
        print(
            "[ ] unable to delete %s: %s." % (e.filename, e.strerror),
            file=sys.stderr,
        )
        return False


def tryrmtree(path, verbose=False):
    """
    Tries to removes an entire directory tree. Path must point to
    a directory. Outputs message to stdin or stderr

    Args:
        path (string): directory path to be removed

    Returns:
        bool: returns true upon successful return false otherwise
    """
    try:
        rmtree(path)
        if verbose:
            print(f"[x] folder '{path}' successfully deleted")
        return True
    except OSError as e:
        if verbose:
            print(
                "[ ] unable to delete %s: %s." % (e.filename, e.strerror),
                file=sys.stderr,
            )
        return False
