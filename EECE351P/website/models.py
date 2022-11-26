from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class HotelRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    checkin= db.Column(db.String(150))
    checkout = db.Column(db.String(150))
    numOfPeople = db.Column(db.String(150))
    roomType = db.Column(db.String(150))
    breakFast = db.Column(db.String(150))
    totalPrice = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    lastName = db.Column(db.String(150))
    hotelroom = relationship('HotelRoom', backref='user', lazy=True) 
    
    
def checkAvailibility(roomType):
    hotelroom = HotelRoom.query.filter_by(roomType=roomType)
    registerDate = sorted([x.checkin for x in hotelroom])
    leaveDate = sorted([x.checkout for x in hotelroom])
    count = 50 if int(roomType) == 1 else 30 if roomType == 2 else 10
    import datetime
    i = j = 0
    while i < len(registerDate):
        checkin = registerDate[i]
        x = datetime.datetime(int(checkin[:4]), int(checkin[5:7]), int(checkin[8:]))
        checkout = leaveDate[i]
        y = datetime.datetime(int(checkout[:4]), int(checkout[5:7]), int(checkout[8:])) 
        if x < y:
            i+=1
            count -=1
        else:
            j += 1
            count +=1
        if count < 0:
            return False
    return True
