import json
import os

from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from flask_login import login_required

from shopyo.api.forms import flash_errors

from .forms import PageForm
from .models import Page

dirpath = os.path.dirname(os.path.abspath(__file__))
module_info = {}

with open(dirpath + "/info.json") as f:
    module_info = json.load(f)

globals()["{}_blueprint".format(module_info["module_name"])] = Blueprint(
    "{}".format(module_info["module_name"]),
    __name__,
    template_folder="templates",
    url_prefix=module_info["url_prefix"],
)


module_blueprint = globals()["{}_blueprint".format(module_info["module_name"])]

module_name = module_info["module_name"]

sidebar = [{"text": "sample", "icon": "fa fa-table", "url": ""}]

module_settings = {"sidebar": sidebar}


@module_blueprint.route("/")
def index():
    context = {}
    pages = Page.query.all()

    context.update({"pages": pages})
    return render_template("page/all_pages.html", **context)


@module_blueprint.route("/<page_id>/<slug>")
def view_page(page_id, slug):
    context = {}
    page = Page.query.get(page_id)

    context.update({"page": page})
    return render_template("page/view_page.html", **context)


@module_blueprint.route(module_info["dashboard"])
@login_required
def dashboard():
    context = {}
    form = PageForm()

    context.update({"form": form, "module_name": module_name})
    context.update(module_settings)
    return render_template("page/dashboard.html", **context)


@module_blueprint.route("/check_pagecontent", methods=["GET", "POST"])
@login_required
def check_pagecontent():
    if request.method == "POST":
        form = PageForm()
        if not form.validate_on_submit():
            flash_errors(form)
            return redirect(url_for("{}.dashboard".format(module_name)))
        toaddpage = Page(
            slug=form.slug.data,
            content=form.content.data,
            title=form.title.data,
        )
        toaddpage.insert()
        return redirect(url_for("{}.dashboard".format(module_name)))
