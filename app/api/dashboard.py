from app.api import bp
from app import db
from app.models.heart_rate_data import HeartRateData
from app.models.user import User
from app.models.activity_data import ActivityData
from app.models.blood_oxygen_saturation_data import BloodOxygenSaturationData
from app.models.breath_data import BreathData
from app.models.food_data import FootData
from app.models.sleep_data import SleepData
from app.models.temperature_data import TemperatureData
from app.models.weight_data import WeightData



from flask import request, jsonify
import json

import requests
from requests.structures import CaseInsensitiveDict
from datetime import datetime, timedelta, date

import pandas as pd
import random
import decimal


@bp.route('/dashboard', methods=['POST'])
def get_heart_rate():
	data = json.loads(request.data)

	email = data['email']	

	user = User.query.filter_by(email=email).first()
	user_information = user.to_dict()

	user_id = user_information['id']

	data = {}

	data['hr'] = get_heart_rate_data(user_id)
	data['activity'] = get_activity_data(user_id)
	data['spo'] = get_spo_data(user_id)
	data['breath'] = get_breath_data(user_id)
	data['food'] = get_food_data(user_id)
	data['sleep'] = get_sleep_data(user_id)
	data['temperature'] = get_temperature_data(user_id)
	data['weight'] = get_weight_data(user_id)

	return jsonify(data)



def get_heart_rate_data(user_id):

	information = HeartRateData.query.filter_by(user_id=user_id).limit(10).all()
	information_array = []
	[information_array.append(x.to_dict()) for x in information]

	return information_array



def get_activity_data(user_id):

	information = ActivityData.query.filter_by(user_id=user_id).order_by(ActivityData.id.desc()).limit(10).all()
	information_array = []
	[information_array.append(x.to_dict()) for x in information]

	return information_array



def get_spo_data(user_id):

	information = BloodOxygenSaturationData.query.filter_by(user_id=user_id).limit(10).all()
	information_array = []
	[information_array.append(x.to_dict()) for x in information]

	return information_array



def get_breath_data(user_id):

	information = BreathData.query.filter_by(user_id=user_id).limit(10).all()
	information_array = []
	[information_array.append(x.to_dict()) for x in information]

	return information_array



def get_food_data(user_id):

	information = FootData.query.filter_by(user_id=user_id).limit(10).all()
	information_array = []
	[information_array.append(x.to_dict()) for x in information]

	return information_array


def get_sleep_data(user_id):

	information = SleepData.query.filter_by(user_id=user_id).limit(10).all()
	information_array = []
	[information_array.append(x.to_dict()) for x in information]

	return information_array



def get_temperature_data(user_id):

	information = TemperatureData.query.filter_by(user_id=user_id).limit(10).all()
	information_array = []
	[information_array.append(x.to_dict()) for x in information]

	return information_array



def get_weight_data(user_id):

	information = WeightData.query.filter_by(user_id=user_id).limit(10).all()
	information_array = []
	[information_array.append(x.to_dict()) for x in information]

	return information_array