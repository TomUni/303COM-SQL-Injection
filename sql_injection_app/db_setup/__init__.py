from flask import Blueprint

ds_bp = Blueprint("db_setup", __name__)

from . import views


