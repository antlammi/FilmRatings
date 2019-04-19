from flask import render_template
from application import app
from application.films.models import Film
from application.directors.models import Director
from application.actors.models import Actor
@app.route("/")
def welcome():
    films = Film.top_films()
    directors = Director.top_directors()
    actors = Actor.top_actors()
   
    return render_template("index.html", top_films = films, top_directors = directors, top_actors = actors)
