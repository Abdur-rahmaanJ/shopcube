import os
import shutil
import uuid
import click

# from werkzeug.utils import secure_filename


def tryrmcache(dir_name, verbose=False):
    """
    removes all __pycache__ starting from directory dir_name
    all the way to leaf directory

    Args:
        dir_name(string) : path from where to start removing pycache
    """
    # directory_list = list()
    is_removed = False
    for root, dirs, files in os.walk(dir_name, topdown=False):
        for name in dirs:
            # directory_list.append(os.path.join(root, name))
            if name == "__pycache__":
                shutil.rmtree(os.path.join(root, name))
                is_removed = True

    if verbose:
        if is_removed:
            click.echo("[x] __pycache__ successfully deleted")
        else:
            click.echo("[ ] __pycache__ doesn't exist", err=True)

    return is_removed


def tryrmfile(path, verbose=False):
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
        if verbose:
            click.echo(f"[x] file '{path}' successfully deleted")
        return True
    except OSError as e:
        if verbose:
            click.echo(
                f"[ ] unable to delete {e.filename}: {e.strerror}",
                err=True,
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
        shutil.rmtree(path)
        if verbose:
            click.echo(f"[x] folder '{path}' successfully deleted")
        return True
    except OSError as e:
        if verbose:
            click.echo(
                f"[ ] unable to delete {e.filename}: {e.strerror}",
                err=True,
            )
        return False


def trycopytree(source, dest, verbose=False):
    """
    Recursive copy of folder

    Parameters
    ----------
    source: str
        source folder path
    dest: str
        destination folder path

    Returns
    -------
    None
    """
    try:
        shutil.copytree(source, dest)
        if verbose:
            print("[x] done copying {} to {}".format(source, dest))
    except Exception as e:
        print(f"[ ] unable to copy directory tree. {e}")


def trycopy(source, dest, verbose=False):
    """
    Non-ecursive copy of folder

    Parameters
    ----------
    source: str
        source folder path
    dest: str
        destination folder path

    Returns
    -------
    None
    """
    try:
        shutil.copy(source, dest)
        if verbose:
            print("[x] done copying {} to {}".format(source, dest))
    except Exception as e:
        print(f"[ ] unable to copy file. {e}")


def trymkdir(path, verbose=False):
    """
    Creates dir at destination

    Parameters
    ----------
    path: str
        path with folder already in

    Returns
    -------
    None
    """
    try:
        os.mkdir(path)
        if verbose:
            print(f"[x] Successfully created dir {path}")
    except Exception as e:
        print(f"[ ] unable to make directory. {e}")


def trymkfile(path, content, verbose=False):
    """
    Creates file

    Parameters
    ----------
    path: str
        path to create file with filename included
    content: str
        file content

    Returns
    -------
    None
    """
    try:
        with open(path, "w+") as f:
            f.write(content)
        if verbose:
            click.echo(f"[x] file {path} created with content: ")
            click.echo(content)
    except Exception as e:
        click.echo(f"[ ] {e}")


def absdiroffile(filepath):
    """
    Gives absolute directory of file, normally expects __file__ as
    param

    Parameters
    ----------
    filepath: str
        path of file

    Returns
    -------
    str
        Absolute dir path of file
    """
    return os.path.dirname(os.path.abspath(filepath))


def get_folders(path):
    dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    return dirs


def unique_filename(fname):
    prepended = str(uuid.uuid4()).replace("-", "_")[:10]
    return "{}_{}".format(prepended, fname)


def delete_file(path):
    os.remove(path)


# def unique_sec_filename(filename):
#     return unique_filename(secure_filename(filename))
