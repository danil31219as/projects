import flask
from flask import jsonify, make_response

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
                    'id', 'team_leader', 'title_of_activity', 'duration',
                    'list_of_collaborators', 'is_finished'))
                    for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:team_leader>', methods=['GET'])
def get_jobs(team_leader):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(team_leader)
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=(
                    'id', 'team_leader', 'title_of_activity', 'duration',
                    'list_of_collaborators', 'is_finished'))
                    for item in jobs]
        }
    )
