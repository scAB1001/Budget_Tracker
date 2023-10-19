from flask import render_template, flash, redirect, url_for
from app import app, db
from .forms import CalculatorForm, IncomeForm, ExpenseForm, GoalForm
from .models import Calculations, Income, Expense, Goal


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

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    msg={'description':'Welcome to this page. Please input two numbers to calculate.'}
    form = CalculatorForm()
    if form.validate_on_submit():
        num1 = form.number1.data
        num2 = form.number2.data
        operation = form.operation.data

        if operation == '+':
            result = num1 + num2
        elif operation == '-':
            result = num1 - num2
        elif operation == '*':
            result = num1 * num2
        elif operation == '/':
            result = num1 / num2

        flash(f'Successfully received form data. {num1} {operation} {num2} = {result}')

        # Save the calculation result to the database
        from datetime import datetime  # makes the entry unique
        expr = f'{num1} {operation} {num2} - {datetime.utcnow()}'
        calculation = Calculations(expr=expr, result=result)

        db.session.add(calculation)
        db.session.commit()

    return render_template('calculator.html', title='Calculator', form=form, msg=msg)
    """msg={'description':'Welcome to this page. Please input two numbers to calculate.'}
    form = CalculatorForm()
    if form.validate_on_submit():
        msg = "Successfully received form data."
        flash_msg(msg, form.number1.data, " + ", form.number2.data, " = ", form.number1.data + form.number2.data)
        #flash('Successfully received form data. %s + %s  = %s'%(form.number1.data, form.number2.data, form.number1.data+form.number2.data))
    return render_template('calculator.html', title='Calculator', form=form, msg=msg)"""

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
    return render_template('expenses.html', title='Expenses')

@app.route('/new_expense')
def new_expense():
    return render_template('new_expense.html', title='New Expense')    

@app.route('/goals')
def goals():
    return render_template('goals.html', title='Goals')

@app.route('/new_goal')
def new_goal():
    return render_template('new_goal.html', title='New Goal')

#########################################################################################
"""
    @app.route('/incomes', methods=['GET', 'POST'])
    def incomes():
        form = IncomeForm()
        if form.validate_on_submit():
            # Add logic to handle form submission (e.g., add income to database)
            flash('Income added successfully!', 'success')
            return redirect(url_for('incomes'))
        return render_template('income_list.html', title='All Incomes', form=form)

    @app.route('/expenditures', methods=['GET', 'POST'])
    def expenditures():
        form = ExpenditureForm()
        if form.validate_on_submit():
            # Add logic to handle form submission (e.g., add expenditure to database)
            flash('Expenditure added successfully!', 'success')
            return redirect(url_for('expenditures'))
        return render_template('expenditure_list.html', title='All Expenditures', form=form)

    @app.route('/goals', methods=['GET', 'POST'])
    def goals():
        form = GoalForm()
        if form.validate_on_submit():
            # Add logic to handle form submission (e.g., add goal to database)
            flash('Goal added successfully!', 'success')
            return redirect(url_for('goals'))
        return render_template('goal_list.html', title='All Goals', form=form)
"""