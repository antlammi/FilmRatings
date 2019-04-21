from application import app, db, login_required
from flask import redirect, render_template, request, url_for
from application.actors.models import Actor, FilmActor
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
@app.route("/actors#<sortby>", methods=["GET"])
def actors_sorted(sortby):
    actors = Actor.query.all()
    if (sortby =='name'):
        actors= sorted(actors, key=lambda actor:actor.name.split()[-1])
    
    if (sortby =='age'):
        actors = sorted(actors, key=lambda actor:actor.age)

    if (sortby == 'nationality'):
        actors = sorted(actors, key =lambda actor:actor.nationality)
    
    return render_template("actors/list.html", actors = actors)


@app.route("/actors/<actor_id>/edit", methods=["GET"])
@login_required(role="ADMIN")
def actors_edit(actor_id):
    formtorender = ActorForm() 
    actor = Actor.query.get(actor_id)
    formtorender.name.data = actor.name
    formtorender.age.data = actor.age
    formtorender.nationality.data = actor.nationality
    formtorender.bio.data = actor.bio
    return render_template("actors/update.html", form=formtorender, actor_id = actor_id)

@app.route("/actors/<actor_id>/update", methods=["POST"])
@login_required(role="ADMIN")
def actors_update(actor_id):
    form = ActorForm(request.form)
    a = Actor.query.get(actor_id)

    a.name = form.name.data
    a.nationality = form.nationality.data
    a.age = form.age.data
    a.bio = form.bio.data
    
    if not form.validate():
        return render_template("actors/update.html", form = form)

    db.session().commit()
    return redirect(url_for("actors_index"))

@app.route("/actors/<actor_id>/delete")
@login_required(role="ADMIN")
def actors_delete(actor_id):
    a = Actor.query.get(actor_id)
    db.session().delete(a)
    db.session().commit()
    return redirect(url_for("actors_index"))

@app.route("/actors/<actor_id>", methods=["GET"])
def actors_show(actor_id):
    a = Actor.query.get(actor_id)
    film_ids = FilmActor.query.filter_by(actor_id = actor_id)
    avg_rating = Actor.avg_rating(actor_id)
    films = []
    for item in film_ids:
        f = Film.query.filter_by(id = item.film_id).first()
        films.append(f)
    
    return render_template("actors/show.html", id = a.id, actor= a, films = films, avg_rating = avg_rating)
