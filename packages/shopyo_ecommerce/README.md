# 🛒 Shopyo Ecommerce — Plug & Play Python Ecommerce for Shopyo

**shopyo-ecommerce** is a full-featured, plug-and-play ecommerce module for the [Shopyo](https://shopyo.readthedocs.io/) Flask framework. Add products, categories, variants, cart, checkout, and order management to your Shopyo app in minutes — no boilerplate, no fuss.

---

## ✨ Features

- **Product & Category Management** — CRUD for products and categories with image uploads
- **Inventory Tracking** — stock counts, low-stock alerts, and variant support
- **Shopping Cart** — session-based cart with quantity controls
- **Checkout Flow** — address collection, order summary, and payment integration hooks
- **Order Dashboard** — admin order management with status tracking
- **POS Interface** — point-of-sale view for in-person transactions
- **RESTful API** — JSON endpoints for headless or mobile frontends
- **Shopyo Native** — respects Shopyo's theming, auth, dashboard, and settings

---

## 🚀 Quick Start

```bash
pip install shopyo-ecommerce
```

Then initialise it in your Shopyo app factory:

```python
from shopyo_ecommerce import ShopyoEcommerce

def create_app():
    app = Flask(__name__)
    # ... load extensions ...
    ShopyoEcommerce(app)
    return app
```

That's it. The ecommerce sub-modules (shop, pos, orders, etc.) will appear automatically in the dashboard and be ready at their default routes.

## 🎨 Available Themes

**shopyo-ecommerce** bundles two themes:

| Theme | Kind | Namespaced Name | Description |
|---|---|---|---|
| `ecommerceus` | Front (storefront) | `shopyo_ecommerce/ecommerceus` | A clean product showcase theme for your online store |
| `sneatlike` | Back (admin panel) | `shopyo_ecommerce/sneatlike` | A lightweight admin back-office theme (52 KB, no external deps) |

Set the active theme in your config:

```python
SHOPYO_THEME_FRONT_DEFAULT = "shopyo_ecommerce/ecommerceus"
SHOPYO_THEME_BACK_DEFAULT  = "shopyo_ecommerce/sneatlike"
```

### Theme Commands

Copy a front theme into your project so you can customise it:

```bash
flask shopyo-ecommerce copy front ecommerceus
```

To overwrite an already-copied theme (backup first if needed):

```bash
flask shopyo-ecommerce update front ecommerceus
```

The copied theme lands at `static/themes/front/ecommerceus/` and becomes available in the Shopyo theme picker.

---

## 📦 What's Inside

| Sub-module | Route Prefix | Description |
|---|---|---|
| `shop` | `/shop` | Product listing, detail, cart, checkout |
| `pos` | `/pos` | Point-of-sale interface |
| `category` | `/category` | Category management |
| `product` | `/product` | Product management |
| `order` | `/order` | Order management |
| `delivery` | `/delivery` | Delivery configuration |
| `payment` | `/payment` | Payment gateway hooks |
| `resource` | `/resource` | Image & asset serving |

---

## 🔧 Configuration

All settings are configured via Flask app config keys. Set them in your `config.py` or before calling `ShopyoEcommerce(app)`.

| Config Key | Default | Description |
|---|---|---|
| `SHOPYO_ECOMMERCE_URL` | `/shopyo-ecommerce` | URL prefix for all ecommerce routes |
| `SHOPYO_ECOMMERCE_CURRENCY` | `USD` | Default currency code (e.g. `USD`, `EUR`, `MUR`) |
| `SHOPYO_ECOMMERCE_SECTION_NAME` | `Shop` | Name shown in dashboard & settings for the ecommerce section |
| `SHOPYO_ECOMMERCE_ITEMS_PER_PAGE` | `12` | Number of products per page in shop listings |
| `SHOPYO_ECOMMERCE_ENABLE_WISHLIST` | `True` | Enable/disable the wishlist feature |
| `SHOPYO_ECOMMERCE_ENABLE_REVIEWS` | `False` | Enable/disable product reviews |
| `SHOPYO_ECOMMERCE_CATEGORYPHOTOS_UPLOADSET` | `categoryphotos` | Flask-Uploads set name for category images |
| `SHOPYO_ECOMMERCE_SUBCATEGORYPHOTOS_UPLOADSET` | `subcategoryphotos` | Flask-Uploads set name for subcategory images |
| `SHOPYO_ECOMMERCE_PRODUCTEXCEL_UPLOADSET` | `productexcel` | Flask-Uploads set name for product Excel imports |
| `SHOPYO_ECOMMERCE_PRODUCTPHOTOS_UPLOADSET` | `productphotos` | Flask-Uploads set name for product images |
| `SHOPYO_ECOMMERCE_UPLOADED_CATEGORYPHOTOS_DEST` | `static/uploads/categoryphotos` | Upload destination for category images (relative paths resolved against `BASE_DIR`) |
| `SHOPYO_ECOMMERCE_UPLOADED_SUBCATEGORYPHOTOS_DEST` | `static/uploads/subcategoryphotos` | Upload destination for subcategory images |
| `SHOPYO_ECOMMERCE_UPLOADED_PRODUCTEXCEL_DEST` | `static/uploads/productexcel` | Upload destination for product Excel files |
| `SHOPYO_ECOMMERCE_UPLOADED_PRODUCTPHOTOS_DEST` | `static/uploads/productphotos` | Upload destination for product images |

**Example:**

```python
class Config:
    SHOPYO_ECOMMERCE_URL = "/shop"
    SHOPYO_ECOMMERCE_CURRENCY = "EUR"
    SHOPYO_ECOMMERCE_ITEMS_PER_PAGE = 24
    SHOPYO_ECOMMERCE_UPLOADED_PRODUCTPHOTOS_DEST = "/data/uploads/products"
```

---

## 🧪 Tested With

- Python 3.10+
- Shopyo 4.18+
- Flask 2+

---

## 🤝 Contributing

Found a bug? Want a feature? Open an issue at [github.com/shopcube/shopcube](https://github.com/shopcube/shopcube).

---

## 📄 License

BSD-3-Clause. See `LICENSE`.
