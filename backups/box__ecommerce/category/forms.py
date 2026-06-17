from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from flask_wtf.file import FileField
from flask_wtf.file import FileRequired
from wtforms import SubmitField

from init import productexcel


class UploadProductForm(FlaskForm):
    product_file = FileField(
        "Product upload",
        validators=[
            FileAllowed(productexcel, "File must be in xls, xlsx, xlsm, xlsb, odf"),
            FileRequired("File was empty!"),
        ],
        render_kw={
            "class": "form-control",
            "autocomplete": "off",
            "id": "upload-product-input",
        },
    )
