from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user
from flask_sqlalchemy import sqlalchemy
from application import app, db, login_manager, login_required
from application.auth.models import User
from application.user.forms import UserForm, EditUserForm, ChangePassword

@app.route("/user/new")
def signup_form():
    return render_template("user/new.html", form = UserForm(), error = None)

@app.route("/user/", methods=["POST"])
def signup():
    form = UserForm(request.form)
    
    u = User(form.name.data, form.username.data, form.password.data)
    u.bio = form.bio.data
    if not form.validate():
        return render_template("user/new.html", form = form, error = None)
    try:
        db.session().add(u)
        db.session().commit()
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        return render_template("user/new.html", form=form, error ="Username already taken")
 
    return redirect(url_for("welcome"))

@app.route("/user/<user_id>/change_password", methods=["GET"])
@login_required(role="DEFAULT")
def change_password(user_id):
    user = User.query.get(user_id)
    if user.id != current_user.id:
        return login_manager.unauthorized()
    return render_template("user/passwordform.html", form = ChangePassword(), user_id = user_id)


@app.route("/user/<user_id>/change_password", methods=["POST"])
@login_required(role="DEFAULT")
def update_password(user_id):
    user = User.query.get(user_id)
    if user.id != current_user.id:
        return login_manager.unauthorized()
    form = ChangePassword(request.form)
   
    user.password = form.password.data
    if not form.validate():
        return render_template("user/passwordform.html", form=form, user_id = user_id)
   
    db.session().add(user)
    db.session().commit()
    

    return redirect(url_for("welcome"))

@app.route("/user/<user_id>/edit", methods=["GET"])
@login_required(role="DEFAULT")
def user_settings(user_id):
    user = User.query.get(user_id)
    if (user.id != current_user.id):
        return login_manager.unauthorized()
    formtorender = EditUserForm()
    
    formtorender.name.data = user.name
    formtorender.username.data = user.username

    formtorender.bio.data = user.bio
    return render_template("user/update.html", form=formtorender, user_id = user_id, error = None)

@app.route("/user/<user_id>/", methods=["POST"])
@login_required(role="DEFAULT")
def update_user(user_id):
    form = EditUserForm(request.form)
    u = User.query.get(user_id)
    if u.id != current_user.id:
        return login_manager.unauthorized()
    
    u.name = form.name.data
    u.username = form.username.data
    u.bio = form.bio.data
    if not form.validate():
        return render_template("user/update.html", form = form, user_id = user_id, error = None)
    try:
        db.session().add(u)
        db.session().commit()
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        return render_template("user/update.html", form=form, user_id = user_id, error = "Username already taken")
   
    return redirect(url_for("user_profile", user_id = user_id))

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