from marshmallow import fields, validate, validates_schema, ValidationError

from app import mm
from app.models import Teacher


class TeacherSchema(mm.SQLAlchemySchema):
    id = fields.Integer(required=False, dump_only=True)
    username = fields.String(required=True, validate=[validate.Length(min=4, max=16)])
    email = fields.String(required=True, validate=[validate.Email()])
    subject = fields.String(required=True, validate=[validate.Length(min=4, max=24)])
    teachers_degree = fields.String(required=True, validate=[validate.Length(min=4, max=30)])

    class Meta:
        model = Teacher
        load_instance = True

    @validates_schema
    def validate_email(self, data, **kwargs):
        id = data.get('id')
        email = data.get('email')
        teacher = Teacher.query.filter_by(email = email).first()
        if not teacher:
            return
        if teacher.id != id:
            raise ValidationError('Email already in use')

