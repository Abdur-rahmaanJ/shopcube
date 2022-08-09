import os
import subprocess
import sys
from pathlib import Path
import shutil
# from .shopyoapi.file import trycopy
from .shopyoapi.file import trycopytree
from .shopyoapi.file import trymkdir
from .shopyoapi.info import printinfo

dirpath = Path(__file__).parent.absolute()
dirpathparent = Path(__file__).parent.parent.absolute()

def main():
    args = sys.argv
    if len(args) == 1:
        printinfo()
        print("No arguments supplied")
        return

    if args[1] == "showjson":
        configjson = os.path.join(dirpath, 'config.json')
        with open(configjson) as f:
            print(f.read())

    if args[1] == "copyjson":
        config_example_json = os.path.join(dirpath, 'config.example.json')
        config_json = os.path.join(os.getcwd(), 'config.json')
        shutil.copyfile(config_example_json, config_json)
        print('json config file copied to', config_json)
    if args[1] == "applyjson":
        config_json_original = os.path.join(dirpath, 'config.json')
        config_json_cwd = os.path.join(os.getcwd(), 'config.json')
        shutil.copyfile(config_json_cwd, config_json_original)
        print('json file applied')

    if args[1] == "restorejson":
        config_json_example = os.path.join(dirpath, 'config.example.json')
        config_json_original = os.path.join(dirpath, 'config.json')
        shutil.copyfile(config_json_example, config_json_original)
        print('json file restored')
    else:
        path = os.path.join(dirpath, "manage.py")
        torun = [sys.executable, path] + args[1:]
        subprocess.run(torun, stdout=subprocess.PIPE)


if __name__ == "__main__":
    main()
