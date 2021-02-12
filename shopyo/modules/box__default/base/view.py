import json
import os

from flask import Blueprint

dirpath = os.path.dirname(os.path.abspath(__file__))
module_info = {}

with open(dirpath + "/info.json") as f:
    module_info = json.load(f)

base_blueprint = Blueprint(
    "base",
    __name__,
    url_prefix=module_info["url_prefix"],
    template_folder="templates",
)
