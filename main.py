import datetime
import os

from flask import Flask, jsonify, make_response, request
from flask_ngrok import run_with_ngrok
from flask_restful import Api, abort

from data import db_session, jobs_api, users_api
from flask_login import LoginManager, login_user, logout_user, login_required, \
    current_user
from requests import get

from data.category import Category
from data.jobs_resource import JobsListResource, JobsResource
from data.users import User
from flask import render_template
from data.login_form import LoginForm
from flask import redirect
from data.register_form import RegisterForm
from data.job_form import JobForm
from data.jobs import Jobs
from data.departments import Departments
from data.department_form import DepartmentForm
from data.users_resource import UsersResource, UsersListResource
from data.maps_api import get_coor, create_image

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
i = 0
# run_with_ngrok(app)


def main():
    db_session.global_init("db/blogs.sqlite")
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)

    app.run()


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
def start():
    global i
    session = db_session.create_session()
    if current_user.is_authenticated:
        if request.method == 'POST':
            i += 1
        if i % 2 == 0:
            param = {}
            param['jobs'] = session.query(Jobs).all()
            param['users'] = session.query(User).all()
            param['title'] = 'Личный кабинет'
            param['text'] = 'Jobs'
            param['char'] = ['Title of activity', 'Team leader', 'Duration',
                         'List of collaborators', 'Category', 'Is finished']
            return render_template('table.html', **param)
        else:
            param = {}
            param['departments'] = session.query(Departments).all()
            param['users'] = session.query(User).all()
            param['title'] = 'Личный кабинет'
            param['text'] = 'Departments'
            param['char'] = ['Title of department', 'Chief', 'Members',
                             'Department Email']
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
            user.city_form = form.city.data
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
            job.categories.append(Category(name=form.categories.data))
            print(job.categories, job.categories[0].name)
            session.add(job)
            session.commit()
            return redirect("/")
        return render_template('add_job.html',
                               message="нет доступа",
                               form=form, name='Добавление')
    return render_template('add_job.html', title='Добавление работы',
                           form=form,
                           text='Наше приложение', name='Добавление')


@app.route('/add_department', methods=['GET', 'POST'])
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        if str(current_user.id) == str(form.chief.data):
            department = Departments()
            department.members = form.members.data
            department.chief = form.chief.data
            department.title = form.title.data
            department.email = form.email.data
            session.add(department)
            session.commit()
            return redirect("/")
        return render_template('add_department.html',
                               message="нет доступа",
                               form=form, name='Добавление')
    return render_template('add_department.html', title='Добавление департамента',
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


@app.route('/departments/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_departments(id):
    form = DepartmentForm()
    if request.method == "GET":
        session = db_session.create_session()
        if str(current_user.id) == '1':
            departments = session.query(Departments).filter(Departments.id == id).first()
        else:
            departments = session.query(Departments).filter(Departments.id == id,
                                              Departments.chief == current_user.id).first()
        if departments:
            form.members.data = departments.members
            form.title.data = departments.title
            form.email.data = departments.email
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        if str(current_user.id) == '1':
            departments = session.query(Departments).filter(Departments.id == id).first()
        else:
            departments = session.query(Departments).filter(Departments.id == id,
                                              Departments.chief == current_user.id).first()
        if departments:
            departments.members = form.members.data
            departments.title = form.title.data
            departments.email = form.email.data
            session.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('add_department.html', title='Редактирование департамента',
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
        jobs.categories.remove(jobs.categories[0])
        session.delete(jobs)
        session.commit()
        return redirect('/')
    else:
        abort(404)
    return render_template('start.html', title='Личный кабинет')


@app.route('/departments_delete/<int:id>')
@login_required
def delete_departments(id):
    session = db_session.create_session()
    if str(current_user.id) == '1':
        departments = session.query(Departments).filter(Departments.id == id).first()
    else:
        departments = session.query(Departments).filter(Departments.id == id,
                                          Departments.chief == current_user.id).first()
    if departments:
        session.delete(departments)
        session.commit()
        return redirect('/')
    else:
        abort(404)
    return render_template('start.html', title='Личный кабинет')


@app.route('/users_show/<int:user_id>', methods=['GET', 'POST'])
def show_city(user_id):
    search = get('http://localhost:5000/api/users/' + str(user_id)).json()
    create_image(get_coor(search['users']['city_form']))
    return render_template('users_show.html', search=search['users'])


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


api.add_resource(UsersListResource, '/api/v2/users')
api.add_resource(UsersResource, '/api/v2/users/<int:user_id>')
api.add_resource(JobsListResource, '/api/v2/jobs')
api.add_resource(JobsResource, '/api/v2/jobs/<int:job_id>')

if __name__ == '__main__':
    main()
    app.run()
