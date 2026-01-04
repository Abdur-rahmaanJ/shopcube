from datetime import datetime
from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import login_required
from modules.box__default.appadmin.admin import admin_required
from modules.box__default.auth.decorators import check_confirmed
from shopyo.api.module import ModuleHelp

from init import db
from modules.box__ecommerce.product.models import Product
from modules.box__ecommerce.category.models import Category, SubCategory

mhelp = ModuleHelp(__file__, __name__)
globals()[mhelp.blueprint_str] = mhelp.blueprint
module_blueprint = globals()[mhelp.blueprint_str]


@module_blueprint.route("/")
def index():
    return mhelp.info['display_string']


@module_blueprint.route("/dashboard")
@login_required
@check_confirmed
@admin_required
def dashboard():
    context = mhelp.context()
    return mhelp.render("import_demo.html", **context)


@module_blueprint.route("/import", methods=["POST"])
@login_required
@check_confirmed
@admin_required
def do_import():
    # Demo Data
    demo_categories = {
        "Electronics": ["Laptops", "Smartphones", "Accessories"],
        "Groceries": ["Fruits", "Vegetables", "Dairy"],
        "Apparel": ["Men", "Women", "Kids"]
    }
    
    demo_products = [
        {"barcode": "1001", "name": "MacBook Pro M2", "price": 1999, "selling_price": 2100, "stock": 10, "subcat": "Laptops", "desc": "Powerful Apple laptop"},
        {"barcode": "1002", "name": "iPhone 15 Pro", "price": 999, "selling_price": 1099, "stock": 25, "subcat": "Smartphones", "desc": "Titanium design"},
        {"barcode": "1003", "name": "AirPods Pro", "price": 249, "selling_price": 279, "stock": 50, "subcat": "Accessories", "desc": "Magic noise cancellation"},
        {"barcode": "2001", "name": "Organic Bananas", "price": 0.5, "selling_price": 0.9, "stock": 100, "subcat": "Fruits", "desc": "Fresh organic bananas"},
        {"barcode": "2002", "name": "Whole Milk", "price": 1.2, "selling_price": 1.5, "stock": 40, "subcat": "Dairy", "desc": "1 Gallon Whole Milk"},
        {"barcode": "3001", "name": "Classic T-Shirt", "price": 15, "selling_price": 25, "stock": 200, "subcat": "Men", "desc": "100% Cotton"},
    ]

    try:
        for cat_name, subcats in demo_categories.items():
            category = Category.query.filter_by(name=cat_name.lower()).first()
            if not category:
                category = Category(name=cat_name)
                db.session.add(category)
                db.session.flush()
            
            for subcat_name in subcats:
                subcategory = SubCategory.query.filter_by(name=subcat_name.lower(), category_id=category.id).first()
                if not subcategory:
                    subcategory = SubCategory(name=subcat_name, category_id=category.id)
                    db.session.add(subcategory)

        db.session.commit()

        for p in demo_products:
            product = Product.query.filter_by(barcode=p['barcode']).first()
            if not product:
                subcat = SubCategory.query.filter_by(name=p['subcat'].lower()).first()
                product = Product(
                    barcode=p['barcode'],
                    name=p['name'],
                    price=p['price'],
                    selling_price=p['selling_price'],
                    in_stock=p['stock'],
                    description=p['desc'],
                    subcategory_id=subcat.id,
                    date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    discontinued=False
                )
                db.session.add(product)
        
        db.session.commit()
        flash("Demo data imported successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error importing demo data: {str(e)}", "danger")
    
    return redirect(url_for("dashboard.index"))
