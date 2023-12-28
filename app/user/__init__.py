from flask import Blueprint

user_bp = Blueprint('user', __name__, template_folder='templates/user', static_folder='static')

from . import views
