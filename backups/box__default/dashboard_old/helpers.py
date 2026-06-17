import json
import os

from flask import current_app
from flask import request


def get_modules_info():
    all_info = {}
    for folder in os.listdir(os.path.join(current_app.config["BASE_DIR"], "modules")):
        if folder.startswith("__"):
            continue
        elif folder.startswith("box__"):
            for sub_folder in os.listdir(
                os.path.join(current_app.config["BASE_DIR"], "modules", folder)
            ):

                if sub_folder in ["dashboard"]:
                    continue
                if sub_folder.startswith("__"):  # ignore __pycache__
                    continue
                elif sub_folder.endswith(".json"):  # box_info.json
                    continue
                with open(
                    os.path.join(
                        current_app.config["BASE_DIR"],
                        "modules",
                        folder,
                        sub_folder,
                        "info.json",
                    )
                ) as f:
                    module_info = json.load(f)
                    module_info["static_name"] = "{}/{}".format(
                        folder, module_info["module_name"]
                    )
                    all_info[sub_folder] = module_info
        else:

            if folder not in ["dashboard"]:
                with open(
                    os.path.join(
                        current_app.config["BASE_DIR"],
                        "modules",
                        folder,
                        "info.json",
                    )
                ) as f:
                    module_info = json.load(f)
                    module_info["static_name"] = f"{folder}"
                    all_info[folder] = module_info

    return all_info


def get_url_prefix(parts=False, as_str=False):
    if parts:
        if as_str:
            return str(request.url_rule)
        else:
            return str(request.url_rule).split("/")
    else:
        return "/" + str(request.url_rule).split("/")[1]
