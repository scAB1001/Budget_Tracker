from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, StringField, FloatField
from wtforms.validators import DataRequired, NumberRange, Length

STR_MESSAGE = "ERR: Enter a name between 2 and 20 characters long."
NUM_MESSAGE = "ERR: Enter a number must be between 0 and 1000000."

class IncomeForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(), Length(min=2, max=20, message=STR_MESSAGE)])
    
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
        NumberRange(min=0.00, max=1000000.00, message=NUM_MESSAGE)])


class ExpenseForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(), Length(min=2, max=20, message=STR_MESSAGE)])
    
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
        NumberRange(min=0.00, max=1000000.00, message=NUM_MESSAGE)])
 
    
class GoalForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(), Length(min=2, max=20, message=STR_MESSAGE)])
    
    amount = FloatField('Amount', validators=[
        DataRequired(), 
        NumberRange(min=0.00, max=1000000.00, message=NUM_MESSAGE)])