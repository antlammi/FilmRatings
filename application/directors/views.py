from application import app, db
from flask_login import login_required
from flask import redirect, render_template, request, url_for
from application.directors.models import Director
from application.directors.forms import DirectorForm

@app.route("/directors/new")
@login_required
def directors_form():
    return render_template("directors/new.html", form = DirectorForm())

@app.route("/directors/", methods=["POST"])
@login_required
def directors_create():
    form = DirectorForm(request.form)

    d = Director(form.name.data, form.nationality.data or 'unknown', form.age.data )

    if not form.validate():
        return render_template("directors/new.html", form = form)
    db.session().add(d)
    db.session().commit()
    
    return redirect(url_for("directors_index"))

@app.route("/directors/", methods=["GET"])
def directors_index():
    return render_template("directors/list.html", directors = Director.query.all())

