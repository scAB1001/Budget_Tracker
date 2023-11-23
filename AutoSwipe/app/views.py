from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from .models import User, Car, Lease, UserInteraction
from .forms import LoginForm, RegistrationForm
from app import app, db, admin
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Car, db.session))
admin.add_view(ModelView(Lease, db.session))
admin.add_view(ModelView(UserInteraction, db.session))

import json
from collections import Counter
from datetime import datetime

# Flash message flags
DANGER, SUCCESS = 'danger', 'success'
views = Blueprint('views', __name__)


# General
"""  

    Helper variables and methods

"""

# Attempts to stage and apply a commit to the db, else rollback the attempt
def update_db(entry):
    try:
        db.session.add(entry)
        db.session.commit()
    except Exception:
        db.session.rollback()
        flash(f"An error occurred while adding this entry.", DANGER)


click_count = 30
should_increment = True
@views.route('/toggle_count', methods=['POST'])
def toggle_count():
    global click_count, should_increment
    if should_increment:
        click_count += 1
    else:
        click_count -= 1
    # Toggle the state
    should_increment = not should_increment
    #print(f"Current click count: {click_count}")
    return jsonify(click_count=click_count)

def pre_populate_db():
    # Create Users
    users = [
        User(email='user1@example.com', password='password1', first_name='User1'),
        User(email='user2@example.com', password='password2', first_name='User2'),
        User(email='user3@example.com', password='password3', first_name='User3'),
        User(email='user4@example.com', password='password4', first_name='User4'),
        User(email='user5@example.com', password='password5', first_name='User5'),
    ]

    # Create Cars
    cars = [
        Car(model='Model S', make='Tesla', year=2020, body_type='Sedan', monthly_payment=700.00, horsepower=670),
        Car(model='Mustang', make='Ford', year=2019, body_type='Coupe', monthly_payment=500.00, horsepower=450),
        # Add more cars as needed
    ]

    # Add users and cars to the session
    db.session.add_all(users)
    db.session.add_all(cars)

    # Commit the users and cars to the database
    db.session.commit()

    # Create Leases and User Interactions
    for user in users:
        for car in cars:
            lease = Lease(user_id=user.id, car_id=car.id, term_length=36, mileage_limit=12000)
            interaction = UserInteraction(user_id=user.id, car_id=car.id, swipe_type='like', timestamp=datetime.now())
            db.session.add(lease)
            db.session.add(interaction)

    # Commit the leases and interactions to the database
    db.session.commit()


def display_user_data():
    users = User.query.all()
    for user in users:
        print(f"User: {user.first_name}, Email: {user.email}")

        # Print all leases for this user
        for lease in user.leases:
            print(
                f"\tLeased Car ID: {lease.car_id}, Lease Term: {lease.term_length} months")

        # Print all interactions for this user
        for interaction in user.interactions:
            print(
                f"\tInteraction: {interaction.swipe_type} with Car ID: {interaction.car_id}")



def isolate_users():
    users = User.query.all()
    print("Users:")
    for user in users:
        print(f"  {user}")

    if str(current_user)[0] != 'I':
        print(f"\ncurrent_user:  Guest")
    else:
        print(f"\ncurrent_user:  {current_user}")


# Routes
"""
    
    View entries

"""
@views.route('/')
def home():
    #if not User.query.first():
    #    print(not User.query.first())
    #    pre_populate_db()
    #isolate_users()

    display_user_data()

    return render_template('home.html', title='Home', user=current_user)


@views.route('/explore')
@login_required
def explore():
    if request.method == 'POST': 
        print("POST")
    return render_template('explore.html', title='Explore', user=current_user, click_count=click_count)


@views.route('/saved')
@login_required
def saved():
    return render_template('saved.html', title='Saved', user=current_user)


@views.route('/history')
@login_required
def history():
    return render_template('history.html', title='History', user=current_user)


@views.route('/settings')
@login_required
def settings():
    return render_template('settings.html', title='Settings', user=current_user)


@views.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    if current_user.is_authenticated:
        user = User.query.get(current_user.id)
        if user:
            db.session.delete(user)
            db.session.commit()
            flash('Your account has been deleted.', category=SUCCESS)
        else:
            flash('User not found.', category=DANGER)
        return redirect(url_for('auth.login'))  # Redirect to logout route
    else:
        flash('You must be logged in to perform this action.', category=DANGER)
        return redirect(url_for('auth.login'))  # Redirect to login page
    return True
