import json
import os
import copy

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

        self._context.update({'info': self.info})

    def render(self, filename, **kwargs):
        '''
        .render('file.html') renders file.html found in module/templates/module/file.html
        '''
        return render_template(
            "{}/{}".format(self.info["module_name"], filename), **kwargs
        )

    def redirect_url(self, url, **kwargs):
        return redirect(url_for(url, **kwargs))

    def context(self):
        return copy.deepcopy(self._context)
