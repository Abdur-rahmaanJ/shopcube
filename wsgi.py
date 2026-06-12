import os
import sys

# Ensure the shopcube package can be imported if running from source
# But if installed via pip, it will be in site-packages
try:
    from shopcube.app import create_app
except ImportError:
    sys.path.insert(0, os.path.join(os.getcwd(), 'src'))
    from shopcube.app import create_app

# Resolve instance path: default to 'instance' in current directory
# This allows users to pip install shopcube, then run gunicorn from their store directory
instance_path = os.environ.get("SHOPCUBE_INSTANCE_PATH", os.path.join(os.getcwd(), "instance"))
config_name = os.environ.get("SHOPCUBE_CONFIG", "production")

application = create_app(config_name=config_name, instance_path=instance_path)

# Auto-initialize database on first run (development only)
if config_name in ("development",):
    with application.app_context():
        import sqlalchemy as sa
        from flask import current_app
        db = current_app.extensions["sqlalchemy"]
        if hasattr(db, "db"):
            db = db.db
        inspector = sa.inspect(db.engine)
        if not inspector.has_table("settings"):
            print("Initialising database...")
            from flask_migrate import upgrade as migrate_upgrade
            import shopcube
            pkg_dir = os.path.dirname(shopcube.__file__)
            migrate_upgrade(directory=os.path.join(pkg_dir, "migrations"))
            from modules.box__default.settings.upload import upload as settings_upload
            settings_upload()
            from shopyo_auth.upload import upload as auth_upload
            application.config['SHOPYO_AUTH_SEED_ADMIN_EMAIL'] = 'admin@domain.com'
            application.config['SHOPYO_AUTH_SEED_ADMIN_PASSWORD'] = 'pass'
            auth_upload()
            print("Database initialised.")

    # Ensure required settings exist
    with application.app_context():
        from modules.box__default.settings.helpers import set_setting
        from shopyo_settings.helpers import get_setting
        if get_setting("ACTIVE_FRONT_THEME") is None:
            set_setting("ACTIVE_FRONT_THEME", "ecommerceus")
            print("Seeded ACTIVE_FRONT_THEME")
        if get_setting("ACTIVE_BACK_THEME") is None:
            set_setting("ACTIVE_BACK_THEME", "sneat")
            print("Seeded ACTIVE_BACK_THEME")
