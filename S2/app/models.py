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

    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    #notes = db.relationship('Note')

    def __repr__(self):
        return f"UserID:{self.id}\t{self.first_name}, {self.email}, {self.password}"
