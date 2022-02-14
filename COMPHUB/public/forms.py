#
#
#

import phonenumbers

from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    TelField, 
    SelectField,
    SubmitField,
    TextAreaField,
    DateField
)
from wtforms.validators import DataRequired, Email, Length

class RepairForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=120)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=120)])
    number = TelField('Phone', validators=[Length(min=11, max=13)])
    hardware = SelectField('Hardware', choices=[
        ('PC', 'PC'),
        ('Laptop', 'Laptop'),
        ('Mobile', 'Mobile'),
        ('iMac', 'iMac'),
        ('MacBook', 'MacBook'),
        ('iPhone', 'iPhone'),
    ])

    message = TextAreaField('Message', validators=[DataRequired()], render_kw={"placeholder": "Message"})
    datetime = DateField('Date', validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(RepairForm, self).__init__(*args, **kwargs)

    def validate(self):
        if self.number.data:
            if phonenumbers.is_valid_number(phonenumbers.parse(self.number.data, "GB")):
                return True
            else:
                return False
        return True
