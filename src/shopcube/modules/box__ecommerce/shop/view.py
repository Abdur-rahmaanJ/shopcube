import json
import os
from datetime import datetime

from flask import current_app
from flask import flash
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from flask_login import current_user

from shopyo.api.forms import flash_errors
from shopyo.api.html import notify_success
from shopyo.api.html import notify_warning
from shopyo.api.module import ModuleHelp
from utils.session import Cart
from shopyo.api.security import get_safe_redirect

from modules.box__default.admin.models import User
from modules.box__default.auth.email import send_async_email
from modules.box__default.settings.helpers import get_setting
from modules.box__ecommerce.category.models import Category
from modules.box__ecommerce.category.models import SubCategory
from modules.box__ecommerce.product.models import Product
from modules.box__ecommerce.shop.forms import CheckoutForm
from modules.box__ecommerce.shop.helpers import get_cart_data
from modules.box__ecommerce.shop.models import BillingDetail
from modules.box__ecommerce.shop.models import Order
from modules.box__ecommerce.shop.models import OrderItem
from modules.box__ecommerce.shopman.models import DeliveryOption
from modules.box__ecommerce.shopman.models import PaymentOption
from modules.box__ecommerce.shopman.models import Coupon
from modules.box__ecommerce.shop.helpers import get_min_max_subcateg

mhelp = ModuleHelp(__file__, __name__)
globals()[mhelp.blueprint_str] = mhelp.blueprint
module_blueprint = globals()[mhelp.blueprint_str]


# mhelp._context.update({"get_currency_symbol": get_currency_symbol})


def get_product(barcode):
    return Product.query.filter_by(barcode=barcode).first()


@module_blueprint.route("/home")
def homepage():
    # cant be defined above but must be manually set each time
    # active_theme_dir = os.path.join(
    #     dirpath, "..", "..", "themes", get_setting("ACTIVE_FRONT_THEME")
    # )
    # module_blueprint.template_folder = active_theme_dir

    # return str(module_blueprint.template_folder)
    context = mhelp.context()
    cart_info = get_cart_data()
    context.update(cart_info)
    return render_template(
        "ecommerceus/index.html", **context
    )


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

    min_price = None
    max_price = None

    def_min_price = min((p.selling_price for p in products))
    def_max_price = max((p.selling_price for p in products))
    filter_min_max = [def_min_price, def_max_price]
    if request.args.get('min') and request.args.get('max'):
        if request.args.get('min').isnumeric() and request.args.get('max').isnumeric():
            min_price = int(request.args.get('min'))
            max_price = int(request.args.get('max'))
            print(min_price, max_price)
            products = list((p for p in products if min_price <= p.selling_price <= max_price))
            products = products[start:end]
            filter_min_max = [min_price, max_price]

    cart_info = get_cart_data()

    min_max = [def_min_price, def_max_price]
    context.update(
        {
            "current_category_name": "",
            "total_pages": total_pages,
            "page": page,
            "products": products,
            "min_max": min_max,
            "filter_min_max": filter_min_max
        }
    )
    context.update(cart_info)
    return mhelp.render("shop.html", **context)


@module_blueprint.route("/c/<category_name>")
def category(category_name):

    context = mhelp.context()
    current_category = Category.query.filter(
        Category.name == category_name
    ).first()

    cart_info = get_cart_data()

    context.update(
        {
            "current_category": current_category,
            "current_category_name": current_category.name,
        }
    )
    context.update(cart_info)
    return mhelp.render("category.html", **context)


@module_blueprint.route("/sub/<sub_id>/page/<int:page>")
@module_blueprint.route("/sub/<sub_id>")
def subcategory(sub_id, page=1, methods=['GET']):
    context = mhelp.context()
    PAGINATION = 5
    end = page * PAGINATION
    start = end - PAGINATION

    subcategory = SubCategory.query.get(sub_id)
    subcategory_name = subcategory.name

    min_price = None
    max_price = None
    products = subcategory.products[start:end]
    filter_min_max = get_min_max_subcateg(subcategory_name)
    if request.args.get('min') and request.args.get('max'):
        if request.args.get('min').isnumeric() and request.args.get('max').isnumeric():
            min_price = int(request.args.get('min'))
            max_price = int(request.args.get('max'))
            print(min_price, max_price)
            products = list((p for p in subcategory.products if min_price <= p.selling_price <= max_price))
            products = products[start:end]
            filter_min_max = [min_price, max_price]
    
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
            "filter_min_max": filter_min_max
        }
    )
    context.update(cart_info)
    return mhelp.render("subcategory.html", **context)


@module_blueprint.route("/product/<product_barcode>")
def product(product_barcode):
    context = mhelp.context()
    product = Product.query.filter_by(barcode=product_barcode).first()

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

        barcode = request.form["barcode"]
        quantity = int(request.form["quantity"])
        size = request.form['size']
        color = request.form['color']

        item_info = {
            'quantity': quantity,
            'size': size,
            'color': color 
        }

        if Cart.add(barcode, item_info):
            return mhelp.redirect_url("shop.product", product_barcode=barcode)
        else:
            flash(
                notify_warning(
                    "Products in cart cannot be greater than product in stock"
                )
            )
            return redirect(
                url_for("shop.product", product_barcode=barcode)
            )
    


@module_blueprint.route(
    "/cart/remove/<product_barcode>/<size>/<color>", methods=["GET", "POST"]
)
def cart_remove(product_barcode, size, color):
    if "cart" in session:
        Cart.remove(product_barcode, size, color)
        flash(notify_success("Removed!"))
        return mhelp.redirect_url("shop.cart")

    else:
        return mhelp.redirect_url("shop.cart")


@module_blueprint.route("/cart", methods=["GET", "POST"])
def cart():
    context = mhelp.context()

    cart_info = get_cart_data()
    delivery_options = DeliveryOption.query.all()

    context.update(
        {"delivery_options": delivery_options, "get_product": get_product}
    )
    context.update(cart_info)
    return mhelp.render("view_cart.html", **context)


@module_blueprint.route("/cart/update", methods=["GET", "POST"])
def cart_update():
    if request.method == "POST":
        Cart.update(request.form)
        return mhelp.redirect_url("shop.cart")


# @module_blueprint.route("/session", methods=['GET', 'POST'])
# def session_view():
#     return str(session['cart'][0])
#




@module_blueprint.route("/checkout", methods=["GET", "POST"])
def checkout():
    context = mhelp.context()

    delivery_options = DeliveryOption.query.all()
    payment_options = PaymentOption.query.all()
    with open(
        os.path.join(
            current_app.config["BASE_DIR"],
            "modules",
            "box__ecommerce",
            "shopman",
            "data",
            "country.json",
        )
    ) as f:
        countries = json.load(f)
    form = CheckoutForm()
    # country_choices = [(c["name"], c["name"]) for c in countries]
    country_choices = [('mauritius', 'Mauritius')]
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
                "box__ecommerce",
                "shopman",
                "data",
                "country.json",
            )
        ) as f:
            countries = json.load(f)
        # country_choices = [(c["name"], c["name"]) for c in countries]
        # form.default_country.choices = country_choices
        # form.diff_country.choices = country_choices

        country_choices = [('mauritius', 'Mauritius')]
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
                    user.is_customer = True
                    user.email_confirm_date = datetime.now()

            order = Order()
            order.billing_detail = billing_detail
            shipping_option = DeliveryOption.query.get(
                request.form["deliveryoption"]
            )
            order.shipping_option = shipping_option
            payment_option = PaymentOption.query.get(
                request.form["paymentoption"]
            )
            order.payment_option = payment_option
            if current_user.is_authenticated:
                order.logged_in_customer_email = current_user.email

            if form.applyCoupon.data:
                coupon = Coupon.query.filter(
                    Coupon.string == form.coupon.data
                ).first()
                if coupon:
                    order.coupon = coupon
                else:
                    flash(notify_warning("Invalid Coupon"))

            cart_info = get_cart_data()
            cart_data = cart_info["cart_data"]

            for barcode in Cart.data()['items']:
                for item in Cart.data()['items'][barcode]:
                    order_item = OrderItem()
                    product = Product.query.filter_by(barcode=barcode).first()
                    order_item.barcode = barcode
                    order_item.quantity = int(item['quantity'])
                    order_item.size = item['size']
                    order_item.color = item['color']
                    order.order_items.append(order_item)

            template = "shop/emails/order_info"
            subject = "FreaksBoutique - Order Details"
            context = {}
            context.update({'order': order, 'int': int, 'sum': sum})
            send_async_email(email, subject, template, **context)

            order.insert()
            flash(notify_success("Great!"))
            context = mhelp.context()
            Cart.reset()
            return render_template("shop/order_complete.html", **context)
        else:
            flash_errors(form)
        return mhelp.redirect_url("shop.checkout")


@module_blueprint.route("/wishlist/toggle/<product_barcode>", methods=["GET"])
def wishlist_toggle(product_barcode):

    # next url hecks
    next_url = request.args.get("next")
    if next_url is None:
        next_url = '/'
    next_url = get_safe_redirect(next_url)

    # product checks
    product = Product.query.get(product_barcode)
    if product is None:
        return redirect(next_url)

    if 'wishlist' not in session:
        session['wishlist'] = []

    if product_barcode not in session['wishlist']:
        session['wishlist'].append(product_barcode)
        session.modified = True
    elif product_barcode in session['wishlist']:
        session['wishlist'].remove(product_barcode)
        session.modified = True

    return redirect(next_url)


@module_blueprint.route("/wishlist", methods=["GET"])
def wishlist():
    context = mhelp.context()
    context.update({
        'Product': Product
        })
    return mhelp.render('wishlist.html', **context)