from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, db
from .forms import IncomeForm, ExpenseForm, GoalForm
from .models import Incomes, Expenses, Goals

import json
from collections import Counter
from time import sleep as s

# Misc
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

# Routes
"""
    
    Goal routes

"""
@app.route('/', methods=['GET', 'POST'])
def homepage():
    home={'description':'Welcome to this application.\nPlease navigate to your desired dir.'}
    
    incomes = Incomes.query.all()
    if incomes != None:
        total_income = '%.2f' % sum(income.amount for income in incomes)
        max_earning = max(incomes, key=lambda income: income.amount)
        
        max_income = '%.2f' % max_earning.amount
        max_income_name = max_earning.name

        category_counts = Counter(income.category for income in incomes)
        most_frequent_income = category_counts.most_common(1)[0][0]

    ##
    expenses = Expenses.query.all()
    if expenses != None:
        total_spend = '%.2f' % sum(expense.amount for expense in expenses)

        # Store the largest expense dict by .amount, to access the .name
        max_expense = max(expenses, key=lambda expense: expense.amount)
        
        max_spend = '%.2f' % max_expense.amount
        max_spend_name = max_expense.name

        category_counts = Counter(expense.category for expense in expenses)
        most_frequent_spend = category_counts.most_common(1)[0][0]
    
    ##
    goal = Goals.query.first()
    if goal == None:
        flash(f"You don't have a goal set!", "danger")
        goal = "You have no goal!"
    else:
        target, target_name = goal.amount, goal.name
    
        incomes, expenses = Incomes.query.all(), Expenses.query.all() 
        total_income = sum(income.amount for income in incomes)
        total_spend = sum(expense.amount for expense in expenses)

        difference = total_income - total_spend
        progress_value = round((difference/target), 2)
        if difference < 0: 
            progress_value = 0
        elif progress_value >= 1:
            progress_value = 1
            extra = difference - target

    return render_template('homepage.html', title='Homepage', home=home,
        incomes=incomes, expenses=expenses, goal=goal,
        total_income=total_income, total_spend=total_spend,
        max_income=max_income, max_income_name=max_income_name, 
        most_frequent_income=most_frequent_income,
        max_spend=max_spend, max_spend_name=max_spend_name, 
        most_frequent_spend=most_frequent_spend, 
        progress_value=progress_value*100
    )

@app.route('/goal')
def goal():
    goal = Goals.query.first()
    if goal == None:
        flash(f"You don't have a goal set!", "danger")
        return new_goal()
    else:
        target, target_name = goal.amount, goal.name
    
        incomes, expenses = Incomes.query.all(), Expenses.query.all() 
        total_income = sum(income.amount for income in incomes)
        total_spend = sum(expense.amount for expense in expenses)

        difference = total_income - total_spend
        progress_value = round((difference/target), 2)

        # Set a default display value
        if difference < 0: 
            flash(f"You're £{difference} away...", "danger")
        elif progress_value >= 1:
            progress_value = 1
            extra = difference - target
            flash(f"Target reached!\n You're £{extra} over budget!?", "success")
    return render_template('goal.html', title='Goal', 
        progress_value=progress_value*100, 
        target_name=target_name, target=target, goal=goal)

@app.route('/new_goal', methods=['GET', 'POST'])
def new_goal():
    form = GoalForm()
    if form.validate_on_submit():
        name = form.name.data
        amount = form.amount.data

        if not is_valid_float(amount):
            flash("Amount must be numerical.", 'danger')

        if amount < 0:
            flash("Amount cannot be negative.", 'danger')
        else:
            goal = Goals(name=name, amount=amount)
            update_db(goal)

            flash(f'Goal added: {name} - £{amount:.2f}', 'success')

    return render_template('new_goal.html', title='New Goal', form=form)

@app.route('/delete_goal', methods=['POST'])
def delete_goal():
    goal = json.loads(request.data)
    goalId = goal['goalId']
    goal = Goals.query.get(goalId)
    
    if goal:
        db.session.delete(goal)
        db.session.commit()
    
    return jsonify({})

@app.route('/edit_goal/<int:goal_id>', methods=['GET', 'POST'])
def edit_goal(goal_id):
    goal = Goals.query.get(goal_id)
    form = GoalForm(obj=goal)

    if form.validate_on_submit():
        goal.name = form.name.data
        goal.amount = form.amount.data

        db.session.commit()

        flash(f'Goal updated: {goal.name} - £{goal.amount:.2f}', 'success')
        return redirect(url_for('goal'))
    
    return render_template('edit_goal.html', title='Edit Goal', form=form, goal=goal)


# Test page
@app.route('/a')
def progress_bar():
    goal = Goals.query.first()
    target, target_name = goal.amount, goal.name
   
    incomes, expenses = Incomes.query.all(), Expenses.query.all() 
    total_income = sum(income.amount for income in incomes)
    total_spend = sum(expense.amount for expense in expenses)

    difference = total_income - total_spend
    progress_value = round((difference/target), 2)
    print(progress_value)

    # Set a default display value
    if difference < 0: 
        flash(f"You're £{difference} away...", "danger")
    elif progress_value >= 1:
        progress_value = 1
        extra = difference - target
        flash(f"Target reached!\n You're £{extra} over budget!?", "success")
    return render_template('progress_bar.html', title='Progress Bar', goal=goal, 
        progress_value=progress_value*100, target_name=target_name, target=target)


"""
    
    Income routes

"""
@app.route('/incomes')
def incomes():
    incomes = Incomes.query.all()
    total_income = '%.2f' % sum(income.amount for income in incomes)
    max_earning = max(incomes, key=lambda income: income.amount)
    
    max_income = '%.2f' % max_earning.amount
    max_income_name = max_earning.name

    category_counts = Counter(income.category for income in incomes)
    most_frequent_income = category_counts.most_common(1)[0][0]

    return render_template('incomes.html', title='incomes', 
        incomes=incomes, total_income=total_income,
        max_income=max_income, max_income_name=max_income_name, 
        most_frequent_income=most_frequent_income)

@app.route('/new_income', methods=['GET', 'POST'])
def new_income():
    form = IncomeForm()
    if form.validate_on_submit():
        name = form.name.data
        category = form.category.data
        amount = form.amount.data

        if not is_valid_float(amount):
            flash("Amount must be numerical.", 'danger')

        if amount < 0:
            flash("Amount cannot be negative.", 'danger')
        else:
            income = Incomes(name=name, category=category, amount=amount)
            update_db(income)

            flash(f'Income added: {name} ({category}) - £{amount:.2f}', 'success')

    return render_template('new_income.html', title='New Income', form=form)

@app.route('/delete_income', methods=['POST'])
def delete_income():
    income = json.loads(request.data)
    incomeId = income['incomeId']
    income = Incomes.query.get(incomeId)
    
    if income:
        db.session.delete(income)
        db.session.commit()
    
    return jsonify({})

@app.route('/edit_income/<int:income_id>', methods=['GET', 'POST'])
def edit_income(income_id):
    income = Incomes.query.get(income_id)
    form = IncomeForm(obj=income)

    if form.validate_on_submit():
        income.name = form.name.data
        income.category = form.category.data
        income.amount = form.amount.data

        db.session.commit()

        flash(f'Income updated: {income.name} ({income.category}) - £{income.amount:.2f}', 'success')
        return redirect(url_for('incomes'))
    
    return render_template('edit_income.html', title='Edit Income', form=form, income=income)


"""
    
    Expense routes

"""
@app.route('/expenses')
def expenses():
    expenses = Expenses.query.all()
    total_spend = '%.2f' % sum(expense.amount for expense in expenses)

    # Store the largest expense dict by .amount, to access the .name
    max_expense = max(expenses, key=lambda expense: expense.amount)
    
    max_spend = '%.2f' % max_expense.amount
    max_spend_name = max_expense.name

    category_counts = Counter(expense.category for expense in expenses)
    most_frequent_spend = category_counts.most_common(1)[0][0]

    return render_template('expenses.html', title='Expenses', 
        expenses=expenses, total_spend=total_spend, 
        max_spend=max_spend, max_spend_name=max_spend_name, 
        most_frequent_spend=most_frequent_spend)

@app.route('/new_expense', methods=['GET', 'POST'])
def new_expense():
    form = ExpenseForm()
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

# Explain '/<int:expense_id>'
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
