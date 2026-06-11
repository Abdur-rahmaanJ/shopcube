from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, IntegerField, DecimalField, FieldList, FormField
from wtforms.validators import DataRequired, Optional, NumberRange


class PurchaseOrderForm(FlaskForm):
    vendor_id = SelectField("Vendor", coerce=int, validators=[Optional()])
    notes = TextAreaField("Notes", validators=[Optional()])
    submit = SubmitField("Save")


class PurchaseOrderItemForm(FlaskForm):
    product_barcode = StringField("Barcode", validators=[DataRequired()])
    product_name = StringField("Product Name", validators=[Optional()])
    quantity_ordered = IntegerField("Quantity", validators=[DataRequired(), NumberRange(min=1)], default=1)
    unit_price = DecimalField("Unit Price", validators=[Optional()], default=0)
