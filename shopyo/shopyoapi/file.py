import shutil
import os


def trycopytree(source, dest):
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
        print("done copying {} to {}".format(source, dest))
    except Exception as e:
        print(e)


def trycopy(source, dest):
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
        print("done copying {} to {}".format(source, dest))
    except Exception as e:
        print(e)


def trymkdir(path):
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
        print("created dir at", path)
    except Exception as e:
        print(e)


def trymkfile(path, content):
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
        print("file created at {}".format(path))
        print("with content:")
        print(content)
    except Exception as e:
        print(e)


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
