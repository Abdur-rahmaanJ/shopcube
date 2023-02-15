# from flask import redirect
# from flask import render_template
from flask import flash
from flask import request
from flask import url_for
from flask import redirect
import datetime
from flask_login import current_user
from flask_login import login_required
from flask_login import logout_user
from flask_login import login_user
from flask import current_app
from shopyo.api.forms import flash_errors
from shopyo.api.html import notify_success
from shopyo.api.html import notify_warning
from shopyo.api.module import ModuleHelp

from init import db

from modules.box__default.auth.models import User
from modules.box__default.auth.models import Role
from shopyo.api.email import send_async_email
from modules.box__ecommerce.shop.forms import RegisterCustomerForm
from modules.box__ecommerce.shop.models import BillingDetail
from modules.box__ecommerce.shop.models import Order
from modules.box__ecommerce.shop.models import OrderItem

from .helpers import send_verify_code

mhelp = ModuleHelp(__file__, __name__)
globals()[mhelp.blueprint_str] = mhelp.blueprint
module_blueprint = globals()[mhelp.blueprint_str]


@module_blueprint.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        
        form = RegisterCustomerForm()
        if not form.validate_on_submit():
            flash_errors(form)
            return redirect('/')
        context = {}
        email = form.email.data
        password = form.password.data
        phone_number = form.phone.data
        user = User.create(
            email=email, 
            password=password, 
            phone_number=phone_number)
        
        login_user(user)

        is_disabled = False

        if "EMAIL_CONFIRMATION_DISABLED" in current_app.config:
            is_disabled = current_app.config["EMAIL_CONFIRMATION_DISABLED"]

        if is_disabled is True:
            user.is_email_confirmed = True
            user.email_confirm_date = datetime.datetime.now()
            user.update()
        else:
            token = user.generate_confirmation_token()
            template = "auth/emails/activate_user"
            subject = "Please confirm your email"
            context.update({"token": token, "user": user})
            send_async_email(email, subject, template, **context)
            flash("A confirmation email has been sent via email.", "ok")

        # return redirect(url_for("dashboard.index"))
        return mhelp.redirect_url("shop.homepage")


@module_blueprint.route("/send-otp", methods=["POST"])
def send_otp():
    if request.method == 'POST':
        print(request.form.listvalues)
        phone_number = request.form['phone-number']
        user = db.session.query(User).filter(User.phone_number==phone_number).first()
        if user is None:
            return redirect('/')
        token = send_verify_code(phone_number)
        user.otp_token = send_verify_code(phone_number)
        user.update()
        flash('otp sent')
        print(token)
        return redirect('/')


@module_blueprint.route("/login-otp", methods=["POST"])
def login_otp():
    if request.method == 'POST':
        phone_number = request.form['phone-number']
        user = db.session.query(User).filter(User.phone_number==phone_number).first()
        if user is None:
            return redirect('/')
        token = request.form['otp']
        
        if token == user.otp_token:
            login_user(user)
            flash('good otp')
            return redirect('/')
        

@module_blueprint.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return mhelp.redirect_url("shop.homepage")


@module_blueprint.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    context = mhelp.context()
    context.update({"_hide_nav": True, "_logout_url": url_for("customer.logout")})
    return mhelp.render("dashboard.html", **context)


@module_blueprint.route("/orders", methods=["GET"])
@login_required
def orders():
    context = mhelp.context()
    NO_OF_ITEMS = 5

    page = request.args.get("page", 1, type=int)
    logged_in_orders = Order.query.filter(
        Order.logged_in_customer_email == current_user.email
    ).paginate(page, NO_OF_ITEMS, False)

    not_logged_in_orders = (
        Order.query.join(BillingDetail)
        .filter(
            (BillingDetail.email == current_user.email)
            & (Order.logged_in_customer_email == "")
        )
        .all()
    )
    context.update(
        {
            "logged_in_orders": logged_in_orders,
            "not_logged_in_orders": not_logged_in_orders,
        }
    )
    context.update({"_hide_nav": True, "_logout_url": url_for("customer.logout")})
    return mhelp.render("orders.html", **context)


@module_blueprint.route("/order/<order_id>/view", methods=["GET", "POST"])
@login_required
def order_view(order_id):
    order = Order.query.get(order_id)
    context = mhelp.context()
    context.update({"order": order})
    context.update({"_hide_nav": True, "_logout_url": url_for("customer.logout")})
    return mhelp.render("order_item_view.html", **context)


# If "dashboard": "/dashboard" is set in info.json
#
# @module_blueprint.route("/dashboard", methods=["GET"])
# def dashboard():

#     context = mhelp.context()

#     context.update({

#         })
#     return mhelp.render('dashboard.html', **context)
