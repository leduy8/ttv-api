from importlib import import_module

from flask import Flask
from flask_cors import CORS
from flask_dance.contrib.google import make_google_blueprint
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .commons.error_handlers import register_error_handlers
from .config import DevelopmentConfig as Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.register_blueprint(
    make_google_blueprint(
        client_id=app.config["GOOGLE_OAUTH_CLIENT_ID"],
        client_secret=app.config["GOOGLE_OAUTH_CLIENT_SECRET"],
        scope=app.config["GOOGLE_SCOPE"].split(" "),
        reprompt_consent=True,
        redirect_url=app.config["REDIRECT_AFTER_OAUTH_LOGIN"],
        redirect_to=app.config["REDIRECT_AFTER_OAUTH_LOGIN"],
    ),
    url_prefix="/google",
)

CORS(app)


def register_subpackages():
    from main import models

    for m in models.__all__:
        import_module("main.models." + m)

    import main.controllers  # noqa
    import main.services  # noqa


register_subpackages()
register_error_handlers(app)
