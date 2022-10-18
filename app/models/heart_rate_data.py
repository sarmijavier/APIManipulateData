from .default_models import CustomSerializer
from app import db

from sqlalchemy.sql import func
from sqlalchemy_serializer import SerializerMixin

class HeartRateData(db.Model, SerializerMixin, CustomSerializer):

    __tablename__ = 'heart_rate_data'
    id = db.Column(db.Integer, primary_key=True)
    heart_rate_avg = db.Column(db.Float, nullable=True)
    complete_date = db.Column(db.DateTime(timezone=True), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, server_default='0')
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    fields = ['id','heart_rate_avg', 'complete_date', 'created_at', 'updated_at']

    def __repr__(self):
        return f'<HeartRateData {self.id}.>'