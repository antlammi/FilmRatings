from application import db
from application.models import Base

from sqlalchemy.sql import text
class Actor(Base):
    
    name = db.Column(db.String(400), nullable=False)
    nationality = db.Column(db.String(400), nullable = True)
    age = db.Column(db.String(3), nullable = True)
    bio = db.Column(db.String(1200), nullable = True)
    films = db.relationship("FilmActor", cascade="all, delete-orphan")


    def __init__(self, name, nationality, age):
        self.name = name
        self.nationality = nationality
        self.age = age
    
    @staticmethod
    def avg_rating(id):
        stmt = text("SELECT AVG(Rating.score) FROM Rating "
                +"LEFT JOIN Film on Rating.film_id = film.id "
                +"LEFT JOIN film_actor on film_actor.film_id = film.id "
                +"WHERE film_actor.actor_id = :id").params(id=id)
        res = db.engine.execute(stmt)
        
        for row in res:
            avg = row[0]
            
        return avg
    
    @staticmethod
    def top_actors():

        #initially used a left join syntax but changed it as that only worked locally and not in heroku
        stmt = text("SELECT Actor.name, AVG(Rating.score) AS avg FROM Actor, Rating, Film_actor, Film"
        " WHERE Film_actor.actor_id = Actor.id AND film_actor.film_id = Film.id "
        " AND Film.id = Rating.film_id GROUP BY Actor.id ORDER BY avg DESC LIMIT 5")
        res = db.engine.execute(stmt)
        top = []
        for row in res:
            top.append([row.name, row.avg])

        return top

class FilmActor(db.Model):
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'), nullable=False, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'), nullable=False, primary_key=True)

    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), 
        onupdate=db.func.current_timestamp())

