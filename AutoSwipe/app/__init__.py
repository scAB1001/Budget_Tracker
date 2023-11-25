from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_admin import Admin

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)

migrate = Migrate(app, db, render_as_batch=True)
admin = Admin(app, template_mode='bootstrap4')


# For debugging
# Set the cache control header to not store the imported static files in cache (I dislike 304s)
@app.after_request
def add_cache_control(response):
    response.headers['Cache-Control'] = 'no-store'
    return response


from app import views, models

# Register blueprints for different parts of the app
def register_blueprints(app):
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

register_blueprints(app)

# Configure the login manager for user authentication
def configure_login_manager(app):
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        from .models import User
        return User.query.get(int(id))


configure_login_manager(app)

from flask_sqlalchemy import SQLAlchemy


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()  # Rollback the session in case of database errors
    return render_template('500.html'), 500
