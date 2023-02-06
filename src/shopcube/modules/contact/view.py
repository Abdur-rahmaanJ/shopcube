from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import login_required
from modules.box__default.theme.helpers import get_active_front_theme
from shopyo.api.html import notify_success

from .forms import ContactForm
from .models import ContactMessage

contact_blueprint = Blueprint(
    "contact",
    __name__,
    url_prefix="/contact",
    template_folder="templates",
)


@contact_blueprint.route("/")
def index():
    context = {}
    form = ContactForm()

    context.update({"form": form})
    return render_template(f"{get_active_front_theme()}/contact.html", **context)


@contact_blueprint.route("/validate_message", methods=["GET", "POST"])
@login_required
def validate_message():
    if request.method == "POST":
        form = ContactForm()
        if not form.validate_on_submit():
            flash_errors(form)
            return redirect(url_for("contact.index"))

        name = form.name.data
        email = form.email.data
        message = form.message.data

        contact_message = ContactMessage(name=name, email=email, message=message)
        contact_message.insert()
        flash("Message submitted!", "ok")
        return redirect(url_for("contact.index"))


@contact_blueprint.route("/dashboard", methods=["GET"], defaults={"page": 1})
@contact_blueprint.route("/dashboard/<int:page>", methods=["GET"])
@login_required
def dashboard(page):
    context = {}

    per_page = 10
    messages = ContactMessage.query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    context.update({"messages": messages})
    return render_template("contact/dashboard.html", **context)
