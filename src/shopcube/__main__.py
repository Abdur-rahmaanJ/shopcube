import os
import subprocess
import sys
from pathlib import Path
import shutil
# from .shopyoapi.file import trycopy
from shopyo.api.file import trycopytree
from shopyo.api.file import trymkdir
from shopyo.api.info import printinfo

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

    elif args[1] == "copyjson":
        config_example_json = os.path.join(dirpath, 'config.example.json')
        config_json = os.path.join(os.getcwd(), 'config.json')
        shutil.copyfile(config_example_json, config_json)
        print('json config file copied to', config_json)
    elif args[1] == "applyjson":
        config_json_original = os.path.join(dirpath, 'config.json')
        config_json_cwd = os.path.join(os.getcwd(), 'config.json')
        shutil.copyfile(config_json_cwd, config_json_original)
        print('json file applied')

    elif args[1] == "restorejson":
        config_json_example = os.path.join(dirpath, 'config.example.json')
        config_json_original = os.path.join(dirpath, 'config.json')
        shutil.copyfile(config_json_example, config_json_original)
        print('json file restored')


    elif args[1] == "create":
        source = os.path.join(dirpathparent, 'shopcube')
        dest = os.path.join(os.getcwd(), 'shopcube')

        print('creating new project!')
        trycopytree(source, dest, verbose=False)
        print('project created')


    elif args[1] == "packageinfo":
        source = os.path.join(dirpathparent, 'shopcube')
        print('Package dir', source)


    elif args[1] == "runhere":
        source = os.path.join(dirpathparent, 'shopcube')
        commands = ['shopyo', *args[2:]]
        p = subprocess.Popen(commands, cwd=os.getcwd())
        p.wait()
    else:
        print('[NOTE] Running shopyo commands inside packages!')
        source = os.path.join(dirpathparent, 'shopcube')
        commands = ['shopyo', *args[1:]]
        p = subprocess.Popen(commands, cwd=source)
        p.wait()


if __name__ == "__main__":
    main()
