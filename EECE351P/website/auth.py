from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, HotelRoom, checkAvailibility
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db
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
    return render_template("sign-up.html")

@auth.route('book',methods=['GET','POST'])
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
        totalPrice = (roomPrice + breakfastPrice) * int(numofpeople)
        
        import datetime
        if datetime.datetime(int(checkin[:4]), int(checkin[5:7]), int(checkin[8:])) < datetime.datetime.now():
            flash('Please Enter a Valid Check In Date!', category = 'error')
            redirect(url_for('auth.Book'))
        elif datetime.datetime(int(checkin[:4]), int(checkin[5:7]), int(checkin[8:])) > datetime.datetime(int(checkout[:4]), int(checkout[5:7]), int(checkout[8:])):
            flash('Please Enter a Valid Check Out Date!', category = 'error')
            redirect(url_for('auth.Book'))
        elif int(numofpeople) > 1 and int(roomType) == 1:
            flash('Please Book a larger room!', category = 'error')
            redirect(url_for('auth.Book'))
        elif int(numofpeople) > 2 and int(roomType) == 2:
            flash('Please Book a larger room!', category = 'error')
            redirect(url_for('auth.Book'))
        elif(-int(checkin[:4]) + int(checkout[:4]) > 1): 
            flash("Please checkout earlier than a year", category = 'error')
            redirect(url_for('auth.Book'))
        else: 
            new_room = HotelRoom(roomType=roomType, breakFast=breakfast, numOfPeople=numofpeople, checkin=checkin, checkout=checkout, totalPrice=totalPrice, id = current_user.id)
            db.session.add(new_room)
            db.session.commit()
            if not checkAvailibility(roomType):
                flash('Room Not Available!', category = 'error')
                redirect(url_for('auth.Book'))
            flash('You have successfully booked the room\n please check your room Type', category = 'success')
    return render_template("Book.html")