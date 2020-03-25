from flask import (
    Blueprint, render_template, request, redirect, url_for, jsonify
    )
from modules.products.models import Product
from modules.settings.models import Settings
from modules.manufacturer.models import Manufacturer
from addon import db, ma

from flask_login import login_required, current_user

from project_api import base_context
from project_api import get_setting
from sqlalchemy import exists

prod_blueprint = Blueprint('prods', __name__,
                           template_folder='templates',
                           url_prefix='/prods'
                           )


class Productchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('barcode',
                  'name',
                  'description',
                  'category',
                  'price',
                  'selling_price',
                  'in_stock',
                  'discontinued')


product_schema = Productchema()
product_schema = Productchema(many=True)


@prod_blueprint.route("/list_prods/<manufac_name>")
@login_required
def list_prods(manufac_name):
    context = base_context()

    manufac = Manufacturer.query.filter(
        Manufacturer.name == manufac_name).first()
    context['products'] = db.session.query(Product).all()
    context['manufac'] = manufac_name
    
    return render_template('prods/list.html', **context)


@prod_blueprint.route('/add/<manufac_name>', methods=['GET', 'POST'])
@login_required
def prods_add(manufac_name):
    context = base_context()

    has_product = False
    if request.method == 'POST':
        barcode = request.form['barcode']
        name = request.form['name']
        description = request.form['description']
        category = request.form['category']
        date = request.form['date']
        price = request.form['price']
        selling_price = request.form['selling_price']
        in_stock = request.form['in_stock']
        if request.form['discontinued'] == 'True':
            discontinued = True
        else:
            discontinued = False
        
        # manufacturer = Manufacturer.query.filter(
        #     Manufacturer.name == manufac_name).first()
        # print(manufacturer, manufac_name, manufacturer.name)
        has_product = db.session.query(exists().where(
            Product.barcode == barcode)).scalar()

        if has_product is False:
            p = Product(
                barcode=barcode,
                name=name,
                description=description,
                category=category,
                date=date,
                price=price,
                selling_price=selling_price,
                in_stock=in_stock,
                discontinued=discontinued,
                manufacturer_name=manufac_name)
            db.session.add(p)
            db.session.commit()
        context['manufac'] = manufac_name
        context['has_product'] = str(has_product)
        return render_template('prods/add.html', **context)

    context['manufac'] = manufac_name
    context['has_product'] = str(has_product)
    return render_template('prods/add.html', **context)


@prod_blueprint.route('/delete/<manufac_name>/<barcode>',
                      methods=['GET', 'POST'])
@login_required
def prods_delete(manufac_name, barcode):
    Product.query.filter(
        Product.barcode == barcode and
        Product.manufacturer == manufac_name).delete()
    db.session.commit()
    return redirect('/prods/list_prods/{}'.format(manufac_name))


@prod_blueprint.route('/edit/<manufac_name>/<barcode>', methods=['GET', 'POST'])
@login_required
def prods_edit(manufac_name, barcode):
    context = base_context()

    product = Product.query.filter(
        Product.barcode == barcode and Product.manufacturer == manufac_name
    ).first()

    context['product'] = product
    context['manufac'] = manufac_name
    return render_template('prods/edit.html', **context)


@prod_blueprint.route('/update', methods=['GET', 'POST'])
@login_required
def prods_update():
    # this block is only entered when the form is submitted
    if request.method == 'POST':
        barcode = request.form['barcode']
        old_barcode = request.form['old_barcode']
        manufacturer = request.form['manufac']

        name = request.form['name']
        description = request.form['description']
        category = request.form['category']
        date = request.form['date']
        price = request.form['price']
        selling_price = request.form['selling_price']
        in_stock = request.form['in_stock']
        if request.form['discontinued'] == 'True':
            discontinued = True
        else:
            discontinued = False

        p = Product.query.filter(
            Product.barcode == old_barcode and
            Product.manufacturer == manufacturer
        ).first()
        p.barcode = barcode
        p.name = name
        p.description = description
        p.category = category
        p.date = date
        p.price = price
        p.selling_price = selling_price
        p.in_stock = in_stock
        p.discontinued = discontinued
        p.manufacturer = manufacturer
        db.session.commit()
        return redirect('/prods/list_prods/{}'.format(manufacturer))


@prod_blueprint.route("/lookup/<manufac_name>")
@login_required
def lookup_prods(manufac_name):
    context = base_context()

    context['manufac'] = manufac_name

    return render_template('prods/lookup.html', **context)

# api
@prod_blueprint.route("/search/<manufac_name>/barcode/<barcode>",
                      methods=["GET"])
@login_required
def search(manufac_name, barcode):
    all_p = Product.query.filter(
            (Product.barcode.like('%'+barcode+'%')) &
            (Product.manufacturer_name == manufac_name)
        ).all()
    result = product_schema.dump(all_p)
    return jsonify(result)

# api
@prod_blueprint.route("/check/<barcode>", methods=["GET"])
@login_required
def check(barcode):
    has_product = db.session.query(exists().where(
        Product.barcode == barcode)).scalar()
    return jsonify({"exists": has_product})
