from flask import flash, redirect, url_for, render_template

from . import todo_bp as app
from .entities import Todo
from .forms import TodoForm
from .. import db



@app.route('/<int:id>', methods=['GET', 'POST'])
def todo_detail(id):
    todo = Todo.query.get_or_404(id)
    form = TodoForm(obj=todo)

    if form.validate_on_submit():
        form.populate_obj(todo)
        db.session.commit()
        flash('Замітка була оновлена!', 'success')
        return redirect(url_for('main.index'))

    return render_template('todo_detail.html', todo=todo, form=form)


@app.route('/create', methods=['GET', 'POST'])
def create_todo():
    form = TodoForm()

    if form.validate_on_submit():
        todo = Todo(title=form.title.data, description=form.description.data)
        db.session.add(todo)
        db.session.commit()
        flash('Замітка була оновлена!', 'success')
        return redirect(url_for('main.index'))

    return render_template('create_todo.html', form=form)


@app.route('/delete/<int:id>', methods=['GET'])
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    flash('Замітка була видалена!', 'success')
    return redirect(url_for('main.index'))
