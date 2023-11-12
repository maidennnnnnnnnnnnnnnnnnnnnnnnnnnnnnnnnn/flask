from flask import Flask, render_template, flash, redirect, url_for, session, request
from flask_wtf import FlaskForm, form
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, BooleanField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, ValidationError, Length
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
import os
import datetime
from app import app

app.config['SECRET_KEY'] = 'asdasd'
@app.route('/')
def index():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    return render_template('index.html', data=data)


@app.route('/about')
def about():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    return render_template('about.html', data=data)


@app.route('/portfolio')
def portfolio():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    return render_template('portfolio.html', data=data)


my_skills = ["Вміння керувати автомобілем",
             "Вміння плавати у глибокій воді", "Знання англійської мови", "Економний"]


@app.route('/skills', defaults={'id': None})
@app.route('/skills/<int:id>')
def skills(id):
    data = [os.name, datetime.datetime.now(), request.user_agent]
    return render_template('skills.html', id=id, skills=my_skills, data=data)



with open("app/static/js/users.json", "r") as file:
    users = json.load(file)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    user = next((u for u in users if u['username'] == username), None)
    if user is None:
        return None

    user_obj = User()
    user_obj.id = user['username']
    return user_obj


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    form = LoginForm()

    if form.is_submitted() and form.validate():
        user = next((u for u in users if u['username'] == form.username.data), None)

        if user and user['password'] == form.password.data:
            user_obj = User()
            user_obj.id = user['username']
            login_user(user_obj, remember=form.remember.data)

            flash('Успішно увійшли!', 'success')
            return redirect(url_for('info'))

        else:
            flash('Неправильний логін чи пароль!', 'danger')
    return render_template('login.html', form=form, data=data)


@app.route('/logout')
@login_required
def logout():
    user_data = session.pop('user_data', current_user.id)
    logout_user()
    return redirect(url_for('login', user_data=user_data))


@app.route('/info', methods=['GET', 'POST'])
@login_required
def info():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    user_data = session.get('user_data', current_user.id)

    user_cookies = session.get('user_cookies', {})
    form = CookieForm()

    if form.validate_on_submit():
        if form.submit_add.data:
            key = form.key.data
            value = form.value.data
            expiration_date = form.expiration_date.data

            user_cookies[key] = {'value': value, 'expiration_date': expiration_date}
            pass

        elif form.submit_delete.data:
            key_to_delete = form.key.data

            if key_to_delete in user_cookies:
                del user_cookies[key_to_delete]
        elif form.submit_delete_all.data:
            user_cookies = {}

        session['user_cookies'] = user_cookies

    return render_template('info.html', data=data, user_cookies=user_cookies, form=form, user_data=user_data)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedbacks.db'
db = SQLAlchemy(app)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    comment = db.Column(db.Text, nullable=False)

class FeedbackForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    comment = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    form = FeedbackForm()

    if form.validate_on_submit():
        feedback = Feedback(name=form.name.data, comment=form.comment.data)
        db.session.add(feedback)
        db.session.commit()
        return redirect(url_for('feedback'))

    feedbacks = Feedback.query.all()
    return render_template('feedback.html', form=form, feedbacks=feedbacks, data=data)

asd = Migrate(app, db)