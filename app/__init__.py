from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config

app = Flask(__name__)
app.config.from_object(Config) 

db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)

from app.models import user, data, user_device, device

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"