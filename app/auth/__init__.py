from flask import Blueprint

auth_bp = Blueprint('auth', __name__, template_folder='templates/auth', static_folder='static')

from . import views
