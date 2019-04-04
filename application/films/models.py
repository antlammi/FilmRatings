from application import db
from application.models import Base

from sqlalchemy.sql import text
class Film(Base):
    name = db.Column(db.String(400), nullable=False)
    director_id = db.Column(db.Integer, db.ForeignKey('director.id'), nullable = False)
    
    def __init__(self, name):
        self.name = name

    @staticmethod
    def average_rating(id):
        stmt = text("SELECT Rating.score from Rating LEFT JOIN"
         " Film ON Rating.film_id = Film.id WHERE Film.id = :id").params(id=id)
        res = db.engine.execute(stmt)
        sum = 0
        count = 0
        for row in res:
            sum += row[0]
            count+= 1
        return 1.0*sum/count
