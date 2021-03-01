import json
import os

# from flask import render_template
from flask import Blueprint
from flask import current_app

# from flask import redirect
from flask import send_from_directory

# from flask import url_for

# from flask_login import login_required
# from PIL import Image as PILimage

# from shopyo.api.enhance import get_setting
# from shopyo.api.file import delete_file

# from modules.box__ecommerce.product.models import Product
# from modules.resource.models import Image

# from modules.resource.models import Resource

# from flask import flash
# from flask import request#
# from shopyo.api.html import notify_success
# from shopyo.api.forms import flash_errors


dirpath = os.path.dirname(os.path.abspath(__file__))
module_info = {}

with open(dirpath + "/info.json") as f:
    module_info = json.load(f)

globals()["{}_blueprint".format(module_info["module_name"])] = Blueprint(
    "{}".format(module_info["module_name"]),
    __name__,
    template_folder="templates",
    url_prefix=module_info["url_prefix"],
)


module_blueprint = globals()["{}_blueprint".format(module_info["module_name"])]


@module_blueprint.route("/")
def index():
    return module_info["display_string"]


@module_blueprint.route(
    "/theme/front/<active_theme>/styles.css", methods=["GET"]
)
def active_front_theme_css(active_theme):
    theme_dir = os.path.join(
        current_app.config["BASE_DIR"],
        "static",
        "themes",
        "front",
        active_theme,
    )
    # return theme_dir
    return send_from_directory(theme_dir, "styles.css")


@module_blueprint.route(
    "/theme/back/<active_theme>/styles.css", methods=["GET"]
)
def active_back_theme_css(active_theme):
    theme_dir = os.path.join(
        current_app.config["BASE_DIR"],
        "static",
        "themes",
        "back",
        active_theme,
    )
    # return theme_dir
    return send_from_directory(theme_dir, "styles.css")


# # Handles javascript image uploads from tinyMCE
# @module_blueprint.route("/upload/tinymce/image", methods=["POST"])
# @login_required
# def upload_tinymce_image():
#     # Kevin Foong
#     file = request.files.get("file")
#     if file:
#         filename = file.filename.lower()
#         fn, ext = filename.split(".")
#         # truncate filename (excluding extension) to 30 characters
#         fn = fn[:30]
#         filename = fn + "." + ext
#         if ext in ["jpg", "gif", "png", "jpeg"]:
#             try:
#                 # everything looks good, save file
#                 img_fullpath = os.path.join(
#                     current_app.config["UPLOADED_PATH_IMAGE"], filename
#                 )
#                 file.save(img_fullpath)
#                 # get the file size to save to db
#                 file_size = os.stat(img_fullpath).st_size
#                 size = 160, 160
#                 # read image into pillow
#                 im = PILimage.open(img_fullpath)
#                 # get image dimension to save to db
#                 file_width, file_height = im.size
#                 # convert to thumbnail
#                 im.thumbnail(size)
#                 thumbnail = fn + "-thumb.jpg"
#                 tmb_fullpath = os.path.join(
#                     current_app.config["UPLOADED_PATH_THUMB"], thumbnail
#                 )
#                 # PNG is index while JPG needs RGB
#                 if not im.mode == "RGB":
#                     im = im.convert("RGB")
#                 # save thumbnail
#                 im.save(tmb_fullpath, "JPEG")

#                 # save to db
#                 img = Image(
#                     filename=filename,
#                     thumbnail=thumbnail,
#                     file_size=file_size,
#                     file_width=file_width,
#                     file_height=file_height,
#                 )
#                 db.session.add(img)
#                 db.session.commit()
#             except IOError:
#                 output = make_response(404)
#                 output.headers["Error"] = (
#                     "Cannot create thumbnail for " + filename
#                 )
#                 return output
#             return jsonify({"location": filename})

#     # fail, image did not upload
#     output = make_response(404)
#     output.headers["Error"] = "Filename needs to be JPG, JPEG, GIF or PNG"
#     return output
