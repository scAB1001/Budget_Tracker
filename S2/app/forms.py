from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, StringField, FloatField
from wtforms.validators import DataRequired, NumberRange

class IncomeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('Salary',                  'Salary'),
        ('Family & Friends',        'Family & Friends'),
        ('Commission',              'Commission'),
        ('Real-estate',             'Real-estate'),
        ('Pension',                 'Pension'),
        ('Donation',                'Donation'),
        ('Investment',             'Investment'),
        ('Other',                   'Other')
    ], validators=[DataRequired()])
    amount = FloatField('Amount', validators=[
        DataRequired(), 
        NumberRange(min=0.0, message="Please enter a realistic value.")])

class ExpenseForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('Transportation',          'Transportation'),
        ('Food & Groceries',        'Food & Groceries'),
        ('Taxation',                'Taxation'),
        ('Entertainment',           'Entertainment'),
        ('Essentials',              'Essentials'),
        ('Housing',                 'Housing'),
        ('Insurance',               'Insurance'),
        ('Other',                   'Other')
    ], validators=[DataRequired()])
    amount = FloatField('Amount', validators=[
        DataRequired(), 
        NumberRange(min=0.0, message="Please enter a valid float.")])
    
class GoalForm(FlaskForm):
    name = StringField('Name')
    amount = FloatField('Amount', validators=[
        DataRequired(), 
        NumberRange(min=0.0, message="Please enter a valid float.")])