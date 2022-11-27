from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, HotelRoom, checkAvailibility
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db
import datetime
auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in Successfully!', category = 'success')
                login_user(user, remember=True)
                return redirect(url_for('auth.Book'))
            else:
                flash('Incorrect Password, Please Try Again!', category = 'error')
        else:
            flash('Email Does Not Exist!', category = 'error')
    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required 
def logout():
    flash('Logged Out Successfully!', category = 'success')
    logout_user()
    return redirect(url_for('views.home'))

@auth.route('sign-up', methods = ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters!', category = 'error')
        elif not('yahoo' in email or 'gmail' in email or 'hotmail' in email or 'outlook' in email):
            flash('Please Enter a valid email address!', category = 'error')
        elif len(firstName) < 3:
            flash('Please Enter a Valid First Name!', category = 'error')
        elif str(password1) != str(password2):
            flash('passwords don\'t match', category = 'error')
        elif len(password1) < 7:
            flash('Password is not secure!', category = 'error')
        else:
            new_user = User(email=email, firstName=firstName, password=generate_password_hash(
            password1, method='sha256'), lastName = lastName)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account successfully created!', category = 'success')
            return redirect(url_for('auth.login'))
    return render_template("sign-up.html", user = current_user)

@auth.route('book', methods=['GET','POST'])
@login_required
def Book():
    if request.method=='POST':
        roomType= request.form.get('roomType')
        breakfast= request.form.get('breakfast')
        numofpeople= request.form.get('number')
        checkin = request.form.get('checkin')
        checkout = request.form.get('checkout')
        if int(roomType) == 1:
            roomPrice = 50
        elif int(roomType) == 2:
            roomPrice = 100
        elif int(roomType) == 3:
            roomPrice = 150
        if int(breakfast) == 1:
            breakfastPrice = 10
        elif int(breakfast) == 2:
            breakfastPrice = 20
        else:
            breakfastPrice = 30
        totalPrice = (roomPrice + breakfastPrice) * int(numofpeople) * int(str(datetime.datetime(int(checkout[:4]), int(checkout[5:7]), int(checkout[8:]))\
    - datetime.datetime(int(checkin[:4]), int(checkin[5:7]), int(checkin[8:]))
)[:2])

        if datetime.datetime(int(checkin[:4]), int(checkin[5:7]), int(checkin[8:]), 23, 59, 59) < datetime.datetime.today():
            flash('Please Enter a Valid Check In Date!', category = 'error')
            redirect(url_for('auth.Book'))
        elif datetime.datetime(int(checkin[:4]), int(checkin[5:7]), int(checkin[8:])) > datetime.datetime(int(checkout[:4]), int(checkout[5:7]), int(checkout[8:])):
            flash('Please Enter a Valid Check Out Date!', category = 'error')
            redirect(url_for('auth.Book'))
        elif int(numofpeople) > 1 and int(roomType) == 1:
            flash('Please Book a larger room!', category = 'error')
            redirect(url_for('auth.Book'))
        elif int(numofpeople) > 3 and int(roomType) == 2:
            flash('Please Book a larger room!', category = 'error')
            redirect(url_for('auth.Book'))
        elif(-int(checkin[:4]) + int(checkout[:4]) > 1): 
            flash("You cannot book the room for more than a year!", category = 'error')
            redirect(url_for('auth.Book'))
        else: 
            new_room = HotelRoom(roomType=roomType, breakFast=breakfast, numOfPeople=numofpeople, checkin=checkin, checkout=checkout, totalPrice=totalPrice, user_id = current_user.id)
            db.session.add(new_room)
            db.session.commit()
            if not checkAvailibility(roomType):
                flash('Room Not Available!', category = 'error')
                db.session.delete(new_room)
                db.session.commit()
                redirect(url_for('auth.Book'))
            else:
                flash('You have successfully booked the room\n please check your registration details', category = 'success')
                return redirect(url_for('auth.About'))
    return render_template("Book.html", user = current_user)

@auth.route("/About", methods=['GET','POST'])
@login_required
def About():
    room = HotelRoom.query.filter_by(id=current_user.id).first()
    if not room:
        flash('Please Book a Room First!', category = 'error')
        return redirect(url_for('auth.Book'))
    if request.method == 'POST':
        dell = request.form.get('delete')
        people = request.form.get('updatePeople')
        checkin = request.form.get('checkin')
        checkout = request.form.get('checkout')
        print(dell)
        if dell:
            cancelRegistration(current_user.id)
        elif people:
            changeNumberOfPeople(current_user.id, request.form.get('updatePeople'))
        elif checkin:
            changeRoomNight(current_user.id, checkin, checkout)
    return render_template("About.html", user = current_user, room = room)

@login_required
def cancelRegistration(id):
    room = HotelRoom.query.filter_by(id=id).first()
    if room:
        db.session.delete(room)
        db.session.commit()
        flash('You have successfully cancelled your room booking!', category = 'success')
        return redirect(url_for('auth.Book'))
    else:
        flash('You have not yet book a room!', category = 'error')
        return redirect(url_for('auth.Book'))

@login_required
def changeNumberOfPeople(id, num):
    room = HotelRoom.query.filter_by(id=id).first()
    if room:
        room.numOfPeople = int(room.numOfPeople) +  int(num)
        if room.numOfPeople > 6:
            flash('You cannot be more than 6 guests, please book a new room!', category = 'error')
            room.numOfPeople = 6
            return redirect(url_for('auth.About'))
        checkin = room.checkin
        checkout =  room.checkout
        room.totalPrice = (int(room.roomType)* 50 + int(room.breakFast) * 10) * int(room.numOfPeople) * int(str(datetime.datetime(int(checkout[:4]), int(checkout[5:7]), int(checkout[8:]))\
    - datetime.datetime(int(checkin[:4]), int(checkin[5:7]), int(checkin[8:]))
)[:2])
        db.session.commit()
        flash('You have successfully changed the number of people!', category = 'success')
        return redirect(url_for('auth.Book'))
    else:
        flash('Room does not exist!', category = 'error')
        return redirect(url_for('auth.Book'))

@login_required #there are some changes to be made here
def changeRoomNight(id, checkin, checkout):
    room = HotelRoom.query.filter_by(id=id).first()
    if room:
        import datetime
        if datetime.datetime(int(checkin[:4]), int(checkin[5:7]), int(checkin[8:]), 23, 59, 59) < datetime.datetime.today():
            flash('Please Enter a Valid Check In Date!', category = 'error')
            redirect(url_for('auth.Book'))
        elif datetime.datetime(int(checkin[:4]), int(checkin[5:7]), int(checkin[8:])) > datetime.datetime(int(checkout[:4]), int(checkout[5:7]), int(checkout[8:])):
            flash('Please Enter a Valid Check Out Date!', category = 'error')
            redirect(url_for('auth.Book'))
        elif(-int(checkin[:4]) + int(checkout[:4]) > 1): 
            flash("You cannot book the room for more than a year!", category = 'error')
            redirect(url_for('auth.Book'))
        else:
            temp1 = room.checkin
            temp2 = room.checkout
            room.checkin = checkin
            room.checkout = checkout
            if checkAvailibility(room.roomType):
                room.totalPrice = (int(room.roomType)* 50 + int(room.breakFast) * 10) * int(room.numOfPeople) * int(str(datetime.datetime(int(checkout[:4]), int(checkout[5:7]), int(checkout[8:]))\
    - datetime.datetime(int(checkin[:4]), int(checkin[5:7]), int(checkin[8:]))
)[:2])
                db.session.commit()
                flash('You have successfully changed the check in and check out dates!', category = 'success')
            else:
                flash('Sorry, the room is not available on the dates you have selected!', category = 'error')
                room.checkin = temp1
                room.checkout = temp2
                return redirect(url_for('auth.About'))
            return redirect(url_for('auth.Book'))
    else:
        flash('Room does not exist!', category = 'error')
        return redirect(url_for('auth.Book'))