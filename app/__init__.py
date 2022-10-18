from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config

app = Flask(__name__)
app.config.from_object(Config) 

db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)

from app.models import heart_rate_data, record_date, user
from app.api import bp as bp

app.register_blueprint(bp, url_prefix='/api/v1/')
