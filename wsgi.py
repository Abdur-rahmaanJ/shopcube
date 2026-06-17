import os
from .app import create_app

# Resolve instance path: default to 'instance' in current directory
# This allows users to pip install shopcube, then run gunicorn from their store directory
instance_path = os.environ.get("SHOPCUBE_INSTANCE_PATH", os.path.join(os.getcwd(), "instance"))
config_name = os.environ.get("SHOPCUBE_CONFIG", "production")

application = create_app(config_name=config_name, instance_path=instance_path)