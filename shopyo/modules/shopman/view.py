# from flask import render_template
# from flask import url_for
# from flask import redirect

import os 
import json

from flask import flash
from flask import request
from flask import current_app

from shopyoapi.forms import flash_errors

# #
from shopyoapi.html import notify_success
from shopyoapi.module import ModuleHelp
from shopyoapi.enhance import get_setting
from shopyoapi.enhance import set_setting

from modules.product.models import Product
from modules.shop.models import Order
from modules.shopman.forms import CouponForm
from modules.shopman.forms import DeliveryOptionForm
from modules.shopman.forms import PaymentOptionForm
from modules.shopman.forms import CurrencyForm

from .models import Coupon
from .models import DeliveryOption
from .models import PaymentOption

mhelp = ModuleHelp(__file__, __name__)

globals()[mhelp.blueprint_str] = mhelp.blueprint

module_blueprint = globals()[mhelp.blueprint_str]


def get_product(barcode):
    return Product.query.get(barcode)


@module_blueprint.route(mhelp.info["dashboard"])
def dashboard():
    context = {}
    form = CurrencyForm()
    with open(os.path.join(current_app.config['BASE_DIR'],'modules', 'shopman', 'data', 'currency.json')) as f:
        currencies = json.load(f)
    currency_choices = [(c['cc'], c['name']) for c in currencies]
    form.currency.choices = currency_choices
    
    context.update({
        'form': form,
        'current_currency': get_setting('CURRENCY')
        })
    context.update({"info": mhelp.info})
    return mhelp.render("dashboard.html", **context)


@module_blueprint.route('currency/set', methods=['GET', 'POST'])
def set_currency():
    if request.method == 'POST':
        form = CurrencyForm()
        set_setting('CURRENCY', form.currency.data)
        return mhelp.redirect_url('shopman.dashboard')


@module_blueprint.route("/delivery" + mhelp.info["dashboard"])
def delivery():
    context = {}
    form = DeliveryOptionForm()
    options = DeliveryOption.query.all()

    context.update({"form": form, "options": options})
    context.update({"info": mhelp.info})
    return mhelp.render("delivery.html", **context)


@module_blueprint.route("/delivery/option/add", methods=["GET", "POST"])
def delivery_add_option():
    if request.method == "POST":
        form = DeliveryOptionForm()
        if form.validate_on_submit():
            toadd = DeliveryOption()
            toadd.option = form.option.data
            toadd.price = float(form.price.data)
            toadd.insert()
            flash(notify_success("Option Added!"))
            return mhelp.redirect_url("shopman.delivery")
        else:
            flash_errors(form)
            return mhelp.redirect_url("shopman.delivery")


@module_blueprint.route("/delivery/option/update", methods=["GET", "POST"])
def delivery_option_update():
    if request.method == "POST":

        opt_id = request.form["id"]
        option_data = request.form["option"]
        price_data = request.form["price"]

        option = DeliveryOption.query.get(opt_id)
        option.option = option_data
        option.price = price_data
        option.update()

        flash(notify_success("Option updated!"))
        return mhelp.redirect_url("shopman.delivery")


@module_blueprint.route("/delivery/option/<option_id>/delete", methods=["GET"])
def delivery_option_delete(option_id):
    option = DeliveryOption.query.get(option_id)
    option.delete()

    flash(notify_success("Option Deleted!"))
    return mhelp.redirect_url("shopman.delivery")


@module_blueprint.route("/payment/dashboard", methods=["GET", "POST"])
def payment():
    context = {}
    form = PaymentOptionForm()
    options = PaymentOption.query.all()

    context.update({"form": form, "options": options})
    context.update({"info": mhelp.info})
    return mhelp.render("payment.html", **context)


@module_blueprint.route("/payment/option/add", methods=["GET", "POST"])
def payment_add_option():
    if request.method == "POST":
        form = PaymentOptionForm()
        if form.validate_on_submit():
            toadd = PaymentOption()
            toadd.name = form.name.data
            toadd.text = form.text.data
            toadd.insert()
            flash(notify_success("Option Added!"))
            return mhelp.redirect_url("shopman.payment")
        else:
            flash_errors(form)
            return mhelp.redirect_url("shopman.payment")


@module_blueprint.route("/payment/option/update", methods=["GET", "POST"])
def payment_option_update():
    if request.method == "POST":

        opt_id = request.form["id"]
        option_data = request.form["name"]
        text_data = request.form["text"]

        option = PaymentOption.query.get(opt_id)
        option.name = option_data
        option.text = text_data
        option.update()

        flash(notify_success("Option updated!"))
        return mhelp.redirect_url("shopman.payment")


@module_blueprint.route("/payment/option/<option_id>/delete", methods=["GET"])
def payment_option_delete(option_id):
    option = PaymentOption.query.get(option_id)
    option.delete()

    flash(notify_success("Option Deleted!"))
    return mhelp.redirect_url("shopman.payment")


@module_blueprint.route("/coupon/dashboard", methods=["GET", "POST"])
def coupon():
    form = CouponForm()
    coupons = Coupon.query.all()
    context = {"form": form, "coupons": coupons}
    context.update({"info": mhelp.info})
    return mhelp.render("coupon.html", **context)


@module_blueprint.route("/coupon/add", methods=["GET", "POST"])
def coupon_add():
    if request.method == "POST":
        form = CouponForm()
        if form.validate_on_submit():
            toadd = Coupon()
            toadd.string = form.string.data
            toadd.type = form.type.data
            toadd.value = form.value.data
            toadd.insert()
            flash(notify_success("Coupon Added!"))
            return mhelp.redirect_url("shopman.coupon")
        else:
            flash_errors(form)
            return mhelp.redirect_url("shopman.coupon")


@module_blueprint.route("/coupon/<coupon_id>/delete", methods=["GET"])
def coupon_delete(coupon_id):
    coupon = Coupon.query.get(coupon_id)
    coupon.delete()

    flash(notify_success("Coupon Deleted!"))
    return mhelp.redirect_url("shopman.coupon")


@module_blueprint.route("/coupon/update", methods=["GET", "POST"])
def coupon_update():
    if request.method == "POST":
        form = CouponForm()
        if form.validate_on_submit:
            coupon_id = request.form["id"]
            coupon = Coupon.query.get(coupon_id)
            coupon.string = form.string.data
            coupon.type = form.type.data
            coupon.value = form.value.data
            coupon.update()

            flash(notify_success("Coupon updated!"))
            return mhelp.redirect_url("shopman.coupon")
        else:
            flash_errors(form)
            return mhelp.redirect_url("shopman.coupon")


@module_blueprint.route("/order/dashboard", methods=["GET", "POST"])
def order():
    orders = Order.query.all()
    context = {"dir": dir, "orders": orders, "get_product": get_product}
    context.update({"info": mhelp.info})
    return mhelp.render("order.html", **context)


@module_blueprint.route("/order/<order_id>/delete", methods=["GET", "POST"])
def order_delete(order_id):
    order = Order.query.get(order_id)
    order.delete()
    return mhelp.redirect_url("shopman.order")
