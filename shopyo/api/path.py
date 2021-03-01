import os

shopyoapi_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.dirname(shopyoapi_path)
static_path = os.path.join(root_path, "static")
modules_path = os.path.join(root_path, "modules")
themes_path = os.path.join(static_path, "themes")
