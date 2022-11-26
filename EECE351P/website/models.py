from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

VIPRoom = 10
SupreemRoom = 5
Economy = 50

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    room = db.relationship('GuestRoom')
    RegistrationDetails = db.relationship('RegistrationDetail')

class GuestRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    check_in_month = db.Column(db.String(150))
    checkInDay = db.Column(db.Integer)
    checkOutMonth = db.Column(db.String(150))
    checkOutDay = db.Column(db.Integer)
    numOfPeople = db.Column(db.String(150))
    roomSize = db.Column(db.String(150))

class RegistrationDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    breakFast = db.Column(db.String(150))