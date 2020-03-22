from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class DepartmentForm(FlaskForm):
    members = StringField('Members', validators=[DataRequired()])
    chief = StringField('Chief', validators=[DataRequired()])
    title = StringField('Title of department', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Добавить')
