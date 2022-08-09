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
    for folder in os.listdir("modules"):
        if folder.startswith("__"):
            continue
        elif folder.startswith("box__"):
            for sub_folder in os.listdir(os.path.join("modules", folder)):
                if sub_folder.startswith("__"):  # ignore __pycache__
                    continue
                elif sub_folder.endswith(".json"):  # box_info.json
                    continue
                try:
                    to_load_submodel = "modules.{}.{}.models".format(
                        folder, sub_folder
                    )
                    importlib.import_module(to_load_submodel)
                    print("[x]", "imported", to_load_submodel)
                except Exception as e:
                    print("[ ]", e)
        else:
            try:
                to_load = "modules.{}.models".format(folder)
                importlib.import_module(to_load)
                print("[x]", "imported", to_load)
            except Exception as e:
                print("[ ]", e)
