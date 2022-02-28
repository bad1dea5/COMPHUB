#
#
#

from flask import Flask

from COMPHUB import public, admin
from COMPHUB.extensions import csrf, db, flask_static_digest, migrate
from COMPHUB.utilities import datetime_filter

#
#
#
def create_app():
    app = Flask(__name__.split(".")[0])
    app.config.from_object("COMPHUB.settings")

    app.jinja_env.trim_blocks=True
    app.jinja_env.lstrip_blocks=True
    app.jinja_env.autoescape = True
    
    register_extensions(app)
    register_blueprints(app)
    register_filters(app)

    return app

#
#
#
def register_blueprints(app):
    app.register_blueprint(admin.views.blueprint)
    app.register_blueprint(public.views.blueprint)
    return None

#
#
#
def register_extensions(app):
    csrf.init_app(app)
    db.init_app(app)
    flask_static_digest.init_app(app)
    migrate.init_app(app, db)
    return None

#
#
#
def register_filters(app):
    app.jinja_env.filters['datetime'] = datetime_filter
    return None
