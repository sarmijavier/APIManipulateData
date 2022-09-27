from app.api import bp
from app import db
from app.models.user import User

from flask import request, jsonify
import json


@bp.route('/hello')
def hello():
	return '<h1>hola</h1>'



@bp.route('/register', methods=['POST'])
def register():
	data = json.loads(request.data)
	email = data['email']	

	if User.query.filter_by(email=email).first() is not None:
		result = {
			'code': 'error',
			'message': 'The user already exists'
		}
		return jsonify(result)
	
	user = User()
	user.from_dict(data)
	user.set_password(user.password)
	user.get_token()
	db.session.add(user)
	db.session.commit()

	
	result = {
		'code': 200,
		'message': 'User created'
	}
	return jsonify(result)



@bp.route('/login', methods=['POST'])
def login():
	data = json.loads(request.data)
	email = data['email']	
	password = data['password']

	user = User.query.filter_by(email=email).first()
	if user:
		is_password_valid = user.check_password(password)
		if(is_password_valid):
			user.get_token()
			db.session.commit()

			result = {
				'code': 200,
				'message': 'the user exists'
			}

			return jsonify(result)
	
	result = {
		'code': 'error',
		'message': 'check you credentials'
	}
	return jsonify(result)
