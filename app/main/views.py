import datetime
import os

from flask import session, flash, render_template, redirect, url_for, request
from flask_login import login_required, current_user

from . import main_bp as app
from .entities import Feedback
from .forms import CookieForm, FeedbackForm
from .. import db
from ..todo.entities import Todo

from ..todo.forms import TodoForm


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



@app.route('/info', methods=['GET', 'POST'])
@login_required
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
        return redirect(url_for('main.feedback'))

    feedbacks = Feedback.query.all()
    return render_template('feedback.html', form=form, feedbacks=feedbacks)

