from .default_models import CustomSerializer
from app import db

from sqlalchemy.sql import func
from sqlalchemy_serializer import SerializerMixin

class FootData(db.Model, SerializerMixin, CustomSerializer):

	__tablename__ = 'foot_data'
	id = db.Column(db.Integer, primary_key=True)
	amount = db.Column(db.Integer, nullable=True)
	brand = db.Column(db.String(100), nullable=True)
	calories = db.Column(db.Float, nullable=True)
	carbs = db.Column(db.Float, nullable=True)
	fat = db.Column(db.Float, nullable=True)
	fiber = db.Column(db.Float, nullable=True)
	protein = db.Column(db.Float, nullable=True)
	sodium = db.Column(db.Float, nullable=True)
	water = db.Column(db.Float, nullable=True)
	name = db.Column(db.String(500), nullable=True)
	complete_date = db.Column(db.DateTime(timezone=True), nullable=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, server_default='0')
	created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
	updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

	fields = ['id','amount', 'brand', 'calories', 'carbs', 'fat', 'fiber', 'protein', 'sodium', 'water', 'name', 'complete_date', 'user_id', 'created_at', 'updated_at']

	def __repr__(self):
		return f'<FoodData {self.id}.>'