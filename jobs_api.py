import flask
from data import db_session
from data.jobs import Jobs
from flask import jsonify, request

blueprint = flask.Blueprint('jobs_api', __name__, template_folder='templates')


@blueprint.route('/api/jobs')
def get_jobs():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('id', 'job', 'team_leader', 'work_size',
                                    'collaborators', 'is_finished'))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'job': job.to_dict(only=('id', 'job', 'team_leader', 'work_size',
                                     'collaborators', 'is_finished'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ('id', 'job', 'team_leader', 'work_size',
                                                 'collaborators', 'is_finished')):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    if bool(session.query(Jobs).get(request.json['id'])):
        return jsonify({'error': 'Id already exists'})
    job = Jobs(
        id=request.json['id'],
        job=request.json['job'],
        team_leader=request.json['team_leader'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished']
    )
    session.add(job)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    session.delete(job)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['PUT'])
def put_job(job_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not any(key in request.json for key in ('id', 'job', 'team_leader', 'work_size',
                                                 'collaborators', 'is_finished')):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    new_job = job.to_dict(only=('id', 'job', 'team_leader', 'work_size',
                                'collaborators', 'is_finished'))
    for key in request.json:
        new_job[key] = request.json[key]
    job.id = new_job['id']
    job.job = new_job['job']
    job.team_leader = new_job['team_leader']
    job.work_size = new_job['work_size']
    job.collaborators = new_job['collaborators']
    job.is_finished = new_job['is_finished']
    session.commit()
    return jsonify({'success': 'OK'})
