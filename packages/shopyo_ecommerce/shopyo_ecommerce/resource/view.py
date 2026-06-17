import os
import json

from flask import Blueprint
from flask import current_app
from flask import send_from_directory
from shopyo.api.module import ModuleHelp


mhelp = ModuleHelp(__file__, __name__)
globals()[mhelp.blueprint_str] = mhelp.blueprint
module_blueprint = globals()[mhelp.blueprint_str]


@module_blueprint.route("/product/<filename>", methods=["GET"])
def product_image(filename):
    if filename == "default":
        return send_from_directory(
            os.path.join(current_app.config["BASE_DIR"], "static", "default"),
            "default_product.jpg",
        )
    return send_from_directory(
        current_app.config["UPLOADED_PRODUCTPHOTOS_DEST"], filename
    )
