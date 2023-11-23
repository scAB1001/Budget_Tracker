from app import db
from sqlalchemy.sql import func
from flask_login import UserMixin

DT = func.now()

class BaseModel(db.Model):
    """
    Base class for SQLAlchemy models that includes common columns.

    Attributes:
        id (int): Primary key column.
        created_at (datetime): Creation timestamp
        updated_at (datetime): Update timestamp
    """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    created_at = db.Column(db.DateTime(timezone=True), default=DT)  # Creation timestamp
    updated_at = db.Column(db.DateTime(timezone=True), default=DT, onupdate=DT)  # Update timestamp


class User(BaseModel, UserMixin):
    __tablename__ = 'user'

    # Existing fields
    email = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(20))
    first_name = db.Column(db.String(20))

    # Define relationships
    leases = db.relationship('Lease', backref='user', lazy=True)
    interactions = db.relationship(
        'UserInteraction', backref='user', lazy=True)

    def __repr__(self):
        return f"ID:{self.id}  {self.first_name}, {self.email}, {self.password}"



class Car(BaseModel):
    __tablename__ = 'cars'

    model = db.Column(db.String(255))
    make = db.Column(db.String(255))
    year = db.Column(db.Integer)
    body_type = db.Column(db.String(255))
    monthly_payment = db.Column(db.Float)
    horsepower = db.Column(db.Integer)

    leases = db.relationship('Lease', backref='car', lazy=True)
    interactions = db.relationship('UserInteraction', backref='car', lazy=True)

    def __repr__(self):
        return f"Car [{self.model}, {self.make}, {self.year}]"


class Lease(BaseModel):
    __tablename__ = 'leases'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    term_length = db.Column(db.Integer)
    mileage_limit = db.Column(db.Integer)

    def __repr__(self):
        return f"Lease [{self.user_id}, {self.car_id}, {self.term_length}]"


class UserInteraction(BaseModel):
    __tablename__ = 'user_interactions'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    swipe_type = db.Column(db.String(10))
    timestamp = db.Column(db.DateTime(timezone=True), default=DT)

    def __repr__(self):
        return f"UserInteraction [{self.user_id}, {self.car_id}, {self.swipe_type}]"
