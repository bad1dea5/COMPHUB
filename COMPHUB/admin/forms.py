#
#
#

import phonenumbers, sys

from flask_wtf import FlaskForm

from wtforms import DateField, EmailField, StringField, SelectField, TelField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Email, Length, Optional

#
#
#
class AppointmentForm(FlaskForm):
    customer_id = HiddenField()
    date = DateField('Date', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    hardware = SelectField('Hardware', choices=
        [
            ('None/None',    'None'),
            ('Desktop/iMac',    'iMac'),
            ('Mobile/iPhone',   'iPhone'),
            ('Laptop/MacBook',  'MacBook'),
            ('Mobile/Android',  'Android'),
            ('Desktop/PC',      'PC'),
            ('Laptop/Laptop',   'Laptop'),
        ]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, extra_validators=None):
        initialize = super(AppointmentForm, self).validate()

        if not initialize:
            return False

        return True

#
#
#
class CustomerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=32)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=2, max=32)])
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(min=8, max=120)])
    number = TelField('Phone', validators=[Length(max=13)])
    message = TextAreaField('Message')
    date = DateField('Date')
    comments = TextAreaField('Comments')
    hardware = SelectField('Hardware', validators=[Optional()], choices=
        [
            ('None/None',       'None'),
            ('Desktop/iMac',    'iMac'),
            ('Mobile/iPhone',   'iPhone'),
            ('Laptop/MacBook',  'MacBook'),
            ('Mobile/Android',  'Android'),
            ('Desktop/PC',      'PC'),
            ('Laptop/Laptop',   'Laptop'),
        ]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, extra_validators=None):
        initialize = super(CustomerForm, self).validate()

        if not initialize:
            return False

        if self.number.data:
            if not phonenumbers.is_valid_number(phonenumbers.parse(self.number.data, 'GB')):
                self.number.errors.append('Invalid phone number.')
                return False

        return True

#
#
#
