from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from .auth_service import authenticate_user, create_user, migrate_password
from .forms import LoginForm, RegistrationForm

auth = Blueprint('auth', __name__)
DANGER, SUCCESS = 'error', 'success'


# Helper method to handle user login
def handle_login(email, password):
    user = authenticate_user(email, password)
    if user:
        migrate_password(user, password)  # Migrate password if needed
        login_user(user, remember=True)
        flash(f'Logged in successfully!', category=SUCCESS)
        return True
    else:
        flash('Incorrect email or password, try again.', category=DANGER)
        return False


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        if handle_login(email, password):
            return redirect(url_for('views.home'))

    return render_template("/admin/login.html", form=form, user=current_user, title='Login')


# Helper method to handle user registration
def handle_registration(email, first_name, password1, password2):
    if password1 != password2:
        flash('Passwords do not match.', category=DANGER)
        return False
    elif len(password1) < 7:
        flash('Password must be at least 7 characters.', category=DANGER)
        return False
    else:
        user = create_user(email, first_name, password1)
        if user:
            login_user(user, remember=True)
            flash('Account created!', category=SUCCESS)
            return True
        else:
            flash('Unable to create an account at this time. Try again.',
                  category=DANGER)
            return False


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        first_name = form.first_name.data
        password1 = form.password.data
        password2 = form.confirm_password.data

        if handle_registration(email, first_name, password1, password2):
            return redirect(url_for('views.home'))
        else:
            flash('Unable to create an account at this time. Try again.', category=DANGER)

    return render_template("/admin/signup.html", form=form, user=current_user, title='Signup')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(f'Logged out successfully!', category=SUCCESS)
    return redirect(url_for('auth.login'))
