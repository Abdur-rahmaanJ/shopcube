from flask import abort
from flask import redirect
from flask import request
from flask import url_for
from flask_admin import AdminIndexView
from flask_admin import expose
from flask_admin.contrib import sqla as flask_admin_sqla
from flask_login import current_user

from shopyo.api.perms import Permission
from shopyo.api.perms import PolicyEngine

policy_engine = PolicyEngine()


class DefaultModelView(flask_admin_sqla.ModelView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("shopyo_auth.login", next=request.url))


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("shopyo_auth.login", next=request.url))

    @expose("/")
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for("shopyo_auth.login"))
        if not policy_engine.has_permission(
            current_user, Permission.ADMIN_PANEL_ACCESS
        ):
            abort(403)
        return super().index()
