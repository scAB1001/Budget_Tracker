from app import db

class Calculations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expr = db.Column(db.String(100), nullable=False)
    result = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Calculation('{self.expr}', {self.result})"

class Incomes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Income('{self.name}', {self.amount})"

class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Expense('{self.name}', '{self.category}', {self.amount})"


class Goals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    value = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Goal('{self.name}', {self.value})"
