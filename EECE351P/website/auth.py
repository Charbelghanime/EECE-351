from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    return render_template("login.html", boolean = True)

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('sign-up', methods = ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
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