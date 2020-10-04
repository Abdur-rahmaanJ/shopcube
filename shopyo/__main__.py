import sys
import os

from .shopyoapi.utils import trymkdir
from .shopyoapi.utils import trycopytree
from .shopyoapi.utils import trycopy

from pathlib import Path

dirpath = Path(__file__).parent.absolute()
dirpathparent = Path(__file__).parent.parent.absolute()

def new_project(path, newfoldername):
    newfoldername = newfoldername.strip('/').strip('\\')
    print("creating new project {}".format(newfoldername))

    base_path = path + "/" + newfoldername
    trymkdir(base_path)
    print("created dir {} in {}".format(newfoldername, path))

    trycopytree(os.path.join(dirpath, "static"), base_path + "/static")
    trycopytree(os.path.join(dirpath, "tests"), base_path + "/tests")
    trycopytree(os.path.join(dirpath, "modules", "base"), base_path + "/modules/base")
    trycopytree(os.path.join(dirpath, "modules", "admin"), base_path + "/modules/admin")
    trycopytree(os.path.join(dirpath, "modules", "login"), base_path + "/modules/login")
    trycopytree(os.path.join(dirpath, "modules", "appointment"), base_path + "/modules/appointment")
    trycopytree(os.path.join(dirpath, "modules", "category"), base_path + "/modules/category")
    trycopytree(os.path.join(dirpath, "modules", "people"), base_path + "/modules/people")
    trycopytree(os.path.join(dirpath, "modules", "product"), base_path + "/modules/product")
    trycopytree(os.path.join(dirpath, "modules", "control_panel"), base_path + "/modules/control_panel")
    trycopytree(os.path.join(dirpath, "modules", "settings"), base_path + "/modules/settings")
    trycopytree(os.path.join(dirpath, "shopyoapi"), base_path + "/shopyoapi")

    trycopy(os.path.join(dirpath, "app.py"), base_path + "/app.py")
    trycopy(os.path.join(dirpath, "config.json"), base_path + "/config.json")
    trycopy(os.path.join(dirpath, "config.py"), base_path + "/config.py")
    trycopy(os.path.join(dirpath, "manage.py"), base_path + "/manage.py")
    trycopy(os.path.join(dirpathparent, "requirements.txt"), base_path + "/requirements.txt")
    trycopy(os.path.join(dirpathparent, "README.md"), base_path + "/README.md")

def main():
    args = sys.argv
    if args[1] == "new" and len(args) == 4:
        new_project(args[2], args[3])


if __name__ == "__main__":
    main()