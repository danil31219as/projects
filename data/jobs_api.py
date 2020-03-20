import flask
from flask import jsonify, make_response, request

from data import db_session
from data.jobs import Jobs

blueprint = flask.Blueprint('jobs_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/jobs')
def get_jobs():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=(
                    'id', 'team_leader', 'job', 'work_size',
                    'collaborators', 'start_date', 'end_date', 'is_finished'))
                    for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:team_leader>', methods=['GET'])
def get_one_jobs(team_leader):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(team_leader)
    if not jobs:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'jobs': jobs.to_dict(
                only=('team_leader', 'job', 'work_size',
                    'collaborators', 'start_date', 'end_date', 'is_finished'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    session = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['job', 'team_leader', 'work_size', 'is_finished',
                  'collaborators']):
        return jsonify({'error': 'Bad request'})
    elif any([job.id == request.json['id'] for job in
              session.query(Jobs).all()]):
        return jsonify({'error': 'Id already exists'})
    jobs = Jobs(
        job=request.json['job'],
        team_leader=request.json['team_leader'],
        work_size=request.json['work_size'],
        is_finished=request.json['is_finished'],
        collaborators=request.json['collaborators']
    )
    session.add(jobs)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:team_leader>', methods=['DELETE'])
def delete_news(team_leader):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(team_leader)
    if not jobs:
        return jsonify({'error': 'Not found'})
    session.delete(jobs)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs', methods=['PUT'])
def edit_jobs():
    session = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['job', 'team_leader', 'work_size', 'is_finished',
                  'collaborators']) or not 'id' in request.json:
        return jsonify({'error': 'Bad request'})
    jobs = session.query(Jobs).filter(Jobs.id == request.json['id']).first()
    if not jobs:
        return jsonify({'error': 'id is not found'})
    jobs.job = request.json['job']
    jobs.team_leader = request.json['team_leader']
    jobs.work_size = request.json['work_size']
    jobs.is_finished = request.json['is_finished']
    jobs.collaborators = request.json['collaborators']
    session.commit()
    return jsonify({'success': 'OK'})
