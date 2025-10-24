from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SECRET_KEY'] = 'cfa4feb4af3a9b829cc1c6abb095696c61de874a67f59624'


db = SQLAlchemy(app)
migrate = Migrate(app, db)


login_manager = LoginManager(app)
from myapp.models import User
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from myapp import routes