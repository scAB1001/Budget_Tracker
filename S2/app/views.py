from flask import render_template
from app import app

@app.route('/')
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