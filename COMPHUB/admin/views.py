#
#
#

import datetime, sys

from werkzeug.exceptions import NotFound
from flask import Blueprint, redirect, render_template, jsonify, flash, url_for, request

from COMPHUB.admin.models import Customer, Appointment
from COMPHUB.admin.forms import CustomerForm, AppointmentForm
from COMPHUB.utilities import flash_form_errors

blueprint = Blueprint("admin", __name__, static_folder = "../static")

#
#
#
@blueprint.route('/admin')
def index():
    customerNewForm = CustomerForm()
    appointments = Appointment.query.filter(
        Appointment.date > datetime.datetime.utcnow()
    ).limit(5).all()
    customers = []

    for appointment in appointments:
        customers.append(Customer.query.get(appointment.customer_id))

    return render_template('admin/index.html',
        customerNewForm=customerNewForm,
        next={ 'appointments': appointments, 'customers': customers }
    )

#
#
#
@blueprint.route('/admin/customers/<int:page>')
def get_customers(page):
    customers = Customer.query.order_by(Customer.surname.asc()).paginate(page, 15, error_out=False)
    data = {
        'customers': [],
        'page': {
            'id': customers.page,
            'pages': customers.pages,
            'total': customers.total,
            'next_num': customers.next_num,
            'prev_num': customers.prev_num,
            'has_next': customers.has_next,
            'has_prev': customers.has_prev,
        }
    }

    for customer in customers.items:
        data['customers'].append(customer.jsonify)

    return jsonify(data)

#
#
#
@blueprint.route('/admin/customer/search/<name>')
def customer_search(name):
    data = []

    customers = Customer.query.filter(
        Customer.name.like('%' + name + '%')
    ).order_by(Customer.name).all()

    for customer in customers:
        data.append({
            'id': customer.id,
            'name': customer.name,
            'surname': customer.surname
        })

    return jsonify(data)

#
#
#
@blueprint.route('/admin/customer/<int:id>', methods=['GET', 'POST'])
def get_customer_info(id):
    customer = Customer.query.filter_by(id=id).first()

    customerForm = CustomerForm(obj=customer)
    appointmentForm = AppointmentForm(customer_id=customer.id)    
    customerNewForm = CustomerForm()

    if request.method == 'POST':

        if customerForm.validate_on_submit():
            customer.update(
                name=customerForm.name.data.capitalize(),
                surname=customerForm.surname.data.capitalize(),
                email=customerForm.email.data.lower(),
                number=customerForm.number.data,
                comments=customerForm.comments.data,
            )
            flash('Updated customer updates.', 'success')
        else:
            flash_form_errors(customerForm)

    return render_template('admin/customer_info.html',
        customer=customer,
        customerForm=customerForm,
        customerNewForm=customerNewForm,
        appointmentForm=appointmentForm
    )

#
#
#
@blueprint.route('/admin/customer/new', methods=['POST'])
def new_customer():
    form = CustomerForm(request.form)

    if form.validate_on_submit():
        customers = Customer.query.filter(
            Customer.surname.like('%' + form.surname.data + '%')
        ).order_by(Customer.surname).all()

        if not customers:
            customer = Customer.create(
                name=form.name.data.capitalize(),
                surname=form.surname.data.capitalize(),
                email=form.email.data.lower(),
                number=form.number.data,
                appointments=[Appointment(message=form.message.data)]
            )
            return redirect(url_for('admin.get_customer_info', id=customer.id))
        else:
            for customer in customers:
                if form.name.data.lower() in customer.name.lower():
                    return redirect(url_for('admin.get_customer_info', id=customer.id))
    else:
        flash_form_errors(form)

    return redirect(url_for('admin.index'))

#
#
#
@blueprint.route('/admin/customer/delete/<int:id>')
def delete_customer(id):
    customer = Customer.query.filter_by(id=id).first()

    if not customer:
        return { 'status': 404 }

    customer.delete()

    flash('Successfully deleted.', 'success')
    return { 'status': 200 }

#
#
#
@blueprint.route('/admin/appointments/get')
def get_appointments():
    appointments = Appointment.query.order_by(Appointment.date).all()
    data = []

    for appointment in appointments:
        data.append({
            'id': appointment.id,
            'hardware': appointment.hardware,
            'device': appointment.device,
            'customer_id': appointment.customer_id
        })

    return jsonify(data)

#
#
#
@blueprint.route('/admin/appointment/new', methods=['POST'])
def appointment_new():
    form = AppointmentForm(request.form)
    if form.validate_on_submit():
        customer = Customer.query.filter_by(id=form.customer_id.data).first()

        if not customer:
            flash('Customer not in database.', 'danger')
            return redirect(url_for('admin.index'))

        devices = form.hardware.data.split('/')

        Appointment.create(
            date=form.date.data,
            message=form.message.data,
            customer_id=form.customer_id.data,
            hardware=devices[1],
            device=devices[0]
        )

        flash('Successfully added.', 'success')
        return redirect(url_for('admin.get_customer_info', id=form.customer_id.data))
    else:
        flash_form_errors(form)

    return redirect(url_for('admin.get_customer_info', id=form.customer_id.data)) 

#
#
#
@blueprint.route('/admin/appointment/delete/<int:id>')
def delete_appointment(id):
    appointment = Appointment.query.filter_by(id=id).first()

    if not appointment:
        return { 'status': 404 }

    appointment.delete()
    flash('Successfully deleted.', 'success')

    return { 'status': 200 }

#
#
#
@blueprint.route('/admin/appointment/update/<int:id>/', methods=['POST'])
def update_appointment(id):
    appointment = Appointment.query.filter_by(id=id).first()

    if not appointment:
        return NotFound()

    appointment.update(message=request.form['message'])
    flash('Successfully updated.', 'success')

    return { 'status': 200 }
