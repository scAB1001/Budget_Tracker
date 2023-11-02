from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# For debugging
"""
# Set the cache control header to not store the imported static files in cache (I dislike 304s)
@app.after_request
def add_cache_control(response):
    response.headers['Cache-Control'] = 'no-store'
    return response
"""

from app import views, models

from flask_sqlalchemy import SQLAlchemy