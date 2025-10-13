from flask import render_template, redirect, url_for
from .models import Recipe
from .forms import RecipeForm
from . import app, db


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
