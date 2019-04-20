from flask import render_template
from application import app
from application.films.models import Film
from application.directors.models import Director
from application.actors.models import Actor
from application.ratings.models import Rating
@app.route("/")
def welcome():
    films = Film.top_films()
    directors = Director.top_directors()
    actors = Actor.top_actors()
    recent_films = Film.recent_films()
    recent_reviews = Rating.recent_reviews()
    return render_template("index.html", top_films = films, top_directors = directors, top_actors = actors, 
            recent_films = recent_films, recent_reviews = recent_reviews)
