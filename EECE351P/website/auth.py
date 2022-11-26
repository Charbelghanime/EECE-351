from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, GuestRoom
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask_login import LoginManager
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
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        country= request.form.get('country')
        if len(email) < 4:
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
            flash('Account successfully created!', category = 'success')
    return render_template("sign-up.html")

@auth.route('book',methods=['GET','POST'])
def Book():
    if request.method=='POST':
        roomType= request.form.get('roomType')
        breakfast= request.form.get('breakfast')
        numofpeople= request.form.get('number')
        checkin= request.form.get('checkin')
        checkout= request.form.get('checkout')
        checkavailability= request.form.get('available')
        print(checkin, roomType, breakfast, numofpeople, checkout, checkavailability)
        flash('You have successfully booked the room', category = 'success')
        
    return render_template("Book.html")

@auth.route('/booking', methods=['GET', 'POST'])
def bookRoom():
    if request.method == 'POST':
        room = GuestRoom()
        room.roomsize = request.form.get('roomsize')
        room.breakfast = request.form.get('breakfast')
        room.numofpeople = request.form.get('numofpeople')
        room.checkin = request.form.get('checkin')
        room.checkout = request.form.get('checkout')
        room.checkavailability = request.form.get('checkavailability')
        db.session.add(room)
        db.session.commit()
        flash('Room Booked Successfully!', category='success')
        return redirect(url_for('views.home'))
    return render_template("Book.html")