import datetime
import os

from flask import render_template, flash, redirect, url_for, session, request
from flask_login import logout_user, current_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db
from app.forms import TodoForm, LoginForm, CookieForm, FeedbackForm, RegistrationForm
from app.models import Todo, Feedback, User

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/todo/<int:id>', methods=['GET', 'POST'])
def todo_detail(id):
    todo = Todo.query.get_or_404(id)
    form = TodoForm(obj=todo)

    if form.validate_on_submit():
        form.populate_obj(todo)
        db.session.commit()
        flash('Замітка була оновлена!', 'success')
        return redirect(url_for('index'))

    return render_template('todo_detail.html', todo=todo, form=form)


@app.route('/todo/create', methods=['GET', 'POST'])
def create_todo():
    form = TodoForm()

    if form.validate_on_submit():
        todo = Todo(title=form.title.data, description=form.description.data)
        db.session.add(todo)
        db.session.commit()
        flash('Замітка була оновлена!', 'success')
        return redirect(url_for('index'))

    return render_template('create_todo.html', form=form)


@app.route('/todo/delete/<int:id>', methods=['GET'])
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    flash('Замітка була видалена!', 'success')
    return redirect(url_for('index'))


@app.route('/')
def index():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    todos = Todo.query.all()
    form = TodoForm()
    return render_template('index.html', data=data, todos=todos, form=form)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')


my_skills = ["Вміння керувати автомобілем",
             "Вміння плавати у глибокій воді", "Знання англійської мови", "Економний"]


@app.route('/skills', defaults={'id': None})
@app.route('/skills/<int:id>')
def skills(id):
    return render_template('skills.html', id=id, skills=my_skills)


@app.route('/users')
def users():
    all_users = User.query.all()
    user_count = len(all_users)

    return render_template('users.html', users=all_users, user_count=user_count)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        existing_email = User.query.filter_by(email=form.email.data).first()

        if existing_user or existing_email:
            flash('Ім\'я користувача або електронна пошта вже зайняті. Виберіть інші.', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Ваш аккаунт було створено!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('info'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            flash('Успішно ввійдено!', 'success')
            return redirect(url_for('info'))
        else:
            flash('Вхід неуспішний. Перевірте дані на правильність введення.', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    user_data = session.pop('user_data', current_user.id)
    logout_user()
    return redirect(url_for('login', user_data=user_data))


@app.route('/info', methods=['GET', 'POST'])
def info():
    user_data = current_user

    user_cookies = session.get('user_cookies', {})
    form = CookieForm()

    if form.validate_on_submit():
        if form.submit_add.data:
            key = form.key.data
            value = form.value.data
            expiration_date = form.expiration_date.data

            user_cookies[key] = {'value': value, 'expiration_date': expiration_date}
            flash(f'Кука "{key}" була успішно додана!', 'success')

        elif form.submit_delete.data:
            key_to_delete = form.key.data

            if key_to_delete in user_cookies:
                del user_cookies[key_to_delete]
                flash(f'Кука "{key_to_delete}" була успішно видалена!', 'success')

        elif form.submit_delete_all.data:
            user_cookies = {}
            flash('Всі куки були успішно видалені!', 'success')

        session['user_cookies'] = user_cookies

    return render_template('info.html', user_cookies=user_cookies, form=form, user_data=user_data)


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()

    if form.validate_on_submit():
        feedback = Feedback(name=form.name.data, comment=form.comment.data)
        db.session.add(feedback)
        db.session.commit()
        return redirect(url_for('feedback'))

    feedbacks = Feedback.query.all()
    return render_template('feedback.html', form=form, feedbacks=feedbacks)
