from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    description = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    recipes = db.relationship('Recipe', backref='author', lazy = 'dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class SharedRecipe(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable = False)
    sharer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    sharee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    recipe = db.relationship('Recipe', backref = db.backref('shared_recipe'), lazy = True)
    sharer = db.relationship('User', foreign_keys = [sharer_id])
    sharee = db.relationship('User', foreign_keys = [sharee_id])