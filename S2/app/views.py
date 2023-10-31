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
# Flash message flags
DANGER, SUCCESS = 'danger', 'success'

# Attempts to stage and apply a commit to the db, else rollback the attempt
def update_db(entry):
    try:
        db.session.add(entry)
        db.session.commit()
    except Exception:
        db.session.rollback()
        flash(f"An error occurred while adding this entry.", DANGER)

# Format numbers to display as nice £x,xxx.xx
def money_format(x):
    from math import log10
    """
        Example cases
        >>> money_format(1000001.949)   >>  '1,000,001.95'
        >>> money_format(10000.9)       >>  '10,000.90'
        >>> money_format(1000)          >>  '1,000.00'
        >>> money_format(999)           >>  '999.00'
    """
    if x < 10:
        return f'{x:.2f}'

    # Split x (2 d.p.) into parts before and after the decimal point
    p1, p2 = f'{x:.2f}'.split('.')

    # Find the multiples of 3 of the base 10's exponent 
    mult3 = log10(int(p1)) // 3

    # Reverse the string to insert commas easily
    revP1, limit = list(p1[::-1]), int(mult3*3)
    
    # Initialised to keep track of growing length
    count = 0
    # Loop from 10^3s, to 10^(n+1), comma every 3 orders of magnitude
    for i in range(3, limit + 1, 3):
        revP1.insert(i + count, ",")
        count += 1

    return f"{''.join(revP1)[::-1]}.{p2}"

# Generates a list of n dictionaries to act as a temp db model 
def gen_list_dict(n, has_category):
    outer = []

    inner = {'name': 0, 'amount': 0}
    if has_category:
        inner = {'name': 0, 'category': 0, 'amount': 0}
    
    # Iteratively append a deep copy of inner to access and update unique keys/values
    for i in range(n):
        outer.append(inner.copy())

    return outer

# Create a shallow copy of the model db and redefine 'amount'
def redefined_amount(model_class, has_category=True):
    # Get all table data from entries, store count
    entries = model_class.query.all()
    num_entries = len(entries)

    # Generate a hollow list of dicts mimicking the model_class
    tmp = gen_list_dict(num_entries, has_category)
    
    # Re-populate the dict values with actual amounts but formatted
    for i in range(num_entries):
        tmp[i]['name'] = entries[i].name
        tmp[i]['category'] = entries[i].category
        tmp[i]['amount'] = money_format(entries[i].amount)
    
    return tmp

# Further validate user input for 'amount'
def validate_userin(value, max_value=1000000):
    try:
        value = float(value)
        if value < 0 or value > max_value:
            return False
    except ValueError:
        return False

    return value

# Further validate user input for 'name'
def validate_tablein(value, max_length=100):
    if isinstance(value, str):
        if len(value) > max_length:
            return False
    return value

# Abstract method to run both name and amount validations
def run_validation(form, model_class, has_category):
    """
        Allows the user to pass in any form or db model.
        The Income and Expense form/db are the same so
            logic is the same.
        The Goal form/db is unique as it has no category field.
            This is checked by a boolean value in args.

        Values are set at 0 by default if validation fails.
        The appropriate values needed to create the entry are returned.
    """
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
            entry = model_class(name=name, amount=amount)

    return entry, name, category, amount

# Abstract method to make changes from the form to the db
def new_entry(form, model_class, has_category=True):
    if form.validate_on_submit():
        entry, name, category, amount = run_validation(form, model_class, has_category)
       
        if entry == 0:
            return 2

        success_message = f'Entry added: "{name}" ({category}) - £{amount:.2f}'
        update_db(entry)
        flash(success_message, SUCCESS)
        return True  

    # If unsuccessful
    return False

# Abstract method to delete any form entry from any associated db model
def delete_entry(formId, model_class):
    """

        Interacts with json method do delete an entry
    
    """
    entry = json.loads(request.data)
    # Store formId specific entry
    entryId = entry[formId]
    # Store entryId specific db row data
    entry = model_class.query.get(entryId)

    # If it exists, delete from the database and return json method call.
    if entry:
        db.session.delete(entry)
        db.session.commit()
    return jsonify({})            

# Abstract method to call upon an from entry in the db and modify it.
def edit_entry(entryId, model_class, formType, has_category=True):
    """

        Interacts with json method do edit an entry
    
    """
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

            entry.name = tmp1
            entry.amount = tmp3
            
            if has_category:
                entry.category = form.category.data
                category = entry.category
            else:
                category = ''

        db.session.commit()
        flash(f'Entry updated: {entry.name} ({category}) - £{entry.amount:.2f}', SUCCESS)
        return form, entry, True

    return form, entry, False

# Abstract method to generate db tbl stats for classes with category
def summary_io_stats(model_class):
    entries = model_class.query.all()
    if entries == []:
        flash(f"You don't have any data!", DANGER)
        return 0, 0, 0, 0, 0
    
    else:
        total = money_format(sum(entry.amount for entry in entries))
        # Store the largest entry dict by .amount, to access the .name
        max_entry = max(entries, key=lambda entry: entry.amount)
        
        max_name = max_entry.name
        max_value = money_format(max_entry.amount)

        # Finds the mode of category type
        category_counts = Counter(entry.category for entry in entries)
        most_frequent = category_counts.most_common(1)[0][0]
        
        # Changes amount key:value formatting
        entries = redefined_amount(model_class)

        return entries, total, max_name, max_value, most_frequent

# Specific method for generating the Goal tbl's stats
def summary_goal_stats():
    goal = Goals.query.first()
    if goal == None:
        return 0, 0, 0, 0
    else:
        target_value, target_name = goal.amount, goal.name
    
        incomes, expenses = Incomes.query.all(), Expenses.query.all() 
        total_income = sum(income.amount for income in incomes)
        total_spend = sum(expense.amount for expense in expenses)

        difference = abs(total_income - total_spend)
        progress_value = round((difference/target_value), 2)

        # Deal with values over 100%
        if progress_value >= 1:
            progress_value = 1
            extra = money_format((difference - target_value))
            flash(f"Target reached! You're £{extra} over budget!", SUCCESS)

        target_value, difference = money_format(target_value), money_format(difference)

        return goal, target_name, target_value, progress_value*100, difference

# Check for an existing goal in the Goal db model
def goal_exists():
    """
        Passed into all templates so that the option
            to add a second (new) goal is hidden and
            the page cannot be navigated to.

        Also acts as a condition to check for goal
            data display (toggles hidden/shown).
    """
    if Goals.query.first() == None:
        return False
    return True



# Routes
"""
    
    View entries

"""
@app.route('/', methods=['GET', 'POST'])
def homepage():
    """

        Call stat methods, store return values to feed template.

    """
    redefined_amount(Incomes)
    # Incomes as i
    i1, i2, i3, i4, i5 = summary_io_stats(Incomes)

    # Expenses as e
    e1, e2, e3, e4, e5 = summary_io_stats(Expenses)

    # Goal as g
    g1, g2, g3, g4, g5 = summary_goal_stats()

    return render_template('homepage.html', title='Homepage',
            incomes=i1, expenses=e1, goals=g1,
            
            total_income=i2, total_spend=e2, difference=g5,
            max_income_name=i3, max_spend_name=e3, target_name=g2,
            max_income=i4, max_spend=e4, target=g3, 
            
            most_frequent_income=i5, most_frequent_spend=e5, 
            goal_exists=goal_exists(), progress_value=g4)

@app.route('/incomes')
def incomes():
    v1, v2, v3, v4, v5 = summary_io_stats(Incomes)
    
    return render_template('incomes.html', title='Incomes', incomes=v1, 
        total_income=v2, max_income_name=v3,
        max_income=v4, most_frequent_income=v5, goal_exists=goal_exists())

@app.route('/expenses')
def expenses():
    v1, v2, v3, v4, v5 = summary_io_stats(Expenses)
    
    return render_template('expenses.html', title='Expenses', expenses=v1, 
        total_spend=v2, max_spend_name=v3,
        max_spend=v4, most_frequent_spend=v5, goal_exists=goal_exists())

@app.route('/goal')
def goal():
    # V5 is the difference between total income and expenses
    v1, v2, v3, v4, v5 = summary_goal_stats()
    
    return render_template('goal.html', title='Goal', goal=v1,
        target_name=v2, target=v3, progress_value=v4, goal_exists=goal_exists())



"""
    
    Add new entries

"""
@app.route('/new_income', methods=['GET', 'POST'])
def new_income():
    """
        Get and Post request actions are enabled.

        Generate a new entry and if successful,
            nav to view page for that form type.

        action:     template variable
        Is passed the title as 'new X' forms are
            abstract and need a page heading. 
    """
    title, form = 'New Income', IncomeForm()

    if new_entry(form, Incomes):
        return redirect(url_for('incomes'))

    return render_template('modify_entry.html', title=title, form=form, 
        goal_exists=goal_exists(), action=title, has_category=True)

@app.route('/new_expense', methods=['GET', 'POST'])
def new_expense():
    title, form = 'New Expense', ExpenseForm()

    if new_entry(form, Expenses):
        return redirect(url_for('expenses'))

    return render_template('modify_entry.html', title=title, form=form, 
        goal_exists=goal_exists(), action=title, has_category=True)

@app.route('/new_goal', methods=['GET', 'POST'])
def new_goal():
    if goal_exists():
        flash("A goal already exists. You cannot add a new one.", 'danger')
        return redirect(url_for('goal'))

    title, form = 'New Goal', GoalForm()
    if new_entry(form, Goals, False):
        return redirect(url_for('goal'))

    return render_template('modify_entry.html', title=title, form=form, 
        action=title, has_category=False)



"""
    
    Delete entries

"""
@app.route('/delete_income', methods=['POST'])
def delete_income():
    """
        Calls abstract method with entryId and db model
            and returns jsonify{{}} result.
    """
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
@app.route('/edit_income/<int:incomeId>', methods=['GET', 'POST'])
def edit_income(incomeId):
    """

        Interacts with json method do edit an entry-
            which needs the unique entryId 
    
    """
    title = 'Edit Income'
    form, income, success = edit_entry(incomeId, Incomes, IncomeForm)

    if success:
        return redirect(url_for('incomes'))

    return render_template('modify_entry.html', title=title, form=form, 
        income=income, goal_exists=goal_exists(),
        action=title, has_category=True)

@app.route('/edit_expense/<int:expenseId>', methods=['GET', 'POST'])
def edit_expense(expenseId):
    title = 'Edit Expense'
    form, expense, success = edit_entry(expenseId, Expenses, ExpenseForm)

    if success:
        return redirect(url_for('expenses'))

    return render_template('modify_entry.html', title=title, form=form, 
        expense=expense, goal_exists=goal_exists(),
        action=title, has_category=True)

@app.route('/edit_goal/<int:goalId>', methods=['GET', 'POST'])
def edit_goal(goalId):
    title = 'Edit Goal'
    form, goal, success = edit_entry(goalId, Goals, GoalForm, False)

    if success:
        return redirect(url_for('goal'))

    return render_template('modify_entry.html', title=title, form=form, 
        goal=goal, goal_exists=goal_exists(),
        action=title, has_category=False)

