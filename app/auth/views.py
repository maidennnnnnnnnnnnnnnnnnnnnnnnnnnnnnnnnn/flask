import datetime

from flask import redirect, url_for, flash, render_template, session
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import auth_bp as app
from .forms import RegistrationForm, LoginForm
from .. import db
from ..user.entities import User


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.info'))
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        existing_email = User.query.filter_by(email=form.email.data).first()

        if existing_user or existing_email:
            flash('Ім\'я користувача або електронна пошта вже зайняті. Виберіть інші.', 'danger')
            return redirect(url_for('auth.register'))
        default_image = 'default.jpg'
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password, image_file = default_image)
        db.session.add(new_user)
        db.session.commit()
        flash('Ваш аккаунт було створено!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.info'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            flash('Успішно ввійдено!', 'success')
            login_user(user, remember=form.remember.data)
            user.last_seen = datetime.datetime.now()
            db.session.commit()
            return redirect(url_for('main.info'))
        else:
            flash('Вхід неуспішний. Перевірте дані на правильність введення.', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    user_data = session.pop('user_data', current_user.id)
    logout_user()
    return redirect(url_for('auth.login', user_data=user_data))
