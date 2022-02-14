#
#
#

from flask import (
    Blueprint,
    render_template,
    url_for,
    redirect,
    flash,
    request
)

from COMPHUB.public.models import Repair
from COMPHUB.admin.forms import SearchForm

blueprint = Blueprint(
    "admin", __name__,
    static_folder = "../static",
    template_folder = "templates"
)

@blueprint.route('/admin')
def index():
    search=SearchForm(request.form)
    new = nextin = Repair.query.order_by(Repair.created).limit(5).all()
    nextin = Repair.query.order_by(Repair.datetime).limit(5).all()
    return render_template('admin/index.html',
        items=new,
        nextin=nextin,
        search=search
    )

@blueprint.route('/admin/view/<id>')
def view_repair(id):
    search=SearchForm(request.form)
    item = Repair.query.filter_by(id=id).first_or_404(description='There is no data with {}'.format(id))
    return render_template('admin/view.html', item=item, search=search)

@blueprint.route('/admin/delete/<id>')
def delete_repair(id):
    item = Repair.query.filter_by(id=id).first_or_404(description='There is no data with {}'.format(id))
    item.delete()
    return redirect(url_for('admin.index'))

@blueprint.route('/admin/update/<id>/<int:status>')
def update_repair(id, status):
    message=''

    if status == 1:
        message='Waiting'
    elif status== 2:
        message='Received'
    elif status== 3:
        message='Repairing'
    elif status== 4:
        message='Delivery'
    
    item = Repair.query.filter_by(id=id).first_or_404(description='There is no data with {}'.format(id)).update(status=message)
    return redirect(url_for('admin.view_repair', id=id))

@blueprint.route('/admin/search')
def search():
    search=SearchForm(request.form)
    items = Repair.query.filter(Repair.name.like('%' + request.args.get('name') + '%')).order_by(Repair.name).all()
    return render_template('admin/search.html', search=search, items=items)
