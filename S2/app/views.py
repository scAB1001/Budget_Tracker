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
    
    result = f"{''.join(revP1)[::-1]}.{p2}"
    return result

# Create a copy of the model db and redefine 'amount'
def gen_model_copy(model_class, has_category=True):
    # Get all table data from entries, store count
    entries = model_class.query.all()
    num_entries = len(entries)
    
    outer, inner = {}, {'name': 0, 'amount': 0}
    
    if has_category:
        inner = {'name': 0, 'category': 0, 'amount': 0}
    
    # Iteratively add a deep copy of inner, update real-time values
    for i in range(num_entries):
        id = entries[i].id
        outer[id] = inner.copy()

        outer[id]['name'] = entries[i].name
        outer[id]['category'] = entries[i].category
        outer[id]['amount'] = money_format(entries[i].amount)

    return outer

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

    if amount != False:
        amount = validate_tablein(amount)
        name = validate_tablein(form.name.data)

    if amount != False and name != False:
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

# Abstract method to delete all form entries from any db model
def delete_all_entries(model_class):
    if model_class.query.first() != None:
        model_class.query.delete() 
        db.session.commit()
    return jsonify({})

# Abstract method to delete any form entry from any db model
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
        
        if entry != None:  
            tmp1 = validate_tablein(form.name.data)
            if tmp1 != False:
                entry.name = tmp1

            tmp3 = validate_userin(form.amount.data)
            if tmp3 != False:
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

# Check for existing data in any db model
def tbl_exists(model_class):
    """
        Passed into all templates (from base),
            so that the option to add a second (new) goal
            is hidden and the page cannot be navigated to.

        Also as a condition to check for goal/income/expense
            data display (toggles hidden/shown).

    """
    if model_class == Goals:
        return model_class.query.first() != None

    return model_class.query.all() != None

click_count = 30
should_increment = True
@app.route('/toggle_count', methods=['POST'])
def toggle_count():
    global click_count, should_increment
    if should_increment:
        click_count += 1
    else:
        click_count -= 1
    # Toggle the state
    should_increment = not should_increment
    #print(f"Current click count: {click_count}")
    return jsonify(click_count=click_count)

# Routes
"""
    
    View entries

"""
@app.route('/')
def home():
    return render_template('home.html', title='Home')


@app.route('/login')  # , methods=['GET', 'POST']
def login():
    return render_template('login.html', title='Login')


@app.route('/signup')
def signup():
    return render_template('signup.html', title='Signup', click_count=click_count)



@app.route('/explore')
def explore():
    return render_template('explore.html', title='Explore')


@app.route('/settings')
def settings():
    return render_template('settings.html', title='Settings')


@app.route('/history')
def history():
    return render_template('history.html', title='History')


@app.route('/incomes')
def incomes():
    v1, v2, v3, v4, v5 = 0, 0, 0, 0, 0,  # summary_io_stats(Incomes)
    
    return render_template('view_entries.html', title='Incomes', 
        entry_type='income', entries=v1,
        total=v2, max_name=v3,
        max_value=v4, most_frequent=v5, 
        goal_exists=tbl_exists(Goals))



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

    return render_template('modify_entry.html', title=title, 
        form=form, goal_exists=tbl_exists(Goals), 
        action=title, has_category=True)



"""
    
    Delete entries

"""
# All entries
@app.route('/delete_all_incomes', methods=['POST'])
def delete_all_incomes():
    """
        Calls abstract method with db model
            and return jsonify{{}} result.
    """
    if not tbl_exists(Incomes):
        flash("There are no incomes to delete.", 'danger')
        return redirect(url_for('incomes'))

    return delete_all_entries(Incomes)


# Specific entries
@app.route('/delete_income', methods=['POST'])
def delete_income():
    """
        Calls abstract method with entryId and db model
            and return jsonify{{}} result.
    """
    if not tbl_exists(Incomes):
        flash("There are no incomes to delete.", 'danger')
        return redirect(url_for('incomes'))

    return delete_entry('entryId', Incomes)


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

    return render_template('modify_entry.html', title=title, 
        form=form, income=income, goal_exists=tbl_exists(Goals),
        action=title, has_category=True)

