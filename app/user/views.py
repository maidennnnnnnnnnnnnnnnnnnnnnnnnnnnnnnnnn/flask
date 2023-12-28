import datetime
import os

from flask import current_app as asd

from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from . import user_bp as app
from flask import render_template, flash, redirect, url_for

from app import login_manager, db
from app.user.entities import User
from .forms import UpdateAccountForm, ChangePasswordForm


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route('/users')
def users():
    all_users = User.query.all()
    user_count = len(all_users)

    return render_template('users.html', users=all_users, user_count=user_count)

@app.route('/change_info', methods=['GET', 'POST'])
@login_required
def change_info():
    account_form = UpdateAccountForm()
    password_form = ChangePasswordForm()

    if account_form.validate_on_submit():
        current_user.username = account_form.username.data
        current_user.email = account_form.email.data
        current_user.about_me = account_form.about_me.data
        current_user.last_seen = datetime.datetime.now()
        if account_form.profile_picture.data:
            os.makedirs(asd.config['UPLOAD_FOLDER'], exist_ok=True)
            filename = secure_filename(account_form.profile_picture.data.filename)
            filepath = os.path.join(asd.config['UPLOAD_FOLDER'], filename)
            account_form.profile_picture.data.save(filepath)
            current_user.image_file = filename
        db.session.commit()
        flash('Ваш профіль був оновлений!', 'success')
        return redirect(url_for('main.info'))

    elif password_form.validate_on_submit():
        current_user.set_password(password_form.new_password.data)
        flash('Ваш пароль був оновлений!', 'success')
        current_user.last_seen = datetime.datetime.now()
        db.session.commit()
        return redirect(url_for('main.info'))

    return render_template('change_info.html', form=account_form, password_form=password_form)



