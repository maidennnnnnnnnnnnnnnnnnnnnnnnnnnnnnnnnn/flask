from flask import Blueprint, jsonify
from flask_restful import Api
from marshmallow import ValidationError

from app.user_api.views import UserView, UsersView

user_api = Blueprint("user_api", __name__)
api = Api(user_api, errors=user_api.errorhandler)

api.add_resource(UsersView, "/users")
api.add_resource(UserView, "/user", "/user/<int:user_id>")


@user_api.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400
