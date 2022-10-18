from .default_models import CustomSerializer
from app import db

from sqlalchemy.sql import func
from sqlalchemy_serializer import SerializerMixin


class RecordDate(db.Model, SerializerMixin, CustomSerializer):
    __tablename__ = 'record_date'
    
    id = db.Column(db.Integer, primary_key=True)
    initial_date = db.Column(db.DateTime(timezone=True), nullable=False)
    last_date = db.Column(db.DateTime(timezone=True), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    fields = ['id','initial_date', 'last_date', 'created_at','updated_at']

    def __repr__(self):
        return f'<RecordDate {self.id}.>'