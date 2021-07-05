import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    from .db_setup import ds_bp
    app.register_blueprint(ds_bp)

    from .injection_portal import ip_bp
    app.register_blueprint(ip_bp)

    return app


app = create_app()
