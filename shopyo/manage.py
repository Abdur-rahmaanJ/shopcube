import os
import subprocess
import click

from app import app
from shopyo.api.cmd import clean
from shopyo.api.cmd import create_box
from shopyo.api.cmd import create_module
from shopyo.api.cmd import create_module_in_box
from shopyo.api.cmd import initialise
from shopyo.api.cmd import collectstatic
from shopyo.api.database import autoload_models
from shopyo.api.info import printinfo
from shopyo.api.file import trycopy


def runserver():
    app.run(host="0.0.0.0", debug=False)


@click.command()
@click.argument("args", nargs=-1)
def process(args):
    printinfo()
    if args[0] == "initialise" or args[0] == "initialize":
        clean(app)
        autoload_models()
        initialise()
    elif args[0] == "clean":
        clean(app)
    elif args[0] == "runserver":
        runserver()
    elif args[0] == "rundebug":
        app.run(debug=True, host="0.0.0.0")
        try:
            if len(args) > 2 and args[1]:
                app.run(debug=True, host="0.0.0.0", port=int(args[1]))
        except IndexError as e:
            raise e
    elif args[0] == "collectstatic":
        if len(args) == 1:
            collectstatic()
        elif len(args) == 2:
            collectstatic(target_module=args[1])
    elif args[0] == "test":
        print("test ok")
    elif args[0] == "startapp" and args[1]:
        create_module(args[1])
    elif args[0] == "startbox" and args[1]:
        create_box(args[1])
    elif args[0] == "startsubapp" and args[1] and args[3]:
        if args[2].lower() == "in":
            create_module_in_box(args[1], args[3])
    elif args[0] == "db":
        try:
            autoload_models()
            if args[1] == "migrate":
                subprocess.run(["flask", "db", "migrate"])
            elif args[1] == "upgrade":
                subprocess.run(["flask", "db", "upgrade"])
            elif args[1] == "init":
                subprocess.run(["flask", "db", "init"])
        except IndexError as e:
            print("db requires more options")
            raise e
    elif args[0] == "createconfig":
        try:
            if not os.path.exists("config.py"):
                trycopy("config_demo.py", "config.py")
            else:
                print("config.py exists")
            if not os.path.exists("config.json"):
                trycopy("config_demo.json", "config.json")
            else:
                print("config.json exists")
        except PermissionError as e:
            print(
                "Cannot continue, permission error"
                "initialising config.py and config.json, "
                "copy and rename them yourself!"
            )
            raise e
    else:
        print("Command not recognised")

    # This will be printed on exit
    print("See you soon!!!")


if __name__ == "__main__":
    process()
