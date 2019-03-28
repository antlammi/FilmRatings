from application import app, db
from flask_login import login_required
from flask import redirect, render_template, request, url_for
from application.films.models import Film
from application.films.forms import FilmForm
@app.route("/films/new")
@login_required
def films_form():
    return render_template("films/new.html", form = FilmForm())

@app.route("/films/", methods=["POST"])
@login_required
def films_create():
    form = FilmForm(request.form)

    f = Film(form.name.data)
    ##f.director = f.director.data

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
    return render_template("films/list.html", films = Film.query.all())

