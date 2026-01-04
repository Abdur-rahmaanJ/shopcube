<div align="center">



<img src="https://github.com/Abdur-rahmaanJ/shopcube/raw/dev/assets/logo.png" width="250" />

[![First Timers Only](https://img.shields.io/badge/first--timers--only-friendly-blue.svg)](https://www.firsttimersonly.com/)

🇲🇺 🇵🇰 🇳🇬 🇮🇳 🇻🇳 🇬🇭 🇬🇧

</div>

<div align="center">

[![Discord](https://img.shields.io/badge/chat%20on-discord-green.svg)](https://discord.gg/k37Ef6w)
[![CodeQL](https://github.com/shopyo/shopcube/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/shopyo/shopcube/actions/workflows/codeql-analysis.yml)

</div>

# shopcube

shopcube is an e-commerce solution for shops. Complete with

- cart
- wishlist
- orders
- upload by csv
- charts
- theming

If you want to contribute, go ahead, we welcome it. We follow a 100% first-timers-friendly policy. Join #shopcube on Discord if you get stuck or would just like to chat and say hi.

Powered by Shopyo, a Python web framework built on top of Flask.

## Quick Start

### Installation

Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/shopyo/shopcube.git
cd shopcube
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools
pip install -e .
```

### Initialisation

To set up the database and default settings without clearing existing migrations:

```bash
cd src/shopcube
shopyo initialise --no-clear-migration
```

### Running the Application

To run the development server:

```bash
flask run
```

Access the application at http://127.0.0.1:5000

Login as administrator:
- Email: admin@domain.com
- Password: pass

The dashboard is available at http://127.0.0.1:5000/dashboard/

## Deployment

For production deployment, use a WSGI server like Gunicorn.

### Example with Gunicorn

```bash
gunicorn --bind 0.0.0.0:8000 wsgi:application
```

Ensure you have a `config.json` in your execution directory. You can copy the demo config:

```bash
cp src/shopcube/config_demo.json config.json
```

## Development

### Running Tests

```bash
cd src/shopcube
python -m pytest
```

### Useful Commands

```bash
flask flight-info
```
