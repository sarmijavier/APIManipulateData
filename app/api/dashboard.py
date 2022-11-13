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

import sqlalchemy as db_manager
import pymysql
import pandas as pd
import os

@bp.route('/csv', methods=['POST'])
def get_csv():
	data = json.loads(request.data)

	email = data['email']	

	user = User.query.filter_by(email=email).first()

	host = 'localhost:3306'
	user = 'root'
	passwd = ''
	database = 'db_thesis'
	conn = "mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4"
	conn = conn.format(user,passwd,host,database)
	engine = db_manager.create_engine(conn)

	query = "select * from db_thesis.heart_rate_data hrd"
	query2 = "select * from db_thesis.activity_data ad"
	query3 = "select * from db_thesis.blood_oxygen_saturation_data bosd"
	query4 = "select * from db_thesis.breath_data bd"
	query5 = "select * from db_thesis.foot_data fd"
	query6 = "select * from db_thesis.sleep_data sd"
	query7 = "select * from db_thesis.temperature_data td"
	query8 = "select * from db_thesis.weight_data wd"

	df = pd.read_sql(query, engine)
	df2 = pd.read_sql(query2, engine)
	df3 = pd.read_sql(query3, engine)
	df4 = pd.read_sql(query4, engine)
	df5 = pd.read_sql(query5, engine)
	df6 = pd.read_sql(query6, engine)
	df7 = pd.read_sql(query7, engine)
	df8 = pd.read_sql(query8, engine)

	titles_df = ['id', 'heart_rate_avg', 'complete_date', 'created_at', 'updated_at']
	titles_df2 = ['id', 'calories', 'distance', 'steps', 'complete_date', 'user_id', 'created_at', 'updated_at']
	titles_df3 = ['id', 'avg', 'min', 'max', 'complete_date', 'user_id', 'created_at', 'updated_at']
	titles_df4 = ['id', 'breath_rate', 'complete_date', 'user_id', 'created_at', 'updated_at']
	titles_df5 = ['id', 'amount', 'brand', 'calories', 'carbs', 'fat', 'fat', 'fiber', 'protein', 'sodium', 'water', 'name' 'complete_date', 'user_id', 'created_at', 'updated_at']
	titles_df6 = ['id', 'category', 'minutes', 'complete_date', 'user_id', 'created_at', 'updated_at']
	titles_df7 = ['id', 'temperature', 'complete_date', 'user_id', 'created_at', 'updated_at']
	titles_df8 = ['id', 'bmi', 'fat', 'weight', 'user_id', 'complete_date', 'created_at', 'updated_at']

	df_list = df.values.tolist()
	df_list.insert(0, titles_df)

	df_list2 = df2.values.tolist()
	df_list2.insert(0, titles_df2)

	df_list3 = df3.values.tolist()
	df_list3.insert(0, titles_df3)

	df_list4 = df4.values.tolist()
	df_list4.insert(0, titles_df4)

	df_list5 = df5.values.tolist()
	df_list5.insert(0, titles_df5)

	df_list6 = df6.values.tolist()
	df_list6.insert(0, titles_df6)
	
	df_list7 = df7.values.tolist()
	df_list7.insert(0, titles_df7)
	
	df_list8 = df8.values.tolist()
	df_list8.insert(0, titles_df8)

	return jsonify({
		'data': df_list,
		'data2': df_list2,
		'data3': df_list3,
		'data4': df_list4,
		'data5': df_list5,
		'data6': df_list6,
		'data7': df_list7,
		'data8': df_list8,
	})



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