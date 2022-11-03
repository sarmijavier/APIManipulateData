from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config

app = Flask(__name__)
app.config.from_object(Config) 

db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)

from app.models import heart_rate_data, record_date, user, activity_data, weight_data, breath_data, food_data, sleep_data, blood_oxygen_saturation_data, temperature_data
from app.api import bp as bp

app.register_blueprint(bp, url_prefix='/api/v1/')
