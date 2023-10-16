from flask import render_template, flash
from app import app
from .forms import CalculatorForm

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

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    form = CalculatorForm()
    if form.validate_on_submit():
        flash('Succesfully received form data. %s + %s  = %s'%(form.number1.data, form.number2.data, form.number1.data+form.number2.data))
    return render_template('calculator.html',
                           title='Calculator',
                           form=form)

@app.route('/calc', methods=['GET', 'POST'])
def home():
    home={'description':'Welcome to this application. Please select Calculator to calculate two numbers.'}
    return render_template('home.html', title='Home', home=home)



@app.route('/', methods=['GET', 'POST'])
def home_page():
    home={'description':'Welcome to this application. Please select Calculator to calculate two numbers.'}
    return render_template('zhomepage.html', title='Homepage', home=home)

@app.route('/Incomes_Expenditures')
def incomes_expenditures():
    return render_template('zie.html', title='Incomes | Expenditures')
    
@app.route('/Goals')
def goals():
    return render_template('zgoals.html', title='Goals')
    