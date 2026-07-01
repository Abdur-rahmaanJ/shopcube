<div align="center">

<img src="https://github.com/Abdur-rahmaanJ/shopcube/raw/dev/assets/logo.png" width="250" />

contribs <br> 🇲🇺 🇵🇰 🇳🇬 🇮🇳 🇻🇳 🇬🇭 🇬🇧

[![First Timers Only](https://img.shields.io/badge/first--timers--only-friendly-blue.svg)](https://www.firsttimersonly.com/)

</div>

<div align="center">

[![Discord](https://img.shields.io/badge/chat%20on-discord-green.svg)](https://discord.gg/k37Ef6w)
[![CodeQL](https://github.com/shopyo/shopcube/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/shopyo/shopcube/actions/workflows/codeql-analysis.yml)

</div>

# ShopCube

E-commerce and POS platform built on the Shopyo Flask framework.

- [x] 🛒 cart
- [x] ⭐ wishlist
- [x] 📑 orders
- [x] 📤 upload by csv
- [ ] 📊 charts
- [x] 🖌️ theming

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install shopcube
```

Then initialise:

```bash
shopcube initialise
shopcube run
```

Dashboard: http://127.0.0.1:5000/dashboard -- Email: `admin@admin.com`, Password: `admin`

## Production

Git clone

```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:8000 shopcube.wsgi:application
```

For development:

```bash
pip install -e .
shopcube initialise
flask --debug run
```

Environment variables:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `SHOPCUBE_CONFIG` | Environment type (`production`, `development`, `testing`) | `production` |
| `SECRET_KEY` | Secret key for session encryption | Required |
| `SHOPCUBE_DATA_DIR` | Directory for database and uploads | Current directory |

## Features

### Inventory
- Products with barcode, images, colors, sizes, categories, subcategories, and vendors
- Low-stock alerts with configurable thresholds
- Stock adjustments with reason codes (manual, POS sale, return, count, PO receive)
- Purchase orders with draft, ordered, received lifecycle; auto-updates stock on receipt
- Vendor/supplier management with contact info
- Physical inventory counts with variance application
- Multi-location inventory with location management
- Stock transfers between locations
- Kit/bundle assembly from components
- Cost price and margin tracking
- Barcode label printing
- Inventory reports (valuation, low-stock, margin)

### POS
- Product grid with category filtering, search, and barcode scanning
- Cart with quantity controls and running total
- Discount (percentage or fixed amount)
- Order notes
- Payment methods: Cash, Card, Other
- Auto change calculation
- Quick keys for one-tap product add
- Transaction history
- Sales reports by date, total, payment method
- Returns with receipt lookup and stock reversal
- Shift management with cash reconciliation
- Cashier role for non-admin staff

### Customers
- Registration with email confirmation
- Order history per customer
- Customer groups with percentage discounts
- Customer Lifetime Value tracking (total spent, order count, AOV)

### Admin
- Product CRUD with images, colors, sizes, vendor assignment
- Category and subcategory management
- Coupon management
- Delivery and payment method configuration
- Order management with status tracking and email notifications
- Bulk product upload via Excel
- Role-based access control

### Security
- CSRF protection on all POST routes
- Admin-only access on management routes
- Login required for all management endpoints
- File upload type and size validation

Built on [Shopyo](https://shopyo.org) with isolated module architecture.

## E-Commerce Configuration

The `shopyo_ecommerce` module reads these Flask config keys. Defaults are applied automatically, override them in your `config.py` or instance config:

| Key | Default | Description |
|---|---|---|
| `SHOPYO_ECOMMERCE_URL` | `/shopyo-ecommerce` | URL prefix for all ecommerce routes |
| `SHOPYO_ECOMMERCE_CURRENCY` | `USD` | ISO 4217 currency code (e.g. `MUR`, `EUR`, `GBP`) |
| `SHOPYO_ECOMMERCE_SECTION_NAME` | `Shop` | Section name shown in dashboard and settings |
| `SHOPYO_ECOMMERCE_ITEMS_PER_PAGE` | `12` | Products per page in shop listings |
| `SHOPYO_ECOMMERCE_ENABLE_WISHLIST` | `True` | Enable/disable the wishlist feature |
| `SHOPYO_ECOMMERCE_ENABLE_REVIEWS` | `False` | Enable/disable product reviews |
| `SHOPYO_ECOMMERCE_CATEGORYPHOTOS_UPLOADSET` | `categoryphotos` | Flask-Uploads set name for category images |
| `SHOPYO_ECOMMERCE_SUBCATEGORYPHOTOS_UPLOADSET` | `subcategoryphotos` | Flask-Uploads set name for subcategory images |
| `SHOPYO_ECOMMERCE_PRODUCTEXCEL_UPLOADSET` | `productexcel` | Flask-Uploads set name for product Excel imports |
| `SHOPYO_ECOMMERCE_PRODUCTPHOTOS_UPLOADSET` | `productphotos` | Flask-Uploads set name for product images |
| `SHOPYO_ECOMMERCE_UPLOADED_CATEGORYPHOTOS_DEST` | `static/uploads/categoryphotos` | Upload destination for category images |
| `SHOPYO_ECOMMERCE_UPLOADED_SUBCATEGORYPHOTOS_DEST` | `static/uploads/subcategoryphotos` | Upload destination for subcategory images |
| `SHOPYO_ECOMMERCE_UPLOADED_PRODUCTEXCEL_DEST` | `static/uploads/productexcel` | Upload destination for product Excel files |
| `SHOPYO_ECOMMERCE_UPLOADED_PRODUCTPHOTOS_DEST` | `static/uploads/productphotos` | Upload destination for product images |

**Example:**

```python
class Config:
    SHOPYO_ECOMMERCE_URL = "/shop"
    SHOPYO_ECOMMERCE_CURRENCY = "MUR"
    SHOPYO_ECOMMERCE_ITEMS_PER_PAGE = 24
    SHOPYO_ECOMMERCE_ENABLE_WISHLIST = False
    SHOPYO_ECOMMERCE_UPLOADED_PRODUCTPHOTOS_DEST = "/data/uploads/products"
```

Currency symbols are resolved from the ISO 4217 code via the `iso4217parse` package (e.g. `MUR` -> `₨`, `EUR` -> `€`).
