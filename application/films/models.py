from application import db
from application.models import Base
from sqlalchemy.sql import text
from application.actors.models import FilmActor
class Film(Base):
    name = db.Column(db.String(400), nullable=False)
    description = db.Column(db.String(1200), nullable=True)
    director_id = db.Column(db.Integer, db.ForeignKey('director.id'), nullable = True)
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


