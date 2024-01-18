from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from app import db
from app.user.entities import User
from app.user_api.schemes import UserSchema, UserCreateSchema


class UsersView(Resource):
    @jwt_required()
    def get(self):
        users = User.query.all()
        schema = UserSchema(many=True)
        return schema.dump(users)


class UserView(Resource):
    @jwt_required()
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'message': 'user not found'}, 404
        schema = UserSchema()
        return schema.dump(user), 200

    def post(self):
        schema = UserCreateSchema()
        user = schema.load(request.json)
        user.set_password(user.password)
        user.image_file = "default.jpg"
        db.session.add(user)
        db.session.commit()
        return UserSchema().dump(user), 201

    @jwt_required()
    def put(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'message': 'user not found'}, 404
        schema = UserSchema()
        user = schema.load(request.json, instance=user)
        db.session.add(user)
        db.session.commit()
        return schema.dump(user)

    @jwt_required()
    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'message': 'user not found'}, 404
        db.session.delete(user)
        db.session.commit()
        return {'status': 'success'}, 200
