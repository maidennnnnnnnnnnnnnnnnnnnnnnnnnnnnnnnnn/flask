from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Regexp, Email, EqualTo, ValidationError

from app.user.entities import User


class RegistrationForm(FlaskForm):
    username = StringField('Ім\'я', validators=[
        DataRequired(),
        Length(min=4, max=14, message="Це обов'язкове поле має бути довжиною між 4 та 14 символів"),
        Regexp(r'^[A-Za-z .]+$', message='Ім\'я користувача може містити тільки латинські літери, пробіли і крапки.')
    ])
    email = StringField('Email', validators=[DataRequired(), Email(message="Це обов'язкове поле, перевірка, що email")])
    password = PasswordField('Пароль',
                             validators=[DataRequired(), Length(min=6, message="Це поле має бути більше 6 символів")])
    confirm_password = PasswordField('Повторіть пароль', validators=[DataRequired(), EqualTo('password',
                                                                                             message='Повторна перевірка правильності паролю')])
    submit = SubmitField('Зареєструватись')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Це ім\'я користувача вже зайняте. Виберіть інше.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
