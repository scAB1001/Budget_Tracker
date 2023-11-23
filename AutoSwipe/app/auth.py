from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from .forms import LoginForm, RegistrationForm
from . import db

auth = Blueprint('auth', __name__)
DANGER, SUCCESS, HASH_TYPE = 'error', 'success', 'pbkdf2:sha256'  # scrypt

# Helper method to migrate old password hash to a new method
def migrate_password(user, password):
    if user.password.startswith('sha256$') and check_password_hash(user.password, password):
        user.password = generate_password_hash(password, method=HASH_TYPE)
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
                        password=generate_password_hash(password1, method=HASH_TYPE))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        flash('Account created!', category=SUCCESS)
        return True

    return False


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        if handle_login(email, password):
            #next_page = request.args.get('next', None); redirect(next_page) if next_page else
            return redirect(url_for('views.explore'))

    return render_template("login.html", form=form, user=current_user, title='Login')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        first_name = form.first_name.data
        password1 = form.password.data
        password2 = form.confirm_password.data

        if handle_registration(email, first_name, password1, password2):
            return redirect(url_for('auth.login'))
        else:
            flash('Unable to create an account at this time. Try again.', category=DANGER)

    return render_template("signup.html", form=form, user=current_user, title='Signup')
