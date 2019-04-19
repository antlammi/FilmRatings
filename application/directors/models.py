from application import db
from application.models import Base

from sqlalchemy.sql import text
class Director(Base):
    
    name = db.Column(db.String(400), nullable=False)
    nationality = db.Column(db.String(400), nullable = True)
    age = db.Column(db.String(3), nullable = True)
    bio = db.Column(db.String(1200), nullable = True)
    films = db.relationship("Film", backref='account', lazy=True)

    def __init__(self, name, nationality, age):
        self.name = name
        self.nationality = nationality
        self.age = age

    @staticmethod
    def avg_rating(id):
        stmt = text("SELECT AVG(Rating.score) from Rating LEFT JOIN"
         " Film ON Rating.film_id = Film.id WHERE Film.director_id = :id").params(id=id)
        res = db.engine.execute(stmt)
        
        for row in res:
            avg = round(row[0], 2)
            
        return avg
    
    @staticmethod
    def top_directors():
        #initially used a left join syntax but changed it as that only worked locally and not in heroku
        stmt = text("SELECT director.name, AVG(Rating.score) as avg FROM Director, Rating, FILM WHERE Director.id = Film.director_id " 
        "AND Film.id = rating.film_id GROUP BY director.name Order By avg desc LIMIT 5")
        res = db.engine.execute(stmt)
        top = []
        for row in res:
            top.append([row.name, row.avg])

        return top