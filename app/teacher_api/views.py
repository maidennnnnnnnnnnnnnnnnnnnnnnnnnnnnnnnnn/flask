from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from app import db
from app.models import Teacher
from app.teacher_api.schemes import TeacherSchema


class TeachersView(Resource):
    @jwt_required()
    def get(self):
        teachers = Teacher.query.all()
        schema = TeacherSchema(many=True)
        return schema.dump(teachers)


class TeacherView(Resource):
    @jwt_required()
    def get(self, teacher_id):
        teacher = Teacher.query.get(teacher_id)
        if not teacher:
            return {'message': 'teacher not found'}, 404
        schema = TeacherSchema()
        return schema.dump(teacher), 200

    @jwt_required()
    def post(self):
        schema = TeacherSchema()
        teacher = schema.load(request.json)
        db.session.add(teacher)
        db.session.commit()
        return schema.dump(teacher), 201

    @jwt_required()
    def put(self, teacher_id):
        teacher = Teacher.query.get(teacher_id)
        if not teacher:
            return {'message': 'teacher not found'}, 404
        schema = TeacherSchema()
        teacher = schema.load(request.json, instance=teacher)
        db.session.add(teacher)
        db.session.commit()
        return schema.dump(teacher)

    @jwt_required()
    def delete(self, teacher_id):
        teacher = Teacher.query.get(teacher_id)
        if not teacher:
            return {'message': 'teacher not found'}, 404
        db.session.delete(teacher)
        db.session.commit()
        return {'status': 'success'}, 200
