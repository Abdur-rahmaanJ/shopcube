<div align="center">



<img src="https://github.com/Abdur-rahmaanJ/shopcube/raw/dev/assets/logo.png" width="250" />

[![First Timers Only](https://img.shields.io/badge/first--timers--only-friendly-blue.svg)](https://www.firsttimersonly.com/)

🇲🇺 🇵🇰 🇳🇬 🇮🇳 🇻🇳 🇬🇭 🇬🇧

</div>

<div align="center">

[![Discord](https://img.shields.io/badge/chat%20on-discord-green.svg)](https://discord.gg/k37Ef6w)
[![CodeQL](https://github.com/shopyo/shopcube/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/shopyo/shopcube/actions/workflows/codeql-analysis.yml)

</div>

# ShopCube

ShopCube is a high-performance, minimalist e-commerce and POS solution. Designed for clarity, speed, and ease of use.

## Installation

### 1. Install via PyPI
You can install ShopCube directly into your virtual environment without cloning the repository.

```bash
python3 -m venv venv
source venv/bin/activate
pip install shopcube
```

### 2. Initialise Workspace
Once installed, use the `shopcube` command to set up your database and assets in your current directory.

```bash
shopcube initialise
```

### 3. Run Locally
Launch the development server directly from the CLI.

```bash
shopcube run
```

Access the dashboard at [http://127.0.0.1:5000/dashboard](http://127.0.0.1:5000/dashboard)
- **Email:** `admin@admin.com`
- **Password:** `admin`

## Production Deployment

When installed via pip, you can deploy using **Gunicorn** by referencing the internal WSGI entry point.

### Running with Gunicorn

```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:8000 shopcube.wsgi:application
```

## Advanced Usage

### Custom Project Directory
If you want to create a full editable copy of the shopcube source in a specific folder:

```bash
shopcube create my_store
cd my_store
# You now have the full source code and templates to customize
```

### Environment Variables
Configure your production environment:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `SHOPCUBE_CONFIG` | Environment type (`production`, `development`, `testing`) | `production` |
| `SECRET_KEY` | Secret key for session encryption | *Required* |
| `SHOPCUBE_DATA_DIR` | Directory for database and uploads | Current Directory |

---

Designed with precision for the modern shop.

## Features

### Inventory Management
- **Product catalog** with barcode, images, colors, sizes, categories, and subcategories
- **Low-stock alerts** — configurable `min_stock` threshold per product; visual badge in POS
- **Stock adjustments with reason codes** — audit trail for all stock changes (manual edit, POS sale, return, count, PO receive)
- **Purchase Orders** — full PO lifecycle (draft → ordered → received); vendor-linked; auto-updates stock on receipt
- **Vendor/Supplier management** — CRUD with contact info; link products to vendors
- **Physical inventory counts** — generate count sheets; record actual qty; auto-apply variances
- **Kit/Bundle management** — assemble products from components; track component stock
- **Barcode label printing** — print-ready label sheets
- **Cost price & margin tracking** — per-product cost tracking; potential margin reports
- **Inventory reports** — valuation at cost and retail; low-stock and out-of-stock views

### Point of Sale (POS)
- **Intuitive grid layout** with category filtering, search, and barcode scanning
- **Cart management** with quantity controls, line-item display, and running total
- **Discount at POS** — percentage or fixed amount; server-side validated
- **Order notes** — optional text memo attached to each transaction
- **Payment method selector** — Cash, Card, Other
- **Change calculation** — auto-computed from amount received
- **Transaction history** with full audit trail
- **Sales reports** — date-filtered summaries by total, transaction count, and payment method
- **Return with receipt lookup** — search by receipt number; reverses stock
- **Shift management** — open/close workflow; tracks starting cash, expected vs actual, variance
- **Low-stock visual warning** — gold border + quantity badge in product grid

### Customer Management
- **Customer accounts** with registration, email confirmation, login/logout
- **Order history** — per-customer view of past orders
- **Customer groups/tiers** — configurable groups with % discount
- **Customer Lifetime Value (CLV)** — total spent, order count, average order value, last purchase date

### Admin Dashboard
- **Product CRUD** — add/edit/delete with images, colors, sizes, vendor assignment
- **Category management** — hierarchical categories and subcategories
- **Coupon management** — configurable discount coupons
- **Delivery & Payment options** — configure available methods
- **Order management** — status tracking (pending → processing → shipped → cancelled/refunded); email notifications
- **Bulk product upload** — via Excel spreadsheet
- **Role-based access** — `@admin_required` on all management routes

### Security
- **CSRF protection** on all POST routes
- **Admin-only access** enforced via `admin_required` decorator
- **Login required** for all management endpoints
- **File upload validation** — type and size restrictions
- **SQLAlchemy ORM** with parameterized queries (no raw SQL)

### Modular Architecture
- Built on [Shopyo](https://shopyo.org) framework
- Fully isolated modules (`box__ecommerce/*`) with independent models, views, and templates
- Event-driven inter-module communication
- Extensible — add custom modules via `shopyo startapp`
