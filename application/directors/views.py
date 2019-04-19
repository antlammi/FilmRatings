from application import app, db, login_required
from flask import redirect, render_template, request, url_for
from application.directors.models import Director
from application.films.models import Film
from application.directors.forms import DirectorForm

@app.route("/directors/new")
@login_required("ANY")
def directors_form():
    return render_template("directors/new.html", form = DirectorForm())

@app.route("/directors/", methods=["POST"])
@login_required(role="ANY")
def directors_create():
    form = DirectorForm(request.form)

    d = Director(form.name.data, form.nationality.data or '', form.age.data )
    d.bio = form.bio.data
    if not form.validate():
        return render_template("directors/new.html", form = form)
    db.session().add(d)
    db.session().commit()
    
    return redirect(url_for("directors_index"))

@app.route("/directors/", methods=["GET"])
def directors_index():
    return render_template("directors/list.html", directors = Director.query.all())


@app.route("/directors/<director_id>/edit", methods=["GET"])
@login_required(role="ADMIN")
def directors_edit(director_id):
    formtorender = DirectorForm() 
    return render_template("directors/update.html", form=formtorender, director_id = director_id)


@app.route("/directors/<director_id>/update", methods=["POST"])
@login_required(role="ADMIN")
def directors_update(director_id):
    form = DirectorForm(request.form)
    d = Director.query.get(director_id)

    d.name = form.name.data
    d.nationality = form.nationality.data
    d.age = form.age.data
    d.bio = form.bio.data
    
    if not form.validate():
        return render_template("directors/update.html", form = form, director_id = director_id)

    db.session().commit()
    return redirect(url_for("directors_index"))


@app.route("/directors/<director_id>/delete")
@login_required(role="ADMIN")
def directors_delete(director_id):
    d = Director.query.get(director_id)
    db.session().delete(d)
    db.session().commit()
    return redirect(url_for("directors_index"))

@app.route("/directors/<director_id>", methods=["GET"])
def directors_show(director_id):
    d = Director.query.get(director_id)
    f = Film.query.filter_by(director_id = d.id)
    return render_template("directors/show.html", id = d.id, director = d, films = f)
