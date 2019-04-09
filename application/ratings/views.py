from flask import render_template, request, redirect, url_for
from flask_login import current_user

from application import app, db, login_required
from application.ratings.models import Rating
from application.films.models import Film
from application.auth.models import User
from application.ratings.forms import RatingForm

@app.route("/ratings/", methods=["GET"])
def ratings_index():
    return render_template("ratings/list.html", ratings=Rating.query.all(), films=Film.query.all(), users=User.query.all())

@app.route("/ratings/new", methods=["GET"])
@login_required(role="DEFAULT")
def ratings_form():
    formtorender = RatingForm()
    ratings = Rating.query.all()
    films = Film.query.all()
    
    #Rajataan käyttäjän vaihtoehdoiksi sellaiset elokuvat, joita tämä ei ole vielä arvostellut (varmaan voisi toteuttaa järkevämminkin)
    for r in ratings:    
        if (r.user_id == current_user.id):
            for f in films:
                if f.id == r.film_id:
                    films.remove(f)
   
    formtorender.film.choices = [(f.id, f.name) for f in films]
    return render_template("ratings/new.html", form = formtorender)

@app.route("/ratings/new", methods=["POST"])
@login_required(role="DEFAULT")
def ratings_create():
    form = RatingForm(request.form)
    r = Rating(form.score.data)

    
    r.user_id = current_user.id
    r.film_id = form.film.data
       
    if not form.validate():
        form.film.choices = [(f.id, f.name) for f in Film.query.all()]
        return render_template("ratings/new.html", form = form)
    db.session().add(r)
    db.session().commit()
    return redirect(url_for("ratings_index"))