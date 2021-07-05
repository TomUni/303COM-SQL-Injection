from flask import Blueprint

ip_bp = Blueprint("injection_portal", __name__)

from . import views


