from flask import (
    Blueprint, render_template, request, redirect, url_for, jsonify
    )
from models import app, db, Products, Settings
from flask_marshmallow import Marshmallow
from settings import get_value

prod_blueprint = Blueprint('prods', __name__, url_prefix='/prods')

ma = Marshmallow(app)

class ProductSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('barcode', 'price', 'vat_price', 'selling_price', 'manufacturer')

product_schema = ProductSchema()
product_schema = ProductSchema(many=True)


@prod_blueprint.route("/list_prods/<manufac_name>")
def list_prods(manufac_name):
    products = Products.query.filter_by(manufacturer=manufac_name)
    return render_template('prods_list.html', prods=products, manufac=manufac_name, 
        OUR_APP_NAME=get_value('OUR_APP_NAME'), SECTION_ITEMS=get_value('SECTION_ITEMS'),
        SECTION_NAME=get_value('SECTION_NAME'))


@prod_blueprint.route('/add/<manufac_name>', methods=['GET', 'POST'])
def prods_add(manufac_name):
    if request.method == 'POST':
        barcode = request.form['barcode']
        price = request.form['price']
        vat_price = request.form['vat_price']
        selling_price = request.form['selling_price']
        manufac = request.form['manufac']
        p = Products(barcode=barcode, price=price, vat_price=vat_price,
            selling_price=selling_price, manufacturer=manufac)
        db.session.add(p)
        db.session.commit()
        return redirect('/prods/add/{}'.format(manufac_name))
    return render_template('prods_add.html', manufac=manufac_name, OUR_APP_NAME=get_value('OUR_APP_NAME'),
        SECTION_ITEMS=get_value('SECTION_ITEMS'))


@prod_blueprint.route('/delete/<manufac_name>/<barcode>', methods=['GET', 'POST'])
def prods_delete(manufac_name, barcode):
    Products.query.filter(
        Products.barcode == barcode and Products.manufacturer == manufac_name).delete()
    db.session.commit()
    return redirect('/prods/list_prods/{}'.format(manufac_name))


@prod_blueprint.route('/edit/<manufac_name>/<barcode>', methods=['GET', 'POST'])
def prods_edit(manufac_name, barcode):
    p = Products.query.filter(
        Products.barcode == barcode and Products.manufacturer == manufac_name
        ).first()
    return render_template(
        'prods_edit.html', barcode=p.barcode, price=p.price, vat_price=p.vat_price,
        selling_price=p.selling_price, manufac=manufac_name, OUR_APP_NAME=get_value('OUR_APP_NAME'),
        SECTION_ITEMS=get_value('SECTION_ITEMS'))


@prod_blueprint.route('/update', methods=['GET', 'POST'])
def prods_update():
    if request.method == 'POST': #this block is only entered when the form is submitted
        barcode = request.form['barcode']
        oldbarcode = request.form['oldbarcode']
        price = request.form['price']
        vat_price = request.form['vat_price']
        selling_price = request.form['selling_price']
        manufacturer = request.form['manufac']

        p = Products.query.filter(
            Products.barcode == oldbarcode and Products.manufacturer == manufac
        ).first()
        p.barcode = barcode
        p.price = price
        p.vat_price = vat_price
        p.selling_price = selling_price
        p.manufacturer = manufacturer
        db.session.commit()
        #return redirect(url_for('edit', barcode=barcode))
        return redirect('/prods/list_prods/{}'.format(manufacturer))

@prod_blueprint.route("/lookup/<manufac_name>")
def lookup_prods(manufac_name):
    return render_template('prods_lookup.html', manufac=manufac_name, OUR_APP_NAME=get_value('OUR_APP_NAME'),
        SECTION_ITEMS=get_value('SECTION_ITEMS'))

# api
@prod_blueprint.route("/search/<manufac_name>/barcode/<barcode>", methods=["GET"])
def search(manufac_name, barcode):
    all_p = Products.query.filter(
            (Products.barcode.like('%'+barcode+'%')) & (Products.manufacturer == manufac_name)
        ).all()
    result = product_schema.dump(all_p)
    return jsonify(result.data)
