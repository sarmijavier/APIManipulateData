from .default_models import CustomSerializer
from app import db

from sqlalchemy.sql import func
from sqlalchemy_serializer import SerializerMixin

class WeightData(db.Model, SerializerMixin, CustomSerializer):

	__tablename__ = 'weight_data'
	id = db.Column(db.Integer, primary_key=True)
	bmi = db.Column(db.Float, nullable=True)
	fat = db.Column(db.Float, nullable=True)
	weight = db.Column(db.Float, nullable=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, server_default='0')
	complete_date = db.Column(db.DateTime(timezone=True), nullable=True)
	created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
	updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

	fields = ['id','bmi', 'fat', 'weight',  'user_id', 'complete_date', 'created_at', 'updated_at']

	def __repr__(self):
		return f'<WeightData {self.id}.>'