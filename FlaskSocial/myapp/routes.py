from flask import render_template, redirect, url_for
from .models import Recipe, User
from .forms import RecipeForm, RegistrationForm
from . import app, db
from flask_login import current_user

@app.route('/')
def home():
    recipes = Recipe.query.all()
    return render_template('home.html', recipes=recipes)

@app.route('/new_recipe')
def new_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(title = form.title.data, description = form.description.data)
        db.session.add(recipe)
        db.session.commit()
        return(redirect(url_for('home')))
    return render_template('new_recipe.html', title = "New Recipe", form=form)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html', title="Register", form=form)
