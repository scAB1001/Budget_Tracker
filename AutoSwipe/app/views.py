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


# Attempts to stage and apply a commit to the db, else rollback the attempt
def update_db(entry):
    try:
        db.session.add(entry)
        db.session.commit()
    except Exception:
        db.session.rollback()
        flash(f"An error occurred while adding this entry.", DANGER)


def is_table_empty(model):
    # Returns True if the table is empty, False otherwise
    print(f"COUNT = {db.session.query(model).count()}")
    return db.session.query(model).count() == 0


def clear_tables():
    # Clear all data from tables
    if not is_table_empty(UserInteraction):
        UserInteraction.query.delete()
        
    if not is_table_empty(Lease):
        Lease.query.delete()
    
    if not is_table_empty(Car):
        Car.query.delete()
    
    if not is_table_empty(User):
        User.query.delete()
    
    db.session.commit()
    
# DANGER #
# Do not use until password is hashed
def pre_populate_db():
    # Clear all tables
    #clear_tables()
    
    # Create Users
    if is_table_empty(User) and is_table_empty(Car) and is_table_empty(Lease) and is_table_empty(UserInteraction):
        users = [
            User(email='user1@example.com', password='password1', first_name='User1'),
            User(email='user2@example.com', password='password2', first_name='User2'),
            User(email='user3@example.com', password='password3', first_name='User3'),
            User(email='user4@example.com', password='password4', first_name='User4'),
            User(email='user5@example.com', password='password5', first_name='User5'),
        ]

        # Create Cars
        cars = [
            Car(model='Model S', make='Tesla', 
                year=2020, body_type='Sedan', monthly_payment=700.00, horsepower=670),

            Car(model='Mustang', make='Ford', 
                year=2019, body_type='Coupe', monthly_payment=500.00, horsepower=450)

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
                f"\tLeased Car ID: {lease.car_id}, Term: {lease.term_length} months")

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
    # DANGER #
    #if not User.query.first():
    #    print(not User.query.first())
    #    pre_populate_db()
    #isolate_users()

    #clear_tables()

    return render_template('home.html', title='Home', user=current_user)



@app.route('/react', methods=['POST'])
def react():
    if not current_user.is_authenticated:
        return jsonify({"status": "error", "message": "User not logged in."}), 401

    data = request.json; print(f"Payload data:\n{data}")
    
    try:
        # .get() results in None type if not found
        carID = int(data.get('carID'))
        status = data.get('liked') == True
        
    except (TypeError, ValueError):
        return jsonify({"status": "error", "message": "Invalid data"}), 400
    
    # Create a new user interaction entry
    new_interaction = UserInteraction(
        user_id=current_user.id, 
        car_id=carID, 
        swiped_right=status
    )
    db.session.add(new_interaction)
    
    try:
        db.session.commit()
        return jsonify({"status": "success", "carID": carID, "liked": status})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    

def pre_populate_tblCars():
    dir = '/static/cars/'  # Prepend before when passing into args
    try:
        # Format: Car(car_name, make, model, year, body_type, horsepower, monthly_payment, mileage)
        
        # List of cars to add
        cars_to_add = [
            Car(image='308GTRainbow1.jpg', car_name='Ferrari 308 GT Bertone Rainbow', make='Ferrari', model='308 GT', 
                year=1976, body_type='Coupe with retractable targa-style roof', horsepower=255, monthly_payment=52585.91, mileage=89017),
            
            Car(image='astonMartinLagonda1.jpg', car_name='Aston Martin Lagonda Series 2', make='Aston Martin', model='Lagonda', 
                year=1976, body_type='4-door saloon', horsepower=280, monthly_payment=15461.56, mileage=103633),
            
            Car(image='testarossa1.jpg', car_name='Ferrari Testarossa', make='Ferrari', model='Testarossa', 
                year=1984, body_type='2-door berlinetta', horsepower=385, monthly_payment=34185.91, mileage=146545),
            
            Car(image='countachlp400Lamborghini1.jpg', car_name='Lamborghini Countach LP400', make='Lamborghini', model='LP400', 
                year=1974, body_type='2-door coupe', horsepower=375, monthly_payment=82042.47, mileage=167228),
        ]
        
        # Add cars to the database
        db.session.add_all(cars_to_add)
        db.session.commit()

        return jsonify({"status": "success", "message": "Cars added successfully"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

@views.route('/test')
def test():
    if not is_table_empty(Car):
        print("Deleting rows...")
        Car.query.delete()
        is_table_empty(Car)
        print("Car table EMPTY")    
    
    print()
    print("Adding rows...")
    pre_populate_tblCars()
    is_table_empty(Car)    
        
    #if not is_table_empty(UserInteraction):
    #    interactions = UserInteraction.query.all()
    #    for interaction in interactions:
    #        print(f"UserID: {interaction.user_id}, CarID: {interaction.car_id}, Liked: {interaction.swiped_right}")
    #else:
    #    print("UserInteraction table EMPTY")    
    
    tblCars = Car.query.all()
    list_of_car_details = []
    for car in tblCars:
        list_of_car_details.append(car.card_info())
    print()
    print(f'List of cars:\n{list_of_car_details}\n\n')
    """
    # After appending all car rows, the output should look like this
    list_of_car_details = [
        {
            'carID': 1,
            'imageUrl': 'static/cars/testarossa1.jpg',
            'carName': '1960 Ferrari Testarossa V6',
            'details': 'Price: £12,000pm\t\tBody: Coupe\nHorsepower: 390bhp\t\tMake: Ferrari'
        },
        {
            'carID': 2,
            'imageUrl': 'static/cars/countachlp400Lamborghini1.jpg',
            'carName': '1990 Lamborghini Countach V12',
            'details': 'Price: £18,000pm\t\tBody: Sports\nHorsepower: 410bhp\t\tMake: Lamborghini'
        },
        {
            'carID': 3,
            'imageUrl': 'static/cars/astonMartinLagonda1.jpg',
            'carName': '1970 Aston Martin Lagonda V8',
            'details': 'Price: £4,000pm\t\tBody: Saloon\nHorsepower: 305bhp\t\tMake: Aston Martin'
        },
        {
            'carID': 4,
            'imageUrl': 'static/cars/308GTRainbow1.jpg',
            'carName': '1976 Ferrari GT Bertone Rainbow V8',
            'details': 'Price: £50,000pm\t\tBody: Coupe\nHorsepower: 255bhp\t\tMake: Ferrari'
        }
    ]"""
    
    numCards = len(list_of_car_details)
    
    return render_template(
        'test.html', title='Test', user=current_user, 
        cars=list_of_car_details, numCards=numCards)



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

def extra_db(): 
    """
    Car(image=dir+'.jpg', car_name='Mercedes-Benz 300SL', make='Mercedes-Benz', model='300SL', 
        year=1954, body_type='Coupe', horsepower=215, monthly_payment=2230.65, mileage=92350),

    Car(image=dir+'.jpg', car_name='Aston Martin Lagonda Series 1', make='Aston Martin', model='Lagonda', 
        year=1974, body_type='4-door saloon', horsepower=280, monthly_payment=54611.96, mileage=18324),


    Car(image=dir+'.jpg', car_name='Aston Martin Lagonda Series 3', make='Aston Martin', model='Lagonda', 
        year=1986, body_type='4-door saloon', horsepower=0, monthly_payment=7766.58, mileage=132084),

    Car(image=dir+'.jpg', car_name='Aston Martin Lagonda Series 4', make='Aston Martin', model='Lagonda', 
        year=1987, body_type='4-door saloon', horsepower=0, monthly_payment=33633.98, mileage=123117),

    Car(image=dir+'.jpg', car_name='Ferrari 512 TR', make='Ferrari', model='512 TR', 
        year=1991, body_type='2-door berlinetta', horsepower=422, monthly_payment=31245.32, mileage=198978),

    Car(image=dir+'.jpg', car_name='Ferrari F512 M', make='Ferrari', model='F512 M', 
        year=1994, body_type='2-door berlinetta', horsepower=434, monthly_payment=6352.03, mileage=196267),

    Car(image=dir+'.jpg', car_name='Lamborghini Countach LP400 S', make='Lamborghini', model='LP400 S', 
        year=1978, body_type='2-door coupe', horsepower=355, monthly_payment=17981.98, mileage=108654),

    Car(image=dir+'.jpg', car_name='Lamborghini Countach LP500 S', make='Lamborghini', model='LP500 S', 
        year=1982, body_type='2-door coupe', horsepower=370, monthly_payment=27854.73, mileage=100220),

    Car(image=dir+'.jpg', car_name='Lamborghini Countach LP5000 Quattrovalvole', make='Lamborghini', model='LP5000 Quattrovalvole', 
        year=1985, body_type='2-door coupe', horsepower=455, monthly_payment=81930.27, mileage=103074),

    Car(image=dir+'.jpg', car_name='Lamborghini Countach 25th Anniversary Edition', make='Lamborghini', model='25th Anniversary Edition', 
        year=1988, body_type='2-door coupe', horsepower=414, monthly_payment=36409.78, mileage=140320)
    """