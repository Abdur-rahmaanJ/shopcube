
from flask import Blueprint
contact_blueprint = Blueprint(
    "contact",
    __name__,
    url_prefix='/contact',
    template_folder="templates",
)


@contact_blueprint.route("/")
def index():
    return ''
