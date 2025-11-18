from flask import render_template, redirect, url_for, request
from .models import Recipe, User, check_password_hash, SharedRecipe
from .forms import RecipeForm, RegistrationForm, LoginForm
from . import app, db
from flask_login import current_user, login_user, logout_user, login_required

@app.route('/')
def home():
    recipes = Recipe.query.all()
    return render_template('home.html', recipes=recipes)

@app.route('/new_recipe', methods = ['GET', 'POST'])
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


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=True)
            return redirect(url_for('home'))
        error = "Invalid username or password"
        return render_template('login.html', form=form, error = error)
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/share_recipe/<int:recipe_id>', methods = ['GET', 'POST'])
@login_required
def share_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    users = User.query.filter(User.id!= current_user.id).all()
    if request.method == "POST":
        selected_user_id = request.form.get('sharee')
        sharee = User.query.get(selected_user_id)
        if sharee:
            shared_recipe = SharedRecipe(recipe_id = recipe.id, sharer_id = current_user.id, sharee_id = sharee.id)
            db.session.add(shared_recipe)
            db.session.commit()
            return redirect(url_for('home'))
        return render_template('share_recipe.html', recipe=recipe, users=users)


@app.route('/recipes/shared')
@login_required
def share_recipes():
    shared = SharedRecipe.query.filter_by(sharee_id = current_user.id).all()
    return render_template('shared_recipes.html', shared=shared)