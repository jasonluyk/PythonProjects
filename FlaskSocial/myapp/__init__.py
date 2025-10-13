from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SECRET_KEY'] = 'cfa4feb4af3a9b829cc1c6abb095696c61de874a67f59624'


db = SQLAlchemy(app)
migrate = Migrate(app, db)
from myapp import routes, models