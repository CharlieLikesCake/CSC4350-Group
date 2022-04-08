from black import re_compile_maybe_verbose
from app import app, db
import os

import flask
from flask_login import login_user, current_user, LoginManager, logout_user
from flask_login.utils import login_required
from models import RecipeData, User

import recipe
import random

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_name):
    return User.query.get(user_name)


@app.route("/")
def landing():
    if current_user.is_authenticated:
        return flask.redirect("index")
    return flask.redirect("login")


@app.route("/signup")
def signup():
    return flask.render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup_post():
    username = flask.request.form.get("username")
    user = User.query.filter_by(username=username).first()
    if len(username) < 3:
        flask.flash("Username must be at least 3 characters in length.")
        return flask.redirect(flask.url_for("signup"))
    elif user:
        flask.flash("Username already in use.")
        return flask.redirect(flask.url_for("signup"))
    else:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
        flask.flash("Successfully registered.")
        return flask.redirect(flask.url_for("login"))


@app.route("/login")
def login():
    return flask.render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    username = flask.request.form.get("username")
    user = User.query.filter_by(username=username).first()
    if user:
        login_user(user)
        return flask.redirect(flask.url_for("index"))

    else:
        flask.flash("Incorrect username.")
        return flask.redirect(flask.url_for("login"))


@app.route("/logout")
def logout():
    logout_user()
    flask.flash("Successfully logged out.")
    return flask.redirect("login")


# route for homepage
@app.route("/index")
@login_required
def index():
    q = ["chicken", "salad", "soup", "pasta", "curry", "sandwich"]
    r = random.randrange(0, 6, 1)
    recipes = recipe.getRandomRecipeList(q[r])

    return flask.render_template(
        "index.html",
        username=current_user.username,
        q=q[r],
        recipes=recipes,
        len_recipes=1,
    )


@app.route("/details", methods=["GET", "POST"])
@login_required
def details():
    id = flask.request.form.get("id")
    recipeDetails = recipe.getRecipeDetails(id)
    mealReco = recipeDetails["mealType"]
    cuisineReco = recipeDetails["cuisineType"]
    ingReco = recipeDetails["ingredients"]
    ingReco = ingReco[0]["food"]
    ingcatReco = recipeDetails["ingredients"]
    ingcatReco = ingcatReco[0]["foodCategory"]
    healthReco = recipeDetails["healthLabels"]

    mealRecipes = recipe.getRandomRecipeList(mealReco)
    cuisineRecipes = recipe.getRandomRecipeList(cuisineReco)
    ingRecipes = recipe.getRandomRecipeList(ingReco)
    ingcatRecipes = recipe.getRandomRecipeList(ingcatReco)
    healthRecipes = recipe.getRandomRecipeList(healthReco)

    return flask.render_template(
        "details.html",
        recipeDetails=recipeDetails,
        mealRecipes=mealRecipes,
        cuisineRecipes=cuisineRecipes,
        ingRecipes=ingRecipes,
        ingcatRecipes=ingcatRecipes,
        healthRecipes=healthRecipes,
    )


@app.route("/profile", methods=["POST", "GET"])
@login_required
def profile():
    userdata = User.query.all()
    data = RecipeData.query.all()
    label_list = []
    image_list = []
    url_list = []

    for i in data:
        label_list.append(i.label)
        image_list.append(i.image)
        url_list.append(i.url)

    num_label = len(label_list)

    return flask.render_template(
        # display database information here
        "favorite.html",
        username=current_user.username,
        label=label_list,
        image=image_list,
        url=url_list,
        num_label=num_label,
    )


@app.route("/favorite", methods=["POST"])
def favorite():
    username = current_user.username
    recipeDetail = flask.request.form.get("recipeDetail")
    recipeImage = flask.request.form.get("recipeImage")
    recipeURL = flask.request.form.get("recipeURL")
    new_saved = RecipeData(
        label=recipeDetail,
        image=recipeImage,
        url=recipeURL,
    )

    db.session.add(new_saved)
    db.session.commit()
    return flask.redirect("index")


if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", 8080)),
        debug=True,
    )
