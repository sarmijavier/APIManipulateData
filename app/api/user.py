from app.api import bp
from app import db
from app.models.temperature_data import TemperatureData
from app.models.user import User
from app.models.record_date import RecordDate
from app.models.heart_rate_data import HeartRateData
from app.models.activity_data import ActivityData
from app.models.weight_data import WeightData
from app.models.breath_data import BreathData
from app.models.food_data import FootData
from app.models.sleep_data import SleepData
from app.models.blood_oxygen_saturation_data import BloodOxygenSaturationData


from flask import request, jsonify
import json

import requests
from requests.structures import CaseInsensitiveDict
from datetime import datetime, timedelta, date

import pandas as pd
import random
import decimal


@bp.route('/hello')
def hello():
	return jsonify({'success': 'exito!'})


@bp.route('/activate/emergency')
def send_whatsapp_message():
	url = "https://graph.facebook.com/v15.0/103819765886206/messages"

	headers = CaseInsensitiveDict()
	headers["Authorization"] = ""
	headers["Content-Type"] = "application/json"

	data = '{ "messaging_product": "whatsapp", "to": "", "type": "template", "template": { "name": "testsendmessage", "language": { "code": "en_US" } } }'


	resp = requests.post(url, headers=headers, data=data)

	print(resp.status_code)
	return jsonify({'success': 'exito!'})


@bp.route('/user', methods=['PUT'])
def update_user_information():
	data = json.loads(request.data)
	email = data['email']	

	user = User.query.filter_by(email=email).first()
	user.name = data['name']
	db.session.commit()
	
	result = {
		'code': 200,
		'message': 'User updated'
	}

	return jsonify(result)


@bp.route('/password', methods=['PUT'])
def update_password_information():
	data = json.loads(request.data)
	email = data['email']	

	user = User.query.filter_by(email=email).first()
	user.set_password(data['password'])
	db.session.commit()
	
	result = {
		'code': 200,
		'message': 'User updated'
	}

	return jsonify(result)



@bp.route('/emergency', methods=['PUT'])
def update_emergency_information():
	data = json.loads(request.data)
	email = data['email']	

	user = User.query.filter_by(email=email).first()
	user.emai_contact = data['emai_contact']
	user.number_contact = data['number_contact']
	user.name_contact = data['name_contact']
	db.session.commit()
	
	result = {
		'code': 200,
		'message': 'User updated'
	}

	return jsonify(result)



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

	today = datetime.today().strftime('%Y-%m-%d')
	today_one_month_ago = (datetime.today() - timedelta(30)).strftime('%Y-%m-%d')

	record_date = RecordDate()
	record_date.initial_date = today
	record_date.last_date = today_one_month_ago
	db.session.add(record_date)
	db.session.commit()

	record_date_id = record_date.id

	user = User()
	user.from_dict(data)
	user.set_password(user.password)
	user.get_token()
	user.record_date_id = record_date_id
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

			record_date = RecordDate.query.filter_by(id=user.to_dict()['record_date_id']).first()

			initial_data = record_date.to_dict()['initial_date']
			last_date = record_date.to_dict()['last_date']
			token = user.to_dict()['token_fitbit']
			user_id = user.to_dict()['id']
			name = user.to_dict()['name']
			name_contact = user.to_dict()['name_contact']
			number_contact = user.to_dict()['number_contact']
			emai_contact = user.to_dict()['emai_contact']
			token_expired = False
			if token:
				token_expired = get_data(token, initial_data, last_date, user_id, record_date)
			

			if token_expired:
				new_token = refresh_token_fitbit(email)
				get_data(new_token, initial_data, last_date, user.id, record_date)

			result = {
				'code': 200,
				'message': 'the user exists',
				'email': email,
				'name': name,
				'name_contact': name_contact,
				'number_contact': number_contact,
				'emai_contact': emai_contact,
				'active_session': False if token_expired else True
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


	user = User.query.filter_by(email=email).first()

	
	token = user.to_dict()['token_fitbit']
	if token:
		refresh_token_fitbit(email)
	else:
		url = "https://api.fitbit.com/oauth2/token"

		headers = CaseInsensitiveDict()
		headers["Authorization"] = ""
		headers["Content-Type"] = "application/x-www-form-urlencoded"

		data = f'clientId=22BN2K&grant_type=authorization_code&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fdashboard&code={code}'


		resp = requests.post(url, headers=headers, data=data)
		json_resp = json.loads(resp.text)

		user.from_dict(data)
		user.token_fitbit = json_resp['access_token']
		user.refresh_token_fitbit = json_resp['refresh_token']
		user.user_id = json_resp['user_id']
		user.active_session = True
		db.session.commit()

		record_date = RecordDate.query.filter_by(id=user.record_date_id).first()

		initial_data = record_date.to_dict()['initial_date']
		last_date = record_date.to_dict()['last_date']


		token = json_resp['access_token']
		token_expired = False
		if token:
			token_expired = get_data(token, initial_data, last_date, user.id, record_date)

		if token_expired:
			new_token = refresh_token_fitbit(email)
			get_data(new_token, initial_data, last_date, user.id, record_date)


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
	headers["Authorization"] = ""
	headers["Content-Type"] = "application/x-www-form-urlencoded"

	data = f'clientId=22BN2K&grant_type=refresh_token&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fdashboard&refresh_token={refresh_token_fitbit}'


	resp = requests.post(url, headers=headers, data=data)
	json_resp = json.loads(resp.text)

	user.token_fitbit = json_resp['access_token']
	user.refresh_token_fitbit = json_resp['refresh_token']
	db.session.commit()

	print(resp.status_code)

	return json_resp['access_token']



#main
def get_data(token, today, today_one_month_ago, user_id, record_date):

	initial_date = record_date.to_dict()['initial_date']
	last_date = record_date.to_dict()['last_date']
	data_taken = record_date.to_dict()['data_taken']
	initial_date = datetime.strptime(initial_date.split(' ')[0], '%Y-%m-%d').date()
	last_date = datetime.strptime(last_date.split(' ')[0], '%Y-%m-%d').date()
	
	days_difference = (date.today() - initial_date).days

	token_expired = False


	if days_difference == 0 and data_taken == False:
		token_expired = get_heart_rate_record(token, today, today_one_month_ago, user_id)
		token_expired = get_activity_record(token, today, user_id)
		token_expired = get_weight_record(token, today, user_id)
		token_expired = get_breath_record(token, today, today_one_month_ago, user_id)
		token_expired = get_food_record(token, today, user_id)
		token_expired = get_sleep_record(token, today, today_one_month_ago, user_id)
		token_expired = get_blood_oxygen_saturation_record(token, today, today_one_month_ago, user_id)
		token_expired = get_temperature_record(token, today, today_one_month_ago, user_id)

		record_date.data_taken = 1
		db.session.commit()

	elif days_difference > 0 and data_taken == True:

		token_expired = get_heart_rate_record(token, today, today_one_month_ago, user_id)
		token_expired = get_activity_record(token, today, user_id)
		token_expired = get_weight_record(token, today, user_id)
		token_expired = get_breath_record(token, today, today_one_month_ago, user_id)
		token_expired = get_food_record(token, today, user_id)
		token_expired = get_sleep_record(token, today, today_one_month_ago, user_id)
		token_expired = get_blood_oxygen_saturation_record(token, today, today_one_month_ago, user_id)
		token_expired = get_temperature_record(token, today, today_one_month_ago, user_id)

		record_date.initial_date = date.today()
		record_date.last_date = initial_date
		record_date.data_taken = 0
		db.session.commit()


	return token_expired


# heart rate
def get_heart_rate_record(token, today, today_one_month_ago, user_id):
	url = f"https://api.fitbit.com/1/user/-/activities/heart/date/{today.split(' ')[0]}/{today_one_month_ago.split(' ')[0]}.json"

	headers = CaseInsensitiveDict()
	headers["Authorization"] = f"Bearer {token}"
	headers["accept"] = "application/json"


	resp = requests.get(url, headers=headers)
	json_resp = json.loads(resp.text)

	token_expired = False
	if 'errors' in json_resp:
		if json_resp['errors'][0]['errorType'] == 'expired_token':
			token_expired = True
			return token_expired
	else:
		json_resp = json_resp['activities-heart']
		df =  pd.DataFrame(json_resp, columns=['dateTime', 'value'])
		df.apply(lambda row: create_hr_record(row['dateTime'], row['value'], user_id), axis=1)


def create_hr_record(date, value, user_id):
	if len(value) == 2:
		hr_record = HeartRateData()
		hr_record.heart_rate_avg = random.randrange(60,100)
		hr_record.complete_date = date
		hr_record.user_id = user_id
		db.session.add(hr_record)
		db.session.commit()
	else:
		#here there is data
		pass



#activity 
def get_activity_record(token, today, user_id):
	url = f"https://api.fitbit.com/1/user/-/activities.json"

	headers = CaseInsensitiveDict()
	headers["Authorization"] = f"Bearer {token}"
	headers["accept"] = "application/json"


	resp = requests.get(url, headers=headers)
	json_resp = json.loads(resp.text)
	token_expired = False
	if 	'errors' in json_resp:
		if json_resp['errors'][0]['errorType'] == 'expired_token':
			token_expired = True
			return token_expired
	else:
		create_activity_record(today, user_id)


def create_activity_record(date, user_id):
	for i in range(1,60):
		random_date = ((datetime.strptime(date.split(' ')[0], '%Y-%m-%d').date()) - timedelta(i)).strftime('%Y-%m-%d')

		activity_record = ActivityData()
		activity_record.calories = random.randrange(300,500)
		activity_record.distance = random.randrange(500, 5000)
		activity_record.steps = random.randrange(10000, 20000)
		activity_record.complete_date = random_date
		activity_record.user_id = user_id
		db.session.add(activity_record)
		db.session.commit()



#weight
def get_weight_record(token, today, user_id):
	url = f"https://api.fitbit.com/1/user/-/body/log/weight/date/{today.split(' ')[0]}.json"

	headers = CaseInsensitiveDict()
	headers["Authorization"] = f"Bearer {token}"
	headers["accept"] = "application/json"


	resp = requests.get(url, headers=headers)
	json_resp = json.loads(resp.text)
	token_expired = False

	if 	'errors' in json_resp:
		if json_resp['errors'][0]['errorType'] == 'expired_token':
			token_expired = True
			return token_expired
	else:
		create_weight_record(today, user_id, json_resp)


def create_weight_record(date, user_id, json_resp):
	if len(json_resp['weight']) == 0:
		for i in range(1,60):
			random_date = ((datetime.strptime(date.split(' ')[0], '%Y-%m-%d').date()) - timedelta(i)).strftime('%Y-%m-%d')

			weight_record = WeightData()
			weight_record.bmi = decimal.Decimal(random.randrange(2500, 3000))/100
			weight_record.fat = decimal.Decimal(random.randrange(2500, 3000))/100
			weight_record.weight = random.randrange(60, 70)
			weight_record.complete_date = random_date
			weight_record.user_id = user_id
			db.session.add(weight_record)
			db.session.commit()
	else:
		#here there is data
		pass



#breathing
def get_breath_record(token, today, today_one_month_ago, user_id):

	today_twenty_eight_days_ago  = datetime.strptime(today.split(' ')[0], '%Y-%m-%d').date() 
	today_twenty_eight_days_ago = (today_twenty_eight_days_ago - timedelta(10)).strftime('%Y-%m-%d')
	url = f"https://api.fitbit.com/1/user/-/br/date/{today_twenty_eight_days_ago}/{today_one_month_ago.split(' ')[0]}.json"

	headers = CaseInsensitiveDict()
	headers["Authorization"] = f"Bearer {token}"
	headers["accept"] = "application/json"


	resp = requests.get(url, headers=headers)
	json_resp = json.loads(resp.text)

	token_expired = False
	if 'errors' in json_resp:
		if json_resp['errors'][0]['errorType'] == 'expired_token':
			token_expired = True
			return token_expired
	else:
		if len(json_resp['br']) == 0:
			create_breath_record(today, decimal.Decimal(random.randrange(15000, 17000))/100, user_id)
		else:
			#real data
			json_resp = json_resp['activities-heart']
			df =  pd.DataFrame(json_resp, columns=['dateTime', 'value'])
			df.apply(lambda row: create_breath_record(row['dateTime'], row['value'], user_id), axis=1)


def create_breath_record(date, value, user_id):
	for i in range(1,60):
		random_date = ((datetime.strptime(date.split(' ')[0], '%Y-%m-%d').date()) - timedelta(i)).strftime('%Y-%m-%d')

		breath_record = BreathData()
		breath_record.breath_rate = value
		breath_record.complete_date = random_date
		breath_record.user_id = user_id
		db.session.add(breath_record)
		db.session.commit()



#food
def get_food_record(token, today, user_id):

	url = f"https://api.fitbit.com/1/user/-/foods/log/date/{today.split(' ')[0]}.json"

	headers = CaseInsensitiveDict()
	headers["Authorization"] = f"Bearer {token}"
	headers["accept"] = "application/json"


	resp = requests.get(url, headers=headers)
	json_resp = json.loads(resp.text)

	token_expired = False
	if 'errors' in json_resp:
		if json_resp['errors'][0]['errorType'] == 'expired_token':
			token_expired = True
			return token_expired
	else:
		if len(json_resp['foods']) == 0:
			create_food_record(today, decimal.Decimal(random.randrange(15000, 17000))/100, user_id)
		else:
			#real data
			json_resp = json_resp['activities-heart']
			df =  pd.DataFrame(json_resp, columns=['dateTime', 'value'])
			df.apply(lambda row: create_food_record(row['dateTime'], row['value'], user_id), axis=1)


def create_food_record(date, value, user_id):
	for i in range(1,60):
		random_date = ((datetime.strptime(date.split(' ')[0], '%Y-%m-%d').date()) - timedelta(i)).strftime('%Y-%m-%d')

		food_record = FootData()
		food_record.amount = 1
		food_record.brand = 'local'
		food_record.calories = 848
		food_record.carbs = 2.31
		food_record.fat = 21.36
		food_record.fiber = 0
		food_record.protein = 151.68
		food_record.sodium = 358
		food_record.water = 0
		food_record.name = 'chicken leg'
		food_record.complete_date = random_date
		food_record.user_id = user_id
		db.session.add(food_record)
		db.session.commit()


#sleep 
def get_sleep_record(token, today, today_one_month_ago, user_id):

	today_twenty_eight_days_ago  = datetime.strptime(today.split(' ')[0], '%Y-%m-%d').date() 
	today_twenty_eight_days_ago = (today_twenty_eight_days_ago - timedelta(10)).strftime('%Y-%m-%d')
	url = f"https://api.fitbit.com/1.2/user/-/sleep/date/{today_one_month_ago.split(' ')[0]}/{today_twenty_eight_days_ago}.json"

	headers = CaseInsensitiveDict()
	headers["Authorization"] = f"Bearer {token}"
	headers["accept"] = "application/json"


	resp = requests.get(url, headers=headers)
	json_resp = json.loads(resp.text)

	token_expired = False
	if 'errors' in json_resp:
		if json_resp['errors'][0]['errorType'] == 'expired_token':
			token_expired = True
			return token_expired
	else:
		if len(json_resp['sleep']) == 0:
			create_sleep_record(today, random.randrange(300,500), user_id)
		else:
			#real data
			json_resp = json_resp['activities-heart']
			df =  pd.DataFrame(json_resp, columns=['dateTime', 'value'])
			df.apply(lambda row: create_breath_record(row['dateTime'], row['value'], user_id), axis=1)


def create_sleep_record(date, value, user_id):
	for i in range(1,60):
		random_date = ((datetime.strptime(date.split(' ')[0], '%Y-%m-%d').date()) - timedelta(i)).strftime('%Y-%m-%d')

		sleep_record = SleepData()
		sleep_record.category = 'ASLEEP'
		sleep_record.minutes = value
		sleep_record.complete_date = random_date
		sleep_record.user_id = user_id
		db.session.add(sleep_record)
		db.session.commit()


#blood_oxygen_saturation_data
def get_blood_oxygen_saturation_record(token, today, today_one_month_ago, user_id):

	today_twenty_eight_days_ago  = datetime.strptime(today.split(' ')[0], '%Y-%m-%d').date() 
	today_twenty_eight_days_ago = (today_twenty_eight_days_ago - timedelta(10)).strftime('%Y-%m-%d')
	url = f"https://api.fitbit.com/1/user/-/spo2/date/{today_twenty_eight_days_ago}/{today_one_month_ago.split(' ')[0]}.json"

	headers = CaseInsensitiveDict()
	headers["Authorization"] = f"Bearer {token}"
	headers["accept"] = "application/json"


	resp = requests.get(url, headers=headers)
	json_resp = json.loads(resp.text)
	token_expired = False
	if 'errors' in json_resp:
		if json_resp['errors'][0]['errorType'] == 'expired_token':
			token_expired = True
			return token_expired
	else:
		if len(json_resp) == 0:
			create_blood_oxygen_saturation_record(today, user_id)
		else:
			#real data
			json_resp = json_resp['activities-heart']
			df =  pd.DataFrame(json_resp, columns=['dateTime', 'value'])
			df.apply(lambda row: create_breath_record(row['dateTime'], row['value'], user_id), axis=1)


def create_blood_oxygen_saturation_record(date, user_id):
	for i in range(1,60):
		random_date = ((datetime.strptime(date.split(' ')[0], '%Y-%m-%d').date()) - timedelta(i)).strftime('%Y-%m-%d')

		avg = decimal.Decimal(random.randrange(60000, 90000))/100
		max = decimal.Decimal(random.randrange(60000, 90000))/100
		min = decimal.Decimal(random.randrange(60000, 90000))/100

		blood_oxygen_saturation_record = BloodOxygenSaturationData()
		blood_oxygen_saturation_record.avg = avg
		blood_oxygen_saturation_record.max = max
		blood_oxygen_saturation_record.min = min
		blood_oxygen_saturation_record.complete_date = random_date
		blood_oxygen_saturation_record.user_id = user_id
		db.session.add(blood_oxygen_saturation_record)
		db.session.commit()



#temperature data
def get_temperature_record(token, today, today_one_month_ago, user_id):

	today_twenty_eight_days_ago  = datetime.strptime(today.split(' ')[0], '%Y-%m-%d').date() 
	today_twenty_eight_days_ago = (today_twenty_eight_days_ago - timedelta(10)).strftime('%Y-%m-%d')
	url = f"https://api.fitbit.com/1/user/-/temp/core/date/{today_twenty_eight_days_ago}/{today_one_month_ago.split(' ')[0]}.json"

	headers = CaseInsensitiveDict()
	headers["Authorization"] = f"Bearer {token}"
	headers["accept"] = "application/json"


	resp = requests.get(url, headers=headers)
	json_resp = json.loads(resp.text)
	token_expired = False
	if 'errors' in json_resp:
		if json_resp['errors'][0]['errorType'] == 'expired_token':
			token_expired = True
			return token_expired
	else:
		if len(json_resp['tempCore']) == 0:
			create_temperature_record(today, user_id)
		else:
			#real data
			json_resp = json_resp['activities-heart']
			df =  pd.DataFrame(json_resp, columns=['dateTime', 'value'])
			df.apply(lambda row: create_breath_record(row['dateTime'], row['value'], user_id), axis=1)


def create_temperature_record(date, user_id):
	for i in range(1,60):
		random_date = ((datetime.strptime(date.split(' ')[0], '%Y-%m-%d').date()) - timedelta(i)).strftime('%Y-%m-%d')

		temperature = decimal.Decimal(random.randrange(25000, 36000))/100

		temperature_record = TemperatureData()
		temperature_record.temperature = temperature
		temperature_record.complete_date = random_date
		temperature_record.user_id = user_id
		db.session.add(temperature_record)
		db.session.commit()