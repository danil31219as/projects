import datetime

from flask import jsonify
from flask_restful import abort, Resource

from data import db_session
from data.jobs import Jobs

from data.job_parse import parser


def abort_if_news_not_found(job_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(job_id)
    if not jobs:
        abort(404, message=f"Job {job_id} not found")


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_news_not_found(job_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(job_id)
        return jsonify({'jobs': jobs.to_dict(
            only=('id', 'team_leader', 'job', 'work_size',
                  'collaborators', 'start_date', 'end_date', 'is_finished'))})

    def delete(self, job_id):
        abort_if_news_not_found(job_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(job_id)
        session.delete(jobs)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict(
            only=('id', 'team_leader', 'job', 'work_size',
                  'collaborators', 'start_date', 'end_date', 'is_finished'))
            for item in jobs]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        jobs = Jobs(

            job=args['job'],
            team_leader=args['team_leader'],
            work_size=args['work_size'],
            is_finished=args['is_finished'],
            collaborators=args['collaborators']
        )
        session.add(jobs)
        session.commit()
        return jsonify({'success': 'OK'})
