import datetime

from flask import Flask, jsonify, make_response, request
from flask_restful import Api, abort

from data import db_session, jobs_api
from flask_login import LoginManager, login_user, logout_user, login_required, \
    current_user
from data.users import User
from flask import render_template
from data.login_form import LoginForm
from flask import redirect
from data.register_form import RegisterForm
from data.job_form import JobForm
from data.jobs import Jobs
from data.users_resource import UsersResource, UsersListResource

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/blogs.sqlite")
    app.register_blueprint(jobs_api.blueprint)

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)

    app.run()


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/')
def start():
    session = db_session.create_session()
    if current_user.is_authenticated:
        param = {}
        param['jobs'] = session.query(Jobs).all()
        param['users'] = session.query(User).all()
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
        if str(current_user.id) == str(form.team_leader.data):
            job = Jobs()
            job.job = form.job.data
            job.team_leader = form.team_leader.data
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
                               form=form, name='Добавление')
    return render_template('add_job.html', title='Добавление работы',
                           form=form,
                           text='Наше приложение', name='Добавление')


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = JobForm()
    if request.method == "GET":
        session = db_session.create_session()
        if str(current_user.id) == '1':
            jobs = session.query(Jobs).filter(Jobs.id == id).first()
        else:
            jobs = session.query(Jobs).filter(Jobs.id == id,
                                              Jobs.team_leader == current_user.id).first()
        if jobs:
            form.job.data = jobs.job
            form.work_size.data = jobs.work_size
            form.collaborators.data = jobs.collaborators
            form.is_finished.data = jobs.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        if str(current_user.id) == '1':
            jobs = session.query(Jobs).filter(Jobs.id == id).first()
        else:
            jobs = session.query(Jobs).filter(Jobs.id == id,
                                              Jobs.team_leader == current_user.id).first()
        if jobs:
            jobs.job = form.job.data
            jobs.work_size = form.work_size.data
            jobs.collaborators = form.collaborators.data
            jobs.is_finished = form.is_finished.data
            session.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('add_job.html', title='Редактирование работы',
                           form=form, name='Редактирование')


@app.route('/jobs_delete/<int:id>')
@login_required
def delete_jobs(id):
    session = db_session.create_session()
    if str(current_user.id) == '1':
        jobs = session.query(Jobs).filter(Jobs.id == id).first()
    else:
        jobs = session.query(Jobs).filter(Jobs.id == id,
                                          Jobs.team_leader == current_user.id).first()
    if jobs:
        session.delete(jobs)
        session.commit()
        return redirect('/')
    else:
        abort(404)
    return render_template('start.html', title='Личный кабинет')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


api.add_resource(UsersListResource, '/api/v2/users')
api.add_resource(UsersResource, '/api/v2/users/<int:user_id>')

if __name__ == '__main__':
    main()
    app.run(port=5000, host='127.0.0.1')
