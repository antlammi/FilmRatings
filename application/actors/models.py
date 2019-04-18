from application import db
from application.models import Base
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

class FilmActor(db.Model):
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'), nullable=False, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'), nullable=False, primary_key=True)

    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), 
        onupdate=db.func.current_timestamp())

