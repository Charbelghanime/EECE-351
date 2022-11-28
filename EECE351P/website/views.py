from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from .auth import auth

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return redirect(url_for('auth.sign_up'))
    return render_template("home.html", user = current_user)