from flask import (
    Blueprint, render_template, request, redirect, url_for, jsonify
    )
from views.products.models import Product
from views.settings.models import Settings
from views.manufacturer.models import Manufacturer
from addon import db, ma

from flask_login import login_required, current_user

from project_api import base_context
from sqlalchemy import exists

prod_blueprint = Blueprint('prods', __name__, url_prefix='/prods')


class Productchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('barcode',
                  'price',
                  'vat_price',
                  'selling_price',
                  'manufacturer')


product_schema = Productchema()
product_schema = Productchema(many=True)


@prod_blueprint.route("/list_prods/<manufac_name>")
@login_required
def list_prods(manufac_name):
    context = base_context()

    manufac = Manufacturer.query.filter(
        Manufacturer.name == manufac_name).first()
    context['prods'] = manufac.products
    context['manufac'] = manufac_name
    return render_template('prods/list.html', **context)


@prod_blueprint.route('/add/<manufac_name>', methods=['GET', 'POST'])
@login_required
def prods_add(manufac_name):
    context = base_context()

    has_product = False
    if request.method == 'POST':
        barcode = request.form['barcode']
        price = request.form['price']
        vat_price = request.form['vat_price']
        selling_price = request.form['selling_price']
        manufacturer = Manufacturer.query.filter(
            Manufacturer.name == manufac_name).first()
        has_product = db.session.query(exists().where(
            Product.barcode == barcode)).scalar()
        if has_product == False:
            p = Product()
            p.barcode = barcode
            p.price = price
            p.vat_price = vat_price
            p.selling_price = selling_price
            p.manufacturer = manufacturer.id
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

    p = Product.query.filter(
        Product.barcode == barcode and Product.manufacturer == manufac_name
    ).first()

    context['barcode'] = p.barcode
    context['price'] = p.price
    context['vat_price'] = p.vat_price
    context['selling_price'] = p.selling_price
    context['manufac'] = manufac_name
    return render_template('prods/edit.html', **context)


@prod_blueprint.route('/update', methods=['GET', 'POST'])
@login_required
def prods_update():
    # this block is only entered when the form is submitted
    if request.method == 'POST':
        barcode = request.form['barcode']
        oldbarcode = request.form['oldbarcode']
        price = request.form['price']
        vat_price = request.form['vat_price']
        selling_price = request.form['selling_price']
        manufacturer = request.form['manufac']

        p = Product.query.filter(
            Product.barcode == oldbarcode and Product.manufacturer == manufac
        ).first()
        p.barcode = barcode
        p.price = price
        p.vat_price = vat_price
        p.selling_price = selling_price
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
            (Product.manufacturer == manufac_name)
        ).all()
    result = product_schema.dump(all_p)
    return jsonify(result.data)

# api
@prod_blueprint.route("/check/<barcode>", methods=["GET"])
@login_required
def check(barcode):
    has_product = db.session.query(exists().where(
        Product.barcode == barcode)).scalar()
    return jsonify({"exists": has_product})
