from flask_wtf import FlaskForm

# from wtforms.validators import Length
# from wtforms.fields import EmailField
from wtforms import StringField
from wtforms import TextAreaField
from wtforms.validators import DataRequired


class AnnounceForm(FlaskForm):
    title = StringField(
        "Title",
        [DataRequired()],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )

    content = TextAreaField(
        "Content",
        [],
        render_kw={
            "class": "form-control",
            "rows": "20",
            "autocomplete": "off",
        },
    )
