from application import app, db, login_required
from flask import redirect, render_template, request, url_for
from application.films.models import Film
from application.directors.models import Director
from application.films.forms import FilmForm

@app.route("/films/new")
@login_required("ANY")
def films_form():
    formtorender = FilmForm() 
    formtorender.director.choices = [(d.id, d.name) for d in Director.query.all()]
    return render_template("films/new.html", form=formtorender)

@app.route("/films/", methods=["POST"])
@login_required(role="ANY")
def films_create():
    form = FilmForm(request.form)
    
    f = Film(form.name.data)
    d_id = form.director.data
   
    f.director_id = d_id
    
    
    if not form.validate():
        form.director.choices = [(d.id, d.name) for d in Director.query.all()]
        return render_template("films/new.html", form = form)
    db.session().add(f)
    db.session().commit()

    return redirect(url_for("films_index"))

@app.route("/films/<film_id>/edit", methods=["GET"])
@login_required(role="ADMIN")
def films_edit(film_id):
    formtorender = FilmForm() 
    formtorender.director.choices = [(d.id, d.name) for d in Director.query.all()]
    return render_template("films/update.html", form=formtorender, film_id = film_id)

@app.route("/films/<film_id>", methods=["GET"])
def films_show(film_id):
    f=Film.query.get(film_id)
    return render_template("films/show.html", film=f, director=Director.query.filter_by(id = f.director_id).first(),
        average_rating=Film.average_rating(film_id), ratings_count=Film.ratings_count(film_id))
 
@app.route("/films/<film_id>/delete", methods=["GET"])
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
   
    f.director_id = d_id

    if not form.validate():
        form.director.choices = [(d.id, d.name) for d in Director.query.all()]
        return render_template("films/new.html", form = form)
    db.session().commit()
    return redirect(url_for("films_index"))

@app.route("/films/", methods=["GET"])
def films_index():
    return render_template("films/list.html", films = Film.query.all(), directors = Director.query.all())

