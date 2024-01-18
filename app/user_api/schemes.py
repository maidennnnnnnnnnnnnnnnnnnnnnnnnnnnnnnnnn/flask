from marshmallow import fields, validate, validates_schema, ValidationError

from app import mm
from app.user.entities import User


class UserSchema(mm.SQLAlchemySchema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    email = fields.String(required=True)
    about_me = fields.String()

    class Meta:
        model = User
        load_instance = True

    @validates_schema
    def validate_email(self, data, **kwargs):
        id = data.get('id')
        email = data.get('email')
        user = User.query.filter_by(email = email).first()
        if not user:
            return
        if user.id != id:
            raise ValidationError('Email already in use')

    @validates_schema
    def validate_username(self, data, **kwargs):
        id = data.get('id')
        username = data.get('username')
        user = User.query.filter_by(username=username).first()
        if not user:
            return
        if user.id != id:
            raise ValidationError('Username already in use')

class UserCreateSchema(UserSchema):
    password = fields.String(required=True)