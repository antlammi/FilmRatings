from flask import render_template, request, redirect, url_for
from flask_login import current_user

from application import app, db, login_required
from application.ratings.models import Rating
from application.films.models import Film
from application.auth.models import User
from application.ratings.forms import RatingForm, EditRatingForm

#admins have full access to a list of every rating
@app.route("/ratings/", methods=["GET"])
@login_required(role="ADMIN")
def ratings_index():
    ratings = Rating.query.all()
    return render_template("ratings/list.html", ratings=ratings, films=Film.query.all(), users=User.query.all())

@app.route("/ratings/reviews", methods=["GET"])
def reviews_index():
    reviews = Rating.reviews()
    return render_template("ratings/reviewlist.html", reviews = reviews, films=Film.query.all(), users=User.query.all())

@app.route("/ratings/reviews#<sortby>", methods=["GET"])
def reviews_sorted(sortby):
    reviews = Rating.reviews()
    
    if (sortby =='film'):
        reviews = sorted(reviews, key=lambda rating:rating[0])
    
    if (sortby =='score'):
        reviews = sorted(reviews, key=lambda rating:rating[4])
    if (sortby == 'user'):
        reviews= sorted(reviews, key =lambda rating:rating[2])
    
    return render_template("ratings/reviewlist.html", reviews = reviews, films = Film.query.all(), users = User.query.all())
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
    r.review = form.review.data       
    if not form.validate():
        form.film.choices = [(f.id, f.name) for f in Film.query.all()]
        return render_template("ratings/new.html", form = form)
    db.session().add(r)
    db.session().commit()
    return redirect(url_for("reviews_index"))


@app.route("/ratings/user/", methods=["GET"])
@login_required(role="DEFAULT")
def user_ratings_index():
    ratings = Rating.query.filter_by(user_id = current_user.id)
    return render_template("ratings/personallist.html", ratings = ratings, films = Film.query.all())

@login_required(role="DEFAULT")
@app.route("/ratings/user/<user_id>/film/<film_id>/edit", methods=["GET"])
def edit_rating_form(user_id, film_id):
    formtorender = EditRatingForm()
    r = Rating.query.filter_by(user_id = user_id, film_id = film_id).first()

    formtorender.score.data = r.score
    formtorender.review.data = r.review
    return render_template("ratings/edit.html", form=formtorender, user_id = user_id, film_id = film_id)

@app.route("/ratings/user/<user_id>/film/<film_id>/", methods=["GET"])
def ratings_show(user_id, film_id):
    user = User.query.get(user_id)
    film = Film.query.get(film_id)
    rating = Rating.query.filter_by(user_id = user_id, film_id=film_id).first()
    return render_template("ratings/show.html", user = user, film = film, rating = rating)

@login_required(role="ADMIN")
@app.route("/ratings/user/<user_id>/film/<film_id>/delete")
def ratings_delete(user_id, film_id):
    r = Rating.query.filter_by(user_id = user_id, film_id = film_id).first()
    db.session().delete(r)
    db.session().commit()
    return redirect(url_for("ratings_index"))

@login_required(role="DEFAULT")
@app.route("/ratings/user/<user_id>/film/<film_id>", methods=["POST"])
def edit_rating(user_id, film_id):
    form = EditRatingForm(request.form)

    r = Rating.query.filter_by(user_id = user_id, film_id=film_id).first()
    
    if not form.validate():
        return render_template("ratings/edit.html", form=form, user_id=user_id, film_id = film_id)
    
    r.score = form.score.data
    r.review = form.review.data
    db.session().commit()
    return redirect(url_for("user_ratings_index"))