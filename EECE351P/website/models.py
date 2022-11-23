from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

class GuestRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    check_in_month = db.Column(db.String(150))
    checkInDay = db.Column(db.Integer)
    checkOutMonth = db.Column(db.String(150))
    checkOutDay = db.Column(db.Integer)
    # user_key =  db.Column(db.Integer, db.ForeignKey('user.id'))