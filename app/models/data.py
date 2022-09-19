from .default_models import CustomSerializer
from app import db

from sqlalchemy.sql import func
from sqlalchemy_serializer import SerializerMixin

class Data(db.Model, SerializerMixin, CustomSerializer):

    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True)
    heart_rate = db.Column(db.Float, nullable=True)
    lat = db.Column(db.String(200), nullable=True)
    lon = db.Column(db.String(200), nullable=True) 
    accelerometer= db.Column(db.Float, nullable=True)
    barometer =  db.Column(db.Float, nullable=True)
    user_device_id = db.Column(db.Integer, db.ForeignKey('user_device.id'), nullable=False, server_default='1')
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    fields = ['id','heart_rate','lat','lon','accelerometer','barometer', 'user_device_id', 'created_at', 'updated_at']

    def __repr__(self):
        return f'<Data {self.id}.>'