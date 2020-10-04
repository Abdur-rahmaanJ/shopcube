import shutil
import os


def trycopytree(source, dest):
    try:
        shutil.copytree(source, dest)
        print("done copying {} to {}".format(source, dest))
    except Exception as e:
        print(e)


def trycopy(source, dest):
    try:
        shutil.copy(source, dest)
        print("done copying {} to {}".format(source, dest))
    except Exception as e:
        print(e)


def trymkdir(path):
    try:
        os.mkdir(path)
        print('created dir at', path)
    except Exception as e:
        print(e)


def trymkfile(path, content):
    try:
        with open(path, 'w+') as f:
            f.write(content)
        print('file created at {}'.format(path))
        print('with content:')
        print(content)
    except Exception as e:
        print(e)
