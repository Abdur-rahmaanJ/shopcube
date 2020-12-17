
import os
import json

from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for

class ModuleHelp:
    def __init__(self, dunderfile, dundername):
        self.dirpath = os.path.dirname(os.path.abspath(dunderfile))
        self.info = {}

        with open(self.dirpath + "/info.json") as f:
            self.info = json.load(f)

        self.blueprint_str = '{}_blueprint'.format(self.info["module_name"])
        self.blueprint = Blueprint("{}".format(
                                self.info["module_name"]),
                                dundername,
                                template_folder="templates",
                                url_prefix=self.info["url_prefix"],
                            )

    def render(self, filename, **kwargs):
        return render_template('{}/{}'.format(self.info['module_name'], filename), **kwargs)

    def redirect_url(self, url, **kwargs):
        return redirect(url_for(url, **kwargs))
