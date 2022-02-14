#
#
#

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class SearchForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=120)])

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)

    def validate(self):
        return True
