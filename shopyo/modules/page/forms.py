from flask_wtf import FlaskForm

# from wtforms.validators import Length
# from wtforms.fields.html5 import EmailField
from wtforms import PasswordField
from wtforms import SelectField
from wtforms import StringField
from wtforms import SubmitField
from wtforms import TextAreaField
from wtforms import TextField
from wtforms.validators import DataRequired

from shopyoapi.validators import verify_slug


class PageForm(FlaskForm):

    content = TextAreaField(
        "Content",
        [],
        render_kw={
            "class": "form-control",
            "rows": "20",
            "autocomplete": "off",
        },
    )
    slug = StringField(
        "Slug",
        [DataRequired(), verify_slug],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    title = StringField(
        "Title",
        [DataRequired()],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
