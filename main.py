import datetime

import flask
from flask import Flask, jsonify, make_response
from flask_restful import Api

from data import db_session, jobs_api
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data.users import User
from flask import render_template
from data.login_form import LoginForm
from flask import redirect
from data.register_form import RegisterForm
from data.job_form import JobForm
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
u_i = 1


def main():
    db_session.global_init("db/blogs.sqlite")
    app.register_blueprint(jobs_api.blueprint)

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)

    app.run()


@login_manager.user_loader
def load_user(user_id):
    global u_i
    session = db_session.create_session()
    u_i = user_id
    return session.query(User).get(user_id)


@app.route('/')
def start():
    session = db_session.create_session()
    if current_user.is_authenticated:
        search = session.query(Jobs).all()
        param = get_params(search)
        param['title'] = 'Личный кабинет'
        param['text'] = 'Jobs'

        param['char'] = ['Title of activity', 'Team leader', 'Duration',
                         'List of collaborators', 'Is finished']
        return render_template('table.html', **param)
    return render_template('start.html', title='Личный кабинет')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(
            User.email == form.email.data).first()
        if user and user.hashed_password == form.password.data:
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form,
                           text='Наше приложение')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(
            User.email == form.email.data).first()
        if not user and form.password and form.password_repeat.data == form.password.data:
            user = User()
            user.name = form.name.data
            user.email = form.email.data
            user.hashed_password = form.password.data
            user.surname = form.surname.data
            user.position = form.position.data
            user.speciality = form.speciality.data
            user.age = form.age.data
            user.address = form.address.data
            user.modified_date = datetime.datetime.now()
            session.add(user)
            session.commit()
            return redirect("/")
        return render_template('register.html',
                               message="несовпадение паролей или пользователь уже зарегистрирован",
                               form=form)
    return render_template('register.html', title='Регистрация', form=form,
                           text='Наше приложение')


@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        if str(u_i) == str(form.team_leader_id.data):
            job = Jobs()
            job.job = form.job_title.data
            job.team_leader = form.team_leader_id.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.is_finished = form.is_finished.data
            job.start_date = datetime.datetime.now()
            job.end_date = datetime.datetime.now()
            session.add(job)
            session.commit()
            return redirect("/")
        return render_template('add_job.html',
                               message="нет доступа",
                               form=form)
    return render_template('add_job.html', title='Добавление', form=form,
                           text='Наше приложение')


def get_params(search):
    param = {}
    param['users'] = []
    session = db_session.create_session()
    for job in search:
        user_list = []
        user_list.append(job.job)
        user = session.query(User).filter(User.id == job.team_leader).first()
        user_list.append(user.name)
        user_list.append(job.work_size)
        user_list.append(job.collaborators)
        user_list.append(
            'is finished' if job.is_finished else 'is not finished')
        param['users'].append(user_list)
    return param


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    main()
    app.run(port=8080, host='127.0.0.1')
