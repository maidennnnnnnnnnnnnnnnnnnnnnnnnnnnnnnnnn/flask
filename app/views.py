from flask import Flask, render_template, flash, redirect, url_for, session, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, ValidationError
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
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
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Ввійти')

    def validate(self):
        if not super(LoginForm, self).validate():
            return False

        user = next((u for u in users if u['username'] == self.username.data), None)

        if user is None or user['password'] != self.password.data:
            self.username.errors.append('Неправильний пароль чи логін!')
            self.password.errors.append('Неправильний пароль чи логін!')
            return False

        return True

    def validate_on_submit(self):
        return self.is_submitted() and self.validate()


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
    if form.validate_on_submit():
        user = User()
        user.id = form.username.data
        login_user(user)
        return redirect(url_for('info'))
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

        elif form.submit_delete.data:
            key_to_delete = form.key.data

            if key_to_delete in user_cookies:
                del user_cookies[key_to_delete]
        elif form.submit_delete_all.data:
            user_cookies = {}

        session['user_cookies'] = user_cookies

    return render_template('info.html', data=data, user_cookies=user_cookies, form=form, user_data=user_data)