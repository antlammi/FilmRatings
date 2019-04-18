from application import app, db, login_required
from flask import redirect, render_template, request, url_for
from application.actors.models import Actor
from application.films.models import Film
from application.actors.forms import ActorForm

@app.route("/actors/new")
@login_required("ANY")
def actors_form():
    return render_template("actors/new.html", form = ActorForm())

@app.route("/actors/", methods=["POST"])
@login_required(role="ANY")
def actors_create():
    form = ActorForm(request.form)

    a = Actor(form.name.data, form.nationality.data or '', form.age.data )
    a.bio = form.bio.data
    if not form.validate():
        return render_template("actors/new.html", form = form)
    db.session().add(a)
    db.session().commit()
    
    return redirect(url_for("actors_index"))

@app.route("/actors/", methods=["GET"])
def actors_index():
    return render_template("actors/list.html", actors = Actor.query.all())


@app.route("/actors/<actor_id>", methods=["GET"])
def actors_show(actor_id):
    a = Actor.query.get(actor_id)
    return render_template("actors/show.html", id = a.id, actor= a)
