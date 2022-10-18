from app.api import bp
from app import db
from app.models.user import User

from flask import request, jsonify
import json

import requests
from requests.structures import CaseInsensitiveDict



@bp.route('/hello')
def hello():
	return jsonify({'success': 'exito!'})



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
				'message': 'the user exists',
				'email': email,
				'active_session': user.to_dict()['active_session']
			}

			return jsonify(result)
	
	result = {
		'code': 'error',
		'message': 'check you credentials'
	}
	return jsonify(result)



@bp.route('/register/fitbit', methods=['POST'])
def register_fitbit():
	data = json.loads(request.data)
	email = data['email']	
	code = data['code']


	url = "https://api.fitbit.com/oauth2/token"

	headers = CaseInsensitiveDict()
	headers["Authorization"] = "Basic MjJCTjJLOmYwYWIzYWE4NDEwN2JjN2Q1OWI4MzA3YzZhZTgwNmJm"
	headers["Content-Type"] = "application/x-www-form-urlencoded"

	data = f'clientId=22BN2K&grant_type=authorization_code&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fdashboard&code={code}'


	resp = requests.post(url, headers=headers, data=data)
	json_resp = json.loads(resp.text)


	user = User.query.filter_by(email=email).first()
	user.from_dict(data)
	user.token_fitbit = json_resp['access_token']
	user.refresh_token_fitbit = json_resp['refresh_token']
	user.user_id = json_resp['user_id']
	user.active_session = True
	db.session.commit()

	result = {
		'code': 200,
		'message': 'fitbit data saved',
		'active_session': True
	}
	return jsonify(result)



def refresh_token_fitbit(email):
	
	user = User.query.filter_by(email=email).first()
	refresh_token_fitbit = user.to_dict()['refresh_token_fitbit']
	url = "https://api.fitbit.com/oauth2/token"

	headers = CaseInsensitiveDict()
	headers["Authorization"] = "Basic MjJCTjJLOmYwYWIzYWE4NDEwN2JjN2Q1OWI4MzA3YzZhZTgwNmJm"
	headers["Content-Type"] = "application/x-www-form-urlencoded"

	data = f'clientId=22BN2K&grant_type=refresh_token&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fdashboard&refresh_token={refresh_token_fitbit}'


	resp = requests.post(url, headers=headers, data=data)
	json_resp = json.loads(resp.text)

	user.token_fitbit = json_resp['access_token']
	user.refresh_token_fitbit = json_resp['refresh_token']
	db.session.commit()

	print(resp.status_code)
