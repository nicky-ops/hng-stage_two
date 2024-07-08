'''
This module creates the models - User and Organization
'''
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import uuid
from sqlalchemy.orm import relationship


db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

user_organisation = db.Table('user_organisation',
                             db.Column('user_id', db.String(50), db.ForeignKey('user.user_id'), primary_key=True),
                             db.Column('org_id', db.String(50), db.ForeignKey('organisations.org_id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'User'

    user_id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    organisations = relationship('Organisation', secondary=user_organisation, back_populates='users')


    def hash_password(self):
        self.password = bcrypt.generate_password_hash(self.password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    

class Organisation(db.Model):
    __tablename__ = 'organisations'

    org_id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))

    users = db.relationship('User', secondary='user_organisation', backref='organisations')


