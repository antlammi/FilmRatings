from application import app, db
from flask import redirect, render_template, request, url_for
from application.films.models import Film
@app.route("/films/new")
def films_form():
    return render_template("films/new.html")

@app.route("/films/", methods=["POST"])
def films_create():
    f = Film(request.form.get("name"))
    db.session().add(f)
    db.session().commit()

    return redirect(url_for("films_index"))

@app.route("/films/", methods=["GET"])
def films_index():
    return render_template("films/list.html", films = Film.query.all())