# health_diagnosis/src/schema.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

class Diagnosis(db.Model):
    __tablename__ = 'diagnoses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    symptoms = db.Column(db.String(500), nullable=False)
    diagnosis = db.Column(db.String(200), nullable=False)
    confidence = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('diagnoses', lazy=True))

    def __repr__(self):
        return f"<Diagnosis {self.diagnosis} for User {self.user_id}>"
    
class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    hospital = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    website = db.Column(db.String(200))
    accepts_new_patients = db.Column(db.Boolean, default=True)
    insurance_accepted = db.Column(db.String(200))  # New field
    appointment_link = db.Column(db.String(200))  # New field
    latitude = db.Column(db.Float)  # New field for map integration
    longitude = db.Column(db.Float)  # New field for map integration
    def __repr__(self):
        return f"<Doctor {self.name}, {self.specialty}>"
    