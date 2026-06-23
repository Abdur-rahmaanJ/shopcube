<div align="center">

<img src="https://github.com/Abdur-rahmaanJ/shopcube/raw/dev/assets/logo.png" width="250" />

[![First Timers Only](https://img.shields.io/badge/first--timers--only-friendly-blue.svg)](https://www.firsttimersonly.com/)

</div>

<div align="center">

[![Discord](https://img.shields.io/badge/chat%20on-discord-green.svg)](https://discord.gg/k37Ef6w)
[![CodeQL](https://github.com/shopyo/shopcube/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/shopyo/shopcube/actions/workflows/codeql-analysis.yml)

</div>

# ShopCube

E-commerce and POS platform built on the Shopyo Flask framework.

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

```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:8000 shopcube.wsgi:application
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