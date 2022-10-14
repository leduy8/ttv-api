from importlib import import_module

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_oauthlib.client import OAuth
from flask_sqlalchemy import SQLAlchemy

from .commons.error_handlers import register_error_handlers
from .config import DevelopmentConfig as Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
oauth = OAuth(app)

CORS(app)


def register_subpackages():
    from main import models

    for m in models.__all__:
        import_module("main.models." + m)

    import main.controllers  # noqa
    import main.services  # noqa


register_subpackages()
register_error_handlers(app)
