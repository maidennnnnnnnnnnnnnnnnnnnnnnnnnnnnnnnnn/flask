from flask import Blueprint, jsonify
from flask_restful import Api
from marshmallow import ValidationError

from .views import TeachersView, TeacherView

teacher_bp = Blueprint("teacher_api", __name__)
api = Api(teacher_bp, errors=teacher_bp.errorhandler)

api.add_resource(TeachersView, "/teachers")
api.add_resource(TeacherView, "/teacher", "/teacher/<int:teacher_id>")


@teacher_bp.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400
