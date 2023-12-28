from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, TextAreaField, SubmitField


class TodoForm(FlaskForm):
    title = StringField('Title', render_kw={"placeholder": "Введіть замітку"})
    description = TextAreaField('Description', render_kw={"placeholder": "Введіть опис замітки"})
    submit = SubmitField('Підтвердити')
