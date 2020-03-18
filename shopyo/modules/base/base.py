from flask import Blueprint


base_blueprint = Blueprint('base', __name__, url_prefix='/base',
                           template_folder='templates')
