from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Optional


class InventoryCountForm(FlaskForm):
    notes = TextAreaField("Notes", validators=[Optional()])
    submit = SubmitField("Save")
