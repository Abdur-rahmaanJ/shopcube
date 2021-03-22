# """
# commandline utilities functions
# """
# import os
# import re
# import subprocess
# import sys
# import importlib

# from init import db
# from init import root_path
# from init import static_path
# from init import modules_path
# from shopyo.api.file import trymkdir
# from shopyo.api.file import trymkfile
# from shopyo.api.file import get_folders
# from shopyo.api.file import trycopytree
# from shopyo.api.file import tryrmcache
# from shopyo.api.file import tryrmfile
# from shopyo.api.file import tryrmtree


# def clean(app):
#     """
#     Deletes shopyo.db and migrations/ if present in current working directory.
#     Deletes all __pycache__ folders starting from current working directory
#     all the way to leaf directory.

#     Parameters
#     ----------
#         - app: flask app that that need to be cleaned

#     Returns
#     -------
#     None
#         ...

#     """
#     SEP_CHAR = "#"
#     SEP_NUM = 23

#     print(SEP_CHAR * SEP_NUM, end="\n\n")
#     print("Cleaning...")

#     # getting app context creates the shopyo.db file even if it is not present
#     with app.test_request_context():
#         db.drop_all()
#         db.engine.execute("DROP TABLE IF EXISTS alembic_version;")
#         print("[x] all tables dropped")

#     tryrmcache(os.getcwd(), verbose=True)
#     tryrmfile(os.path.join(os.getcwd(), "shopyo.db"), verbose=True)
#     tryrmtree(os.path.join(os.getcwd(), "migrations"), verbose=True)


# def initialise():
#     """
#     Create db, migrate, adds default users, add settings

#     Parameters
#     ----------


#     Returns
#     -------
#     None


#     """
#     SEP_CHAR = "#"
#     SEP_NUM = 23

#     print("Creating Db")
#     print(SEP_CHAR * SEP_NUM, end="\n\n")
#     subprocess.run(
#         [sys.executable, "manage.py", "db", "init"], stdout=subprocess.PIPE
#     )

#     print("Migrating")
#     print(SEP_CHAR * SEP_NUM, end="\n\n")
#     subprocess.run(
#         [sys.executable, "manage.py", "db", "migrate"], stdout=subprocess.PIPE
#     )
#     subprocess.run(
#         [sys.executable, "manage.py", "db", "upgrade"], stdout=subprocess.PIPE
#     )

#     print("Collecting static")
#     print(SEP_CHAR * SEP_NUM, end="\n\n")
#     subprocess.run(
#         [sys.executable, "manage.py", "collectstatic"], stdout=subprocess.PIPE
#     )

#     # Uploads
#     print("Uploads")
#     print(SEP_CHAR * SEP_NUM, end="\n\n")

#     for folder in os.listdir(os.path.join(root_path, "modules")):
#         if folder.startswith("__"):  # ignore __pycache__
#             continue
#         if folder.startswith("box__"):
#             # boxes
#             for sub_folder in os.listdir(
#                 os.path.join(root_path, "modules", folder)
#             ):
#                 if sub_folder.startswith("__"):  # ignore __pycache__
#                     continue
#                 elif sub_folder.endswith(".json"):  # box_info.json
#                     continue

#                 try:
#                     upload = importlib.import_module(
#                         "modules.{}.{}.upload".format(folder, sub_folder)
#                     )
#                     upload.upload()
#                 except ImportError as e:
#                     # print(e)
#                     pass
#         else:
#             # apps
#             try:
#                 upload = importlib.import_module(
#                     "modules.{}.upload".format(folder)
#                 )
#                 upload.upload()
#             except ImportError as e:
#                 # print(e)
#                 pass

#     print("Done!")


# def create_module(modulename, base_path=None):
#     """
#     creates module with the structure defined in the modules section in docs

#     Parameters
#     ----------
#     modulename: str
#         name of module, in alphanumeric-underscore

#     Returns
#     -------
#     None


#     """

#     if bool(re.match(r"^[A-Za-z0-9_]+$", modulename)) is False:
#         print(
#             "Error: modulename is not valid, please use alphanumeric\
#              and underscore only"
#         )
#         sys.exit()
#     print(f"creating module: {modulename}")
#     if not base_path:
#         base_path = f"modules/{modulename}"
#     trymkdir(base_path)
#     trymkdir(f"{base_path}/templates")
#     trymkdir(f"{base_path}/templates/{modulename}")
#     trymkdir(f"{base_path}/tests")
#     trymkdir(f"{base_path}/static")
#     test_func_content = """
# Please add your functional tests to this file.
# """
#     test_model_content = """
# Please add your models tests to this file.
# """
#     trymkfile(
#         f"{base_path}/tests/test_{modulename}_functional.py", test_func_content
#     )
#     trymkfile(
#         f"{base_path}/tests/test_{modulename}_models.py", test_model_content
#     )
#     view_content = """
# from shopyo.api.module import ModuleHelp
# # from flask import render_template
# # from flask import url_for
# # from flask import redirect
# # from flask import flash
# # from flask import request

# # from shopyo.api.html import notify_success
# # from shopyo.api.forms import flash_errors

# mhelp = ModuleHelp(__file__, __name__)
# globals()[mhelp.blueprint_str] = mhelp.blueprint
# module_blueprint = globals()[mhelp.blueprint_str]

# @module_blueprint.route("/")
# def index():
#     return mhelp.info['display_string']

# # If "dashboard": "/dashboard" is set in info.json
# #
# # @module_blueprint.route("/dashboard", methods=["GET"])
# # def dashboard():

# #     context = mhelp.context()

# #     context.update({

# #         })
# #     return mhelp.render('dashboard.html', **context)
# """
#     trymkfile(f"{base_path}/view.py", view_content)
#     trymkfile(f"{base_path}/forms.py", "")
#     trymkfile(f"{base_path}/models.py", "")
#     info_json_content = """{{
#         "display_string": "{0}",
#         "module_name":"{1}",
#         "type": "show",
#         "fa-icon": "fa fa-store",
#         "url_prefix": "/{1}",
#         "author": {{
#             "name":"",
#             "website":"",
#             "mail":""
#         }}
# }}""".format(
#         modulename.capitalize(), modulename
#     )
#     trymkfile(f"{base_path}/info.json", info_json_content)

#     trymkdir(f"{base_path}/templates/{modulename}/blocks")
#     trymkfile(f"{base_path}/templates/{modulename}/blocks/sidebar.html", "")
#     dashboard_file_content = """
# {% extends "base/module_base.html" %}
# {% set active_page = info['display_string']+' dashboard' %}
# {% block pagehead %}
# <title></title>
# <style>
# </style>
# {% endblock %}
# {% block sidebar %}
# {% include info['module_name']+'/blocks/sidebar.html' %}
# {% endblock %}
# {% block content %}
# <br>

# <div class="card">
#     <div class="card-body">

#     </div>
#  </div>
# {% endblock %}
# """
#     trymkfile(
#         f"{base_path}/templates/{modulename}/dashboard.html",
#         dashboard_file_content,
#     )
#     global_file_content = """
# available_everywhere = {

# }
# """
#     trymkfile(f"{base_path}/global.py", global_file_content)


# def create_box(name, verbose=False):
#     """
#     creates box with box_info.json

#     Parameters
#     ----------
#     name: str
#         name of box, in alphanumeric-underscore

#     Returns
#     -------
#     None


#     """
#     base_path = f"modules/box__{name}"
#     if os.path.exists(base_path):
#         print(
#             f"[ ] unable to create. Box {base_path} already exists!",
#             file=sys.stderr
#         )
#     else:
#         trymkdir(base_path, verbose=verbose)
#         info_json_content = """{{
#         "display_string": "{0}",
#         "box_name":"{1}",
#         "author": {{
#             "name":"",
#             "website":"",
#             "mail":""
#         }}
#     }}""".format(
#             name.capitalize(), name
#         )
#         trymkfile(
#             f"{base_path}/box_info.json",
#             info_json_content,
#             verbose=verbose
#         )


# def create_module_in_box(modulename, boxname):
#     """
#     creates module with the structure defined in the modules section in docs in
#     a box

#     Parameters
#     ----------
#     modulename: str
#         name of module, in alphanumeric-underscore

#     boxname: str
#         name of box, in alphanumeric-underscore

#     Returns
#     -------
#     None


#     """
#     box_path = os.path.join("modules", boxname)
#     module_path = os.path.join("modules", boxname, modulename)

#     if not boxname.startswith("box__"):
#         print(f"Invalid box {boxname}. Boxes should start with box__")

#     elif not os.path.exists(box_path):
#         print(f"Box {box_path} does not exists!")
#         available_boxes = "\n* ".join(
#             [f for f in os.listdir("modules/") if f.startswith("box__")]
#         )
#         print(f"Available boxes: \n* {available_boxes}")

#     elif os.path.exists(module_path):
#         print(f"Module {module_path} exists")

#     else:
#         print(f"Creating module {module_path}")
#         create_module(modulename, base_path=module_path)


# def collectstatic(target_module=None, static_path_=None, modules_path_=None):
#     """
#     Copies ``module/static`` into ``/static/modules/module``.
#     In static it becomes like
#     ::
#        static/
#             modules/
#                 box_something/
#                     modulename
#                 modulename2
#     Parameters
#     ----------
#     target_module: str
#         name of module, in alphanumeric-underscore,
#         supports ``module`` or ``box__name/module``
#     Returns
#     -------
#     None
#     """
#     if static_path_ is None:
#         static_path_ = static_path
#     if modules_path_ is None:
#         modules_path_ = modules_path
#     modules_path_in_static = os.path.join(static_path_, "modules")

#     if target_module is None:
#         # clear modules dir if exists.
#         tryrmtree(modules_path_in_static)
#         # look for static folders in all project
#         for folder in get_folders(modules_path_):
#             if folder.startswith("box__"):
#                 box_path = os.path.join(modules_path_, folder)
#                 for subfolder in get_folders(box_path):
#                     module_name = subfolder
#                     module_static_folder = os.path.join(
#                         box_path, subfolder, "static"
#                     )
#                     if not os.path.exists(module_static_folder):
#                         continue
#                     module_in_static_dir = os.path.join(
#                         modules_path_in_static, folder, module_name
#                     )
#                     trycopytree(module_static_folder, module_in_static_dir)
#             else:
#                 module_name = folder
#                 module_static_folder = os.path.join(
#                     modules_path_, folder, "static"
#                 )
#                 if not os.path.exists(module_static_folder):
#                     continue
#                 module_in_static_dir = os.path.join(
#                     modules_path_in_static, module_name
#                 )
#                 trycopytree(module_static_folder, module_in_static_dir)
#     else:
#         # copy only module's static folder
#         module_static_folder = os.path.join(
#             modules_path_, target_module, "static"
#         )
#         if os.path.exists(module_static_folder):
#             if target_module.startswith("box__"):
#                 if "/" in target_module:
#                     module_name = target_module
#                 else:
#                     print("Could not understand module name")
#                     sys.exit()
#             else:
#                 module_name = target_module
#             module_in_static_dir = os.path.join(
#                 modules_path_in_static, module_name
#             )
#             tryrmtree(module_in_static_dir)
#             trycopytree(module_static_folder, module_in_static_dir)
#         else:
#             print("Module does not exist")
