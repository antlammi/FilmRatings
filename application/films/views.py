from application import app, db, login_required
from flask import redirect, render_template, request, url_for
from application.films.models import Film
from application.directors.models import Director
from application.actors.models import Actor, FilmActor
from application.ratings.models import Rating
from application.ratings.forms import FilmRatingForm
from application.films.forms import FilmForm
from flask_login import current_user

from sqlalchemy import and_
@app.route("/films/new")
@login_required("ANY")
def films_form():
    formtorender = FilmForm() 
    formtorender.director.choices = [(d.id, d.name) for d in Director.query.all()]
    formtorender.actors.choices = [(a.id, a.name) for a in Actor.query.all()]
    return render_template("films/new.html", form=formtorender)

@app.route("/films/", methods=["POST"])
@login_required(role="ANY")
def films_create():
    form = FilmForm(request.form)
    
    f = Film(form.name.data)
    d_id = form.director.data
    f.year = form.year.data
    f.director_id = d_id
    f.poster = form.poster.data
    actors = form.actors.data

    f.description = form.description.data
    if not form.validate():
        form.director.choices = [(d.id, d.name) for d in Director.query.all()]
        form.actors.choices = [(a.id, a.name) for a in Actor.query.all()]
        return render_template("films/new.html", form = form)
    db.session().add(f)
    db.session().commit()
    for actor in actors:
        fa = FilmActor()
        fa.film_id = Film.query.filter_by(name=form.name.data).first().id
        fa.actor_id = actor
        db.session().add(fa)
        db.session().commit()
    return redirect(url_for("films_index"))

@app.route("/films/<film_id>/edit", methods=["GET"])
@login_required(role="ADMIN")
def films_edit(film_id):
    formtorender = FilmForm() 
    formtorender.director.choices = [(d.id, d.name) for d in Director.query.all()]
    formtorender.actors.choices = [(a.id, a.name) for a in Actor.query.all()]

    film = Film.query.get(film_id)

    for director in formtorender.director.choices:
        if director[0] == film.director_id:
            formtorender.director.process_data(film.director_id)

    fa = FilmActor.query.filter_by(film_id = film_id)
    formtorender.actors.data = []
    for actor in formtorender.actors.choices:
        for a in fa:
            formtorender.actors.data.append(a.actor_id)
    formtorender.name.data = film.name
    formtorender.year.data = film.year
    formtorender.poster.data = film.poster
    formtorender.description.data = film.description
    
    return render_template("films/update.html", form=formtorender, film_id = film_id, film = film)
@app.route("/films/<film_id>", methods=["GET"])
def films_show(film_id):
    f=Film.query.get(film_id)
    actor_ids = FilmActor.query.filter_by(film_id = film_id)
    actors = []
    for a in actor_ids:
        actors.append(Actor.query.filter_by(id = a.actor_id).first())     
    ratingform = FilmRatingForm()
    user_rating = -1
    if current_user.is_authenticated:
        if current_user.urole == "DEFAULT":
            user_rating = Rating.query.filter_by(user_id = current_user.id, film_id = f.id).first()

    reviews = Film.film_reviews(film_id)
    return render_template("films/show.html", film=f, director=Director.query.filter_by(id = f.director_id).first(),
        average_rating=Film.average_rating(film_id), ratings_count=Film.ratings_count(film_id),
        actors = actors, reviews = reviews, rf = ratingform, user_rating = user_rating)
 
@app.route("/films/<film_id>/delete")
@login_required(role="ADMIN")
def films_delete(film_id):
    f = Film.query.get(film_id)
    db.session().delete(f)
    db.session().commit()
    return redirect(url_for("films_index"))

@app.route("/films/<film_id>/update", methods=["POST"])
@login_required(role="ADMIN")
def films_update(film_id):
    form = FilmForm(request.form)
    f = Film.query.get(film_id)

    f.name = form.name.data
    d_id = form.director.data
    f.poster = form.poster.data 
    f.year = form.year.data   
    f.director_id = d_id
    actors = form.actors.data
    f.description = form.description.data
    if not form.validate():
        form.director.choices = [(d.id, d.name) for d in Director.query.all()]
        form.actors.choices = [(a.id, a.name) for a in Actor.query.all()]
        return render_template("films/update.html", form = form, film_id = film_id)
    db.session().commit()
    
    #clearing out previous film_actor instances so edited information can replace it
    falist = FilmActor.query.filter_by(film_id = film_id)
    for fa in falist:
        db.session().delete(fa)
        db.session().commit()

    for actor in actors:
        if (FilmActor.query.filter_by(film_id = film_id, actor_id = actor).first() == None):
            fa = FilmActor()
            fa.film_id = Film.query.filter_by(name=form.name.data).first().id
            fa.actor_id = actor
            
            db.session().add(fa)
            db.session().commit()
        

    return redirect(url_for("films_index"))

@app.route("/films/", methods=["GET"])
def films_index():
    films = Film.films_with_ratings()
    return render_template("films/list.html", films = films, directors = Director.query.all(), sortby = None, desc = None)

@app.route ("/films#<sortby>", methods = ["GET"])
def films_sorted(sortby):
    films = Film.films_with_ratings()
    desc = False
    if ('name' in sortby):
        films = sorted(films, key=lambda film:film[1])
    if ('year' in sortby):
        films = sorted(films, key=lambda film:film[2])
    if ('director' in sortby):
        films = sorted(films, key=lambda film:film[4].split()[-1])
        # -1 loops back to the end of the array, getting the last name
    if ('rating' in sortby):
        films = sorted(films, key=lambda film:film[5], reverse=True)

    if ('desc' in sortby):
        films.reverse()
        desc = True

    return render_template("films/list.html", films = films, directors = Director.query.all(), sortby = sortby, desc = desc)