import json
import os
from datetime import datetime

from flask import Blueprint
from flask import current_app
from flask import flash
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from flask_login import current_user

from shopyoapi.enhance import get_setting
from shopyoapi.enhance import set_setting
from shopyoapi.forms import flash_errors

# #
from shopyoapi.html import notify_success
from shopyoapi.html import notify_warning
from shopyoapi.module import ModuleHelp

from modules.admin.models import User
from modules.category.models import Category
from modules.category.models import SubCategory
from modules.product.models import Product
from modules.shop.forms import CheckoutForm
from modules.shop.helpers import get_cart_data
from modules.shop.helpers import get_currency_symbol
from modules.shop.models import BillingDetail
from modules.shop.models import Order
from modules.shop.models import OrderItem
from modules.shopman.models import DeliveryOption
from modules.shopman.models import PaymentOption

mhelp = ModuleHelp(__file__, __name__)
globals()[mhelp.blueprint_str] = mhelp.blueprint
module_blueprint = globals()[mhelp.blueprint_str]


# mhelp._context.update({"get_currency_symbol": get_currency_symbol})


def get_product(product_id):
    return Product.query.get(product_id)


@module_blueprint.route("/home")
def homepage():
    # cant be defined above but must be manually set each time
    # active_theme_dir = os.path.join(
    #     dirpath, "..", "..", "themes", get_setting("ACTIVE_THEME")
    # )
    # module_blueprint.template_folder = active_theme_dir

    # return str(module_blueprint.template_folder)
    context = mhelp.context()
    cart_info = get_cart_data()
    context.update(cart_info)
    return render_template(get_setting("ACTIVE_THEME") + "/index.html", **context)


@module_blueprint.route("/page/<int:page>")
@module_blueprint.route("/")
def index(page=1):
    context = mhelp.context()
    PAGINATION = 5
    end = page * PAGINATION
    start = end - PAGINATION
    # total_pages = (data.count_posts(name, data.STATE_PUBLISHED) // PAGINATION) + 1
    total_pages = (len(Product.query.all()) // PAGINATION) + 1
    products = Product.query.all()[::-1][start:end]

    cart_info = get_cart_data()

    context.update(
        {
            "current_category_name": "",
            "total_pages": total_pages,
            "page": page,
            "products": products,
        }
    )
    context.update(cart_info)
    return mhelp.render("shop.html", **context)


@module_blueprint.route("/c/<category_name>")
def category(category_name):

    context = mhelp.context()
    current_category = Category.query.filter(Category.name == category_name).first()

    cart_info = get_cart_data()

    context.update(
        {
            "current_category": current_category,
            "current_category_name": current_category.name,
        }
    )
    context.update(cart_info)
    return mhelp.render("category.html", **context)


@module_blueprint.route("/sub/<subcategory_name>/page/<int:page>")
@module_blueprint.route("/sub/<subcategory_name>")
def subcategory(subcategory_name, page=1):
    context = mhelp.context()
    PAGINATION = 5
    end = page * PAGINATION
    start = end - PAGINATION

    subcategory = SubCategory.query.filter(SubCategory.name == subcategory_name).first()
    products = subcategory.products[start:end]
    total_pages = (len(products) // PAGINATION) + 1
    current_category_name = subcategory.category.name
    subcategory_name = subcategory.name

    cart_info = get_cart_data()

    context.update(
        {
            "subcategory": subcategory,
            "current_category_name": current_category_name,
            "total_pages": total_pages,
            "page": page,
            "products": products,
            "subcategory_name": subcategory_name,
        }
    )
    context.update(cart_info)
    return mhelp.render("subcategory.html", **context)


@module_blueprint.route("/product/<product_barcode>")
def product(product_barcode):
    context = mhelp.context()
    product = Product.query.get(product_barcode)

    cart_info = get_cart_data()
    # 'cart_data': cart_data,
    # 'cart_items': cart_items,
    # 'cart_total_price': cart_total_price

    context.update({"product": product})
    context.update(cart_info)
    return mhelp.render("product.html", **context)


@module_blueprint.route("/cart/add/<product_barcode>", methods=["GET", "POST"])
def cart_add(product_barcode):
    if request.method == "POST":
        flash("")
        if "cart" in session:

            barcode = request.form["barcode"]
            quantity = int(request.form["quantity"])

            product = Product.query.get(barcode)

            data = session["cart"][0]
            if barcode not in data:
                data[barcode] = quantity
                session["cart"][0] = data
            elif barcode in data:
                updated_quantity = data[barcode] + quantity
                if updated_quantity > product.in_stock:
                    flash(
                        notify_warning(
                            "Products in cart cannot be greater than product in stock"
                        )
                    )
                    return redirect(url_for("shop.product", product_barcode=barcode))
                data[barcode] = updated_quantity
                session["cart"][0] = data

        else:
            # In this block, the user has not started a cart, so we start it for them and add the product.
            session["cart"] = [{barcode: quantity}]

    return mhelp.redirect_url("shop.product", product_barcode=barcode)


@module_blueprint.route("/cart/remove/<product_barcode>", methods=["GET", "POST"])
def cart_remove(product_barcode):
    if "cart" in session:

        data = session["cart"][0]
        if product_barcode in data:
            del data[product_barcode]
        flash(notify_success("Removed!"))
        return mhelp.redirect_url("shop.cart")

    else:
        # In this block, the user has not started a cart, so we start it for them and add the product.
        return mhelp.redirect_url("shop.cart")


@module_blueprint.route("/cart", methods=["GET", "POST"])
def cart():
    context = mhelp.context()

    cart_info = get_cart_data()
    delivery_options = DeliveryOption.query.all()

    context.update({"delivery_options": delivery_options, "get_product": get_product})
    context.update(cart_info)
    return mhelp.render("view_cart.html", **context)


@module_blueprint.route("/cart/update", methods=["GET", "POST"])
def cart_update():
    if request.method == "POST":
        data = {}
        for key in request.form:
            if key.startswith("barcode"):
                barcode = request.form[key].strip()
                product = Product.query.get(barcode)

                number = key.split("_")[1]
                quantity = request.form["quantity_{}".format(number)]
                if int(quantity) > product.in_stock:
                    quantity = product.in_stock
                data[barcode] = int(quantity)

        if "cart" in session:
            session["cart"] = [data]
        else:
            session["cart"] = [{}]
        return mhelp.redirect_url("shop.cart")


# @module_blueprint.route("/session", methods=['GET', 'POST'])
# def session_view():
#     return str(session['cart'][0])
#


@module_blueprint.route("/prepare/checkout", methods=["GET", "POST"])
def prepare_checkout():
    if request.method == "POST":
        # update cart

        all_data = request.get_json()
        session["option_id"] = all_data["option_id"]

        data = {}
        for key in all_data["cart"]:
            barcode = key
            quantity = all_data["cart"][key]
            product = Product.query.get(barcode)
            if int(quantity) > product.in_stock:
                quantity = product.in_stock
            data[barcode] = int(quantity)

        if "cart" in session:
            session["cart"] = [data]
        else:
            session["cart"] = [{}]

        return jsonify({"goto": url_for("shop.checkout")})


@module_blueprint.route("/checkout", methods=["GET", "POST"])
def checkout():
    context = mhelp.context()

    delivery_options = DeliveryOption.query.all()
    payment_options = PaymentOption.query.all()
    with open(
        os.path.join(
            current_app.config["BASE_DIR"],
            "modules",
            "shopman",
            "data",
            "country.json",
        )
    ) as f:
        countries = json.load(f)
    form = CheckoutForm()
    country_choices = [(c["name"], c["name"]) for c in countries]
    form.default_country.choices = country_choices
    form.diff_country.choices = country_choices

    if "checkout_data" not in session:
        checkout_data = {}
        for key in form._fields:
            checkout_data[key] = ""

        session["checkout_data"] = [{}]
        session["checkout_data"][0] = [checkout_data]
    else:
        checkout_data = session["checkout_data"][0]

    context.update(
        {
            "get_product": get_product,
            "delivery_options": delivery_options,
            "payment_options": payment_options,
            "form": form,
            "checkout_data": checkout_data,
        }
    )
    cart_info = get_cart_data()
    context.update(cart_info)
    return mhelp.render("checkout.html", **context)


@module_blueprint.route("/checkout/process", methods=["GET", "POST"])
def checkout_process():
    if request.method == "POST":
        cart_info = get_cart_data()
        if len(cart_info["cart_data"]) == 0:
            flash(notify_warning("Cart cannot be empty!"))
            return mhelp.redirect_url("shop.checkout")

        form = CheckoutForm()
        with open(
            os.path.join(
                current_app.config["BASE_DIR"],
                "modules",
                "shopman",
                "data",
                "country.json",
            )
        ) as f:
            countries = json.load(f)
        country_choices = [(c["name"], c["name"]) for c in countries]
        form.default_country.choices = country_choices
        form.diff_country.choices = country_choices
        # print(dir(form))
        # ordered dict print(form._fields[0][0])

        # print(form._fields['default_first_name'].data)

        checkout_data = {}
        for key in form._fields:
            checkout_data[key] = form._fields[key].data

        session["checkout_data"][0] = checkout_data

        print(request.form["paymentoption"])
        if form.validate_on_submit():
            if not form.diffAddress.data:
                first_name = form.default_first_name.data
                last_name = form.default_last_name.data
                country = form.default_country.data
                street = form.default_street.data
                town_city = form.default_town_city.data
                phone = form.default_phone.data
                email = form.default_email.data
                order_notes = form.default_order_notes.data

            elif form.diffAddress.data:
                first_name = form.diff_first_name.data
                last_name = form.diff_last_name.data
                country = form.diff_country.data
                street = form.diff_street.data
                town_city = form.diff_town_city.data
                phone = form.diff_phone.data
                email = form.diff_email.data
                order_notes = form.dif_order_notes.data

            billing_detail = BillingDetail()
            billing_detail.first_name = first_name
            billing_detail.last_name = last_name
            billing_detail.country = country
            billing_detail.street = street
            billing_detail.town_city = town_city
            billing_detail.phone = phone
            billing_detail.email = email
            billing_detail.order_notes = order_notes

            if form.createAccount.data:
                if not User.query.filter((User.email == email)).first():
                    user = User()
                    user.first_name = first_name
                    user.last_name = last_name
                    user.email = email
                    user.password = form.passoword.data
                    user.email_confirmed = True
                    user.email_confirm_date = datetime.now()

            order = Order()
            order.billing_detail = billing_detail
            shipping_option = DeliveryOption.query.get(request.form["deliveryoption"])
            order.shipping_option_name = shipping_option.option
            order.shipping_option_price = shipping_option.price
            payment_option = PaymentOption.query.get(request.form["paymentoption"])
            order.payment_option_name = payment_option.name
            order.payment_option_text = payment_option.text

            if current_user.is_authenticated:
                order.logged_in_customer_email = current_user.email

            if form.applyCoupon.data:
                order.coupon_string = form.coupon.data

            cart_info = get_cart_data()
            cart_data = cart_info["cart_data"]

            for barcode in cart_data:
                order_item = OrderItem()
                product = Product.query.get(barcode)
                order_item.barcode = barcode
                order_item.quantity = cart_data[barcode]
                order_item.price = product.selling_price
                order.order_items.append(order_item)

            order.insert()
            flash(notify_success("Great!"))
            context = mhelp.context()
            return render_template("shop/order_complete.html", **context)
        else:
            flash_errors(form)
        return mhelp.redirect_url("shop.checkout")
