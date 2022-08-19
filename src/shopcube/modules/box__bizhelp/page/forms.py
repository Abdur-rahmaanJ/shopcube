from flask_wtf import FlaskForm
from shopyo.api.validators import verify_slug

# from wtforms.validators import Length
# from wtforms.fields import EmailField
from wtforms import StringField
from wtforms import TextAreaField
from wtforms.validators import DataRequired


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
