from app.api import bp
from app import db
from app.models.heart_rate_data import HeartRateData
from app.models.user import User

from flask import request, jsonify
import json

import requests
from requests.structures import CaseInsensitiveDict
from datetime import datetime, timedelta, date

import pandas as pd
import random
import decimal


@bp.route('/hr', methods=['POST'])
def get_heart_rate():
	data = json.loads(request.data)

	email = data['email']	


	user = User.query.filter_by(email=email).first()
	user_information = user.to_dict()

	user_id = user_information['id']

	hr_information = HeartRateData.query.filter_by(user_id=user_id).all()
	hr_array = []
	[hr_array.append(x.to_dict()) for x in hr_information]

	return jsonify(hr_array)
