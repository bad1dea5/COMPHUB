#
#
#

from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect
)

from COMPHUB.public.forms import RepairForm
from COMPHUB.public.models import Repair

blueprint = Blueprint(
    "public", __name__,
    static_folder = "../static",
    template_folder = "templates"
)

@blueprint.route('/', methods=['GET', 'POST'])
def index():
    form = RepairForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            Repair.create(
                name=form.name.data.lower(),
                email=form.email.data.lower(),
                number=form.number.data,
                hardware=form.hardware.data,
                message=form.message.data,
                status="Waiting",
                datetime=form.datetime.data
            )
            flash("Successfully send, thank you.", "success")
            return render_template('public/index.html', form=form)
        else:
            flash("An error has occurred.", "danger")
    return render_template('public/index.html', form=form)
