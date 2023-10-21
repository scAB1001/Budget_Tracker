from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, db
from .forms import CalculatorForm, IncomeForm, ExpenseForm, GoalForm
from .models import Calculations, Incomes, Expenses, Goal

import json

def flash_msg(*args, **kwargs):
    """
    Display flash messages based on the provided arguments.

    Args:
        *args: Positional arguments for formatting the flash message.
        **kwargs: Keyword arguments for additional message options.
            - category: Flash category (default is 'info').
            - escape: Whether to escape HTML in the message (default is True).
    """
    # Extracting keyword arguments or using defaults
    category = kwargs.get('category', 'info')
    escape = kwargs.get('escape', True)

    # Constructing the flash message
    message = ' '.join(str(arg) for arg in args)

    # Display the flash message
    flash(message, category=category)

def update_db(entry):
    try:
        db.session.add(entry)
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # will this fuck with my flask db migrate/upgrade
        flash(f"An error occurred while adding this entry. Please try again. Error: {e}", 'danger')

def is_valid_float(value):
    val = str(value)
    dot_count = val.count('.')
    if dot_count > 1:
        return False
    
    val = val.replace('.', '')
    return val.isdigit()


@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    msg={'description':'Welcome to this page. Please input two numbers to calculate.'}
    form = CalculatorForm()
    if form.validate_on_submit():
        num1 = form.number1.data
        num2 = form.number2.data
        operation = form.operation.data
        expr = f'{num1} {operation} {num2}'

        if operation == '+':
            result = num1 + num2
        elif operation == '-':
            result = num1 - num2
        elif operation == '*':
            result = num1 * num2
        elif operation == '/':
            result = num1 / num2

        update_db(Calculations(expr=expr, result=result))
        flash(f'Successfully received form data. {num1} {operation} {num2} = {result}')

    return render_template('calculator.html', title='Calculator', form=form, msg=msg)

@app.route('/', methods=['GET', 'POST'])
def homepage():
    home={'description':'Welcome to this application.\nPlease navigate to your desired dir.'}
    return render_template('homepage.html', title='Homepage', home=home)

@app.route('/incomes')
def incomes():
    return render_template('incomes.html', title='Incomes')

@app.route('/new_income')
def new_income():
    return render_template('new_income.html', title='New Income')    


@app.route('/expenses')
def expenses():
    # Fetch all expenses from the database
    expenses = Expenses.query.all()
    return render_template('expenses.html', title='Expenses', expenses=expenses)

@app.route('/new_expense', methods=['GET', 'POST'])
def new_expense():
    form = ExpenseForm()
    # Add additional client-side validation here if needed
    if form.validate_on_submit():
        # Removing trailing white space and tabs and multiple spaces between words
        name = form.name.data
        category = form.category.data
        amount = form.amount.data

        # Doesn't do
        if not is_valid_float(amount):
            flash("Amount must be numerical.", 'danger')

        if amount < 0:
            flash("Amount cannot be negative.", 'danger')
        else:
            expense = Expenses(name=name, category=category, amount=amount)
            update_db(expense)

            flash(f'Expense added: {name} ({category}) - £{amount:.2f}', 'success')

    return render_template('new_expense.html', title='New Expense', form=form)

@app.route('/delete_expense', methods=['POST'])
def delete_expense():
    expense = json.loads(request.data)
    expenseId = expense['expenseId']
    expense = Expenses.query.get(expenseId)
    
    if expense:
        db.session.delete(expense)
        db.session.commit()
    
    return jsonify({})

# Check about the '/<int:expense_id>'
@app.route('/edit_expense/<int:expense_id>', methods=['GET', 'POST'])
def edit_expense(expense_id):
    expense = Expenses.query.get(expense_id)
    form = ExpenseForm(obj=expense)

    if form.validate_on_submit():
        expense.name = form.name.data
        expense.category = form.category.data
        expense.amount = form.amount.data

        db.session.commit()

        flash(f'Expense updated: {expense.name} ({expense.category}) - £{expense.amount:.2f}', 'success')
        # Check if I need to do this after ALL form submission/validation(s)
        return redirect(url_for('expenses'))
    
    #flash(f'Failed to update expense', 'danger')

    return render_template('edit_expense.html', title='Edit Expense', form=form, expense=expense)

@app.route('/goal')
def goal():
    return render_template('goal.html', title='Goal')

@app.route('/new_goal')
def new_goal():
    return render_template('new_goal.html', title='New Goal')

#########################################################################################
