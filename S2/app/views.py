from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from app import app, db
from .forms import LoginForm, RegistrationForm
from .models import User

import json
from collections import Counter

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
@app.route('/toggle_count', methods=['POST'])
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

# Routes
"""
    
    View entries

"""
@app.route('/')
def home():
    return render_template('home.html', title='Home')

@app.route('/explore')
@login_required
def explore():
    if request.method == 'POST': 
        print("POST")
    return render_template('explore.html', title='Explore')


@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html', title='Settings')


@app.route('/history')
@login_required
def history():
    return render_template('history.html', title='History')


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
