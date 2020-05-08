import flask
from data import db_session
from data.users import User
from flask import jsonify, request

blueprint = flask.Blueprint('users_api', __name__, template_folder='templates')


@blueprint.route('/api/users')
def get_users():
    session = db_session.create_session()
    users = session.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'surname', 'name', 'age', 'position',
                                    'speciality', 'address', 'email'))
                 for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'user': user.to_dict(only=('id', 'surname', 'name', 'age', 'position',
                                       'speciality', 'address', 'email', 'city_from'))
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['id', 'surname', 'name', 'age', 'position',
                                                 'speciality', 'address', 'email', 'city_from']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    if bool(session.query(User).get(request.json['id'])):
        return jsonify({'error': 'Id already exists'})
    user = User(
        id=request.json['id'],
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email'],
        city_from=request.json['city_from']
    )
    session.add(user)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    session.delete(user)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not any(key in request.json for key in ['id', 'surname', 'name', 'age', 'position',
                                                 'speciality', 'address', 'email', 'city_from']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    new_user = user.to_dict(only=('id', 'surname', 'name', 'age', 'position',
                                  'speciality', 'address', 'email', 'city_from'))
    for key in request.json:
        new_user[key] = request.json[key]
    user.id = new_user['id']
    user.surname = new_user['surname']
    user.name = new_user['name']
    user.age = new_user['age']
    user.position = new_user['position']
    user.speciality = new_user['speciality']
    user.address = new_user['address']
    user.email = new_user['email']
    user.city_from = new_user['city_from']
    session.commit()
    return jsonify({'success': 'OK'})
