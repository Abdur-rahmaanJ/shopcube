import copy
import json
import os

from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import url_for

from shopyoapi.assets import get_static


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

    def get_self_static(self, filename):
        module_parent = os.path.dirname(self.dirpath)
        module_folder = self.dirpath

        module_parent = os.path.normpath(module_parent)
        module_parent = os.path.basename(module_parent)

        module_folder = os.path.normpath(module_folder)
        module_folder = os.path.basename(module_folder)

        print(module_parent, module_parent)
        if module_parent.startswith("box__"):
            boxormodule = "{}/{}".format(module_parent, module_folder)
        else:
            boxormodule = module_folder
        return get_static(boxormodule=boxormodule, filename=filename)
