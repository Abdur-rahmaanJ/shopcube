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
