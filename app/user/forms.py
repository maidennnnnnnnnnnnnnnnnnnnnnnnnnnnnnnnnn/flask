from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms.fields.simple import StringField, FileField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Regexp, Email, ValidationError, EqualTo

from app.user.entities import User


class UpdateAccountForm(FlaskForm):
    username = StringField('Ім\'я', validators=[
        DataRequired(),
        Length(min=4, max=14, message="Це обов'язкове поле має бути довжиною між 4 та 14 символів"),
        Regexp(r'^[A-Za-z .]+$', message='Ім\'я користувача може містити тільки латинські літери, пробіли і крапки.')
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message="Це обов'язкове поле, перевірка, що email")])
    profile_picture = FileField('Фото профілю', validators=[
        FileAllowed(['jpg', 'png'], 'Дозволені лише файли з розширенням .jpg або .png.')])
    about_me = TextAreaField('Про мене', validators=[Length(max=140, message='Максимальна довжина 140 символів')])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Це ім\'я користувача вже зайняте. Виберіть інше.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Цей email вже використовується. Виберіть інший.')

    submit = SubmitField('Оновити профіль')


class ChangePasswordForm(FlaskForm):
    new_password = PasswordField('Новий пароль',
                                 validators=[Length(min=6, message="Пароль має бути більше 6 символів")])
    confirm_new_password = PasswordField('Повторіть новий пароль',
                                         validators=[EqualTo('new_password', message='Паролі повинні співпадати')])
    submit_change_password = SubmitField('Змінити пароль')



