#
#
#

from werkzeug.exceptions import NotImplemented

from flask import Blueprint, flash, render_template, request

from COMPHUB.public.forms import AppointmentForm
from COMPHUB.admin.models import Appointment, Customer

from COMPHUB.utilities import flash_form_errors

blueprint = Blueprint("public", __name__, static_folder = "../static")

#
#
#
@blueprint.route('/', methods=['GET', 'POST'])
def index():
    form = AppointmentForm(request.form)

    if request.method == 'POST' and form.validate_on_submit():

        if not form.tos.data:
            flash('You must agree to the terms and conditions.', 'danger')
            return render_template('public/index.html', form=form)

        customers = Customer.query.filter(
            Customer.surname.like('%' + form.surname.data + '%')
        ).order_by(Customer.surname).all()

        devices = form.hardware.data.split('/')

        if not customers:
            Customer.create(
                name=form.name.data.capitalize(),
                surname=form.surname.data.capitalize(),
                email=form.email.data.lower(),
                number=form.number.data,
                appointments=[Appointment(
                    date=form.date.data,
                    message=form.message.data,
                    hardware=devices[1],
                    device=devices[0]
                )]
            )
        else:
            for customer in customers:
                if form.name.data.lower() in customer.name.lower():
                    Appointment.create(
                        customer_id=customer.id,
                        date=form.date.data,
                        message=form.message.data,
                        hardware=devices[1],
                        device=devices[0]
                    )
        flash('Your message has been successfully send.', 'success')
    else:
        flash_form_errors(form)

    return render_template('public/index.html', form=form)
