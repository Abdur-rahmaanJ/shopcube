import importlib
import os


def autoload_models():
    """
    Auto imports models from modules/ in desired file. Used so that
    flask_migrate does not miss models when migrating

    Returns
    -------
    None
    """
    print("Auto importing models")
    for module in os.listdir("modules"):
        if module.startswith("__"):
            continue
        try:
            to_load = "modules.{}.models".format(module)
            importlib.import_module(to_load)
            print("[x]", "imported", to_load)
        except Exception as e:
            print("[ ]", e)
