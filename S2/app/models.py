from app import db
from datetime import datetime

DT = datetime.utcnow()

class Incomes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=DT)

    def __repr__(self):
        return f"Income('{self.name}', '{self.category}', £{self.amount})"

class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=DT)

    def __repr__(self):
        return f"Expense('{self.name}', '{self.category}', £{self.amount})"

class Goals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=DT)

    def __repr__(self):
        return f"Goal('{self.name}', £{self.amount})"
