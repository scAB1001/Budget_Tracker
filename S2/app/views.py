from flask import render_template, flash
from app import app
from .forms import CalculatorForm

"""
    @app.route('/sam')
    def index():
        user = {'name': 'Sam Wilson'}
        return render_template('index.html',
                            title='Simple template example',
                            user=user)

    @app.route('/fruit')
    def displayFruit():
        fruits = ["Apple", "Banana", "Orange", "Kiwi"]
        return render_template("fruit.html",fruits=fruits)

    @app.route('/fruit_with_inheritance')
    def displayFruit_with_inheritance():
        fruits = ["Apple", "Banana", "Blackberry", "Kiwi"]
        return render_template("template_with_inheritance.html",fruits=fruits)

    @app.route('/calc', methods=['GET', 'POST'])
    def home():
        home={'description':'Welcome to this application. Please select Calculator to calculate two numbers.'}
        return render_template('home.html', title='Home', home=home)
"""

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

@app.route('/', methods=['GET', 'POST'])
def home_page():
    home={'description':'Welcome to this application.\nPlease navigate to your desired dir.'}
    return render_template('homepage.html', title='Homepage', home=home)

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    msg={'description':'Welcome to this page. Please input two numbers to calculate.'}
    form = CalculatorForm()
    if form.validate_on_submit():
        flash_msg("Successfully received form data. ", form.number1.data, " + ", form.number2.data, " = ", form.number1.data + form.number2.data)
        #flash('Successfully received form data. %s + %s  = %s'%(form.number1.data, form.number2.data, form.number1.data+form.number2.data))
    return render_template('calculator.html', title='Calculator', form=form, msg=msg)

@app.route('/Incomes_Expenditures')
def incomes_expenditures():
    return render_template('incomeExpenditures.html', title='Incomes | Expenditures')
    
@app.route('/Goals')
def goals():
    return render_template('goals.html', title='Goals')
    