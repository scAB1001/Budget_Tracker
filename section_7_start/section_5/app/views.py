from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, db
from .models import Landlord, Property

from datetime import datetime

def populate_db():
    with app.app_context():
        # Clear existing data
        Property.query.delete()
        Landlord.query.delete()

        # Create sample landlords
        landlord1 = Landlord(name="John Doe", contact_number="1234567890", address="123 Maple Street")
        landlord2 = Landlord(name="Jane Smith", contact_number="0987654321", address="456 Oak Avenue")

        # Add landlords to the session
        db.session.add(landlord1)
        db.session.add(landlord2)

        # Commit to save landlords so they get assigned an ID
        db.session.commit()

        # Create properties with landlord references
        property1 = Property(address="101 Elm Street", start_date=datetime(2023, 1, 1), duration=12, rent=1200.00, landlord_id=landlord1.id)
        property2 = Property(address="202 Pine Lane", start_date=datetime(2023, 2, 15), duration=6, rent=1500.00, landlord_id=landlord2.id)

        # Add properties to the session
        db.session.add(property1)
        db.session.add(property2)

        # Commit the session to the database
        db.session.commit()

def query_all_data():
    # Query all landlords
    landlords = Landlord.query.all()

    # Create a list to hold the data
    all_data = []

    # Iterate through each landlord
    for landlord in landlords:
        # Fetch the landlord's properties
        properties = Property.query.filter_by(landlord_id=landlord.id).all()

        # Create a dictionary to store landlord and their properties
        landlord_data = {
            'Landlord': {
                'ID': landlord.id,
                'Name': landlord.name,
                'Contact Number': landlord.contact_number,
                'Address': landlord.address
            },
            'Properties': []
        }

        # Iterate through the properties and add them to the landlord's data
        for property in properties:
            property_data = {
                'ID': property.id,
                'Address': property.address,
                'Start Date': property.start_date,
                'Duration': property.duration,
                'Rent': property.rent
            }
            landlord_data['Properties'].append(property_data)

        # Add the landlord's data to the all_data list
        all_data.append(landlord_data)

    return all_data


@app.route('/a')
def view_meth():
    Property.query.delete()
    Landlord.query.delete()

    l = Landlord(name="Joe Blogs")
    p = Property(address="New Street",start_date=datetime.utcnow(),duration=6, rent=84.32)
    p.landlord = l
    db.session.add(p)
    db.session.add(l)
    db.session.commit()

    l = Landlord.query.first()
    for prop in l.properties:
        print(prop)

    prop = Property.query.first()
    print(prop.landlord)

    """'
    populate_db()
    data = query_all_data()

    for landlord in data:
        print(f"Landlord ID: {landlord['Landlord']['ID']}")
        print(f"Name: {landlord['Landlord']['Name']}")
        print(f"Contact Number: {landlord['Landlord']['Contact Number']}")
        print(f"Address: {landlord['Landlord']['Address']}")
        print("Properties:")

        if landlord['Properties']:
            for property in landlord['Properties']:
                print(f"  Property ID: {property['ID']}")
                print(f"  Address: {property['Address']}")
                print(
                    f"  Start Date: {property['Start Date'].strftime('%Y-%m-%d') if property['Start Date'] else 'N/A'}")
                print(f"  Duration: {property['Duration']}")
                print(f"  Rent: {property['Rent']}")
                print("  ----------------")
        else:
            print("  No properties listed.")
        print("======================================\n")
    #"""

    return "LOL"

@app.route('/')
def index():
    return "Hello World!!!"
