from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField, ValidationError, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp

from app.models import User


class TodoForm(FlaskForm):
    title = StringField('Title', render_kw={"placeholder": "Введіть замітку"})
    description = TextAreaField('Description', render_kw={"placeholder": "Введіть опис замітки"})
    submit = SubmitField('Підтвердити')


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
