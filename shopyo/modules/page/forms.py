from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import TextField
from wtforms import SelectField
# from wtforms.fields.html5 import EmailField
from wtforms import SubmitField
from wtforms import PasswordField
from wtforms.validators import DataRequired
# from wtforms.validators import Length
from wtforms import TextAreaField


class PageForm(FlaskForm):

    content = TextAreaField(
        "Content",
        [],
        render_kw={"class": "form-control", "rows": "20", "autocomplete": "off"},
    )

    title = StringField(
        "title",
        [DataRequired()],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
