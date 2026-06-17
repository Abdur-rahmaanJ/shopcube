from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required
from shopyo.api.html import notify_success, notify_warning
from shopyo.api.forms import flash_errors
from shopyo.api.module import ModuleHelp
from shopyo_appadmin.admin import admin_required

from init import db
from .models import Vendor
from .forms import VendorForm

mhelp = ModuleHelp(__file__, __name__)
globals()[mhelp.blueprint_str] = mhelp.blueprint
module_blueprint = globals()[mhelp.blueprint_str]


@module_blueprint.route(mhelp.info["dashboard"])
@login_required
@admin_required
def dashboard():
    context = mhelp.context()
    vendors = Vendor.query.order_by(Vendor.name).all()
    context.update({"vendors": vendors})
    return mhelp.render("dashboard.html", **context)


@module_blueprint.route("/add", methods=["GET", "POST"])
@login_required
@admin_required
def add():
    form = VendorForm()
    if request.method == "POST":
        if form.validate_on_submit():
            vendor = Vendor(
                name=form.name.data.strip(),
                email=form.email.data.strip() if form.email.data else "",
                phone=form.phone.data.strip() if form.phone.data else "",
                address=form.address.data.strip() if form.address.data else "",
                notes=form.notes.data.strip() if form.notes.data else "",
            )
            vendor.insert()
            flash(notify_success(f"Vendor '{vendor.name}' added successfully"))
            return redirect(url_for("vendor.dashboard"))
        else:
            flash_errors(form)
    context = mhelp.context()
    context.update({"form": form})
    return mhelp.render("add.html", **context)


@module_blueprint.route("/<vendor_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit(vendor_id):
    vendor = Vendor.query.get_or_404(vendor_id)
    form = VendorForm(obj=vendor)
    if request.method == "POST":
        if form.validate_on_submit():
            vendor.name = form.name.data.strip()
            vendor.email = form.email.data.strip() if form.email.data else ""
            vendor.phone = form.phone.data.strip() if form.phone.data else ""
            vendor.address = form.address.data.strip() if form.address.data else ""
            vendor.notes = form.notes.data.strip() if form.notes.data else ""
            vendor.update()
            flash(notify_success(f"Vendor '{vendor.name}' updated"))
            return redirect(url_for("vendor.dashboard"))
        else:
            flash_errors(form)
    context = mhelp.context()
    context.update({"form": form, "vendor": vendor})
    return mhelp.render("edit.html", **context)


@module_blueprint.route("/<vendor_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete(vendor_id):
    vendor = Vendor.query.get_or_404(vendor_id)
    if vendor.products:
        flash(notify_warning(
            f"Cannot delete vendor '{vendor.name}'. "
            f"Remove or reassign {len(vendor.products)} product(s) first."
        ))
        return redirect(url_for("vendor.dashboard"))
    db.session.delete(vendor)
    db.session.commit()
    flash(notify_success(f"Vendor '{vendor.name}' deleted"))
    return redirect(url_for("vendor.dashboard"))
