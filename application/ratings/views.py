from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import app, db
from application.ratings.models import Rating
from application.films.models import Film
from application.auth.models import User
from application.ratings.forms import RatingForm

@app.route("/ratings", methods=["GET"])
def ratings_index():
    return render_template("ratings/list.html", ratings=Rating.query.all(), films=Film.query.all(), users=User.query.all())

@app.route("/ratings/new", methods=["GET"])
def ratings_form():
    return render_template("ratings/new.html", form = RatingForm())

@app.route("/ratings/new", methods=["POST"])
def ratings_create():
    form = RatingForm(request.form)
    r = Rating(form.score.data)

    #user = User.query.filter_by(id=form.account_id.data).first()
    r.user_id = form.account_id.data
    r.film_id = form.film_id.data
    #film = Film.query.filter_by(id=form.film_id.data).first()
    ##check if null, create director with name if so
       
    if not form.validate():
        return render_template("ratings/new.html", form = form)
    db.session().add(r)
    db.session().commit()
    return redirect(url_for("ratings_index"))