from application import app, db
from flask_login import login_required
from flask import redirect, render_template, request, url_for
from application.films.models import Film
from application.directors.models import Director
from application.films.forms import FilmForm

@app.route("/films/new")
def films_form():
    return render_template("films/new.html", form = FilmForm())

@app.route("/films/", methods=["POST"])
def films_create():
    form = FilmForm(request.form)

    f = Film(form.name.data)

    director = Director.query.filter_by(name=form.director.data).first()
    
    f.director_id = director.id
    ##check if null, create director with name if so
       
    if not form.validate():
        return render_template("films/new.html", form = form)
    db.session().add(f)
    db.session().commit()

    return redirect(url_for("films_index"))
##update
#@app.route("/films/<film_id>", methods=["POST"])
#@login_required
@app.route("/films/", methods=["GET"])
def films_index():
    return render_template("films/list.html", films = Film.query.all(), directors = Director.query.all())

