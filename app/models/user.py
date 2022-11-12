from .default_models import CustomSerializer
from app import db

from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime, timedelta
import os
import base64


class User(db.Model, SerializerMixin, CustomSerializer):
    """ class with all the information of the table user """

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    token_fitbit = db.Column(db.String(1000))
    user_id = db.Column(db.String(32))
    refresh_token_fitbit = db.Column(db.String(1000))
    active_session = db.Column(db.Boolean, default=False, nullable=False)
    record_date_id = db.Column(db.Integer, db.ForeignKey('record_date.id'), nullable=False, server_default='1')
    emai_contact = db.Column(db.String(150), nullable=False)
    number_contact = db.Column(db.String(150), nullable=False)
    name_contact = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    
    fields = [
        'id', 
        'name', 
        'email', 
        'password',
        'token_fitbit',
        'refresh_token_fitbit',
        'user_id',
        'active_session',
        'emai_contact',
        'number_contact',
        'name_contact',
        'created_at', 
        'updated_at',
    ]    

    def get_token(self, expires_in=30):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token

        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(days=expires_in)
        db.session.add(self)

        return self.token


    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)


    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None

        return user


    def set_password(self, password):
        self.password = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.email}.>'