import os
import sys

sys.path.append(os.getcwd())
from app import create_app


# CONFIG_JSON_PATH = os.path.dirname(os.path.abspath(__file__))


# try:
#     if not os.path.exists("config.json"):
#         trycopy("config_demo.json", "config.json")
# except Exception as e:
#     print(e)
#     sys.exit(1)

# with open(os.path.join(CONFIG_JSON_PATH, "config.json")) as f:
#     config_json = json.load(f)

# environment = config_json["environment"]
app = create_app("production")
