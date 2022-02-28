#
#
#

from flask import flash

#
#
#
def flash_form_errors(form, category='danger'):
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{ getattr(form, field).label.text } - { error }', category)

#
#
#
def datetime_filter(value, format='%a %b %d %Y'):
    return value.strftime(format)
