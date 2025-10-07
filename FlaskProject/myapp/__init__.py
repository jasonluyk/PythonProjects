from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new_database.db'
app.config['SECRET_KEY'] ='682d03736eec7ff403d3337741a7109a30f73f1b89e57719'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from myapp import routes, models