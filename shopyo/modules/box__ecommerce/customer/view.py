
from shopyoapi.module import ModuleHelp
from modules.box__default.auth.forms import RegisterCustomerForm
from modules.box__default.admin.models import User
from modules.box__ecommerce.shop.models import Order
from modules.box__ecommerce.shop.models import OrderItem
from modules.box__ecommerce.shop.models import BillingDetail

# from flask import render_template
from flask import url_for
# from flask import redirect
from flask import flash
from flask import request

from shopyoapi.html import notify_warning
from shopyoapi.html import notify_success
from shopyoapi.forms import flash_errors
from shopyoapi.init import db

from flask_login import login_required
from flask_login import logout_user
from flask_login import current_user

mhelp = ModuleHelp(__file__, __name__)
globals()[mhelp.blueprint_str] = mhelp.blueprint
module_blueprint = globals()[mhelp.blueprint_str]

@module_blueprint.route("/register", methods=['POST'])
@login_required
def register():
    if request.method == 'POST':
        form = RegisterCustomerForm()
        if not form.validate_on_submit():
            flash_errors(form)
        user = User()
        if User.query.filter(User.email == form.email.data).first():
            flash(notify_warning("Email exists"))
            return mhelp.redirect_url('shop.homepage')
        user.email = form.email.data
        password1 = form.password.data
        password2 = form.reconfirm_password.data
        if not password1 == password2:
            flash(notify_warning("Passwords don't match"))
            return mhelp.redirect_url('shop.homepage')
        user.set_hash(password1)
        user.is_customer = True
        user.save()
        flash(notify_success('Successfully registered, please log in!'))
        return mhelp.redirect_url('shop.homepage')

@module_blueprint.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return mhelp.redirect_url('shop.homepage')

@module_blueprint.route("/dashboard", methods=['GET'])
@login_required
def dashboard():
    context = mhelp.context()
    context.update({'_hide_nav': True, '_logout_url':url_for('customer.logout')})
    return mhelp.render('dashboard.html', **context)


@module_blueprint.route("/orders", methods=['GET'])
@login_required
def orders():
    context = mhelp.context()
    logged_in_orders = Order.query.filter(Order.logged_in_customer_email == current_user.email).all()
    not_logged_in_orders = Order.query.join(BillingDetail).filter(
        (BillingDetail.email == current_user.email) &
        (Order.logged_in_customer_email == '')).all()
    context.update({'logged_in_orders': logged_in_orders, 'not_logged_in_orders': not_logged_in_orders})
    context.update({'_hide_nav': True, '_logout_url':url_for('customer.logout')})
    return mhelp.render('orders.html', **context)


@module_blueprint.route("/order_item/<item_id>/view", methods=["GET", "POST"])
@login_required
def order_view(item_id):
    order_item = OrderItem.query.get(item_id)
    context = mhelp.context()
    context.update({'order_item': order_item})
    context.update({'_hide_nav': True, '_logout_url':url_for('customer.logout')})
    return mhelp.render("order_item_view.html", **context)



# If "dashboard": "/dashboard" is set in info.json
#
# @module_blueprint.route("/dashboard", methods=["GET"])
# def dashboard():

#     context = mhelp.context()

#     context.update({

#         })
#     return mhelp.render('dashboard.html', **context)
