from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, db
from .forms import IncomeForm, ExpenseForm, GoalForm
from .models import Incomes, Expenses, Goals

import json
from collections import Counter


# General
"""  

    Helper variables and methods

"""
# Flash message flags
DANGER, SUCCESS = 'danger', 'success'

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


@app.route('/login')  # , methods=['GET', 'POST']
def login():
    return render_template('login.html', title='Login')


@app.route('/signup')
def signup():
    return render_template('signup.html', title='Signup', click_count=click_count)



@app.route('/explore')
def explore():
    return render_template('explore.html', title='Explore')


@app.route('/settings')
def settings():
    return render_template('settings.html', title='Settings')


@app.route('/history')
def history():
    return render_template('history.html', title='History')
