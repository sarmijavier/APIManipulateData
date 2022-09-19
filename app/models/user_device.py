from .default_models import CustomSerializer
from app import db

from sqlalchemy.sql import func
from sqlalchemy_serializer import SerializerMixin


class UserDevice(db.Model, SerializerMixin, CustomSerializer):

    __tablename__ = 'user_device'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, server_default='1')
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False, server_default='1')
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    fields = ['id','user_id','device_id','created_at','updated_at']

    def __repr__(self):
        return f'<User Device {self.id}, USER {self.user_id}, DEVICE {self.device_id}.>'