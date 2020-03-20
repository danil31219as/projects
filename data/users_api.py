import datetime

import flask
from flask import jsonify, make_response, request

from data import db_session
from data.jobs import Jobs
from data.users import User

blueprint = flask.Blueprint('users_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/users')
def get_users():
    session = db_session.create_session()
    users = session.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=(
                    'id', 'name', 'surname', 'age', 'position', 'speciality',
                    'address', 'email', 'hashed_password', 'modified_date',
                    'city_form'))
                    for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_users(user_id):
    session = db_session.create_session()
    users = session.query(User).get(user_id)
    if not users:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'users': users.to_dict(
                only=('name', 'surname', 'age', 'position', 'speciality',
                    'address', 'email', 'hashed_password', 'modified_date',
                    'city_form'))
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_users():
    session = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['name', 'surname', 'age', 'position', 'speciality',
                  'address', 'email', 'hashed_password', 'city_form']):
        return jsonify({'error': 'Bad request'})
    elif any([user.id == request.json['id'] for user in
              session.query(User).all()]):
        return jsonify({'error': 'Id already exists'})
    users = User(
        id=request.json['id'],
        name=request.json['name'],
        surname=request.json['surname'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email'],
        hashed_password=request.json['hashed_password'],
        city_form=request.json['city_form'],
        modified_date=datetime.datetime.now()
    )
    session.add(users)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_users(user_id):
    session = db_session.create_session()
    users = session.query(User).get(user_id)
    if not users:
        return jsonify({'error': 'Not found'})
    session.delete(users)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def put_users(user_id):
    session = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['name', 'surname', 'age', 'position', 'speciality',
                  'address', 'email', 'hashed_password',
                  'city_form']) or not 'id' in request.json:
        return jsonify({'error': 'Bad request'})
    users = session.query(User).filter(User.id == user_id).first()
    if not users:
        return jsonify({'error': 'id is not found'})
    users.name = request.json['name']
    users.surname = request.json['surname']
    users.age = request.json['age']
    users.position = request.json['position']
    users.speciality = request.json['speciality']
    users.address = request.json['address']
    users.email = request.json['email']
    users.hashed_password = request.json['hashed_password']
    users.modified_date = datetime.datetime.now()
    session.commit()
    return jsonify({'success': 'OK'})
