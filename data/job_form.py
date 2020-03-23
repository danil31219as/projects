from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    job = StringField('Job title', validators=[DataRequired()])
    team_leader = StringField('Team leader id', validators=[DataRequired()])
    work_size = StringField('Work Size', validators=[DataRequired()])
    collaborators = StringField('Collaborators', validators=[DataRequired()])
    categories = StringField('Category', validators=[DataRequired()])
    is_finished = BooleanField('Is job finished?')

    submit = SubmitField('Добавить')
