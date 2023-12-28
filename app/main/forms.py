from flask_wtf import FlaskForm
from wtforms.fields.datetime import DateField
from wtforms.fields.simple import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


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