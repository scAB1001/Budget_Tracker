from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, StringField, FloatField
from wtforms.validators import DataRequired, NumberRange

class CalculatorForm(FlaskForm):
    operation = SelectField('Operation', choices=[('+', '+'), ('-', '-'), ('*', '*'), ('/', '/')], validators=[DataRequired()])
    number1 = IntegerField('number1', validators=[DataRequired()])
    number2 = IntegerField('number2', validators=[DataRequired()])

class IncomeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])

class ExpenseForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('Transportation', 'Transportation'),
        ('Food & Groceries', 'Food & Groceries'),
        ('Taxation', 'Taxation'),
        ('Entertainment', 'Entertainment'),
        ('Essentials', 'Essentials'),
        ('Housing', 'Housing'),
        ('Insurance', 'Insurance')
    ], validators=[DataRequired()])
    # NumberRange doesn't help with error checking either
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0.0, message="Please enter a valid float.")])
    
class GoalForm(FlaskForm):
    name = StringField('Name')
    value = FloatField('Value', validators=[DataRequired()])