import json
import os
from typing import Any

import jinja2
from flask import Blueprint
from flask import Flask
from flask import current_app
from flask_uploads import DOCUMENTS
from flask_uploads import IMAGES
from flask_uploads import configure_uploads
from flask_uploads import UploadSet


info = {}
with open(os.path.dirname(os.path.abspath(__file__)) + os.sep + "box_info.json") as f:
    info = json.load(f)

default_config = {
    "SHOPYO_ECOMMERCE_URL": "/shopyo-ecommerce",
    "SHOPYO_ECOMMERCE_CURRENCY": "USD",
    "SHOPYO_ECOMMERCE_SECTION_NAME": "Shop",
    "SHOPYO_ECOMMERCE_ITEMS_PER_PAGE": 12,
    "SHOPYO_ECOMMERCE_ENABLE_WISHLIST": True,
    "SHOPYO_ECOMMERCE_ENABLE_REVIEWS": False,
    "SHOPYO_ECOMMERCE_CATEGORYPHOTOS_UPLOADSET": "categoryphotos",
    "SHOPYO_ECOMMERCE_SUBCATEGORYPHOTOS_UPLOADSET": "subcategoryphotos",
    "SHOPYO_ECOMMERCE_PRODUCTEXCEL_UPLOADSET": "productexcel",
    "SHOPYO_ECOMMERCE_PRODUCTPHOTOS_UPLOADSET": "productphotos",
    "SHOPYO_ECOMMERCE_UPLOADED_CATEGORYPHOTOS_DEST": "static/uploads/categoryphotos",
    "SHOPYO_ECOMMERCE_UPLOADED_SUBCATEGORYPHOTOS_DEST": "static/uploads/subcategoryphotos",
    "SHOPYO_ECOMMERCE_UPLOADED_PRODUCTEXCEL_DEST": "static/uploads/productexcel",
    "SHOPYO_ECOMMERCE_UPLOADED_PRODUCTPHOTOS_DEST": "static/uploads/productphotos",
}

categoryphotos = UploadSet("categoryphotos", IMAGES)
subcategoryphotos = UploadSet("subcategoryphotos", IMAGES)
productexcel = UploadSet("productexcel", DOCUMENTS)
productphotos = UploadSet("productphotos", IMAGES)

_pkg_dir = os.path.dirname(os.path.abspath(__file__))

blueprint_names = [
    "category",
    "customer",
    "demo",
    "inventory",
    "pos",
    "product",
    "purchase",
    "resource",
    "shop",
    "shopman",
    "vendor",
]


class ShopyoEcommerce:
    def __init__(self, app: Any = None) -> None:
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        if not hasattr(app, "extensions"):
            app.extensions = {}

        for key, value in default_config.items():
            app.config.setdefault(key, value)

        url_prefix = app.config.get("SHOPYO_ECOMMERCE_URL", "/shopyo-ecommerce")
        parent = Blueprint(
            "shopyo_ecommerce",
            __name__,
            url_prefix=url_prefix,
            template_folder="templates",
            static_folder="static",
        )

        for name in blueprint_names:
            mod = __import__(
                f"shopyo_ecommerce.{name}.view", fromlist=["module_blueprint"]
            )
            parent.register_blueprint(mod.module_blueprint)

        from shopyo_ecommerce.resource.models import Resource  # noqa: F401
        from shopyo_ecommerce.product.models import Product  # noqa: F401
        from shopyo_ecommerce.category.models import Category, SubCategory  # noqa: F401
        from shopyo_ecommerce.vendor.models import Vendor  # noqa: F401
        from shopyo_ecommerce.customer.models import Customer, CustomerGroup  # noqa: F401
        from shopyo_ecommerce.inventory.models import (  # noqa: F401
            Location, StockPerLocation, StockTransfer, StockTransferItem,
            InventoryCount, InventoryCountItem,
        )
        from shopyo_ecommerce.pos.models import Transaction, TransactionItem, Shift, QuickKey  # noqa: F401
        from shopyo_ecommerce.purchase.models import PurchaseOrder, PurchaseOrderItem  # noqa: F401
        from shopyo_ecommerce.shop.models import Order, OrderItem, BillingDetail  # noqa: F401
        from shopyo_ecommerce.shopman.models import DeliveryOption, PaymentOption, Coupon  # noqa: F401

        global_modules = [
            "shopyo_ecommerce.category.global",
            "shopyo_ecommerce.shop.global",
            "shopyo_ecommerce.product.global",
        ]

        for g_path in global_modules:
            try:
                mod = __import__(g_path, fromlist=["available_everywhere"])
                app.jinja_env.globals.update(mod.available_everywhere)
            except (ImportError, AttributeError):
                pass

        app.register_blueprint(parent)

        pkg_templates = os.path.join(_pkg_dir, "templates")
        if os.path.isdir(pkg_templates):
            current = app.jinja_loader
            if not isinstance(current, jinja2.ChoiceLoader):
                current = jinja2.ChoiceLoader([current])
                app.jinja_loader = current
            current.loaders.insert(0, jinja2.FileSystemLoader(pkg_templates))

        app.extensions["shopyo_ecommerce"] = self

        from shopyo_ecommerce import cli as shopyo_ecommerce_cli

        app.cli.add_command(shopyo_ecommerce_cli.cli)

        upload_set_names = {
            "categoryphotos": categoryphotos,
            "subcategoryphotos": subcategoryphotos,
            "productexcel": productexcel,
            "productphotos": productphotos,
        }
        base = app.config.get("BASE_DIR", os.getcwd())
        for name, uset in upload_set_names.items():
            config_key = f"SHOPYO_ECOMMERCE_UPLOADED_{name.upper()}_DEST"
            dest = app.config[config_key]
            if not os.path.isabs(dest):
                dest = os.path.join(base, dest)
            app.config[f"UPLOADED_{name.upper()}_DEST"] = dest
            configure_uploads(app, uset)

    def get_info(self):
        info_copy = dict(info)
        modules_info = {}
        base_url = current_app.config.get("SHOPYO_ECOMMERCE_URL", "/shopyo-ecommerce")
        for name in blueprint_names:
            info_path = os.path.join(_pkg_dir, name, "info.json")
            if os.path.exists(info_path):
                with open(info_path) as f:
                    mod_info = json.load(f)
                mod_info["url_prefix"] = base_url + mod_info.get("url_prefix", f"/{name}")
                modules_info[name] = mod_info
        info_copy["modules"] = modules_info
        return info_copy