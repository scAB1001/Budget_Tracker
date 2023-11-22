from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)
DANGER, SUCCESS = 'error', 'success'
EMAIL, PASS = 'email', 'password'

# Helper method to migrate old password hash to a new method
def migrate_password(user, password):
    if user.password.startswith('sha256$') and check_password_hash(user.password, password):
        user.password = generate_password_hash(password, method='scrypt')
        db.session.commit()


# Helper method to handle user login
def handle_login(email, password):
    user = User.query.filter_by(email=email).first()
    if user:
        # Migrate old password hash if needed
        migrate_password(user, password)

        if check_password_hash(user.password, password):
            flash('Logged in successfully!', category=SUCCESS)
            login_user(user, remember=True)
            return True
        else:
            flash('Incorrect email or password, try again.', category=DANGER)
    else:
        flash('Email does not exist.', category=DANGER)

    return False


# Helper method to handle user registration
def handle_registration(email, first_name, password1, password2):
    user = User.query.filter_by(email=email).first()
    if user:
        flash('Email already exists.', category=DANGER)
    elif len(email) < 4:
        flash('Email must be greater than 3 characters.', category=DANGER)
    elif len(first_name) < 2:
        flash('First name must be greater than 1 character.', category=DANGER)
    elif password1 != password2:
        flash('Passwords do not match.', category=DANGER)
    elif len(password1) < 7:
        flash('Password must be at least 7 characters.', category=DANGER)
    else:
        new_user = User(email=email, first_name=first_name,
                        password=generate_password_hash(password1, method='scrypt'))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        flash('Account created!', category=SUCCESS)
        return True

    return False


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get(EMAIL)
        password = request.form.get(PASS)

        if handle_login(email, password):
            return redirect(url_for('views.home'))

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get(EMAIL)
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if handle_registration(email, first_name, password1, password2):
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)
