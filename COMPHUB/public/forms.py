#
#
#

import datetime
import phonenumbers

from flask_wtf import FlaskForm

from wtforms import BooleanField, DateField, EmailField, StringField, TelField, TextAreaField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, Email, Length

#
#
#
class AppointmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=32)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=2, max=32)])
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(min=8, max=120)])
    number = TelField('Phone', validators=[Length(max=13)])
    message = TextAreaField('Message', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    hardware = SelectField('Hardware', choices=
        [
            ('Desktop/iMac',    'iMac'),
            ('Mobile/iPhone',   'iPhone'),
            ('Laptop/MacBook',  'MacBook'),
            ('Mobile/Android',  'Android'),
            ('Desktop/PC',      'PC'),
            ('Laptop/Laptop',   'Laptop'),
        ]
    )
    tos = BooleanField('checkTOS', default=True)

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)

    def validate(self, extra_validators=None):
        initialize = super(AppointmentForm, self).validate()

        if not initialize:
            return False

        if self.number.data:
            if not phonenumbers.is_valid_number(
                phonenumbers.parse(
                    self.number.data, 'GB'
            )):
                self.number.errors.append('Invalid phone number.')
                return False

        if self.date.data < datetime.date.today():
            self.date.errors.append('The date cannot be in the past.')
            return False

        return True
