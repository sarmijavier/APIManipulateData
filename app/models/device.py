from .default_models import CustomSerializer
from app import db

from sqlalchemy.sql import func
from sqlalchemy_serializer import SerializerMixin


class Device(db.Model, SerializerMixin, CustomSerializer):

    __tablename__ = 'device'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    fields = ['id','code', 'created_at','updated_at']

    def __repr__(self):
        return f'<Device {self.id}.>'