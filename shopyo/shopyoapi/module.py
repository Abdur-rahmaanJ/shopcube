import copy
import json
import os

from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import url_for


class ModuleHelp:
    def __init__(self, dunderfile, dundername):
        self.dirpath = os.path.dirname(os.path.abspath(dunderfile))
        self.info = {}
        self._context = {}

        with open(self.dirpath + "/info.json") as f:
            self.info = json.load(f)

        self.blueprint_str = "{}_blueprint".format(self.info["module_name"])
        self.blueprint = Blueprint(
            "{}".format(self.info["module_name"]),
            dundername,
            template_folder="templates",
            url_prefix=self.info["url_prefix"],
        )

        self._context.update({"info": self.info})

    def render(self, filename, **kwargs):
        """
        .render('file.html') renders file.html found in module/templates/module/file.html
        """
        return render_template(
            "{}/{}".format(self.info["module_name"], filename), **kwargs
        )

    def redirect_url(self, url, **kwargs):
        return redirect(url_for(url, **kwargs))

    def context(self):
        return copy.deepcopy(self._context)

    def method(self, methodname):
        return "{}.{}".format(self.info["module_name"], methodname)

    def get_asset(self, assetname):
        """returns url for static, filename=assetname"""
        return url_for("static", filename=assetname)

    def get_static(self, filename):
        """Django inspired, returns get asset for modules/filename"""
        return self.get_asset("modules/{}".format(filename))
