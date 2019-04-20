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
    def recent_films():
        stmt = text("SELECT * FROM Film ORDER BY Film.date_modified desc limit 5")
        res = db.engine.execute(stmt)
        recent = []
        for row in res:
            recent.append([row.name, row.id])
        
        return recent
    @staticmethod
    def top_films():
        stmt = text("SELECT name, id, avg(Rating.score) AS avg FROM Film, Rating WHERE Film.id = rating.film_id GROUP BY Film.id Order By avg desc LIMIT 5")
        res = db.engine.execute(stmt)
        top = []
        for row in res:
            top.append([row.name, row.id, round(row.avg, 2)])

        return top