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

    if not form.validate():
        return render_template("user/new.html", form = form)
    db.session().add(u)
    db.session().commit()

    return redirect(url_for("films_index"))

##@app.route("/user/<user_id>", methods=["GET"])
##def user_profile(user_id):
