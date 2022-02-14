#
#
#

import os

DEBUG = os.environ.get("FLASK_ENV", default="production") == "development"
SECRET_KEY = os.urandom(32)

SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", default="sqlite:///database.db3")
SQLALCHEMY_TRACK_MODIFICATIONS = False
