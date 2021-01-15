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


class AnnounceForm(FlaskForm):

    content = TextAreaField(
        "Content",
        [],
        render_kw={
            "class": "form-control",
            "rows": "20",
            "autocomplete": "off",
        },
    )
    title = StringField(
        "Title",
        [DataRequired()],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
