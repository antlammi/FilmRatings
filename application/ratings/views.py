from flask import render_template, request, redirect, url_for
from flask_login import current_user

from application import app, db, login_required, login_manager
from application.ratings.models import Rating
from application.films.models import Film
from application.auth.models import User
from application.ratings.forms import FilmRatingForm,ReviewForm, EditRatingForm

#admins have full access to a list of every rating
@app.route("/ratings/", methods=["GET"])
@login_required(role="ADMIN")
def ratings_index():
    ratings = Rating.all_ratings_with_films_and_users()
    return render_template("ratings/list.html", ratings=ratings, sortby = None, desc = None)

@app.route("/ratings#<sortby>", methods=["GET"])
@login_required(role="ADMIN")
def ratings_index_sorted(sortby):
    ratings = Rating.all_ratings_with_films_and_users()
    desc = False
    if ('film' in sortby):
        ratings= sorted(ratings, key=lambda rating:rating[0])
    if ('score' in sortby):
        ratings= sorted( ratings, key=lambda rating:rating[4], reverse = True)
    if ('user' in sortby):
        ratings = sorted(ratings, key =lambda rating:rating[2])
    if ('review' in sortby):
        ratings = sorted(ratings, key = lambda rating:rating[6])
    if ('desc' in sortby):
        ratings.reverse()
        desc = True
    return render_template("ratings/list.html", ratings=ratings, sortby = sortby, desc = desc)
    
@app.route("/ratings/reviews", methods=["GET"])
def reviews_index():
    reviews = Rating.reviews()
    return render_template("ratings/reviewlist.html", reviews = reviews, sortby = None, desc = None)

@app.route("/ratings/reviews#<sortby>", methods=["GET"])
def reviews_sorted(sortby):
    reviews = Rating.reviews()
    desc = False
    if ('film' in sortby):
        reviews = sorted(reviews, key=lambda rating:rating[0])
    
    if ('score' in sortby):
        reviews = sorted(reviews, key=lambda rating:rating[4], reverse = True)
    if ('user' in sortby):
        reviews= sorted(reviews, key =lambda rating:rating[2])
    if ('review' in sortby):
        reviews = sorted(reviews, key=lambda rating:rating[5])
    if ('desc' in sortby):
        reviews.reverse()
        desc = True
    return render_template("ratings/reviewlist.html", reviews = reviews, sortby = sortby, desc = desc)

@app.route("/ratings/new", methods=["GET"])
@login_required(role="DEFAULT")
def ratings_form():
    formtorender = ReviewForm()
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
@app.route("/ratings/new/film/<film_id>", methods=["POST"])
@login_required(role="DEFAULT")
def ratings_create_quick(film_id):
    form = FilmRatingForm(request.form)
    r = Rating(form.score.data)

    r.user_id = current_user.id
    r.film_id = film_id
    
    db.session().add(r)
    db.session().commit()
    return redirect(url_for("films_show", film_id = film_id))


@app.route("/ratings/new", methods=["POST"])
@login_required(role="DEFAULT")
def ratings_create():
    form = ReviewForm(request.form)
    r = Rating(form.score.data)

    r.user_id = current_user.id
    r.film_id = form.film.data
    r.title = form.title.data
    r.review = form.review.data       
    if not form.validate() or form.film.data == None:
        ratings = Rating.query.all()
        films = Film.query.all()
        for r in ratings:    
            if (r.user_id == current_user.id):
                for f in films:
                    if f.id == r.film_id:
                        films.remove(f)


        form.film.choices = [(f.id, f.name) for f in films]
        return render_template("ratings/new.html", form = form)
    db.session().add(r)
    db.session().commit()
    return redirect(url_for("reviews_index"))


@app.route("/ratings/user/", methods=["GET"])
@login_required(role="DEFAULT")
def user_ratings_index():
    ratings = Rating.user_ratings(current_user.id)

    return render_template("ratings/personallist.html", ratings = ratings, sortby = None, desc = None)

@app.route("/ratings/user#<sortby>", methods=["GET"])
@login_required(role="DEFAULT")
def user_ratings_sorted(sortby):
    ratings = Rating.user_ratings(current_user.id)
    desc = False
    if ('film' in sortby):
        ratings = sorted(ratings, key=lambda rating:rating[0])
    
    if ('score' in sortby):
        ratings = sorted(ratings, key=lambda rating:rating[4], reverse = True)
    
    if ('review' in sortby):
        ratings = sorted(ratings, key=lambda rating:rating[6])
    if ('desc' in sortby):
        ratings.reverse()
        desc = True
    return render_template("ratings/personallist.html", ratings = ratings, sortby = sortby, desc = desc)


@login_required(role="DEFAULT")
@app.route("/ratings/user/<user_id>/film/<film_id>/edit", methods=["GET"])
def edit_rating_form(user_id, film_id):
    u = User.query.get(user_id)
    if u.id != current_user.id:
        return login_manager.unauthorized()
    formtorender = EditRatingForm()
    r = Rating.query.filter_by(user_id = user_id, film_id = film_id).first()

    formtorender.score.data = r.score
    formtorender.title.data = r.title
    formtorender.review.data = r.review
    film = Film.query.get(film_id)
    formtorender.film.data = film.name
    return render_template("ratings/edit.html", form=formtorender, user_id = user_id, film_id = film_id ) 

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
@app.route("/ratings/user/<user_id>/film/<film_id>/delete#personal")
def ratings_delete_personal(user_id, film_id):
    r = Rating.query.filter_by(user_id = user_id, film_id = film_id).first()
    u = User.query.get(user_id)
    if u.id != current_user.id:
        return login_manager.unauthorized()
    db.session().delete(r)
    db.session().commit()
    return redirect(url_for("user_ratings_index"))

@login_required(role="DEFAULT")
@app.route("/ratings/user/<user_id>/film/<film_id>", methods=["POST"])
def edit_rating(user_id, film_id):
    form = EditRatingForm(request.form)
    film = Film.query.get(film_id)
    u = User.query.get(user_id)
    if u.id != current_user.id:
        return login_manager.unauthorized()
    r = Rating.query.filter_by(user_id = user_id, film_id=film_id).first()
    
    if not form.validate():
        film = Film.query.get(film_id)
        return render_template("ratings/edit.html", form=form, user_id=user_id, film_id = film_id, film_name = film.name)
    
    r.score = form.score.data
    r.title = form.title.data
    r.review = form.review.data
    db.session().commit()
    return redirect(url_for("user_ratings_index"))