"""
Helper utility functions for commandline api
"""
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
        print("[ ] __pycache__ doesn't exist")


def remove_file_or_dir(name):
    """removes the file or directory

    Args:
        name (string): file path or directory path to be removed
    """
    if os.path.exists(name) and os.path.isdir(name):
        rmtree(name)
        print(f"[x] folder '{name}' successfully deleted")
    elif os.path.exists(name) and not os.path.isdir(name):
        os.remove(name)
        print(f"[x] file '{name}' successfully deleted")
    else:
        print(f"[ ] file/folder '{name}' doesn't exist")
