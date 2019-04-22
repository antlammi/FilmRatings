from application import db
from application.models import Base
from sqlalchemy.sql import text
from application.actors.models import FilmActor
import os
class Film(Base):
    name = db.Column(db.String(400), nullable=False)
    description = db.Column(db.String(1200), nullable=True)
    year = db.Column(db.Integer, nullable=True)
    director_id = db.Column(db.Integer, db.ForeignKey('director.id'), nullable = True)
    poster = db.Column(db.String(400), nullable=True)
    actors = db.relationship("FilmActor", cascade="all, delete-orphan")
    ratings = db.relationship("Rating", cascade="all, delete-orphan")
    
    def __init__(self, name):
        self.name = name

    @staticmethod
    def average_rating(id):
        stmt = text("SELECT AVG(Rating.score) from Rating LEFT JOIN"
         " Film ON Rating.film_id = Film.id WHERE Film.id = :id").params(id=id)
        res = db.engine.execute(stmt)
    
        for row in res:
            if row[0] != None: 
                avg = round(row[0], 2)
            else:
                avg = row[0]
            
        return avg

    @staticmethod
    def ratings_count(id):
        stmt = text("SELECT Count(*) from Rating LEFT JOIN"
         " Film ON Rating.film_id = Film.id WHERE Film.id = :id").params(id=id)
        res = db.engine.execute(stmt)
    
        for row in res:
            count = row[0]
            
        return count
    @staticmethod
    def film_reviews(id):
        stmt = text("SELECT Rating.user_id, Rating.score, Account.username FROM Rating, Account"
        " WHERE length(Rating.review) > 0 AND Account.id = Rating.user_id AND Rating.film_id = :id").params(id=id)
        res = db.engine.execute(stmt)
        reviews = []
        for row in res:
            reviews.append([row[0], row[1], row[2]])
        
        return reviews

    @staticmethod
    def recent_films():
        stmt = text("SELECT * FROM Film ORDER BY Film.date_modified desc limit 5")
        res = db.engine.execute(stmt)
        recent = []
        for row in res:
            recent.append([row.name, row.id])
        
        return recent
    @staticmethod
    def top_films():
        stmt = text("SELECT name, id, avg(Rating.score) AS avg FROM Film, Rating WHERE Film.id = rating.film_id GROUP BY Film.id ORDER BY avg DESC LIMIT 5")
        res = db.engine.execute(stmt)
        top = []
        for row in res:
            top.append([row.name, row.id, round(row.avg, 2)])

        return top

    @staticmethod
    def films_with_ratings():
        ##couldn't figure out a statement that worked both locally and on heroku, local one could be a lot cleaner but just did bare minimum
        if os.environ.get("HEROKU"):
            stmt = text("SELECT film.id, film.name, film.year, director_id, director.name, avg(Rating.score) AS avg FROM Director, Film "
            "LEFT JOIN Rating on Rating.film_id = id WHERE Director.id = film.director_id GROUP BY Film.id, director.name ORDER BY film.id")
        else:
            stmt = text("SELECT film.id, film.name, film.year, director_id, director.name, avg(Rating.score) AS avg FROM Director, Film "
            "LEFT JOIN Rating on Rating.film_id = film.id WHERE Director.id = film.director_id GROUP BY Film.id, director.name ORDER BY film.id")

        res = db.engine.execute(stmt)
        top = []
        for row in res:
            if row[5] != None:
                top.append([row[0], row[1], row[2], row[3], row[4], round(row[5], 2)])
            else :
                top.append([row[0], row[1], row[2], row[3], row[4], 0.0])
        return top
    
    


    