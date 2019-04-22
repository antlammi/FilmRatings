from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db
from application.auth.models import User
from application.user.forms import UserForm

@app.route("/user/new")
def signup_form():
    return render_template("user/new.html", form = UserForm())

@app.route("/user/", methods=["POST"])
def signup():
    form = UserForm(request.form)
    
    u = User(form.name.data, form.username.data, form.password.data)
    u.bio = form.bio.data
    if not form.validate():
        return render_template("user/new.html", form = form)
    db.session().add(u)
    db.session().commit()

    return redirect(url_for("welcome"))

@app.route("/user/<user_id>", methods=["GET"])
def user_profile(user_id):
    user = User.query.get(user_id)
    name = user.username
    bio = user.bio
    favorite_films = User.favorite_films(user_id)
    favorite_actors = User.favorite_actors(user_id)
    favorite_directors = User.favorite_directors(user_id)

    reviews = User.user_reviews(user_id)
    return render_template("user/profile.html", name = name, bio=bio, favorite_films = favorite_films, favorite_actors = favorite_actors, favorite_directors = favorite_directors, reviews = reviews)