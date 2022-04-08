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
        len_recipes=len(recipes),
    )


@app.route("/profile", methods=["POST", "GET"])
@login_required
def profile():
    return flask.render_template(
        # display database information here
        "favorite.html",
        username=current_user.username,
    )


@app.route("/favorite", methods=["POST", "GET"])
def favorite():
    # save the information to database
    if flask.request.method == "POST":
        data = flask.request.form
        detail = data.get("favorite")
        new_saved = RecipeData(
            detail=detail,
        )
        db.session.add(new_saved)
        db.session.commit()


if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", 8080)),
        debug=True,
    )
