
import os
import json

from flask import Blueprint
from flask import render_template
from flask import url_for
from flask import redirect
from flask import flash
from flask import request
from flask import session
from flask import jsonify

# # 
from shopyoapi.html import notify_success
from shopyoapi.forms import flash_errors

from shopyoapi.html import notify_success
from shopyoapi.html import notify_warning

from modules.product.models import Product
from modules.category.models import Category
from modules.category.models import SubCategory
from modules.shopman.models import DeliveryOption
from modules.shopman.models import PaymentOption

from .helpers import get_cart_data

from .models import Order
from .models import OrderItem
from .models import BillingDetail

from .forms import CheckoutForm

dirpath = os.path.dirname(os.path.abspath(__file__))
module_info = {}

with open(dirpath + "/info.json") as f:
    module_info = json.load(f)

globals()['{}_blueprint'.format(module_info["module_name"])] = Blueprint(
    "{}".format(module_info["module_name"]),
    __name__,
    template_folder="templates",
    url_prefix=module_info["url_prefix"],
)


def get_product(product_id):
    return Product.query.get(product_id)



module_blueprint = globals()['{}_blueprint'.format(module_info["module_name"])]

@module_blueprint.route("/page/<int:page>")
@module_blueprint.route("/")
def index(page=1):
    context = {}
    PAGINATION = 5
    end = page * PAGINATION
    start = end - PAGINATION
    # total_pages = (data.count_posts(name, data.STATE_PUBLISHED) // PAGINATION) + 1
    total_pages = (len(Product.query.all()) // PAGINATION) + 1
    products = Product.query.all()[::-1][start:end]

    cart_info = get_cart_data()

    context.update({
        'current_category_name': '',
        'total_pages': total_pages,
        'page': page,
        'products': products
        })
    context.update(cart_info)
    return render_template('shop/shop.html', **context)


@module_blueprint.route("/c/<category_name>")
def category(category_name):
    context = {}
    current_category = Category.query.filter(Category.name == category_name).first()

    cart_info = get_cart_data()

    context.update({
        'current_category': current_category,
        'current_category_name': current_category.name
        })
    context.update(cart_info)
    return render_template('shop/category.html', **context)


@module_blueprint.route("/sub/<subcategory_name>/page/<int:page>")
@module_blueprint.route("/sub/<subcategory_name>")
def subcategory(subcategory_name, page=1):
    context = {}
    PAGINATION = 5
    end = page * PAGINATION
    start = end - PAGINATION

    subcategory = SubCategory.query.filter(SubCategory.name == subcategory_name).first()
    products = subcategory.products[start:end]
    total_pages = (len(products) // PAGINATION) + 1
    current_category_name = subcategory.category.name
    subcategory_name = subcategory.name

    cart_info = get_cart_data()

    context.update({
        'subcategory': subcategory,
        'current_category_name': current_category_name,
        'total_pages': total_pages,
        'page': page,
        'products': products,
        'subcategory_name': subcategory_name
        })
    context.update(cart_info)
    return render_template('shop/subcategory.html', **context)


@module_blueprint.route("/product/<product_barcode>")
def product(product_barcode):
    context = {}
    product = Product.query.get(product_barcode)

    cart_info = get_cart_data()
    # 'cart_data': cart_data,
    # 'cart_items': cart_items,
    # 'cart_total_price': cart_total_price

    context.update({
        'product': product
        })
    context.update(cart_info)
    return render_template('shop/product.html', **context)


@module_blueprint.route("/cart/add/<product_barcode>", methods=['GET', 'POST'])
def cart_add(product_barcode):
    if request.method == 'POST':
        flash('')
        if 'cart' in session:

            barcode = request.form['barcode']
            quantity = int(request.form['quantity'])

            product = Product.query.get(barcode)

            data = session['cart'][0]
            if barcode not in data:
                data[barcode] = quantity
                session['cart'][0] = data
            elif barcode in data:
                updated_quantity = data[barcode]+quantity
                if updated_quantity > product.in_stock:
                    flash(notify_warning('Products in cart cannot be greater than product in stock'))
                    return redirect(url_for('shop.product', product_barcode=barcode))
                data[barcode] = updated_quantity
                session['cart'][0] = data


        else:
            # In this block, the user has not started a cart, so we start it for them and add the product. 
            session['cart'] = [{barcode: quantity}]

    return redirect(url_for('shop.product', product_barcode=barcode))


@module_blueprint.route("/cart/remove/<product_barcode>", methods=['GET', 'POST'])
def cart_remove(product_barcode):
    if 'cart' in session:

        data = session['cart'][0]
        if product_barcode in data:
            del data[product_barcode]
        flash(notify_success('Removed!'))
        return redirect(url_for('shop.cart'))

    else:
        # In this block, the user has not started a cart, so we start it for them and add the product. 
        return redirect(url_for('shop.cart'))



@module_blueprint.route("/cart", methods=['GET', 'POST'])
def cart():
    context = {}

    cart_info = get_cart_data()
    delivery_options = DeliveryOption.query.all()

    context.update({
        'delivery_options': delivery_options,
        'get_product': get_product
        })
    context.update(cart_info)
    return render_template('shop/view_cart.html', **context)


@module_blueprint.route("/cart/update", methods=['GET', 'POST'])
def cart_update():
    if request.method == 'POST':
        data = {}
        for key in request.form:
            if key.startswith('barcode'):
                barcode = request.form[key].strip()
                product = Product.query.get(barcode)

                number = key.split('_')[1]
                quantity = request.form['quantity_{}'.format(number)]
                if int(quantity) > product.in_stock:
                    quantity = product.in_stock
                data[barcode] = int(quantity)

        if 'cart' in session:
            session['cart'] = [data]
        else:
            session['cart'] = [{}]
        return redirect(url_for('shop.cart'))

# @module_blueprint.route("/session", methods=['GET', 'POST'])
# def session_view():
#     return str(session['cart'][0]) 
# 

@module_blueprint.route("/prepare/checkout", methods=['GET', 'POST'])
def prepare_checkout():
    if request.method == 'POST':
        # update cart

        all_data = request.get_json()
        session['option_id'] = all_data['option_id']

        data = {}
        for key in all_data['cart']:
            barcode = key
            quantity = all_data['cart'][key]
            product = Product.query.get(barcode);
            if int(quantity) > product.in_stock:
                quantity = product.in_stock
            data[barcode] = int(quantity)

        if 'cart' in session:
            session['cart'] = [data]
        else:
            session['cart'] = [{}]
        
        return jsonify({'goto': url_for('shop.checkout')})


@module_blueprint.route("/checkout", methods=['GET', 'POST'])
def checkout():
    context = {}
    delivery_options = DeliveryOption.query.all()
    payment_options = PaymentOption.query.all()
    form = CheckoutForm()
    

    if 'checkout_data' not in session:
        checkout_data = {}
        for key in form._fields:
            checkout_data[key] = ''

        session['checkout_data'] = [{}]
        session['checkout_data'][0] = [checkout_data]
    else:
        checkout_data = session['checkout_data'][0]

    context.update({
        'get_product': get_product,
        'delivery_options': delivery_options,
        'payment_options': payment_options,
        'form': form,
        'checkout_data': checkout_data
        })
    cart_info = get_cart_data()
    context.update(cart_info)
    return render_template('shop/checkout.html', **context)

@module_blueprint.route("/checkout/process", methods=['GET', 'POST'])
def checkout_process():
    if request.method == 'POST':
        form = CheckoutForm()
        # print(dir(form))
        # ordered dict print(form._fields[0][0])

        # print(form._fields['default_first_name'].data)

        checkout_data = {}
        for key in form._fields:
            checkout_data[key] = form._fields[key].data

        session['checkout_data'][0] = checkout_data

        print(request.form['deliveryoption'])
        if form.validate_on_submit():
            flash(notify_success('Great!'))
        else:
            flash_errors(form)
        return redirect(url_for('shop.checkout'))
