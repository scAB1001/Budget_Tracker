from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, db
from .forms import IncomeForm, ExpenseForm, GoalForm
from .models import Incomes, Expenses, Goals

import json
from collections import Counter


# General
"""  

    Helper variables and methods

"""
DANGER, SUCCESS = 'danger', 'success'

def update_db(entry):
    try:
        db.session.add(entry)
        db.session.commit()#;print("\nSuccessfully updated db\n")
    except Exception:
        db.session.rollback()
        flash(f"An error occurred while adding this entry.", DANGER)

def validate_userin(value, max_value=1000000):
    try:
        value = float(value)
        if value < 0 or value > max_value:
            flash("Amount must be between 0 and 1,000,000.", DANGER)#; print(f"\nERR: max_value\n")
            return False
    except ValueError:
        flash("Input must be a number.", DANGER)#; print(f"\nERR: float conversion\n")
        return False

    return value

def validate_tablein(value, max_length=100):
    if isinstance(value, str):
        if len(value) > max_length:
            flash("Input string is too long.", DANGER); print(f"\nERR: string length\n")
            return False
    elif isinstance(value, int):
        value = float(value); print(f"\nERR: integer conversion\n")
    
    return value

def run_validation(form, model_class, has_category):
    entry, name, category = 0, 0, 0
    amount = validate_userin(form.amount.data)

    if amount is not False:
        amount = validate_tablein(amount)
        name = validate_tablein(form.name.data)

    if amount is not False and name is not False:
        if has_category:
            category = form.category.data
            entry = model_class(name=name, category=category, amount=amount)
        else:
            category = ''
            entry = model_class(name=name, amount=amount)#; print(f'\nNO CATEGORY\n')

    return entry, name, category, amount

def new_entry(form, model_class, has_category=True):
    if form.validate_on_submit():
        entry, name, category, amount = run_validation(form, model_class, has_category)
       
        if entry == 0:
            return 2

        success_message = f'Entry added: "{name}" ({category}) - £{amount:.2f}'
        update_db(entry)#; print(0)
        flash(success_message, SUCCESS)
        return 0

    return 1

def delete_entry(formId, model_class):
    entry = json.loads(request.data)
    entryId = entry[formId]
    entry = model_class.query.get(entryId)

    if entry:
        db.session.delete(entry)
        db.session.commit()
    return jsonify({})            

def edit_entry(entryId, model_class, formType, has_category=True):
    entry = model_class.query.get(entryId)
    form = formType(obj=entry)

    if form.validate_on_submit():
        
        if entry is not None:  
            tmp1 = validate_tablein(form.name.data)
            if tmp1 is not False:
                entry.name = tmp1

            tmp3 = validate_userin(form.amount.data)
            if tmp3 is not False:
                entry.amount = tmp3

            entry.name = tmp1  #form.name.data
            entry.amount = tmp3  #form.amount.data
            
            if has_category:
                entry.category = form.category.data
                category = entry.category
            else:
                category = ''

        db.session.commit()
        flash(f'Entry updated: {entry.name} ({category}) - £{entry.amount:.2f}', SUCCESS)
        return form, entry, True

    return form, entry, False

def summary_io_stats(model_class):
    entries = model_class.query.all()

    total = round(sum(entry.amount for entry in entries), 2)
    # Store the largest entry dict by .amount, to access the .name
    max_entry = max(entries, key=lambda entry: entry.amount)
    
    max_name = max_entry.name
    max_value = round(max_entry.amount, 2)

    category_counts = Counter(entry.category for entry in entries)
    most_frequent = category_counts.most_common(1)[0][0]

    return entries, total, max_name, max_value, most_frequent

def summary_goal_stats():
    goal = Goals.query.first()
    if goal == None:
        flash(f"You don't have a goal set!", "danger")
        return new_goal()
    else:
        target_value, target_name = goal.amount, goal.name
    
        incomes, expenses = Incomes.query.all(), Expenses.query.all() 
        total_income = sum(income.amount for income in incomes)
        total_spend = sum(expense.amount for expense in expenses)

        difference = total_income - total_spend
        progress_value = round((difference/target_value), 2)

        if difference < 0: 
            flash(f"You're £{difference} away...", "danger")
        elif progress_value >= 1:
            progress_value = 1
            extra = difference - target_value
            flash(f"Target reached!\n You're £{extra} over budget!?", SUCCESS)
        return goal, target_name, target_value, progress_value*100

# Routes
    # Test page
@app.route('/a')
def progress_bar():
    goal = Goals.query.first()#; print(f'\n{goal}: is of type{type(goal)}')
    if goal == None:
        goal = {"HyundaiFrX_10":16250}
    target, target_name = goal.amount, goal.name
   
    incomes, expenses = Incomes.query.all(), Expenses.query.all() 
    total_income = sum(income.amount for income in incomes)
    total_spend = sum(expense.amount for expense in expenses)

    difference = total_income - total_spend
    progress_value = round((difference/target), 2)
    #print(progress_value, '\n')

    # Set a default display value
    if difference < 0: 
        flash(f"You're £{difference} away...", "danger")
    elif progress_value >= 1:
        progress_value = 1
        extra = difference - target
        flash(f"Target reached!\n You're £{extra} over budget!?", SUCCESS)
    return render_template('progress_bar.html', title='Progress Bar', goal=goal, 
        progress_value=progress_value*100, target_name=target_name, target=target)



"""
    
    View entries

"""
# Address homepage and stat generation
@app.route('/', methods=['GET', 'POST'])
def homepage():
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
        total_income = '%.2f' % sum(income.amount for income in incomes)
        total_spend = '%.2f' % sum(expense.amount for expense in expenses)

        difference = float(total_income) - float(total_spend)        
        progress_value = round((difference/target), 2)
        if difference < 0: 
            progress_value = 0
        elif progress_value >= 1:
            progress_value = 1
            extra = difference - target

    return render_template('homepage.html', title='Homepage',
        incomes=incomes, expenses=expenses, 
        target=target, target_name=target_name,
        total_income=float(total_income), total_spend=float(total_spend),
        max_income=max_income, max_income_name=max_income_name, 
        most_frequent_income=most_frequent_income,
        max_spend=max_spend, max_spend_name=max_spend_name, 
        most_frequent_spend=most_frequent_spend, 
        progress_value=progress_value*100
    )

@app.route('/incomes')
def incomes():
    """
        incomes = Incomes.query.all()
        total_income = '%.2f' % sum(income.amount for income in incomes)
        max_earning = max(incomes, key=lambda income: income.amount)
        
        max_income = '%.2f' % max_earning.amount
        max_income_name = max_earning.name

        category_counts = Counter(income.category for income in incomes)
        most_frequent_income = category_counts.most_common(1)[0][0]
    """
    v1, v2, v3, v4, v5 = summary_io_stats(Incomes)
    return render_template('incomes.html', title='Incomes', incomes=v1, 
        total_income=v2, max_income_name=v3,
        max_income=v4, most_frequent_income=v5)

@app.route('/expenses')
def expenses():
    """
        expenses = Expenses.query.all()
        print("OH: ", expenses[0].amount)
        total_spend = '%.2f' % sum(expense.amount for expense in expenses)

        # Store the largest expense dict by .amount, to access the .name
        max_expense = max(expenses, key=lambda expense: expense.amount)
        
        max_spend = '%.2f' % max_expense.amount
        max_spend_name = max_expense.name

        category_counts = Counter(expense.category for expense in expenses)
        most_frequent_spend = category_counts.most_common(1)[0][0]

        return render_template('incomes.html', title='Incomes', incomes=v1, 
            total_income=v2, max_income_name=v3,
            max_income=v4, most_frequent_income=v5)
    """
    v1, v2, v3, v4, v5 = summary_io_stats(Expenses)
    return render_template('expenses.html', title='Expenses', expenses=v1, 
        total_spend=v2, max_spend_name=v3,
        max_spend=v4, most_frequent_spend=v5)

@app.route('/goal')
def goal():
    v1, v2, v3, v4 = summary_goal_stats()
    return render_template('goal.html', title='Goal', goal=v1,
        target_name=v2, target=v3, progress_value=v4)



"""
    
    Add new entries

"""
@app.route('/new_income', methods=['GET', 'POST'])
def new_income():
    form = IncomeForm()
    new_entry(form, Incomes)
    return render_template('new_income.html', title='New Income', form=form)

@app.route('/new_expense', methods=['GET', 'POST'])
def new_expense():
    form = ExpenseForm()
    new_entry(form, Expenses)
    return render_template('new_expense.html', title='New Expense', form=form)

@app.route('/new_goal', methods=['GET', 'POST'])
def new_goal():
    form = GoalForm()
    new_entry(form, Goals, False)
    return render_template('new_goal.html', title='New Goal', form=form)



"""
    
    Delete entries

"""
@app.route('/delete_income', methods=['POST'])
def delete_income():
    return delete_entry('incomeId', Incomes)

@app.route('/delete_expense', methods=['POST'])
def delete_expense():
    return delete_entry('expenseId', Expenses)

@app.route('/delete_goal', methods=['POST'])
def delete_goal():
    return delete_entry('goalId', Goals)



"""
    
    Edit entries

"""
# Explain '/<int:incomeId>'
@app.route('/edit_income/<int:incomeId>', methods=['GET', 'POST'])
def edit_income(incomeId):
    form, income, success = edit_entry(incomeId, Incomes, IncomeForm)
    if success:
        return redirect(url_for('incomes'))
    return render_template('edit_income.html', title='Edit Income', form=form, income=income)

@app.route('/edit_expense/<int:expenseId>', methods=['GET', 'POST'])
def edit_expense(expenseId):
    form, expense, success = edit_entry(expenseId, Expenses, ExpenseForm)
    if success:
        return redirect(url_for('expenses'))
    return render_template('edit_expense.html', title='Edit Expense', form=form, expense=expense)

@app.route('/edit_goal/<int:goalId>', methods=['GET', 'POST'])
def edit_goal(goalId):
    form, goal, success = edit_entry(goalId, Goals, GoalForm, False)
    if success:
        return redirect(url_for('goal'))
    return render_template('edit_goal.html', title='Edit Goal', form=form, goal=goal)

