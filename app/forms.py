import json

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField, ValidationError, DateField
from wtforms.validators import DataRequired, Length

with open("app/static/js/users.json", "r") as file:
    users = json.load(file)


class TodoForm(FlaskForm):
    title = StringField('Title', render_kw={"placeholder": "Введіть замітку"})
    description = TextAreaField('Description', render_kw={"placeholder": "Введіть опис замітки"})
    submit = SubmitField('Підтвердити')


class LoginForm(FlaskForm):
    username = StringField('Логін', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=4, max=10)])
    remember = BooleanField('Запам’ятати мене')
    submit = SubmitField('Ввійти')

    def validate_username(self, field):
        user = next((u for u in users if u['username'] == field.data), None)
        if user is None:
            raise ValidationError('Такого користувача не існує!')

    def validate_password(self, field):
        user = next((u for u in users if u['username'] == self.username.data), None)
        if user is not None and user['password'] != field.data:
            raise ValidationError('Неправильний пароль!')

    csrf_token = StringField('CSRF Token', render_kw={'value': 'form.csrf_token'})


class CookieForm(FlaskForm):
    key = StringField('Ключ', validators=[DataRequired()])
    value = StringField('Значення', validators=[DataRequired()])
    expiration_date = DateField('Дата закінчення', format='%Y-%m-%d', validators=[DataRequired()])
    submit_add = SubmitField('Додати куку')
    submit_delete = SubmitField('Прибрати куку')
    submit_delete_all = SubmitField('Прибрати всі куки')


class FeedbackForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    comment = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit')
